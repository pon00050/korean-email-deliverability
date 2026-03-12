"""FastAPI web application — Senderfit hosted monitoring SaaS.

Routes:
    GET  /                    — Landing page (Phase 4.3) or signup form
    POST /subscribe           — Create subscription + trigger immediate scan
    GET  /unsubscribe         — Deactivate subscription by token
    GET  /health              — Healthcheck (Railway deploy gate)
    POST /batch               — Phase 3 B2B batch enrichment API (≤50 domains)
    GET  /scan/{domain}       — Run scan, persist, redirect to /report/{token}
    GET  /report/{token}      — View a persisted scan report (no auth required)

Environment variables:
    DATABASE_URL    — PostgreSQL DSN (provided by Railway)
    RESEND_API_KEY  — Resend API key
    FROM_EMAIL      — Verified sender address
    BASE_URL        — Public URL of this app (for unsubscribe links)
    BATCH_API_KEY   — Optional/legacy API key for /batch; per-customer keys preferred
"""

from __future__ import annotations

import asyncio
import logging
import os
import threading
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Literal

import psycopg
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Form, Header, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.auth import (
    authenticate_api_key, hash_password, verify_password,
    create_session_token, get_current_customer_id,
    generate_csrf_token, validate_csrf_token,
    SESSION_COOKIE_NAME, SESSION_MAX_AGE,
)
from src.batch import batch_result_to_csv, run_batch_scan, _MAX_BATCH_DOMAINS
from src.db import (
    create_tables, create_subscriber, deactivate_subscriber,
    get_subscriber_by_token, get_scan_by_token,
    create_customer, get_customer_by_email, get_customer_by_id,
    list_customer_domains, list_scans_by_domain,
    save_dmarc_upload, list_dmarc_uploads, get_dmarc_upload,
)
from src.emailer import send_scan_report
from src.scanner import persist_scan
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
# Rate limiter (in-memory, resets on deploy — no Redis needed at this scale)
# ---------------------------------------------------------------------------

SCAN_RATE_LIMIT = 3  # scans per IP per hour
_scan_requests: dict[str, list[float]] = defaultdict(list)
_scan_lock = threading.Lock()


def _check_rate_limit(client_ip: str) -> bool:
    """Return True if the request is allowed, False if rate-limited."""
    with _scan_lock:
        now = time.time()
        window = 3600  # 1 hour
        timestamps = _scan_requests[client_ip]
        # Evict old entries
        active = [t for t in timestamps if now - t < window]
        if not active:
            # Clean up the key entirely to prevent unbounded dict growth
            _scan_requests.pop(client_ip, None)
            _scan_requests[client_ip] = [now]
            return True
        if len(active) >= SCAN_RATE_LIMIT:
            _scan_requests[client_ip] = active
            return False
        active.append(now)
        _scan_requests[client_ip] = active
        return True


# ---------------------------------------------------------------------------
# CSRF protection helpers
# ---------------------------------------------------------------------------

def _csrf_session_id(request: Request) -> str:
    """Derive a stable session identifier for CSRF token scoping."""
    token = request.cookies.get(SESSION_COOKIE_NAME, "")
    client_ip = request.client.host if request.client else "unknown"
    return f"{client_ip}:{token[:16]}"


def _make_csrf_token(request: Request) -> str:
    """Generate a CSRF token for the current request's session."""
    return generate_csrf_token(_csrf_session_id(request))


def _check_csrf(request: Request, csrf_token: str) -> None:
    """Validate CSRF token. Raises HTTPException(403) on failure."""
    if not csrf_token or not validate_csrf_token(csrf_token, _csrf_session_id(request)):
        raise HTTPException(status_code=403, detail="CSRF 토큰이 유효하지 않습니다.")


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
async def landing_page(request: Request):
    return templates.TemplateResponse(request, "landing.html", {"csrf_token": _make_csrf_token(request)})


@app.get("/subscribe", response_class=HTMLResponse)
async def subscribe_page(request: Request):
    return templates.TemplateResponse(request, "signup.html", {"csrf_token": _make_csrf_token(request)})


