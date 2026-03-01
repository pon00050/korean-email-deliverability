"""Tests for src/db.py — subscriber CRUD operations.

All tests use an in-memory SQLite database (via the db module's connection
factory) so they run without a live PostgreSQL instance in CI.
The db module must accept a DSN override for testing.
"""
import secrets
from datetime import datetime, timezone, timedelta

import pytest

from src.db import (
    create_tables,
    create_subscriber,
    deactivate_subscriber,
    get_due_subscribers,
    update_next_scan,
    get_subscriber_by_token,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def conn():
    """Return a fresh in-memory SQLite connection with schema applied."""
    import sqlite3
    c = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c.row_factory = sqlite3.Row
    create_tables(c)
    yield c
    c.close()


# ---------------------------------------------------------------------------
# create_subscriber
# ---------------------------------------------------------------------------

def test_create_subscriber_returns_id(conn):
    sub_id = create_subscriber(conn, domain="example.co.kr", email="test@example.co.kr", interval_hours=168)
    assert isinstance(sub_id, int)
    assert sub_id > 0


def test_create_subscriber_stores_fields(conn):
    sub_id = create_subscriber(conn, domain="example.co.kr", email="test@example.co.kr", interval_hours=24)
    row = get_subscriber_by_token(conn, _fetch_token(conn, sub_id))
    assert row["domain"] == "example.co.kr"
    assert row["email"] == "test@example.co.kr"
    assert row["interval_hours"] == 24
    assert row["active"] in (1, True)


def test_create_subscriber_generates_unique_tokens(conn):
    id1 = create_subscriber(conn, domain="a.co.kr", email="a@a.com", interval_hours=168)
    id2 = create_subscriber(conn, domain="b.co.kr", email="b@b.com", interval_hours=168)
    t1 = _fetch_token(conn, id1)
    t2 = _fetch_token(conn, id2)
    assert t1 != t2


def test_create_subscriber_next_scan_near_now(conn):
    before = datetime.now(timezone.utc)
    sub_id = create_subscriber(conn, domain="example.co.kr", email="t@t.com", interval_hours=168)
    after = datetime.now(timezone.utc)
    row = get_subscriber_by_token(conn, _fetch_token(conn, sub_id))
    # next_scan_at should be within a few seconds of now (immediate first scan)
    next_scan = _parse_dt(row["next_scan_at"])
    assert before - timedelta(seconds=5) <= next_scan <= after + timedelta(seconds=5)


# ---------------------------------------------------------------------------
# deactivate_subscriber
# ---------------------------------------------------------------------------

def test_deactivate_subscriber_sets_inactive(conn):
    sub_id = create_subscriber(conn, domain="example.co.kr", email="t@t.com", interval_hours=168)
    token = _fetch_token(conn, sub_id)
    deactivate_subscriber(conn, token)
    row = get_subscriber_by_token(conn, token)
    assert row["active"] in (0, False)


def test_deactivate_nonexistent_token_is_noop(conn):
    # Should not raise
    deactivate_subscriber(conn, "nonexistent-token-xyz")


# ---------------------------------------------------------------------------
# get_due_subscribers
# ---------------------------------------------------------------------------

def test_get_due_subscribers_returns_overdue(conn):
    sub_id = create_subscriber(conn, domain="example.co.kr", email="t@t.com", interval_hours=168)
    # next_scan_at is set to now → should be due
    rows = get_due_subscribers(conn)
    ids = [r["id"] for r in rows]
    assert sub_id in ids


def test_get_due_subscribers_excludes_future(conn):
    import sqlite3
    sub_id = create_subscriber(conn, domain="example.co.kr", email="t@t.com", interval_hours=168)
    # Push next_scan_at far into the future
    future = datetime.now(timezone.utc) + timedelta(hours=24)
    conn.execute(
        "UPDATE subscribers SET next_scan_at = ? WHERE id = ?",
        (future.isoformat(), sub_id),
    )
    conn.commit()
    rows = get_due_subscribers(conn)
    ids = [r["id"] for r in rows]
    assert sub_id not in ids


def test_get_due_subscribers_excludes_inactive(conn):
    sub_id = create_subscriber(conn, domain="example.co.kr", email="t@t.com", interval_hours=168)
    token = _fetch_token(conn, sub_id)
    deactivate_subscriber(conn, token)
    rows = get_due_subscribers(conn)
    ids = [r["id"] for r in rows]
    assert sub_id not in ids


# ---------------------------------------------------------------------------
# update_next_scan
# ---------------------------------------------------------------------------

def test_update_next_scan_advances_time(conn):
    sub_id = create_subscriber(conn, domain="example.co.kr", email="t@t.com", interval_hours=24)
    before = datetime.now(timezone.utc)
    update_next_scan(conn, sub_id, interval_hours=24)
    token = _fetch_token(conn, sub_id)
    row = get_subscriber_by_token(conn, token)
    next_scan = _parse_dt(row["next_scan_at"])
    expected = before + timedelta(hours=24)
    # Allow ±10 second tolerance
    assert abs((next_scan - expected).total_seconds()) < 10


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fetch_token(conn, sub_id: int) -> str:
    row = conn.execute("SELECT unsubscribe_token FROM subscribers WHERE id = ?", (sub_id,)).fetchone()
    return row["unsubscribe_token"]


def _parse_dt(value) -> datetime:
    """Parse ISO datetime string or datetime object to aware datetime."""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    # SQLite returns strings
    s = str(value)
    if s.endswith("+00:00") or "Z" in s:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
