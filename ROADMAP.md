# ROADMAP.md

Post-MVP feature roadmap. MVP is the CLI scan tool with 7 checks + Naver score.

---

## Phase 1 — MVP ✅ (complete)

- CLI scan: 7 checks (SPF, DKIM, DMARC, PTR, KISA RBL, 화이트도메인, international
  blacklists) + Naver compatibility score
- Self-contained HTML report output
- `check.py <domain>` entry point

---

## Phase 2 — Hosted Monitoring Service (March 2026, ~4 weeks)

- [ ] **Cloud deployment** — host existing scan logic on a server (not customer's machine).
  Single hosted endpoint that accepts a domain and runs the full check suite.
- [ ] **Subscriber store** — minimal persistent store: (domain, email, interval, next_scan_at).
  Seeded manually by operator; no customer-facing UI required.
- [ ] **Scheduler** — cron/task runner: for each active subscription, run scan at interval,
  store result.
- [ ] **Email delivery** — on each scheduled scan, send the existing HTML report to the
  subscriber's email address.

**Out of scope this phase:** web UI, dashboard, multi-domain views, self-serve signup,
payment processing.

---

## Phase 3 — Web UI + Multi-Domain Dashboard (post-May 2026)

- [ ] Hosted web UI: submit a domain, get a shareable scan URL (mail-tester.com style)
- [ ] Multi-domain dashboard: customer sees all subscribed domains and their current scores
- [ ] DMARC aggregate report upload: XML parsing, pass/fail summary by source IP
- [ ] PDF export of scan report

---

## Phase 4 — Additional Checks + Intelligence (longer-term)

- [ ] 카카오/다음 메일 호환성 점수 (Kakao/Daum Mail compatibility score — same proxy-indicator approach as Naver)
- [ ] 도메인 일괄 검사 — CSV 입력 (Bulk domain scan via CSV input)
- [ ] DMARC 집계 리포트 추세 뷰 (DMARC aggregate report trend view — weekly/monthly pass rate over time)

---

## Phase 5 — Hard Problems (deferred)

- [ ] 네이버 시드 계정 받은편지함 테스트 (Naver seed account inbox placement test) —
  requires owning seed Naver accounts, actual mail delivery, inbox vs. spam classification.
  Hard operational problem, deferred until there is paying demand for it.
