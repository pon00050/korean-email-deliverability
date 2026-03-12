"""Database layer — subscriber, customer, API key, and scan CRUD.

Supports both PostgreSQL (production via Railway) and SQLite (tests/local dev).
The connection object is passed explicitly so callers control the connection
lifecycle (no hidden global state).

Tables:
    subscribers   — email monitoring subscriptions (Phase 2)
    customers     — registered user accounts (Phase 4)
    api_keys      — per-customer batch API keys (Phase 4)
    scans         — persisted scan results with shareable tokens (Phase 4)
    scan_checks   — individual check results belonging to a scan (Phase 4)

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

import json
import secrets
from datetime import datetime, timezone, timedelta
from typing import Any

# ---------------------------------------------------------------------------
# Schema — SQLite
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
    active            INTEGER NOT NULL DEFAULT 1,
    customer_id       INTEGER REFERENCES customers(id)
)
"""

_CREATE_CUSTOMERS = """
CREATE TABLE IF NOT EXISTS customers (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT NOT NULL UNIQUE,
    name          TEXT,
    password_hash TEXT,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    active        INTEGER NOT NULL DEFAULT 1
)
"""

_CREATE_API_KEYS = """
CREATE TABLE IF NOT EXISTS api_keys (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id   INTEGER NOT NULL REFERENCES customers(id),
    key_hash      TEXT NOT NULL UNIQUE,
    label         TEXT DEFAULT '',
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    active        INTEGER NOT NULL DEFAULT 1
)
"""

_CREATE_SCANS = """
CREATE TABLE IF NOT EXISTS scans (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    domain        TEXT NOT NULL,
    customer_id   INTEGER REFERENCES customers(id),
    overall       INTEGER NOT NULL,
    grade         TEXT NOT NULL,
    naver         INTEGER NOT NULL,
    naver_label   TEXT NOT NULL,
    scanned_at    TEXT NOT NULL DEFAULT (datetime('now')),
    public_token  TEXT NOT NULL UNIQUE
)
"""

_CREATE_SCAN_CHECKS = """
CREATE TABLE IF NOT EXISTS scan_checks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id         INTEGER NOT NULL REFERENCES scans(id),
    name            TEXT NOT NULL,
    status          TEXT NOT NULL,
    score           INTEGER NOT NULL,
    message_ko      TEXT NOT NULL,
    detail_ko       TEXT DEFAULT '',
    remediation_ko  TEXT DEFAULT '',
    raw             TEXT DEFAULT ''
)
"""

# ---------------------------------------------------------------------------
# Schema — PostgreSQL
# ---------------------------------------------------------------------------

_CREATE_SUBSCRIBERS_PG = """
CREATE TABLE IF NOT EXISTS subscribers (
    id                SERIAL PRIMARY KEY,
    domain            TEXT NOT NULL,
    email             TEXT NOT NULL,
    interval_hours    INT NOT NULL DEFAULT 168,
    next_scan_at      TIMESTAMPTZ NOT NULL,
    unsubscribe_token TEXT NOT NULL UNIQUE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    active            BOOLEAN NOT NULL DEFAULT TRUE,
    customer_id       INT REFERENCES customers(id)
)
"""

_CREATE_CUSTOMERS_PG = """
CREATE TABLE IF NOT EXISTS customers (
    id            SERIAL PRIMARY KEY,
    email         TEXT NOT NULL UNIQUE,
    name          TEXT,
    password_hash TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    active        BOOLEAN NOT NULL DEFAULT TRUE
)
"""

_CREATE_API_KEYS_PG = """
CREATE TABLE IF NOT EXISTS api_keys (
    id            SERIAL PRIMARY KEY,
    customer_id   INT NOT NULL REFERENCES customers(id),
    key_hash      TEXT NOT NULL UNIQUE,
    label         TEXT DEFAULT '',
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    active        BOOLEAN NOT NULL DEFAULT TRUE
)
"""

_CREATE_SCANS_PG = """
CREATE TABLE IF NOT EXISTS scans (
    id            SERIAL PRIMARY KEY,
    domain        TEXT NOT NULL,
    customer_id   INT REFERENCES customers(id),
    overall       INT NOT NULL,
    grade         TEXT NOT NULL,
    naver         INT NOT NULL,
    naver_label   TEXT NOT NULL,
    scanned_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    public_token  TEXT NOT NULL UNIQUE
)
"""

_CREATE_SCAN_CHECKS_PG = """
CREATE TABLE IF NOT EXISTS scan_checks (
    id              SERIAL PRIMARY KEY,
    scan_id         INT NOT NULL REFERENCES scans(id),
    name            TEXT NOT NULL,
    status          TEXT NOT NULL,
    score           INT NOT NULL,
    message_ko      TEXT NOT NULL,
    detail_ko       TEXT DEFAULT '',
    remediation_ko  TEXT DEFAULT '',
    raw             TEXT DEFAULT ''
)
"""