@app.post("/subscribe", response_class=HTMLResponse)
async def subscribe(
    request: Request,
    domain: Annotated[str, Form()] = "",
    email: Annotated[str, Form()] = "",
    interval_hours: Annotated[int, Form()] = 168,
    csrf_token: Annotated[str, Form()] = "",
):
    _check_csrf(request, csrf_token)
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
# POST /api/scan — HTMX scan from landing page (returns HTML partial)
# ---------------------------------------------------------------------------

@app.post("/api/scan", response_class=HTMLResponse)
async def api_scan(request: Request, domain: Annotated[str, Form()] = "", csrf_token: Annotated[str, Form()] = ""):
    _check_csrf(request, csrf_token)
    client_ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(client_ip):
        return HTMLResponse(
            '<div class="rate-limit-msg">'
            "&#x23F3; 시간당 검사 횟수를 초과했습니다. 잠시 후 다시 시도해 주세요."
            "</div>",
            status_code=429,
        )

    domain = normalize_domain(domain)
    if not domain or "." not in domain:
        return HTMLResponse(
            '<div class="rate-limit-msg">'
            "유효한 도메인을 입력해 주세요 (예: example.co.kr)."
            "</div>",
            status_code=400,
        )

    conn = get_db()
    try:
        results, scores, public_token = await asyncio.to_thread(
            persist_scan, conn, domain=domain
        )
    finally:
        conn.close()

    checks = [
        {"name": r.name, "status": r.status, "score": r.score, "message_ko": r.message_ko}
        for r in results
    ]
    return templates.TemplateResponse(
        request,
        "partials/scan_result.html",
        {
            "scores": scores,
            "checks": checks,
            "public_token": public_token,
        },
    )


# ---------------------------------------------------------------------------
# GET /scan/{domain} — Run scan, persist, redirect to report
# ---------------------------------------------------------------------------

@app.get("/scan/{domain}")
async def scan_domain(domain: str):
    domain = normalize_domain(domain)
    if not domain or "." not in domain:
        raise HTTPException(status_code=400, detail="유효한 도메인을 입력해 주세요.")

    conn = get_db()
    try:
        _, _, public_token = await asyncio.to_thread(
            persist_scan, conn, domain=domain
        )
    finally:
        conn.close()

    return RedirectResponse(url=f"/report/{public_token}", status_code=303)


# ---------------------------------------------------------------------------
# GET /report/{token} — View persisted scan report
# ---------------------------------------------------------------------------

@app.get("/report/{token}", response_class=HTMLResponse)
async def view_report(request: Request, token: str):
    conn = get_db()
    try:
        scan = get_scan_by_token(conn, token)
    finally:
        conn.close()

    if not scan:
        raise HTTPException(status_code=404, detail="보고서를 찾을 수 없습니다.")

    base_url = os.environ.get("BASE_URL", "http://localhost:8000")
    report_url = f"{base_url}/report/{token}"

    return templates.TemplateResponse(
        request,
        "report_web.html.j2",
        {
            "scan": scan,
            "report_url": report_url,
        },
    )


# ---------------------------------------------------------------------------
# GET /report/{token}/pdf — PDF export
# ---------------------------------------------------------------------------

@app.get("/report/{token}/pdf")
async def report_pdf(token: str):
    conn = get_db()
    try:
        scan = get_scan_by_token(conn, token)
    finally:
        conn.close()

    if not scan:
        raise HTTPException(status_code=404, detail="보고서를 찾을 수 없습니다.")

    try:
        from src.pdf import generate_pdf
    except ImportError:
        raise HTTPException(status_code=501, detail="PDF 생성 기능이 이 서버에서 사용 불가합니다 (WeasyPrint 미설치).")

    base_url = os.environ.get("BASE_URL", "http://localhost:8000")
    pdf_bytes = await asyncio.to_thread(generate_pdf, scan, base_url)

    filename = f"senderfit_{scan['domain']}_{token}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ---------------------------------------------------------------------------
# Auth — Register / Login / Logout
# ---------------------------------------------------------------------------

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"csrf_token": _make_csrf_token(request)})


