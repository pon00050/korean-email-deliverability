"""Tests for FastAPI routes in app.py.

Uses FastAPI's TestClient with an in-memory SQLite database.
The background scan thread started by POST /subscribe is mocked out
so no real DNS calls occur.

psycopg is stubbed at import time because libpq is not available in the CI
test environment — only SQLite is used here.
"""
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
from types import ModuleType
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.db import create_tables


# ---------------------------------------------------------------------------
# Stub psycopg before app.py is imported (no libpq in CI)
# ---------------------------------------------------------------------------

def _make_psycopg_stub():
    stub = ModuleType("psycopg")
    stub.connect = MagicMock(side_effect=RuntimeError("psycopg not available — use get_db mock instead"))
    return stub


try:
    import psycopg  # noqa: F401
except ImportError:
    sys.modules.setdefault("psycopg", _make_psycopg_stub())


# ---------------------------------------------------------------------------
# App fixture — override get_db() to use SQLite in-memory
# ---------------------------------------------------------------------------

class _NoCloseConn:
    """Thin wrapper around a sqlite3 connection that ignores close() calls.

    Routes call conn.close() after each request; we don't want them to actually
    close the shared in-memory database that the test inspects afterwards.
    sqlite3.Connection.close is a read-only C slot so it cannot be monkey-patched,
    hence this wrapper.
    """

    def __init__(self, conn):
        self._conn = conn
        # Copy row_factory so attribute lookup via __getattr__ is not needed for it
        self.row_factory = conn.row_factory

    def close(self):
        pass  # intentional no-op

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass  # intentional no-op — keep underlying connection open for test inspection

    def __getattr__(self, name):
        return getattr(self._conn, name)


@pytest.fixture
def sqlite_conn():
    # check_same_thread=False: FastAPI/Starlette runs the ASGI app in a worker thread
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
    """Return a TestClient backed by in-memory SQLite, no scheduler, no real scans."""
    import app as app_module

    with (
        patch.object(app_module, "get_db", return_value=sqlite_conn),
        patch.object(app_module, "BackgroundScheduler"),   # prevent real scheduler start
        patch("threading.Thread"),                          # prevent real DNS scan threads
        patch.dict("os.environ", {"SECRET_KEY": "test-secret-routes"}),
        TestClient(app_module.app, raise_server_exceptions=True) as c,
    ):
        yield c, sqlite_conn


def _get_csrf_token():
    """Generate a valid CSRF token matching TestClient's session identity."""
    from src.auth import generate_csrf_token
    # TestClient sets request.client.host = "testclient", no session cookie → empty prefix
    return generate_csrf_token("testclient:")


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------

def test_health_returns_ok(client):
    c, _ = client
    resp = c.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

def test_landing_page_returns_html(client):
    c, _ = client
    resp = c.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "Senderfit" in resp.text


# ---------------------------------------------------------------------------
# POST /subscribe
# ---------------------------------------------------------------------------

def test_subscribe_creates_subscriber(client):
    c, conn = client
    csrf = _get_csrf_token()
    resp = c.post("/subscribe", data={"domain": "example.co.kr", "email": "user@example.com", "csrf_token": csrf})
    assert resp.status_code == 200
    row = conn.execute("SELECT * FROM subscribers WHERE domain = 'example.co.kr'").fetchone()
    assert row is not None
    assert row["email"] == "user@example.com"
    assert row["active"] == 1


def test_subscribe_strips_https_prefix(client):
    c, conn = client
    csrf = _get_csrf_token()
    resp = c.post(
        "/subscribe",
        data={"domain": "https://example.co.kr/", "email": "u@example.com", "csrf_token": csrf},
    )
    assert resp.status_code == 200
    row = conn.execute("SELECT domain FROM subscribers").fetchone()
    assert row["domain"] == "example.co.kr"


def test_subscribe_returns_success_html(client):
    c, _ = client
    csrf = _get_csrf_token()
    resp = c.post("/subscribe", data={"domain": "example.co.kr", "email": "u@example.com", "csrf_token": csrf})
    assert resp.status_code == 200
    # The template renders a success message when success=True is passed
    assert b"example.co.kr" in resp.content


# ---------------------------------------------------------------------------
# GET /unsubscribe
# ---------------------------------------------------------------------------

