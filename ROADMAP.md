# ROADMAP.md

Post-MVP feature roadmap. MVP is the CLI scan tool with 7 checks + Naver score.

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
- [ ] **Resend credentials** — `RESEND_API_KEY` and `FROM_EMAIL` are placeholders in
  Railway Variables. End-to-end email delivery blocked until a sending domain is
  verified in Resend and credentials are updated. See `SETUP_PHASE2.md` Step 2.

**Delivered beyond original scope:** self-serve signup UI (originally "out of scope this phase").

---

## Phase 3 — Batch B2B Enrichment API (pre-KISA / K-DATA)

- [ ] **Batch input endpoint** — accept domain list via CSV upload or JSON API (POST `/batch`)
- [ ] **Structured output** — per-domain risk data returned as CSV/JSON (not HTML report)
- [ ] **API authentication** — API key issuance and validation for B2B clients
- [ ] **Diff / alerting logic** — detect score changes between runs; trigger email alert on regression
- [ ] **Async job handling** — queue large batches (100K+ domains) without blocking; poll endpoint for results

**Rationale:** This is the genuine monetizable product. A Tax SaaS company (e.g., Barobill with
100K+ client domains) submits their domain list; Senderfit returns structured risk data on a
weekly/monthly cadence. The ThreadPoolExecutor scanner is ~80% of the work — batch I/O and
structured output are the remaining gap. Also the product shape that makes K-DATA Track 2
(가공기업) eligible and KISA SECaaS credible.

---

## Phase 4 — Web UI + Multi-Domain Dashboard (post-May 2026)

- [ ] Hosted web UI: submit a domain, get a shareable scan URL (mail-tester.com style)
- [ ] Multi-domain dashboard: customer sees all subscribed domains and their current scores
- [ ] DMARC aggregate report upload: XML parsing, pass/fail summary by source IP
- [ ] PDF export of scan report

---

## Phase 5 — Additional Checks + Intelligence (longer-term)

- [ ] 카카오/다음 메일 호환성 점수 (Kakao/Daum Mail compatibility score — same proxy-indicator approach as Naver)
- [ ] 도메인 일괄 검사 — CSV 입력 (Bulk domain scan via CSV input)
- [ ] DMARC 집계 리포트 추세 뷰 (DMARC aggregate report trend view — weekly/monthly pass rate over time)

---

## Phase 6 — Hard Problems (deferred)

- [ ] 네이버 시드 계정 받은편지함 테스트 (Naver seed account inbox placement test) —
  requires owning seed Naver accounts, actual mail delivery, inbox vs. spam classification.
  Hard operational problem, deferred until there is paying demand for it.
