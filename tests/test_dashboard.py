"""Tests for dashboard routes — register, login, dashboard access."""

import sqlite3
import sys
from types import ModuleType
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.db import create_tables, create_customer, save_scan
from src.auth import hash_password, generate_csrf_token, SESSION_COOKIE_NAME


# ---------------------------------------------------------------------------
# Stub psycopg before app.py is imported
# ---------------------------------------------------------------------------

def _make_psycopg_stub():
    stub = ModuleType("psycopg")
    stub.connect = MagicMock(side_effect=RuntimeError("psycopg not available"))
    return stub


try:
    import psycopg  # noqa: F401
except ImportError:
    sys.modules.setdefault("psycopg", _make_psycopg_stub())


# ---------------------------------------------------------------------------
# _NoCloseConn reused from test_routes pattern
# ---------------------------------------------------------------------------

class _NoCloseConn:
    def __init__(self, conn):
        self._conn = conn
        self.row_factory = conn.row_factory

    def close(self): pass
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def __getattr__(self, name): return getattr(self._conn, name)


@pytest.fixture
def sqlite_conn():
    raw = sqlite3.connect(
        ":memory:",
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        check_same_thread=False,
    )
    raw.row_factory = sqlite3.Row
    create_tables(raw)
    yield _NoCloseConn(raw)
    raw.close()


@pytest.fixture
def client(sqlite_conn):
    import app as app_module

    with (
        patch.object(app_module, "get_db", return_value=sqlite_conn),
        patch.object(app_module, "BackgroundScheduler"),
        patch("threading.Thread"),
        patch.dict("os.environ", {"SECRET_KEY": "test-secret"}),
        TestClient(app_module.app, raise_server_exceptions=True) as c,
    ):
        yield c, sqlite_conn


# ---------------------------------------------------------------------------
# Register
# ---------------------------------------------------------------------------

def test_register_page_renders(client):
    c, _ = client
    resp = c.get("/register")
    assert resp.status_code == 200
    assert "회원가입" in resp.text


def _get_csrf_token():
    return generate_csrf_token("testclient:")


def test_register_creates_account_and_redirects(client):
    c, conn = client
    csrf = _get_csrf_token()
    resp = c.post("/register", data={
        "email": "test@example.com",
        "password": "securepass123",
        "name": "테스터",
        "csrf_token": csrf,
    }, follow_redirects=False)
    assert resp.status_code == 303
    assert "/dashboard" in resp.headers["location"]
    # Session cookie set
    assert SESSION_COOKIE_NAME in resp.cookies

    # Customer exists in DB
    row = conn.execute("SELECT * FROM customers WHERE email = 'test@example.com'").fetchone()
    assert row is not None
    assert row["name"] == "테스터"


def test_register_rejects_short_password(client):
    c, _ = client
    csrf = _get_csrf_token()
    resp = c.post("/register", data={"email": "t@t.com", "password": "short", "csrf_token": csrf})
    assert resp.status_code == 200
    assert "8자" in resp.text


def test_register_rejects_duplicate_email(client):
    c, conn = client
    csrf = _get_csrf_token()
    create_customer(conn, email="dup@example.com", password_hash=hash_password("pass12345"))
    resp = c.post("/register", data={"email": "dup@example.com", "password": "pass12345", "csrf_token": csrf})
    assert resp.status_code == 200
    assert "이미 등록된" in resp.text


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

def test_login_page_renders(client):
    c, _ = client
    resp = c.get("/login")
    assert resp.status_code == 200
    assert "로그인" in resp.text


def test_login_with_valid_credentials(client):
    c, conn = client
    csrf = _get_csrf_token()
    pw_hash = hash_password("mypassword")
    create_customer(conn, email="user@example.com", password_hash=pw_hash)

    resp = c.post("/login", data={
        "email": "user@example.com",
        "password": "mypassword",
        "csrf_token": csrf,
    }, follow_redirects=False)
    assert resp.status_code == 303
    assert "/dashboard" in resp.headers["location"]
    assert SESSION_COOKIE_NAME in resp.cookies


def test_login_with_wrong_password(client):
    c, conn = client
    csrf = _get_csrf_token()
    pw_hash = hash_password("correct")
    create_customer(conn, email="user@example.com", password_hash=pw_hash)

    resp = c.post("/login", data={"email": "user@example.com", "password": "wrong", "csrf_token": csrf})
    assert resp.status_code == 200
    assert "올바르지 않습니다" in resp.text


# ---------------------------------------------------------------------------
# Dashboard access
# ---------------------------------------------------------------------------

def test_dashboard_requires_auth(client):
    c, _ = client
    resp = c.get("/dashboard", follow_redirects=False)
    assert resp.status_code == 303
    assert "/login" in resp.headers["location"]


def test_dashboard_shows_domains(client):
    c, conn = client
    # Create customer and log in
    pw_hash = hash_password("pass12345")
    cid = create_customer(conn, email="user@example.com", password_hash=pw_hash)

    # Create some scans for this customer
    save_scan(
        conn, domain="a.co.kr", overall=80, grade="B",
        naver=70, naver_label="양호", checks=[], customer_id=cid,
    )

    # Log in
    csrf = _get_csrf_token()
    login_resp = c.post("/login", data={
        "email": "user@example.com", "password": "pass12345", "csrf_token": csrf,
    }, follow_redirects=False)

    # Use session cookie to access dashboard
    cookies = {SESSION_COOKIE_NAME: login_resp.cookies[SESSION_COOKIE_NAME]}
    resp = c.get("/dashboard", cookies=cookies)
    assert resp.status_code == 200
    assert "a.co.kr" in resp.text
    assert "80" in resp.text


def test_logout_clears_session(client):
    c, _ = client
    resp = c.get("/logout", follow_redirects=False)
    assert resp.status_code == 303
    # Cookie should be deleted
    assert SESSION_COOKIE_NAME in resp.headers.get("set-cookie", "")


# ---------------------------------------------------------------------------
# DMARC upload — gzip bomb protection
# ---------------------------------------------------------------------------

def test_dmarc_upload_rejects_gzip_bomb(client):
    """A small .gz that decompresses to >50MB must be rejected."""
    import gzip
    import io

    c, conn = client
    csrf = _get_csrf_token()

    # Create customer and login
    pw_hash = hash_password("pass12345")
    cid = create_customer(conn, email="uploader@example.com", password_hash=pw_hash)
    login_resp = c.post("/login", data={
        "email": "uploader@example.com", "password": "pass12345", "csrf_token": csrf,
    }, follow_redirects=False)
    cookies = {SESSION_COOKIE_NAME: login_resp.cookies[SESSION_COOKIE_NAME]}

    # Generate CSRF token scoped to the authenticated session
    session_cookie = login_resp.cookies[SESSION_COOKIE_NAME]
    auth_csrf = generate_csrf_token(f"testclient:{session_cookie[:16]}")

    # Create a gzip file that decompresses to >50MB (all zeros compress extremely well)
    big_content = b"\x00" * (51 * 1024 * 1024)  # 51 MB of zeros
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as f:
        f.write(big_content)
    gz_bytes = buf.getvalue()

    resp = c.post(
        "/dashboard/dmarc-upload",
        files={"file": ("bomb.xml.gz", gz_bytes, "application/gzip")},
        data={"csrf_token": auth_csrf},
        cookies=cookies,
    )
    assert resp.status_code == 400
    assert "50MB" in resp.text
