"""Database layer — subscriber CRUD.

Supports both PostgreSQL (production via Railway) and SQLite (tests/local dev).
The connection object is passed explicitly so callers control the connection
lifecycle (no hidden global state).

PostgreSQL (production):
    import psycopg
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    create_tables(conn)

SQLite (tests):
    import sqlite3
    conn = sqlite3.connect(":memory:", detect_types=...)
    conn.row_factory = sqlite3.Row
    create_tables(conn)
"""

import secrets
from datetime import datetime, timezone, timedelta
from typing import Any

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_CREATE_SUBSCRIBERS = """
CREATE TABLE IF NOT EXISTS subscribers (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    domain            TEXT NOT NULL,
    email             TEXT NOT NULL,
    interval_hours    INTEGER NOT NULL DEFAULT 168,
    next_scan_at      TEXT NOT NULL,
    unsubscribe_token TEXT NOT NULL UNIQUE,
    created_at        TEXT NOT NULL DEFAULT (datetime('now')),
    active            INTEGER NOT NULL DEFAULT 1
)
"""

# PostgreSQL variant (used when conn is a psycopg connection)
_CREATE_SUBSCRIBERS_PG = """
CREATE TABLE IF NOT EXISTS subscribers (
    id                SERIAL PRIMARY KEY,
    domain            TEXT NOT NULL,
    email             TEXT NOT NULL,
    interval_hours    INT NOT NULL DEFAULT 168,
    next_scan_at      TIMESTAMPTZ NOT NULL,
    unsubscribe_token TEXT NOT NULL UNIQUE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    active            BOOLEAN NOT NULL DEFAULT TRUE
)
"""


def _is_psycopg(conn) -> bool:
    return type(conn).__module__.startswith("psycopg")


def _placeholder(conn) -> str:
    """Return the parameter placeholder for the given connection type."""
    return "%s" if _is_psycopg(conn) else "?"


def create_tables(conn) -> None:
    """Create the subscribers table if it does not exist."""
    sql = _CREATE_SUBSCRIBERS_PG if _is_psycopg(conn) else _CREATE_SUBSCRIBERS
    conn.execute(sql)
    conn.commit()


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def create_subscriber(
    conn,
    *,
    domain: str,
    email: str,
    interval_hours: int = 168,
) -> int:
    """Insert a new subscriber and return its id.

    next_scan_at is set to now so the scheduler triggers an immediate first scan.
    """
    p = _placeholder(conn)
    token = secrets.token_urlsafe(32)
    now = datetime.now(timezone.utc)

    if _is_psycopg(conn):
        cur = conn.execute(
            f"""
            INSERT INTO subscribers (domain, email, interval_hours, next_scan_at, unsubscribe_token)
            VALUES ({p}, {p}, {p}, {p}, {p})
            RETURNING id
            """,
            (domain, email, interval_hours, now, token),
        )
        row = cur.fetchone()
        conn.commit()
        return row[0]
    else:
        cur = conn.execute(
            f"""
            INSERT INTO subscribers (domain, email, interval_hours, next_scan_at, unsubscribe_token)
            VALUES ({p}, {p}, {p}, {p}, {p})
            """,
            (domain, email, interval_hours, now.isoformat(), token),
        )
        conn.commit()
        return cur.lastrowid


def deactivate_subscriber(conn, token: str) -> None:
    """Set active = false for the subscriber with the given unsubscribe token."""
    p = _placeholder(conn)
    active_false = False if _is_psycopg(conn) else 0
    conn.execute(
        f"UPDATE subscribers SET active = {p} WHERE unsubscribe_token = {p}",
        (active_false, token),
    )
    conn.commit()


def get_due_subscribers(conn) -> list[Any]:
    """Return active subscribers whose next_scan_at is <= now."""
    p = _placeholder(conn)
    now = datetime.now(timezone.utc)
    now_val = now if _is_psycopg(conn) else now.isoformat()
    active_true = True if _is_psycopg(conn) else 1
    cur = conn.execute(
        f"SELECT * FROM subscribers WHERE active = {p} AND next_scan_at <= {p}",
        (active_true, now_val),
    )
    return cur.fetchall()


def update_next_scan(conn, subscriber_id: int, *, interval_hours: int) -> None:
    """Advance next_scan_at by interval_hours from now."""
    p = _placeholder(conn)
    next_scan = datetime.now(timezone.utc) + timedelta(hours=interval_hours)
    next_val = next_scan if _is_psycopg(conn) else next_scan.isoformat()
    conn.execute(
        f"UPDATE subscribers SET next_scan_at = {p} WHERE id = {p}",
        (next_val, subscriber_id),
    )
    conn.commit()


def get_subscriber_by_token(conn, token: str) -> Any | None:
    """Return the subscriber row for the given unsubscribe token, or None."""
    p = _placeholder(conn)
    cur = conn.execute(
        f"SELECT * FROM subscribers WHERE unsubscribe_token = {p}",
        (token,),
    )
    return cur.fetchone()
