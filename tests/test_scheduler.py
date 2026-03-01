"""Tests for src/scheduler.py — due-scan detection and next_scan_at update logic.

The scheduler's _run_due_scans() function is tested in isolation with a
mocked scan executor and an in-memory SQLite database so tests run offline.
"""
import sqlite3
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

import pytest

from src.db import create_tables, create_subscriber, get_due_subscribers, update_next_scan
from src.scheduler import run_due_scans


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c.row_factory = sqlite3.Row
    create_tables(c)
    yield c
    c.close()


def _push_to_past(conn, sub_id: int, hours: int = 1) -> None:
    """Set next_scan_at to hours in the past."""
    past = datetime.now(timezone.utc) - timedelta(hours=hours)
    conn.execute(
        "UPDATE subscribers SET next_scan_at = ? WHERE id = ?",
        (past.isoformat(), sub_id),
    )
    conn.commit()


def _push_to_future(conn, sub_id: int, hours: int = 24) -> None:
    """Set next_scan_at to hours in the future."""
    future = datetime.now(timezone.utc) + timedelta(hours=hours)
    conn.execute(
        "UPDATE subscribers SET next_scan_at = ? WHERE id = ?",
        (future.isoformat(), sub_id),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# run_due_scans
# ---------------------------------------------------------------------------

def test_run_due_scans_calls_executor_for_due_rows(conn):
    sub_id = create_subscriber(conn, domain="example.co.kr", email="t@t.com", interval_hours=168)
    _push_to_past(conn, sub_id)

    mock_executor = MagicMock(return_value={"overall": 52, "grade": "D", "naver": 44, "naver_label": "주의"})
    mock_send = MagicMock()

    run_due_scans(conn, scan_executor=mock_executor, email_sender=mock_send)

    mock_executor.assert_called_once()
    call_args = mock_executor.call_args
    assert call_args[0][0] == "example.co.kr"


def test_run_due_scans_skips_future_subscribers(conn):
    sub_id = create_subscriber(conn, domain="example.co.kr", email="t@t.com", interval_hours=168)
    _push_to_future(conn, sub_id)

    mock_executor = MagicMock()
    mock_send = MagicMock()

    run_due_scans(conn, scan_executor=mock_executor, email_sender=mock_send)

    mock_executor.assert_not_called()


def test_run_due_scans_sends_email_after_scan(conn):
    sub_id = create_subscriber(conn, domain="example.co.kr", email="user@example.co.kr", interval_hours=168)
    _push_to_past(conn, sub_id)

    mock_executor = MagicMock(return_value=(
        [MagicMock(name="SPF", status="pass", score=100, message_ko="OK")],
        {"overall": 80, "grade": "B", "naver": 70, "naver_label": "양호"},
    ))
    mock_send = MagicMock()

    run_due_scans(conn, scan_executor=mock_executor, email_sender=mock_send)

    mock_send.assert_called_once()
    send_kwargs = mock_send.call_args[1]
    assert send_kwargs["to_email"] == "user@example.co.kr"
    assert send_kwargs["domain"] == "example.co.kr"


def test_run_due_scans_advances_next_scan_at(conn):
    sub_id = create_subscriber(conn, domain="example.co.kr", email="t@t.com", interval_hours=24)
    _push_to_past(conn, sub_id)

    mock_executor = MagicMock(return_value=(
        [],
        {"overall": 50, "grade": "D", "naver": 40, "naver_label": "주의"},
    ))
    mock_send = MagicMock()

    before = datetime.now(timezone.utc)
    run_due_scans(conn, scan_executor=mock_executor, email_sender=mock_send)
    after = datetime.now(timezone.utc)

    # next_scan_at should now be ~24 hours in the future
    row = conn.execute("SELECT next_scan_at FROM subscribers WHERE id = ?", (sub_id,)).fetchone()
    next_scan = datetime.fromisoformat(row["next_scan_at"]).replace(tzinfo=timezone.utc)
    expected = before + timedelta(hours=24)
    assert abs((next_scan - expected).total_seconds()) < 10


def test_run_due_scans_handles_multiple_subscribers(conn):
    ids = []
    for i in range(3):
        sid = create_subscriber(conn, domain=f"domain{i}.co.kr", email=f"u{i}@example.com", interval_hours=168)
        _push_to_past(conn, sid)
        ids.append(sid)

    mock_executor = MagicMock(return_value=(
        [],
        {"overall": 50, "grade": "D", "naver": 40, "naver_label": "주의"},
    ))
    mock_send = MagicMock()

    run_due_scans(conn, scan_executor=mock_executor, email_sender=mock_send)

    assert mock_executor.call_count == 3
    assert mock_send.call_count == 3
