# JOURNEY.md — How This Project Came to Be

A narrative walkthrough of the architecture, written so any future developer or AI
can reconstruct the full arc without re-exploring the codebase from scratch.

---

## Act 1 — The Original Problem

Korea has the lowest DMARC adoption rate in APAC: roughly 1.8%.
Tax and accounting SaaS companies send legally-significant transactional email
(세금계산서, 전자계산서) and face a 0.3–0.5% surcharge per failed delivery.
Yet almost none of them know whether their emails are being silently blocked.

The KISA RBL (Korea Internet & Security Agency Real-time Blacklist) is the
killer detail: it blocks senders with no bounce notification. A company can be
blacklisted and have no idea. There is no Korean-language deliverability tool.
No one has built this.

The project exists to fill that gap — starting with a CLI scanner that answers
the question "why is my email going to spam?" in Korean, for Korean domains.

---

## Act 2 — The Eight Checks and Why Each Exists

Eight checks were chosen for the MVP. Each maps to a specific failure mode
observed in Korean infrastructure:

1. **SPF** (`src/checks/spf.py`) — the baseline. Without an SPF record, any
   server can claim to send as your domain. Most Korean companies either have
   no record or have `~all` (soft fail) instead of `-all`.

2. **DKIM** (`src/checks/dkim.py`) — required for DMARC alignment. The check
   auto-discovers selectors (common ones: `default`, `google`, `mail`, `dkim`,
   `selector1`, `selector2`). It also validates key strength — RSA keys under
   1024 bits are flagged.

3. **DMARC** (`src/checks/dmarc.py`) — the strongest policy signal. Korea's
   1.8% adoption rate means this fails for almost every prospect, making it the
   highest-weight check (25 points). The check validates policy strictness
   (`none` / `quarantine` / `reject`) and pct alignment.

4. **PTR / Reverse DNS** (`src/checks/ptr.py`) — Naver Mail specifically
   checks whether the sending IP has a valid PTR record matching the forward
   hostname. Missing PTR is one of the most common causes of Naver rejection.

5. **KISA RBL** (`src/checks/kisa_rbl.py`) — the Korea-specific silent killer.
   Query format: `{reversed-ip}.rbl.kisa.or.kr`. Verified active as of
   2026-02-28. A listed IP means silent delivery failure with no bounce.

6. **KISA 화이트도메인** (`src/checks/kisa_whitedomain.py`) — the inverse of
   the RBL. KISA runs a voluntary whitelist at `spam.kisa.or.kr`. There is no
   public API, so the check always returns `status="error"` and directs the
   user to register manually. The scorer excludes this check's weight when the
   status is `error`, so a perfect 100/100 score is still achievable.

7. **International Blacklists** (`src/checks/blacklists.py`) — Spamhaus
   ZEN, Barracuda BRBL, SURBL. All DNS-based. Global reputation affects
   non-Korean mailboxes (Gmail, Outlook) even when KISA RBL is clean.

8. **Naver Mail Compatibility** — a composite score derived from checks 1–7
   using Naver-specific weights. This is NOT a separate check module; it is
   computed entirely inside `src/scorer.py` from the results of the other
   checks. Displayed as a secondary indicator. NOT added to the overall score
   to avoid double-counting.

---

## Act 3 — Infrastructure Beneath the Checks

### Parallelization

The original sequential implementation took ~79 seconds. That is unusable.

All checks run in parallel via `ThreadPoolExecutor` in `check.py`. Each check
is submitted as a future and results are collected after all futures resolve.
Within checks that make multiple DNS queries (e.g., DKIM trying many selectors,
international blacklist checking multiple lists), internal queries are also
parallelized with their own `ThreadPoolExecutor`.

### DNS Timeout

Every `dns.resolver.resolve()` call uses `lifetime=DNS_TIMEOUT` where
`DNS_TIMEOUT = 5` (seconds), imported from `src/checks/_dns_cache.py`. Without
this, a single unresponsive nameserver can hang the entire scan indefinitely.

### Shared MX Cache

`src/checks/_dns_cache.py` also provides `get_sending_ips()` — a cached
function that resolves MX records and then the A records for each MX host,
returning the actual sending IP addresses. Multiple checks need these IPs
(PTR, KISA RBL, international blacklists). Without caching, each check would
independently query MX and A records, adding latency and risk of inconsistency.

---

## Act 4 — The Scoring Problem

### Overall Score

Weights are defined in `src/scorer.py` and must sum to 100:

| Check               | Weight | Rationale                                              |
|---------------------|--------|--------------------------------------------------------|
| DMARC               | 25     | Strongest policy signal; almost never set in Korea     |
| SPF                 | 20     | Baseline authentication; widely supported              |
| KISA RBL            | 15     | Korea-specific silent blocking                         |
| DKIM                | 15     | Required for DMARC alignment                           |
| PTR                 | 10     | Naver Mail sender signal; often misconfigured          |
| 국제 블랙리스트     | 10     | Global reputation; affects non-Korean mailboxes        |
| KISA 화이트도메인   | 5      | Beneficial but not blocking; most domains unregistered |

