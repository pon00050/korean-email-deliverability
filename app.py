"""FastAPI web application — Phase 2 hosted monitoring SaaS.

Routes:
    GET  /              — Signup form
    POST /subscribe     — Create subscription + trigger immediate scan
    GET  /unsubscribe   — Deactivate subscription by token
    GET  /health        — Healthcheck (Railway deploy gate)

Environment variables:
    DATABASE_URL    — PostgreSQL DSN (provided by Railway)
    RESEND_API_KEY  — Resend API key
    FROM_EMAIL      — Verified sender address
    BASE_URL        — Public URL of this app (for unsubscribe links)
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

import psycopg
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.db import create_tables, create_subscriber, deactivate_subscriber, get_subscriber_by_token
from src.emailer import send_scan_report
from src.scheduler import make_apscheduler_job

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ---------------------------------------------------------------------------
# Database connection
# ---------------------------------------------------------------------------

def get_db():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    return psycopg.connect(url)


# ---------------------------------------------------------------------------
# Lifespan (startup / shutdown)
# ---------------------------------------------------------------------------

_scheduler: BackgroundScheduler | None = None
_db_conn = None
_startup_error: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler, _db_conn, _startup_error
    try:
        _db_conn = get_db()
        create_tables(_db_conn)
        logger.info("Database connection established")

        _scheduler = BackgroundScheduler()
        _scheduler.add_job(
            make_apscheduler_job(_db_conn),
            "interval",
            minutes=5,
            id="scan_job",
        )
        _scheduler.start()
        logger.info("Scheduler started")
    except Exception as e:
        _startup_error = str(e)
        logger.error("Startup error (app will still serve /health): %s", e)

    yield

    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
    if _db_conn:
        _db_conn.close()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Korean Email Deliverability Monitor",
    description="이메일 발송 건강도 모니터링 서비스",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    if _startup_error:
        return {"status": "degraded", "error": _startup_error}
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/subscribe", response_class=HTMLResponse)
async def subscribe(
    request: Request,
    domain: Annotated[str, Form()],
    email: Annotated[str, Form()],
    interval_hours: Annotated[int, Form()] = 168,
):
    domain = domain.strip().lower().removeprefix("https://").removeprefix("http://").rstrip("/")

    conn = get_db()
    try:
        sub_id = create_subscriber(conn, domain=domain, email=email, interval_hours=interval_hours)
    finally:
        conn.close()

    import threading
    threading.Thread(
        target=_run_scan_for_subscriber,
        args=(sub_id, domain, email, interval_hours),
        daemon=True,
    ).start()

    return templates.TemplateResponse(
        "signup.html",
        {
            "request": request,
            "success": True,
            "domain": domain,
            "email": email,
        },
    )


@app.get("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe(request: Request, token: str = ""):
    if not token:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "유효하지 않은 구독 취소 링크입니다."},
        )
    conn = get_db()
    try:
        row = get_subscriber_by_token(conn, token)
        if row:
            deactivate_subscriber(conn, token)
            domain = row["domain"]
        else:
            domain = None
    finally:
        conn.close()

    return templates.TemplateResponse(
        "signup.html",
        {
            "request": request,
            "unsubscribed": True,
            "domain": domain,
        },
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _run_scan_for_subscriber(
    sub_id: int, domain: str, email: str, interval_hours: int
) -> None:
    """Run a scan and send the report, then advance next_scan_at."""
    from src.scheduler import _default_scan_executor
    from src.db import update_next_scan

    base_url = os.environ.get("BASE_URL", "http://localhost:8000")
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT unsubscribe_token FROM subscribers WHERE id = %s", (sub_id,)
        ).fetchone()
        token = row[0] if row else ""
        unsubscribe_url = f"{base_url}/unsubscribe?token={token}"

        results, scores = _default_scan_executor(domain)
        send_scan_report(
            to_email=email,
            domain=domain,
            results=results,
            scores=scores,
            unsubscribe_url=unsubscribe_url,
        )
        update_next_scan(conn, sub_id, interval_hours=interval_hours)
    except Exception:
        logger.exception("Immediate scan failed for %s", domain)
    finally:
        conn.close()