def test_unsubscribe_with_valid_token_deactivates(client):
    c, conn = client
    csrf = _get_csrf_token()
    # First subscribe to get a real token
    c.post("/subscribe", data={"domain": "example.co.kr", "email": "u@example.com", "csrf_token": csrf})
    row = conn.execute("SELECT unsubscribe_token FROM subscribers").fetchone()
    token = row["unsubscribe_token"]

    resp = c.get(f"/unsubscribe?token={token}")
    assert resp.status_code == 200

    updated = conn.execute("SELECT active FROM subscribers").fetchone()
    assert updated["active"] == 0


def test_unsubscribe_with_missing_token_shows_error(client):
    c, _ = client
    resp = c.get("/unsubscribe")
    assert resp.status_code == 200
    assert "유효하지 않은" in resp.text


# T5 — Invalid / random unsubscribe token must never return 5xx
# A 500 on a random token would surface in logs and alarm users following an
# old or corrupted unsubscribe link.
@pytest.mark.parametrize("token", [
    "notarealtoken",
    "00000000-0000-0000-0000-000000000000",
    "'; DROP TABLE subscribers; --",
    "a" * 256,
])
def test_invalid_unsubscribe_token_never_returns_5xx(client, token):
    c, _ = client
    resp = c.get(f"/unsubscribe?token={token}")
    assert resp.status_code < 500


# ---------------------------------------------------------------------------
# POST /subscribe — input validation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "form_data,expected_keyword",
    [
        ({"domain": "", "email": "u@example.com"}, "도메인"),
        ({"domain": "localhost", "email": "u@example.com"}, "도메인"),
        ({"domain": "example.co.kr", "email": "notanemail"}, "이메일"),
        ({"domain": "example.co.kr", "email": "user@nodot"}, "이메일"),
        ({"domain": "example.co.kr", "email": "u@example.com", "interval_hours": 0}, "스캔 주기"),
        ({"domain": "example.co.kr", "email": "u@example.com", "interval_hours": 9000}, "스캔 주기"),
    ],
)
def test_subscribe_rejects_invalid_input(client, form_data, expected_keyword):
    c, conn = client
    form_data["csrf_token"] = _get_csrf_token()
    resp = c.post("/subscribe", data=form_data)
    assert resp.status_code == 200
    assert expected_keyword in resp.text
    row = conn.execute("SELECT * FROM subscribers").fetchone()
    assert row is None


# ---------------------------------------------------------------------------
# Rate limiter thread safety
# ---------------------------------------------------------------------------

def test_rate_limiter_thread_safety():
    """Concurrent calls to _check_rate_limit must not exceed SCAN_RATE_LIMIT."""
    import app as app_module
    # Reset rate limiter state
    app_module._scan_requests.clear()

    results = []
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(app_module._check_rate_limit, "test-ip") for _ in range(10)]
        results = [f.result() for f in futures]

    allowed = sum(1 for r in results if r)
    assert allowed == app_module.SCAN_RATE_LIMIT  # exactly 3


# ---------------------------------------------------------------------------
# DB failure handling
# ---------------------------------------------------------------------------

def test_subscribe_raises_on_db_failure(client):
    """When get_db raises during POST /subscribe, the error propagates (500 in production)."""
    import app as app_module
    c, _ = client
    csrf = _get_csrf_token()
    with patch.object(app_module, "get_db", side_effect=RuntimeError("DB down")):
        with pytest.raises(RuntimeError, match="DB down"):
            c.post(
                "/subscribe",
                data={"domain": "example.co.kr", "email": "u@example.com", "csrf_token": csrf},
            )


# ---------------------------------------------------------------------------
# CSRF protection
# ---------------------------------------------------------------------------

def test_post_subscribe_without_csrf_returns_403(client):
    """POST /subscribe without CSRF token must return 403."""
    c, _ = client
    resp = c.post("/subscribe", data={"domain": "example.co.kr", "email": "u@example.com"})
    assert resp.status_code == 403


def test_post_subscribe_with_valid_csrf_succeeds(client):
    """POST /subscribe with valid CSRF token succeeds."""
    c, conn = client
    csrf = _get_csrf_token()
    resp = c.post("/subscribe", data={
        "domain": "example.co.kr", "email": "u@example.com", "csrf_token": csrf,
    })
    assert resp.status_code == 200
    row = conn.execute("SELECT * FROM subscribers").fetchone()
    assert row is not None


def test_batch_route_has_no_csrf_parameter():
    """POST /batch (JSON API) does not have a csrf_token parameter — CSRF is structurally skipped."""
    import inspect
    import app as app_module
    sig = inspect.signature(app_module.batch_scan)
    assert "csrf_token" not in sig.parameters
