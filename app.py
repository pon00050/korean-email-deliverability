"""FastAPI web application — Phase 2 hosted monitoring SaaS.

Routes:
    GET  /              — Signup form
    POST /subscribe     — Create subscription + trigger immediate scan
    GET  /unsubscribe   — Deactivate subscription by token
    GET  /health        — Healthcheck (Railway deploy gate)
    POST /batch         — Phase 3 B2B batch enrichment API (≤50 domains)

Environment variables:
    DATABASE_URL    — PostgreSQL DSN (provided by Railway)
    RESEND_API_KEY  — Resend API key
    FROM_EMAIL      — Verified sender address
    BASE_URL        — Public URL of this app (for unsubscribe links)
    BATCH_API_KEY   — Optional API key for /batch; if unset, auth is disabled
"""

from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Literal

import psycopg
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Form, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.batch import batch_result_to_csv, run_batch_scan, _MAX_BATCH_DOMAINS
from src.db import create_tables, create_subscriber, deactivate_subscriber, get_subscriber_by_token
from src.emailer import send_scan_report
from src.scheduler import make_apscheduler_job
from src.utils import normalize_domain

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
_startup_error: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler, _startup_error
    _startup_error = None  # reset each startup (avoids state leaking between test runs)

    if os.environ.get("SENDERFIT_SKIP_DB"):
        # Batch-only dev mode: skip DB and scheduler so /health returns "ok"
        # and /batch works without a Postgres connection.
        logger.info("SENDERFIT_SKIP_DB set — DB and scheduler init skipped")
    else:
        try:
            with get_db() as _init_conn:
                create_tables(_init_conn)
            logger.info("Database tables ready")

            _scheduler = BackgroundScheduler()
            _scheduler.add_job(
                make_apscheduler_job(get_db),
                "interval",
                minutes=5,
                id="scan_job",
                max_instances=1,
            )
            _scheduler.start()
            logger.info("Scheduler started")
        except Exception as e:
            _startup_error = str(e)
            logger.error("Startup error (app will still serve /health): %s", e)

    yield

    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)


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


MIN_INTERVAL_HOURS = 1
MAX_INTERVAL_HOURS = 8760  # 1 year


def _validate_subscribe_input(
    domain: str, email: str, interval_hours: int
) -> str | None:
    """Return an error message string if input is invalid, else None."""
    if not domain or "." not in domain:
        return "유효한 도메인을 입력해 주세요 (예: example.co.kr)."
    at_pos = email.find("@")
    if at_pos < 1 or "." not in email[at_pos:]:
        return "유효한 이메일 주소를 입력해 주세요."
    if not (MIN_INTERVAL_HOURS <= interval_hours <= MAX_INTERVAL_HOURS):
        return f"스캔 주기는 {MIN_INTERVAL_HOURS}시간에서 {MAX_INTERVAL_HOURS}시간 사이여야 합니다."
    return None


@app.get("/", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request, "signup.html", {})


@app.post("/subscribe", response_class=HTMLResponse)
async def subscribe(
    request: Request,
    domain: Annotated[str, Form()] = "",
    email: Annotated[str, Form()] = "",
    interval_hours: Annotated[int, Form()] = 168,
):
    domain = normalize_domain(domain)
    email = email.strip()

    error = _validate_subscribe_input(domain, email, interval_hours)
    if error:
        return templates.TemplateResponse(request, "signup.html", {"error": error})

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
        request,
        "signup.html",
        {
            "success": True,
            "domain": domain,
            "email": email,
        },
    )


@app.get("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe(request: Request, token: str = ""):
    if not token:
        return templates.TemplateResponse(
            request,
            "signup.html",
            {"error": "유효하지 않은 구독 취소 링크입니다."},
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
        request,
        "signup.html",
        {
            "unsubscribed": True,
            "domain": domain,
        },
    )


# ---------------------------------------------------------------------------
# POST /batch — Phase 3 B2B Enrichment API
# ---------------------------------------------------------------------------

class BatchRequest(BaseModel):
    domains: list[str]
    format: Literal["json", "csv"] = "json"


@app.post("/batch")
async def batch_scan(
    body: BatchRequest,
    x_api_key: str = Header(default=""),
):
    # Auth — disabled when BATCH_API_KEY is not set (dev/test mode)
    required_key = os.environ.get("BATCH_API_KEY", "")
    if required_key and x_api_key != required_key:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")

    if not body.domains or len(body.domains) > _MAX_BATCH_DOMAINS:
        raise HTTPException(
            status_code=422,
            detail=f"domains must be 1–{_MAX_BATCH_DOMAINS} items",
        )
    domains = [normalize_domain(d) for d in body.domains if "." in d]
    if not domains:
        raise HTTPException(status_code=422, detail="No valid domains provided")

    data = await asyncio.to_thread(run_batch_scan, domains)

    if body.format == "csv":
        return _batch_to_csv_response(data)
    return JSONResponse(content=data)


def _batch_to_csv_response(data: dict) -> Response:
    return Response(
        content=batch_result_to_csv(data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=senderfit_batch.csv"},
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
