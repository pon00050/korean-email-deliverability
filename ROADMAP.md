# ROADMAP.md

Post-MVP feature roadmap. MVP is the CLI scan tool with 7 checks + Naver score.

For current open action items, see NEXT_ACTIONS.md.

---

## Phase 1 — MVP ✅ (complete)

- CLI scan: 7 checks (SPF, DKIM, DMARC, PTR, KISA RBL, 화이트도메인, international
  blacklists) + Naver compatibility score
- Self-contained HTML report output
- `check.py <domain>` entry point

---

## Phase 2 — Hosted Monitoring Service ✅ (live 2026-03-02)

- [x] **Cloud deployment** — FastAPI app running on Railway (`dev` branch auto-deploy).
  Live at `https://senderfit.kr`.
- [x] **Subscriber store** — PostgreSQL on Railway; `subscribers` table with
  (domain, email, interval, next_scan_at, active).
- [x] **Scheduler** — APScheduler running inside FastAPI `lifespan`; scans each active
  subscriber at configured interval.
- [x] **Email delivery** — Resend integration implemented (`src/emailer.py`);
  HTML report delivered to subscriber on each scheduled scan.
- [x] **Self-serve signup form** — `/` serves a signup form (scope expanded beyond
  original plan; operator no longer needs to seed subscribers manually).
- [x] **Typer CLI + `senderfit` entry point** — Phase 1 CLI upgraded from argparse
  to Typer; `senderfit` installable command registered in `[project.scripts]`.
  Backward-compatible: `uv run check.py` continues to work.
- [x] **Resend credentials** — `RESEND_API_KEY` and `FROM_EMAIL` set in Railway Variables.
  End-to-end email delivery verified 2026-03-05: scan report received in inbox,
  Korean text correct, unsubscribe link working. Phase 2 is 100% ✅.

**Delivered beyond original scope:** self-serve signup UI (originally "out of scope this phase").

---

## Phase 3 — Batch B2B Enrichment API ✅ (complete)

- [x] **Batch input endpoint** — accept domain list via CSV upload or JSON API (POST `/batch`)
- [x] **Structured output** — per-domain risk data returned as CSV/JSON (not HTML report)
- [x] **API authentication** — API key issuance and validation for B2B clients
Planned extensions: diff/alerting logic (score-change email triggers) and async job
handling for batches >50 domains are scoped but not yet scheduled.

---

## Phase 4 — Web UI + Multi-Domain Dashboard 🔧 (in progress)

- [x] **Database schema foundation** — customers, api_keys, scans, scan_checks, dmarc_uploads tables (SQLite + PG)
- [x] **Per-customer API keys** — `sf_live_` prefixed keys, SHA-256 hashed, admin CLI provisioning
- [x] **Scan persistence + shareable URLs** — every scan gets a permanent `/report/{token}` URL
- [x] **Landing page + web scan UI** — HTMX-powered Korean landing page with inline scan results
- [x] **Multi-domain dashboard** — session auth (itsdangerous), login/register, scan history per domain
- [x] **DMARC aggregate report upload** — XML parsing (RFC 7489), per-source-IP pass/fail summary
- [x] **PDF export** — WeasyPrint HTML→PDF with Korean font support

---

## Phase 5 — Additional Checks + Intelligence (longer-term)

- 카카오/다음 메일 호환성 점수 (Kakao/Daum Mail compatibility score — same proxy-indicator approach as Naver)
- 도메인 일괄 검사 — CSV 입력 (Bulk domain scan via CSV input)
- DMARC 집계 리포트 추세 뷰 (DMARC aggregate report trend view — weekly/monthly pass rate over time)

---

## Phase 6 — Hard Problems (deferred)

- 네이버 시드 계정 받은편지함 테스트 (Naver seed account inbox placement test) —
  requires owning seed Naver accounts, actual mail delivery, inbox vs. spam classification.
  Hard operational problem, deferred until there is paying demand for it.