@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    email: Annotated[str, Form()] = "",
    password: Annotated[str, Form()] = "",
    name: Annotated[str, Form()] = "",
    csrf_token: Annotated[str, Form()] = "",
):
    _check_csrf(request, csrf_token)
    email = email.strip().lower()
    if not email or "@" not in email:
        return templates.TemplateResponse(request, "register.html", {"error": "유효한 이메일을 입력해 주세요."})
    if len(password) < 8:
        return templates.TemplateResponse(request, "register.html", {"error": "비밀번호는 8자 이상이어야 합니다."})

    conn = get_db()
    try:
        existing = get_customer_by_email(conn, email)
        if existing:
            return templates.TemplateResponse(request, "register.html", {"error": "이미 등록된 이메일입니다."})

        pw_hash = hash_password(password)
        cid = create_customer(conn, email=email, name=name, password_hash=pw_hash)
    finally:
        conn.close()

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        create_session_token(cid),
        max_age=SESSION_MAX_AGE,
        httponly=True,
        samesite="lax",
    )
    return response


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"csrf_token": _make_csrf_token(request)})


@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: Annotated[str, Form()] = "",
    password: Annotated[str, Form()] = "",
    csrf_token: Annotated[str, Form()] = "",
):
    _check_csrf(request, csrf_token)
    email = email.strip().lower()
    conn = get_db()
    try:
        customer = get_customer_by_email(conn, email)
    finally:
        conn.close()

    if not customer or not customer["password_hash"]:
        return templates.TemplateResponse(request, "login.html", {"error": "이메일 또는 비밀번호가 올바르지 않습니다."})

    if not verify_password(password, customer["password_hash"]):
        return templates.TemplateResponse(request, "login.html", {"error": "이메일 또는 비밀번호가 올바르지 않습니다."})

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        create_session_token(customer["id"]),
        max_age=SESSION_MAX_AGE,
        httponly=True,
        samesite="lax",
    )
    return response


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response


# ---------------------------------------------------------------------------
# Dashboard — Multi-domain overview + scan history (auth required)
# ---------------------------------------------------------------------------

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    cid = get_current_customer_id(request)
    if not cid:
        return RedirectResponse(url="/login", status_code=303)

    conn = get_db()
    try:
        customer = get_customer_by_id(conn, cid)
        if not customer:
            return RedirectResponse(url="/login", status_code=303)
        domains = list_customer_domains(conn, cid)
    finally:
        conn.close()

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"customer": customer, "domains": domains},
    )


# ---------------------------------------------------------------------------
# DMARC Report Upload (auth required)
# NOTE: These routes MUST be declared before /dashboard/{domain} to avoid
# the path parameter capturing "dmarc" as a domain name.
# ---------------------------------------------------------------------------

DMARC_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
DMARC_MAX_DECOMPRESSED_SIZE = 50 * 1024 * 1024  # 50 MB — guards against gzip bombs


@app.get("/dashboard/dmarc", response_class=HTMLResponse)
async def dmarc_list(request: Request):
    cid = get_current_customer_id(request)
    if not cid:
        return RedirectResponse(url="/login", status_code=303)

    conn = get_db()
    try:
        customer = get_customer_by_id(conn, cid)
        if not customer:
            return RedirectResponse(url="/login", status_code=303)
        uploads = list_dmarc_uploads(conn, cid)
    finally:
        conn.close()

    return templates.TemplateResponse(
        request, "dmarc_list.html",
        {"customer": customer, "uploads": uploads, "csrf_token": _make_csrf_token(request)},
    )


