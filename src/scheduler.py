"""Background scheduler — polls subscribers and runs due scans.

In production this is started as a background thread by app.py using APScheduler.
The core logic (run_due_scans) is kept dependency-free so it can be unit-tested
with a mock executor and email sender.

Production wiring (in app.py):
    from apscheduler.schedulers.background import BackgroundScheduler
    from src.scheduler import make_apscheduler_job

    scheduler = BackgroundScheduler()
    scheduler.add_job(make_apscheduler_job(db_conn), "interval", minutes=5)
    scheduler.start()
"""

from __future__ import annotations

import logging
from typing import Any, Callable

from src.db import get_due_subscribers, update_next_scan

logger = logging.getLogger(__name__)


def run_due_scans(
    conn,
    *,
    scan_executor: Callable[[str], tuple[list, dict]],
    email_sender: Callable[..., None],
) -> None:
    """Fetch subscribers whose next_scan_at has passed and run scans for each.

    Args:
        conn: Database connection (psycopg or sqlite3).
        scan_executor: Callable(domain) → (results, scores_dict).
        email_sender: Callable matching src.emailer.send_scan_report signature.
    """
    due = get_due_subscribers(conn)
    for row in due:
        domain = row["domain"]
        email = row["email"]
        sub_id = row["id"]
        interval_hours = row["interval_hours"]

        logger.info("Scanning %s for subscriber %s", domain, sub_id)
        try:
            scan_result = scan_executor(domain)
            # scan_executor may return (results, scores) tuple or just scores dict
            if isinstance(scan_result, tuple):
                results, scores = scan_result
            else:
                results, scores = [], scan_result

            unsubscribe_token = row["unsubscribe_token"]
            base_url = _get_base_url()
            unsubscribe_url = f"{base_url}/unsubscribe?token={unsubscribe_token}"

            email_sender(
                to_email=email,
                domain=domain,
                results=results,
                scores=scores,
                unsubscribe_url=unsubscribe_url,
            )
        except Exception:
            logger.exception("Error scanning %s (subscriber %s)", domain, sub_id)
        finally:
            update_next_scan(conn, sub_id, interval_hours=interval_hours)


def _get_base_url() -> str:
    import os
    return os.environ.get("BASE_URL", "http://localhost:8000")


def make_apscheduler_job(conn, scan_executor=None, email_sender=None):
    """Return a zero-argument callable suitable for APScheduler."""
    if scan_executor is None:
        scan_executor = _default_scan_executor
    if email_sender is None:
        from src.emailer import send_scan_report
        email_sender = send_scan_report

    def job():
        run_due_scans(conn, scan_executor=scan_executor, email_sender=email_sender)

    return job


def _default_scan_executor(domain: str) -> tuple[list, dict]:
    """Run the full check pipeline and return (results, scores)."""
    from concurrent.futures import ThreadPoolExecutor
    from src.checks import (
        check_spf, check_dkim, check_dmarc, check_ptr,
        check_kisa_rbl, check_kisa_whitedomain, check_blacklists,
    )
    from src.scorer import overall_score, naver_score, grade, naver_label

    checks = [
        check_spf, check_dkim, check_dmarc, check_ptr,
        check_kisa_rbl, check_kisa_whitedomain, check_blacklists,
    ]

    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(fn, domain) for fn in checks]
        results = [f.result() for f in futures]

    o_score = overall_score(results)
    n_score = naver_score(results)
    _, n_label = naver_label(n_score)
    scores = {
        "overall": o_score,
        "grade": grade(o_score),
        "naver": n_score,
        "naver_label": n_label,
    }
    return results, scores
