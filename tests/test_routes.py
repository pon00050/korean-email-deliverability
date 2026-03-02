"""Tests for FastAPI routes in app.py.

Uses FastAPI's TestClient with an in-memory SQLite database.
The background scan thread started by POST /subscribe is mocked out
so no real DNS calls occur.

psycopg is stubbed at import time because libpq is not available in the CI
test environment — only SQLite is used here.
"""
import sqlite3
import sys
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
        TestClient(app_module.app, raise_server_exceptions=True) as c,
    ):
        yield c, sqlite_conn


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

def test_signup_page_returns_html(client):
    c, _ = client
    resp = c.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert b"<form" in resp.content


# ---------------------------------------------------------------------------
# POST /subscribe
# ---------------------------------------------------------------------------

def test_subscribe_creates_subscriber(client):
    c, conn = client
    resp = c.post("/subscribe", data={"domain": "example.co.kr", "email": "user@example.com"})
    assert resp.status_code == 200
    row = conn.execute("SELECT * FROM subscribers WHERE domain = 'example.co.kr'").fetchone()
    assert row is not None
    assert row["email"] == "user@example.com"
    assert row["active"] == 1


def test_subscribe_strips_https_prefix(client):
    c, conn = client
    resp = c.post(
        "/subscribe",
        data={"domain": "https://example.co.kr/", "email": "u@example.com"},
    )
    assert resp.status_code == 200
    row = conn.execute("SELECT domain FROM subscribers").fetchone()
    assert row["domain"] == "example.co.kr"


def test_subscribe_returns_success_html(client):
    c, _ = client
    resp = c.post("/subscribe", data={"domain": "example.co.kr", "email": "u@example.com"})
    assert resp.status_code == 200
    # The template renders a success message when success=True is passed
    assert b"example.co.kr" in resp.content


# ---------------------------------------------------------------------------
# GET /unsubscribe
# ---------------------------------------------------------------------------

def test_unsubscribe_with_valid_token_deactivates(client):
    c, conn = client
    # First subscribe to get a real token
    c.post("/subscribe", data={"domain": "example.co.kr", "email": "u@example.com"})
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


def test_unsubscribe_with_unknown_token_returns_200(client):
    c, _ = client
    resp = c.get("/unsubscribe?token=notarealtoken")
    assert resp.status_code == 200