@app.post("/dashboard/dmarc-upload", response_class=HTMLResponse)
async def dmarc_upload(request: Request, file: UploadFile, csrf_token: Annotated[str, Form()] = ""):
    _check_csrf(request, csrf_token)
    cid = get_current_customer_id(request)
    if not cid:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    content = await file.read()
    if len(content) > DMARC_MAX_SIZE:
        raise HTTPException(status_code=400, detail="파일 크기가 10MB를 초과합니다.")

    # Handle gzipped files
    if file.filename and file.filename.endswith(".gz"):
        import gzip
        try:
            content = gzip.decompress(content)
        except Exception:
            raise HTTPException(status_code=400, detail="gzip 파일을 해제할 수 없습니다.")
        if len(content) > DMARC_MAX_DECOMPRESSED_SIZE:
            raise HTTPException(status_code=400, detail="압축 해제된 파일이 50MB를 초과합니다.")

    import json
    from src.dmarc_parser import parse_dmarc_report

    try:
        report = parse_dmarc_report(content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    conn = get_db()
    try:
        save_dmarc_upload(
            conn,
            customer_id=cid,
            domain=report.domain,
            org_name=report.org_name,
            date_begin=report.date_begin,
            date_end=report.date_end,
            total_count=report.total_count,
            pass_count=report.pass_count,
            report_json=json.dumps(report.to_dict(), ensure_ascii=False),
        )
    finally:
        conn.close()

    return RedirectResponse(url="/dashboard/dmarc", status_code=303)


@app.get("/dashboard/dmarc/{upload_id}", response_class=HTMLResponse)
async def dmarc_detail(request: Request, upload_id: int):
    cid = get_current_customer_id(request)
    if not cid:
        return RedirectResponse(url="/login", status_code=303)

    conn = get_db()
    try:
        customer = get_customer_by_id(conn, cid)
        upload = get_dmarc_upload(conn, upload_id)
    finally:
        conn.close()

    if not upload or not customer:
        raise HTTPException(status_code=404, detail="보고서를 찾을 수 없습니다.")

    # Authorization: ensure the upload belongs to the current customer
    if upload["customer_id"] != cid:
        raise HTTPException(status_code=403, detail="접근 권한이 없습니다.")

    import json
    report_data = json.loads(upload["report_json"])

    return templates.TemplateResponse(
        request, "dmarc_detail.html",
        {"customer": customer, "upload": upload, "report": report_data},
    )


# ---------------------------------------------------------------------------
# GET /dashboard/{domain} — Scan history for a single domain (auth required)
# NOTE: This route MUST be declared AFTER /dashboard/dmarc* routes to avoid
# the {domain} parameter capturing "dmarc" as a domain name.
# ---------------------------------------------------------------------------

@app.get("/dashboard/{domain}", response_class=HTMLResponse)
async def dashboard_domain(request: Request, domain: str):
    cid = get_current_customer_id(request)
    if not cid:
        return RedirectResponse(url="/login", status_code=303)

    conn = get_db()
    try:
        customer = get_customer_by_id(conn, cid)
        if not customer:
            return RedirectResponse(url="/login", status_code=303)
        scans = list_scans_by_domain(conn, domain, customer_id=cid)
    finally:
        conn.close()

    return templates.TemplateResponse(
        request,
        "dashboard_domain.html",
        {"customer": customer, "domain": domain, "scans": scans},
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
    # Auth — per-customer key lookup with legacy env var fallback.
    # authenticate_api_key() handles both per-customer DB keys and BATCH_API_KEY fallback.
    # When neither is configured, auth is disabled (dev mode).
    has_legacy_key = bool(os.environ.get("BATCH_API_KEY", ""))
    if has_legacy_key or x_api_key:
        try:
            conn = get_db()
            customer = authenticate_api_key(x_api_key, conn)
            conn.close()
        except Exception:
            # DB unavailable — authenticate_api_key can't check DB keys,
            # but we can still check the legacy env var directly.
            customer = authenticate_api_key(x_api_key, None) if x_api_key else None
        if has_legacy_key and not customer:
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
    """Run a scan, persist results, send the report, then advance next_scan_at."""
    from src.scanner import run_scan
    from src.db import update_next_scan

    base_url = os.environ.get("BASE_URL", "http://localhost:8000")
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT unsubscribe_token FROM subscribers WHERE id = %s", (sub_id,)
        ).fetchone()
        token = row[0] if row else ""
        unsubscribe_url = f"{base_url}/unsubscribe?token={token}"

        results, scores = run_scan(domain)
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