> **Source of truth:** `WEIGHTS` dict in `src/scorer.py`. The table above mirrors
> it for reference — update scorer.py first if weights change.

### The Error Exclusion Rule

When a check returns `status="error"` (infrastructure problem — not the
sender's fault), its weight is excluded from the denominator before computing
the percentage score. This means `kisa_whitedomain` (which always returns
`error` because there is no public API) does not penalize legitimate senders.
A domain with all other checks passing can still score 100/100.

### The Naver Score

Naver Mail has its own weighting table (`NAVER_WEIGHTS` in `src/scorer.py`)
because its filtering logic differs from global standards — PTR and SPF matter
more; DMARC matters less (Naver's spam filter predates widespread DMARC). The
Naver score is computed separately and displayed alongside the overall score
as a secondary indicator. It is intentionally excluded from the overall score
to prevent double-counting.

### Grade Thresholds

Defined as `GRADE_THRESHOLDS` in `src/scorer.py`:
`A (90+)`, `B (75–89)`, `C (60–74)`, `D (40–59)`, `F (<40)`.

### Terminal Display Note

`status_emoji()` in `src/scorer.py` maps both `"warn"` and `"error"` to `⚠️`.
A `⚠️` in CLI output does **not** mean the check returned `warn` — it may be
`error` (e.g. `kisa_whitedomain`). Always check `result.status` directly if
the distinction matters (e.g. when debugging scorer weight exclusion).

---

## Act 5 — The Data Model

`src/models.py` defines `CheckResult` — the contract every check must return:

```python
@dataclass
class CheckResult:
    name: str              # e.g. "spf", "dkim", "dmarc"
    status: str            # "pass" | "warn" | "fail" | "error"
    score: int             # 0–100
    message_ko: str        # one-line Korean summary
    detail_ko: str         # extended Korean explanation
    remediation_ko: str    # actionable fix in Korean
    raw: str | None        # raw DNS/lookup data for debugging
```

Korean is the primary language for all user-facing strings. The `raw` field
preserves the underlying data so the HTML report can show exactly what was
found in DNS without re-querying.

---

## Act 6 — Phase 1 Complete: The CLI Report

`check.py` is the Phase 1 entry point. It:

1. Accepts a domain argument
2. Runs all eight checks in parallel via `ThreadPoolExecutor`
3. Passes results to `src/scorer.py` to compute overall + Naver scores
4. Passes everything to `src/report.py` to render a self-contained HTML file

The HTML report is generated from a Jinja2 template (`templates/report.html.j2`).
It is designed to be a single file with all styles inlined — no external
dependencies, shareable by email attachment.

---

## Act 7 — Phase 2: The Complexity Multiplies

Phase 2 added four new components to turn the CLI tool into a hosted SaaS:

### `src/db.py` — PostgreSQL via psycopg3

Stores subscriber information in a single `subscribers` table (email, domain,
signup metadata, last scan results as a JSON blob, timestamps).

Connection is established at startup in `app.py` using the `DATABASE_URL`
environment variable injected by Railway.

### `src/emailer.py` — Resend API

Sends the weekly scan report to registered users. Uses Resend (not SMTP)
because Resend provides reliable transactional delivery with SPF/DKIM/DMARC
already configured on the sending domain — appropriate for a deliverability
product to eat its own dog food.

The email body is rendered from `templates/email_report.html.j2` (Jinja2).
Fallback: if Resend returns an error, the result is logged but does not raise
— the scheduler must not crash on a single failed delivery.

### `src/scheduler.py` — APScheduler

Runs periodic scans on all registered domains. Uses a conn-per-run pattern:
each job invocation calls `conn = conn_factory()` to get a fresh connection,
and closes it in a `try/finally` block. This avoids stale connections between
scheduled runs (PostgreSQL closes idle connections).

Key constraint: the scheduler must not trigger duplicate scans if a previous
job is still running. APScheduler's `misfire_grace_time` and job coalescing
handle this.

### `app.py` — FastAPI

Three routes:

- `GET /` — landing page / signup form (`templates/signup.html`)
- `POST /subscribe` — validates domain, writes to DB, triggers immediate scan
- `GET /health` — health check endpoint for Railway

The app uses `fastapi[standard]` (not bare `fastapi`) because the `[standard]`
extra pulls in `python-multipart` (required for form parsing), `jinja2`
(required for template rendering), and `uvicorn[standard]` automatically.
Using bare `fastapi` causes silent runtime crashes when forms are submitted.

---

## Act 8 — The Deployment Layer

Railway hosts two services: a managed Postgres instance and the app service.

### Lessons Learned (the hard way)

**Always commit `uv.lock` after editing `pyproject.toml`.**
Railway runs `uv sync --locked` (strict mode). A stale lockfile means packages
are not installed. No error is shown during build — the crash only happens at
runtime.

**Do not include `[build] builder = "nixpacks"` in `railway.toml`.**
Railpack is the current default. Forcing Nixpacks conflicts with Railpack's
start command resolution, causing the start command to be silently ignored.

**Start command must use `uv run`:**
```
uv run uvicorn app:app --host 0.0.0.0 --port $PORT
```
The virtual environment is not on the system PATH. Bare `uvicorn` or
`python -m uvicorn` fail because they cannot find the installed packages.

**`DATABASE_URL` is not auto-injected cross-service.**
Even when the Postgres service is in the same Railway project, the app service
does not automatically receive `DATABASE_URL`. It must be manually added to
the app service's Variables tab as `${{Postgres.DATABASE_URL}}`.

**`healthcheckTimeout = 300`.**
The default 30-second timeout is too short for an app that establishes a DB
connection during startup. Set to 300 seconds in `railway.toml`.

---

## Act 9 — The Consistency Fixes

After Phase 2 launched, a pre-Phase-3 review found seven silent inconsistencies
that had accumulated. Resolved in commit `f95dd51` (later extended by
integration-pipeline tests in `cd0ce8d`, bringing the suite to 83 tests):

1. **`kisa_whitedomain` status** was `"warn"` — changed to `"error"` so the
   scorer correctly excludes its weight. Previously, a domain with no KISA
   registration was being penalized for something outside their control.

2. **`ptr` dead code** — the `if not mx_hosts` branch was unreachable (MX
   lookup always returns a list, never `None`). Removed. The no-MX case now
   correctly returns `status="fail"` instead of `"warn"`.

3. **`kisa_rbl` error constant** — `KISA_RBL_SCORE_ERROR = 50` was unused by
   the scorer (which handles error exclusion itself). Changed to `0` to reflect
   reality rather than imply the check assigns its own score on error.

4. **`dkim` naming convention** — `DKIM_WEAK_KEY_SCORE` renamed to
   `DKIM_SCORE_WEAK_KEY` to match the project-wide constant naming pattern.

5. **`scheduler` type hint** — tightened `scan_executor` return type to
   `tuple[list[CheckResult], dict[str, Any]]`.

6. **`scorer` comment** — added rationale comment to `NAVER_WEIGHTS` explaining
   why PTR/SPF are weighted higher for Naver than globally.

7. **Tests updated** — whitedomain assertions updated for new `"error"` status;
   `TestPTR.test_no_mx_returns_fail` added.

---

## Act 9.5 — The Connection Factory Pattern

`src/scheduler.py` accepts a `conn_factory: Callable[[], Connection]` argument
instead of a single `conn`. APScheduler calls the job function on a schedule —
potentially many times over days or weeks. A single connection passed at startup
goes stale between runs: PostgreSQL closes idle connections after its
`tcp_keepalives_idle` / `idle_in_transaction_session_timeout` thresholds.

The factory solves this by creating a fresh connection at the start of each job
run and closing it in a `try/finally` block regardless of success or failure.
This pattern is encapsulated in `src/scheduler.py:make_apscheduler_job()`.

---

## Act 10 — The Test Suite

83 tests across 9 files, organized into four categories:

| Category | Files | What they test |
|---|---|---|
| Pure unit (no I/O) | `test_scorer.py`, `test_utils.py` | Score calculation, grade thresholds, weight sums |
| Unit with mocked DNS/HTTP | `test_check_spf_dmarc_ptr_blacklists.py`, `test_kisa_whitedomain.py`, `test_emailer.py` | Each check in isolation; DNS responses are patched |
| Integration (real SQLite, real Jinja2) | `test_db.py`, `test_scheduler.py`, `test_routes.py` | DB schema, scheduler job logic, FastAPI routes |
| Pipeline integration (all 7 checks, DNS mocked) | `test_integration_scan_pipeline.py` | Full scan-to-score pipeline; catches weight-sum drift and missing check wiring |

The pipeline integration tests are the most important safety net for Phase 3
work: adding a new check without updating the pipeline test will silently cause
the all-pass scenario to score below 100.

---

## The Mental Map

```
check.py (CLI entry)          app.py (FastAPI entry)
     |                              |
     |  ←— parallel ThreadPool —→  |
     |                              |
     +——————————————————————————————+
                    |
          [8 checks run in parallel]
                    |
     ┌──────────────┼──────────────┐
     |              |              |
  spf.py         dkim.py       dmarc.py
  ptr.py       kisa_rbl.py   blacklists.py
  kisa_whitedomain.py
     |              |              |
     └──────────────┼──────────────┘
                    |
             CheckResult ×8
            (src/models.py)
                    |
          ┌─────────┴──────────┐
          |                    |
      scorer.py           report.py
   (overall score,      (HTML render —
    Naver score,         Phase 1 CLI)
    grade)                    |
          |              report.html
          |
     Phase 2 only:
          |
     ┌────┴────┐
     |         |
   db.py    emailer.py
(Postgres)  (Resend)
     |         |
     └────┬────┘
          |
    scheduler.py
   (APScheduler —
    weekly scans)


Infrastructure shared across all checks:
  src/checks/_dns_cache.py
    - DNS_TIMEOUT = 5 (applied to every resolve() call)
    - get_sending_ips() (resolves MX then A records; cached, shared across checks)
```

---

*Last updated: 2026-03-02. Reflects codebase state after commit `cd0ce8d` on `dev` branch. 83 tests passing.*
