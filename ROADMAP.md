# ROADMAP.md

Post-MVP feature roadmap. MVP is the CLI scan tool with 7 checks + Naver score.

## Content / GTM — Thundermail 권위 공백 (즉시 실행 가능)

**배경:** 썬더메일(앤드와이즈)은 KISA 화이트도메인 등록 절차 가이드를 가장 상세히 작성해 온
국내 이메일 전송 분야 권위 콘텐츠 제공자였다. 화이트도메인 서비스가 2024년 6월 28일 종료된 후
해당 콘텐츠는 더 이상 유효하지 않으며, 대체 콘텐츠는 존재하지 않는다.

**기회:** 이 프로젝트는 화이트도메인 종료 이후의 공백을 채울 수 있는 위치에 있다.

**즉시 작성 가능한 콘텐츠:**
- "KISA 화이트도메인 종료 이후 네이버/카카오 수신함 도달률 확보 방법" (SPF/DKIM/DMARC 전환 가이드)
- 타깃 검색어: "화이트도메인 종료", "화이트도메인 대체", "네이버 메일 수신함 도달"
- 배포 채널: 요즘IT, Velog, GitHub README

**왜 지금인가:** 썬더메일의 마지막 실질적 업데이트는 2024년 7월. 이 틈새는 현재 열려 있다.

---

## KISA SECaaS Eligibility Threshold

To qualify as a SECaaS 공급기업 under the KISA ICT 중소기업 정보보호 지원사업, the product
must clear four requirements (currently all unmet):

| Requirement | Current state | What needs to change |
|---|---|---|
| Runs on vendor's cloud, not customer's machine | CLI runs locally | Host the scanner on a server |
| Customer receives results without running the CLI | Manual invocation | Customer subscribes; results pushed to them |
| Scans happen on a recurring schedule | One-shot | Add a scheduler (daily or weekly cron) |
| Results delivered remotely | Local HTML file | Email the report (or dashboard) |

**Minimum viable change:** host the existing scan logic, add a scheduler, email the HTML output.
Everything beyond this (dashboard, subscription management, multi-domain UI) is product polish,
not an eligibility requirement.

**Why this matters:** Clearing this threshold is the prerequisite for applying to the 2026
공급기업 pool (application window: ~April–May 2026). The pool grants access to the government
80% subsidy program (최대 ₩4.4M per SME buyer). No certification is required to apply —
the above architectural change alone is sufficient to argue SECaaS eligibility.
Apply under the **네트워크 위협탐지 및 대응** or **스팸차단** category, not "이메일 보안"
(that slot is defined as gateway/filtering tools).

The items in Phase 2 below that satisfy this threshold are marked **(KISA gate)**.

---

## Phase 1 — MVP ✅ (complete)

**Technical:**
- CLI scan: 7 checks (SPF, DKIM, DMARC, PTR, KISA RBL, 화이트도메인, international
  blacklists) + Naver compatibility score
- Self-contained HTML report output
- `check.py <domain>` entry point

**Commercial unlocks:** Free lead gen, one-time paid scan (₩30K–80K), remediation
package (₩200K–500K), annual health check retainer (₩150K–300K/year, delivered manually).

---

## Phase 2 — Hosted Monitoring Service (March 2026, ~4 weeks)

**Technical:**
- [ ] **Cloud deployment** — host existing scan logic on a server (not customer's machine).
  Single hosted endpoint that accepts a domain and runs the full check suite.
  **(KISA gate: hosted)**
- [ ] **Subscriber store** — minimal persistent store: (domain, email, interval, next_scan_at).
  Seeded manually by operator; no customer-facing UI required.
- [ ] **Scheduler** — cron/task runner: for each active subscription, run scan at interval,
  store result. **(KISA gate: scheduler)**
- [ ] **Email delivery** — on each scheduled scan, send the existing HTML report to the
  subscriber's email address. **(KISA gate: remote delivery)**

**Out of scope this phase:** web UI, dashboard, multi-domain views, self-serve signup,
payment processing (manual invoicing to start).

**Commercial unlocks:** Monthly monitoring subscription ₩19K–49K/월 (first recurring
revenue). Annual retainer upgrades from manual-delivery to automated at same price.

**Business / Ops (April, after dev complete):**
- Confirm legal entity type with KISA before registering: email risc@kisa.or.kr or
  call 02-405-5031 (국민신문고 민원 draft already written in pricing_strategy_research.md)
- Register legal entity (개인사업자 or 1인 법인 depending on KISA answer)
- Prepare 공급기업 pool application: 제품 소개서, 서비스 설명, 가격표
- Submit application — window ~late April to May 28, 2026;
  category: **네트워크 위협탐지 및 대응** or **스팸차단** (NOT "이메일 보안")
- Optional: minimal landing page describing the hosted monitoring service

**KISA unlock:** SECaaS eligibility threshold cleared by Phase 2 tech → 2026
공급기업 pool application possible → government 80% subsidy channel (earliest
revenue: 2027 if pool accepted).

---

## Phase 3 — Web UI + Multi-Domain Dashboard (post-May 2026)

**Technical:**
- [ ] Hosted web UI: submit a domain, get a shareable scan URL (mail-tester.com style)
- [ ] Multi-domain dashboard: customer sees all subscribed domains and their current scores
- [ ] DMARC aggregate report upload: XML parsing, pass/fail summary by source IP
- [ ] PDF export of scan report

**Commercial unlock:** Agency/ESP multi-domain tier ₩100K+/월; self-serve onboarding
(removes manual subscriber setup bottleneck).

**Business / Ops:**
- Self-serve payment integration (Toss Payments or equivalent)
- 벤처나라 registration if pursuing public-sector sales
  (requires 벤처기업 확인서 or 창업기업 확인서 — check eligibility in parallel)

---

## Phase 4 — Additional Checks + Intelligence (longer-term)

**Technical:**
- [ ] 카카오/다음 메일 호환성 점수 (Kakao/Daum Mail compatibility score — same proxy-indicator approach as Naver)
- [ ] 도메인 일괄 검사 — CSV 입력 (Bulk domain scan via CSV input)
- [ ] DMARC 집계 리포트 추세 뷰 (DMARC aggregate report trend view — weekly/monthly pass rate over time)

**Business / Ops:**
- 정보보호제품 성능평가 (~₩300K–500K after 공모 감면) — only if pursuing KISA pool
  more aggressively or 벤처나라 listing requires it
- NIPA 바우처 공급기업 eligibility — contact NIPA first (action item N-1 in
  pricing_strategy_research.md)

---

## Phase 5 — Hard Problems (deferred)

**Technical:**
- [ ] 네이버 시드 계정 받은편지함 테스트 (Naver seed account inbox placement test) —
  requires owning seed Naver accounts, actual mail delivery, inbox vs. spam classification.
  Hard operational problem, deferred until there is paying demand for it.