_CREATE_DMARC_UPLOADS = """
CREATE TABLE IF NOT EXISTS dmarc_uploads (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id   INTEGER NOT NULL REFERENCES customers(id),
    domain        TEXT NOT NULL,
    org_name      TEXT,
    date_begin    TEXT,
    date_end      TEXT,
    total_count   INTEGER,
    pass_count    INTEGER,
    report_json   TEXT NOT NULL,
    uploaded_at   TEXT NOT NULL DEFAULT (datetime('now'))
)
"""

_CREATE_DMARC_UPLOADS_PG = """
CREATE TABLE IF NOT EXISTS dmarc_uploads (
    id            SERIAL PRIMARY KEY,
    customer_id   INT NOT NULL REFERENCES customers(id),
    domain        TEXT NOT NULL,
    org_name      TEXT,
    date_begin    TIMESTAMPTZ,
    date_end      TIMESTAMPTZ,
    total_count   INT,
    pass_count    INT,
    report_json   TEXT NOT NULL,
    uploaded_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
)
"""

# Table creation order matters due to foreign key references.
# customers must be created before subscribers (customer_id FK),
# api_keys, and scans. scans must be created before scan_checks.
_SQLITE_TABLES = [
    _CREATE_CUSTOMERS,
    _CREATE_SUBSCRIBERS,
    _CREATE_API_KEYS,
    _CREATE_SCANS,
    _CREATE_SCAN_CHECKS,
    _CREATE_DMARC_UPLOADS,
]

_PG_TABLES = [
    _CREATE_CUSTOMERS_PG,
    _CREATE_SUBSCRIBERS_PG,
    _CREATE_API_KEYS_PG,
    _CREATE_SCANS_PG,
    _CREATE_SCAN_CHECKS_PG,
    _CREATE_DMARC_UPLOADS_PG,
]


def _is_psycopg(conn) -> bool:
    return type(conn).__module__.startswith("psycopg")


def _placeholder(conn) -> str:
    """Return the parameter placeholder for the given connection type."""
    return "%s" if _is_psycopg(conn) else "?"


def create_tables(conn) -> None:
    """Create all tables if they do not exist."""
    sqls = _PG_TABLES if _is_psycopg(conn) else _SQLITE_TABLES
    for sql in sqls:
        conn.execute(sql)
    conn.commit()


# ---------------------------------------------------------------------------
# CRUD — Subscribers
# ---------------------------------------------------------------------------

def create_subscriber(
    conn,
    *,
    domain: str,
    email: str,
    interval_hours: int = 168,
    customer_id: int | None = None,
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
            INSERT INTO subscribers (domain, email, interval_hours, next_scan_at, unsubscribe_token, customer_id)
            VALUES ({p}, {p}, {p}, {p}, {p}, {p})
            RETURNING id
            """,
            (domain, email, interval_hours, now, token, customer_id),
        )
        row = cur.fetchone()
        conn.commit()
        return row[0]
    else:
        cur = conn.execute(
            f"""
            INSERT INTO subscribers (domain, email, interval_hours, next_scan_at, unsubscribe_token, customer_id)
            VALUES ({p}, {p}, {p}, {p}, {p}, {p})
            """,
            (domain, email, interval_hours, now.isoformat(), token, customer_id),
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
    if _is_psycopg(conn):
        import psycopg.rows
        cur = conn.cursor(row_factory=psycopg.rows.dict_row)
        cur.execute(
            f"SELECT * FROM subscribers WHERE active = {p} AND next_scan_at <= {p}",
            (active_true, now_val),
        )
    else:
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
    if _is_psycopg(conn):
        import psycopg.rows
        cur = conn.cursor(row_factory=psycopg.rows.dict_row)
        cur.execute(
            f"SELECT * FROM subscribers WHERE unsubscribe_token = {p}",
            (token,),
        )
    else:
        cur = conn.execute(
            f"SELECT * FROM subscribers WHERE unsubscribe_token = {p}",
            (token,),
        )
    return cur.fetchone()


# ---------------------------------------------------------------------------
# CRUD — Customers
# ---------------------------------------------------------------------------

def create_customer(conn, *, email: str, name: str = "", password_hash: str = "") -> int:
    """Insert a new customer and return its id. Raises on duplicate email."""
    p = _placeholder(conn)
    if _is_psycopg(conn):
        cur = conn.execute(
            f"""
            INSERT INTO customers (email, name, password_hash)
            VALUES ({p}, {p}, {p})
            RETURNING id
            """,
            (email, name, password_hash),
        )
        row = cur.fetchone()
        conn.commit()
        return row[0]
    else:
        cur = conn.execute(
            f"""
            INSERT INTO customers (email, name, password_hash)
            VALUES ({p}, {p}, {p})
            """,
            (email, name, password_hash),
        )
        conn.commit()
        return cur.lastrowid


def get_customer_by_email(conn, email: str) -> Any | None:
    """Return the customer row for the given email, or None."""
    p = _placeholder(conn)
    if _is_psycopg(conn):
        import psycopg.rows
        cur = conn.cursor(row_factory=psycopg.rows.dict_row)
        cur.execute(f"SELECT * FROM customers WHERE email = {p}", (email,))
    else:
        cur = conn.execute(f"SELECT * FROM customers WHERE email = {p}", (email,))
    return cur.fetchone()


def get_customer_by_id(conn, customer_id: int) -> Any | None:
    """Return the customer row for the given id, or None."""
    p = _placeholder(conn)
    if _is_psycopg(conn):
        import psycopg.rows
        cur = conn.cursor(row_factory=psycopg.rows.dict_row)
        cur.execute(f"SELECT * FROM customers WHERE id = {p}", (customer_id,))
    else:
        cur = conn.execute(f"SELECT * FROM customers WHERE id = {p}", (customer_id,))
    return cur.fetchone()


# ---------------------------------------------------------------------------
# CRUD — API Keys
# ---------------------------------------------------------------------------

def create_api_key(conn, *, customer_id: int, key_hash: str, label: str = "") -> int:
    """Insert a new API key and return its id."""
    p = _placeholder(conn)
    if _is_psycopg(conn):
        cur = conn.execute(
            f"""
            INSERT INTO api_keys (customer_id, key_hash, label)
            VALUES ({p}, {p}, {p})
            RETURNING id
            """,
            (customer_id, key_hash, label),
        )
        row = cur.fetchone()
        conn.commit()
        return row[0]
    else:
        cur = conn.execute(
            f"""
            INSERT INTO api_keys (customer_id, key_hash, label)
            VALUES ({p}, {p}, {p})
            """,
            (customer_id, key_hash, label),
        )
        conn.commit()
        return cur.lastrowid


def get_customer_by_api_key_hash(conn, key_hash: str) -> Any | None:
    """Return the customer row for the given API key hash, or None if key is invalid or revoked."""
    p = _placeholder(conn)
    active_true = True if _is_psycopg(conn) else 1
    if _is_psycopg(conn):
        import psycopg.rows
        cur = conn.cursor(row_factory=psycopg.rows.dict_row)
        cur.execute(
            f"""
            SELECT c.* FROM customers c
            JOIN api_keys k ON c.id = k.customer_id
            WHERE k.key_hash = {p} AND k.active = {p} AND c.active = {p}
            """,
            (key_hash, active_true, active_true),
        )
    else:
        cur = conn.execute(
            f"""
            SELECT c.* FROM customers c
            JOIN api_keys k ON c.id = k.customer_id
            WHERE k.key_hash = {p} AND k.active = {p} AND c.active = {p}
            """,
            (key_hash, active_true, active_true),
        )
    return cur.fetchone()


def revoke_api_key(conn, key_hash: str) -> None:
    """Set active = false for the API key with the given hash."""
    p = _placeholder(conn)
    active_false = False if _is_psycopg(conn) else 0
    conn.execute(
        f"UPDATE api_keys SET active = {p} WHERE key_hash = {p}",
        (active_false, key_hash),
    )
    conn.commit()


def list_api_keys(conn, customer_id: int) -> list[Any]:
    """Return all API key rows for a customer."""
    p = _placeholder(conn)
    cur = conn.execute(
        f"SELECT * FROM api_keys WHERE customer_id = {p}",
        (customer_id,),
    )
    return cur.fetchall()


# ---------------------------------------------------------------------------
# CRUD — Scans
# ---------------------------------------------------------------------------

def save_scan(
    conn,
    *,
    domain: str,
    overall: int,
    grade: str,
    naver: int,
    naver_label: str,
    checks: list[dict[str, Any]],
    customer_id: int | None = None,
) -> tuple[int, str]:
    """Persist a scan and its check results. Returns (scan_id, public_token)."""
    p = _placeholder(conn)
    public_token = secrets.token_urlsafe(8)

    if _is_psycopg(conn):
        cur = conn.execute(
            f"""
            INSERT INTO scans (domain, customer_id, overall, grade, naver, naver_label, public_token)
            VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p})
            RETURNING id
            """,
            (domain, customer_id, overall, grade, naver, naver_label, public_token),
        )
        scan_id = cur.fetchone()[0]
    else:
        cur = conn.execute(
            f"""
            INSERT INTO scans (domain, customer_id, overall, grade, naver, naver_label, public_token)
            VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p})
            """,
            (domain, customer_id, overall, grade, naver, naver_label, public_token),
        )
        scan_id = cur.lastrowid

    for check in checks:
        conn.execute(
            f"""
            INSERT INTO scan_checks (scan_id, name, status, score, message_ko, detail_ko, remediation_ko, raw)
            VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p}, {p})
            """,
            (
                scan_id,
                check["name"],
                check["status"],
                check["score"],
                check["message_ko"],
                check.get("detail_ko", ""),
                check.get("remediation_ko", ""),
                check.get("raw", ""),
            ),
        )

    conn.commit()
    return scan_id, public_token


def get_scan_by_token(conn, public_token: str) -> dict[str, Any] | None:
    """Return scan with its checks for the given public_token, or None."""
    p = _placeholder(conn)
    scan_row = conn.execute(
        f"SELECT * FROM scans WHERE public_token = {p}",
        (public_token,),
    ).fetchone()
    if not scan_row:
        return None

    scan = dict(scan_row)
    scan_id = scan["id"]
    check_rows = conn.execute(
        f"SELECT * FROM scan_checks WHERE scan_id = {p} ORDER BY id",
        (scan_id,),
    ).fetchall()
    scan["checks"] = [dict(r) for r in check_rows]
    return scan


def list_scans_by_domain(
    conn, domain: str, *, customer_id: int | None = None, limit: int = 50
) -> list[Any]:
    """Return recent scans for a domain, newest first.

    If customer_id is provided, only returns scans belonging to that customer.
    """
    p = _placeholder(conn)
    if customer_id is not None:
        cur = conn.execute(
            f"SELECT * FROM scans WHERE domain = {p} AND customer_id = {p} ORDER BY id DESC LIMIT {p}",
            (domain, customer_id, limit),
        )
    else:
        cur = conn.execute(
            f"SELECT * FROM scans WHERE domain = {p} ORDER BY id DESC LIMIT {p}",
            (domain, limit),
        )
    return cur.fetchall()


def list_scans_for_customer(conn, customer_id: int, *, limit: int = 100) -> list[Any]:
    """Return recent scans for a customer, newest first."""
    p = _placeholder(conn)
    cur = conn.execute(
        f"SELECT * FROM scans WHERE customer_id = {p} ORDER BY id DESC LIMIT {p}",
        (customer_id, limit),
    )
    return cur.fetchall()


def list_customer_domains(conn, customer_id: int) -> list[dict[str, Any]]:
    """Return distinct domains scanned by a customer with their latest score/grade."""
    p = _placeholder(conn)
    rows = conn.execute(
        f"""
        SELECT domain, overall, grade, naver, naver_label, scanned_at, public_token
        FROM scans
        WHERE customer_id = {p}
        AND id IN (
            SELECT MAX(id) FROM scans WHERE customer_id = {p} GROUP BY domain
        )
        ORDER BY domain
        """,
        (customer_id, customer_id),
    ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# CRUD — DMARC Uploads
# ---------------------------------------------------------------------------

def save_dmarc_upload(
    conn,
    *,
    customer_id: int,
    domain: str,
    org_name: str,
    date_begin: str,
    date_end: str,
    total_count: int,
    pass_count: int,
    report_json: str,
) -> int:
    """Persist a parsed DMARC aggregate report. Returns the upload id."""
    p = _placeholder(conn)
    if _is_psycopg(conn):
        cur = conn.execute(
            f"""
            INSERT INTO dmarc_uploads (customer_id, domain, org_name, date_begin, date_end, total_count, pass_count, report_json)
            VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p}, {p})
            RETURNING id
            """,
            (customer_id, domain, org_name, date_begin, date_end, total_count, pass_count, report_json),
        )
        row = cur.fetchone()
        conn.commit()
        return row[0]
    else:
        cur = conn.execute(
            f"""
            INSERT INTO dmarc_uploads (customer_id, domain, org_name, date_begin, date_end, total_count, pass_count, report_json)
            VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p}, {p})
            """,
            (customer_id, domain, org_name, date_begin, date_end, total_count, pass_count, report_json),
        )
        conn.commit()
        return cur.lastrowid


def list_dmarc_uploads(conn, customer_id: int) -> list[Any]:
    """Return all DMARC uploads for a customer, newest first."""
    p = _placeholder(conn)
    cur = conn.execute(
        f"SELECT * FROM dmarc_uploads WHERE customer_id = {p} ORDER BY id DESC",
        (customer_id,),
    )
    return cur.fetchall()


def get_dmarc_upload(conn, upload_id: int) -> Any | None:
    """Return a single DMARC upload by id, or None."""
    p = _placeholder(conn)
    cur = conn.execute(
        f"SELECT * FROM dmarc_uploads WHERE id = {p}",
        (upload_id,),
    )
    return cur.fetchone()
