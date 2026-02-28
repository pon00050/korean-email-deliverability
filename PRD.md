# PRD: Korean Email Domain Health Checker
## Product Requirements Document — v1.0

**Date:** 2026-02-28
**Status:** MVP complete — pre-release verification in progress
**Build date:** 2026-02-28
**Target release:** 2–4 weeks (personal-brand GitHub repo)
**Shape:** CLI pipeline tool — run locally, outputs self-contained HTML report (kr-forensic-finance pattern)

---

## Decision Log (All 11 Questions Resolved)

| # | Question | Decision |
|---|---|---|
| 1 | Kakao/Daum or Naver-only? | **Naver-only** (MVP) |
| 2 | UI language? | **No standalone UI** — CLI pipeline; HTML report output |
| 3 | Free vs. gated? | **Freemium from day one** — core scan free, advanced features paid later |
| 4 | Shareable URL / PDF / web page? | **Web page only** (self-contained HTML output, no hosted backend) |
| 5 | KISA RBL API? | DNS-based query at `{reversed-ip}.rbl.kisa.or.kr`; fallback to HTTP scrape |
| 6 | KISA 화이트도메인 API? | Web scrape of `https://화이트도메인.한국` — no public API |
| 7 | Blacklist APIs? | Spamhaus ZEN (DNS), Barracuda BRBL (DNS), SURBL (DNS) — all free tier |
| 8 | Naver Mail compatibility score? | Composite of 5 proxy indicators — PTR, SPF alignment, DMARC policy, KISA whitelist, major blacklist clean |
| 9 | Monetization path? | Freemium: free CLI scan, paid monitoring/history/bulk scan post-MVP |
| 10 | Standalone brand vs. personal brand? | **Personal brand** — released under operator's GitHub handle |
| 11 | White-label for Stibee/TasOn? | **No** — ship opinionated MVP; revisit if partnerships form |

---

## 1. Executive Summary

**Problem:** Korean businesses sending email — especially Tax/Accounting SaaS companies whose e-invoice delivery failures carry legal penalties (0.3–0.5% surcharge per transaction) — have no Korean-language tool to audit their email domain health. DMARC adoption in Korea is 1.8% (APAC lowest). KISA RBL silently blocks senders. Naver Mail filtering is a black box. Global tools have zero Korean mailbox coverage.

**Solution:** A Python CLI tool that accepts a domain name and produces a scored, Korean-language HTML health report covering SPF, DKIM, DMARC, KISA blacklist status, KISA 화이트도메인 registration, major international blacklists, and a Naver Mail compatibility score — in under 60 seconds.

**Success metric:** 100 domain scans (unique domains) within 30 days of GitHub release.

**Test case used throughout this document:** `barobill.co.kr` (Barobill — Korea's largest e-invoice API provider; DMARC likely absent; KISA whitedomain status unknown; a delivery failure means their downstream clients incur tax surcharges).

---

## 2. Product Definition

### What it is
A local CLI tool (Python, `uv`-managed) that:
1. Accepts a domain name as argument
2. Performs 8 domain health checks via DNS lookups and HTTP requests
3. Scores each check and produces an overall 0–100 score
4. Writes a self-contained Korean-language HTML report to disk

```bash
uv run check.py barobill.co.kr
# → Writes: reports/barobill.co.kr_20260228.html
# → Prints: summary table to terminal
```

### What it is not
- Not a hosted web service (no server, no backend, no database — MVP)
- Not a monitoring service (no scheduled re-checks — post-MVP)
- Not an inbox placement tester (no seed accounts for Naver mailboxes — hard problem, post-MVP)
- Not a DMARC report parser (requires existing DMARC setup — only 1.8% of Korean companies qualify)

### Core value proposition
> "바로빌.co.kr의 이메일 도메인 상태를 60초 만에 진단하세요. 전자세금계산서 발송 실패는 가산세로 이어집니다."

---

## 3. User Stories

### Primary persona: Tax/Accounting SaaS developer or CTO
- "I want to know if our sending domain is on any blacklist before we get customer complaints."
- "I want to verify our SPF/DKIM/DMARC is correct without hiring a consultant."
- "I want to check if our domain is registered on KISA 화이트도메인 — we don't know what that even is."
- "I want to share the results with our IT team without them needing to run code."

### Secondary persona: Email marketer at a Korean company using Stibee or TasOn
- "Our open rates dropped. I want to know if we're blacklisted."
- "I want to check my domain before switching ESP."

### Secondary persona: Korean ESP customer support representative
- "A customer reports emails going to spam. I want to do a quick audit to help them troubleshoot."

---

## 4. Feature Specification — MVP

### 4.1 Input
```bash
python check.py <domain> [--dkim-selector <selector>] [--output <path>]
```

- `domain`: Required. Domain to check (e.g. `barobill.co.kr`)
- `--dkim-selector`: Optional. If not provided, tool tries 10 common selectors automatically
- `--output`: Optional. Output path for HTML report (default: `reports/<domain>_<date>.html`)

### 4.2 Check Modules (8 checks)

#### Check 1: SPF Record
- **What:** DNS TXT record lookup for `v=spf1` at the domain root
- **Pass criteria:** Record exists; syntax is valid; no more than 10 DNS lookups; ends in `-all` or `~all`
- **Findings output (Korean):**
  - ✅ SPF 레코드가 올바르게 설정되어 있습니다
  - ⚠️ SPF 레코드는 있지만 `?all` 또는 `+all`로 설정되어 효과가 없습니다
  - ❌ SPF 레코드가 없습니다 — 발신 도메인 위조 방어가 불가합니다
- **Remediation text:** Step-by-step Korean instructions to add/fix SPF
- **Test case (barobill.co.kr):** Lookup `barobill.co.kr` TXT records

#### Check 2: DKIM Record
- **What:** DNS TXT lookup at `<selector>._domainkey.<domain>`
- **Selectors tried automatically:** `default`, `google`, `selector1`, `selector2`, `k1`, `dkim`, `mail`, `smtp`, `stibee`, `nhn`
- **Pass criteria:** At least one valid DKIM public key found; key length ≥ 1024 bits (warn if < 2048)
- **Findings output (Korean):**
  - ✅ DKIM 서명이 설정되어 있습니다 (`{selector}` 셀렉터)
  - ⚠️ DKIM 키 길이가 1024비트입니다 — 2048비트 이상을 권장합니다
  - ❌ DKIM 레코드를 찾을 수 없습니다 — 셀렉터를 직접 입력해주세요
- **Note:** DKIM selector must be known; if auto-detection fails, tool instructs user to provide `--dkim-selector`

#### Check 3: DMARC Record
- **What:** DNS TXT lookup at `_dmarc.<domain>`
- **Pass criteria:** Record exists; policy is `quarantine` or `reject` (not `none`); `pct=100`; `rua` tag present
- **Scoring:**
  - `p=reject` → full score
  - `p=quarantine` → partial score
  - `p=none` → near-zero (monitoring only, no protection)
  - Missing → zero score
- **Findings output (Korean):**
  - ✅ DMARC 정책이 `reject`으로 설정되어 있습니다
  - ⚠️ DMARC가 있지만 `p=none` (모니터링 전용) — 실제 차단 효과가 없습니다
  - ❌ DMARC 레코드가 없습니다 — 한국 기업 중 약 98%가 이 상태입니다
- **Note:** Absence of DMARC is the expected finding for Korean companies; Korean-language context is critical here to normalize but motivate action

#### Check 4: PTR Record (Reverse DNS)
- **What:** Resolve MX records for the domain; attempt reverse DNS lookup on the MX host IPs
- **Pass criteria:** PTR record exists; PTR hostname matches forward A record of the MX server
- **Why it matters:** Naver Mail uses PTR record presence and match as a basic sender signal
- **Findings output (Korean):**
  - ✅ PTR(역방향 DNS) 레코드가 설정되어 있습니다
  - ❌ PTR 레코드가 없거나 IP와 일치하지 않습니다 — 네이버 메일 필터에 영향을 줄 수 있습니다

#### Check 5: KISA RBL (Korea Internet & Security Agency Blacklist)
- **What:** DNS-based blacklist lookup. Query format: `{reversed-ip}.rbl.kisa.or.kr`
  - Example: IP `1.2.3.4` → query `4.3.2.1.rbl.kisa.or.kr`
  - If DNS resolves → listed; if NXDOMAIN → clean
- **Fallback:** If DNS method fails or returns unexpected results, HTTP GET to KISA lookup page
- **Pass criteria:** Not listed on KISA RBL
- **Why it matters:** KISA RBL is used by Korean ISPs (Naver, Kakao, KT) as a primary blocklist signal. Being listed means silent delivery failures with no bounce notification.
- **Findings output (Korean):**
  - ✅ KISA RBL(한국인터넷진흥원 차단 목록)에 등록되지 않았습니다
  - ❌ KISA RBL에 등록되어 있습니다 — 네이버, 카카오 메일로의 발송이 차단될 수 있습니다

#### Check 6: KISA 화이트도메인 Registration
- **What:** Web scrape of `https://화이트도메인.한국` (or `https://whitedomains.kisa.or.kr`) to check if the domain is registered
- **Method:** HTTP GET with domain query parameter; parse response for registration status
- **Pass criteria:** Domain is registered on KISA 화이트도메인
- **Why it matters:** 화이트도메인 registration is a positive signal to Korean ISPs. Stibee's sending IPs are registered; individual company sending domains typically are not.
- **Findings output (Korean):**
  - ✅ KISA 화이트도메인에 등록되어 있습니다
  - ⚠️ KISA 화이트도메인에 등록되지 않았습니다 — 등록 시 네이버 메일 수신율 향상에 도움이 됩니다
- **Remediation:** Link to 화이트도메인 registration page with step-by-step guide

#### Check 7: International Blacklist Check
- **What:** DNS-based checks against 3 major blacklists
  - **Spamhaus ZEN:** `{reversed-ip}.zen.spamhaus.org`
  - **Barracuda BRBL:** `{reversed-ip}.b.barracudacentral.org`
  - **SURBL:** `{domain}.multi.surbl.org`
- **IP source:** Resolved from MX records of the domain
- **Pass criteria:** Not listed on any of the 3
- **Findings output (Korean):**
  - ✅ 주요 국제 블랙리스트(Spamhaus, Barracuda, SURBL)에 등록되지 않았습니다
  - ❌ {blacklist_name}에 등록되어 있습니다 — 글로벌 이메일 발송에 영향을 줍니다

#### Check 8: Naver Mail Compatibility Score (Composite)
- **What:** Calculated score (not a single check) based on checks 1–7
- **Method:** Weighted sum of proxy indicators:

| Signal | Weight | Pass Condition |
|---|---|---|
| SPF valid with `-all` or `~all` | 25% | Check 1 passes |
| DKIM present (any selector) | 20% | Check 2 passes |
| DMARC policy ≥ `quarantine` | 25% | Check 3 score ≥ partial |
| PTR record present and matching | 15% | Check 4 passes |
| KISA 화이트도메인 registered | 15% | Check 6 passes |

- **Output:** Score 0–100 with color coding and Korean label:
  - 80–100: 🟢 양호 — 네이버 메일 수신 가능성 높음
  - 50–79: 🟡 보통 — 일부 이메일이 스팸함에 분류될 수 있음
  - 0–49: 🔴 위험 — 네이버 메일 수신율이 크게 저하될 가능성 있음
- **Disclaimer (Korean):** "네이버 메일은 공식 API를 제공하지 않습니다. 이 점수는 공개된 기술 신호를 기반으로 한 추정값입니다."

### 4.3 Overall Score
- Weighted average across all 8 checks (Naver score is itself a composite)
- 0–100, color-coded
- Letter grade: A (90+), B (75–89), C (50–74), D (25–49), F (0–24)

### 4.4 HTML Report Output
Self-contained single HTML file (no external dependencies), matching kr-forensic-finance's `beneish_viz.html` pattern:

- **Header:** Domain scanned, timestamp, overall score + grade (large, color-coded)
- **Summary table:** All 8 checks with pass/warn/fail status
- **Detail sections (per check):** Finding in Korean, severity, remediation steps
- **Naver Mail Compatibility panel:** Composite score, breakdown table, disclaimer
- **Footer:** Tool name, GitHub link, "이 결과는 참고용이며 전문 컨설팅을 대체하지 않습니다"

**Terminal output (on run):**
```
바로빌.co.kr 도메인 검사 중...

✅ SPF          valid (-all)
✅ DKIM         found (selector: default)
❌ DMARC        missing
⚠️  PTR          partial match
❌ KISA RBL      not listed ✅ / listed ❌
⚠️  KISA 화이트도메인  not registered
✅ 블랙리스트     clean (Spamhaus, Barracuda, SURBL)

네이버 메일 호환성 점수: 42/100 🔴
전체 점수: 58/100 (C등급)

리포트 저장됨: reports/barobill.co.kr_20260228.html
```

---

## 5. Feature Specification — Post-MVP Roadmap

| Feature | Phase | Notes |
|---|---|---|
| Monitoring / scheduled re-checks | Phase 2 | Cron-based; email/Slack alert on status change |
| Bulk domain scan | Phase 2 | CSV input; ESP use case (check all customer domains) |
| DMARC aggregate report upload + visualization | Phase 3 | Requires DMARC already set up; only 1.8% of Korean companies |
| Hosted web UI (mail-tester.com style) | Phase 3 | Hosted backend; shareable URL; requires server |
| Kakao Mail / Daum compatibility score | Phase 2 | Same proxy-indicator approach as Naver |
| PDF export | Phase 3 | Requires hosted service or wkhtmltopdf |
| Naver seed account inbox test | Phase 4 | Hard; requires Naver account management |

---

## 6. Technology Stack

Mirrors kr-forensic-finance architecture. No deviation from established patterns.

| Layer | Technology | Reason |
|---|---|---|
| Language | Python ≥ 3.11 | Same as kr-forensic-finance |
| Package manager | `uv` | Same as kr-forensic-finance; deterministic |
| DNS lookups | `dnspython` | Standard Python DNS library; no external API needed |
| HTTP requests | `requests` | KISA 화이트도메인 scrape; blacklist HTTP fallbacks |
| HTML report | `jinja2` + inline CSS | Self-contained output, no build step |
| CLI | `argparse` (stdlib) | No external CLI framework needed for MVP |
| Testing | `pytest` | Same as kr-forensic-finance |
| Config | `python-dotenv` | For any future API keys (none needed for MVP) |

**No framework, no database, no server required for MVP.**

```toml
# pyproject.toml
[project]
name = "kr-email-health"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "dnspython",       # DNS lookups (SPF, DKIM, DMARC, PTR, blacklists)
    "requests",        # KISA 화이트도메인 HTTP scrape
    "jinja2",          # HTML report templating
    "python-dotenv",   # future API keys
]

[project.optional-dependencies]
dev = ["pytest>=8.0.0"]
```

**Project structure (proposed):**
```
kr-email-health/
├── check.py                  # CLI entry point
├── pyproject.toml
├── .env.example
├── README.md
├── 00_Reference/
│   ├── PRD.md                # this document
│   └── ROADMAP.md
├── src/
│   ├── checks/
│   │   ├── spf.py
│   │   ├── dkim.py
│   │   ├── dmarc.py
│   │   ├── ptr.py
│   │   ├── kisa_rbl.py
│   │   ├── kisa_whitedomain.py
│   │   ├── blacklists.py
│   │   └── naver_score.py
│   ├── report.py             # HTML report generator (Jinja2)
│   └── scorer.py             # Weighted scoring logic
├── templates/
│   └── report.html.j2        # Jinja2 report template
├── reports/                  # Output directory (gitignored)
└── tests/
    ├── test_checks.py
    └── test_scoring.py
```

---

## 7. Go-to-Market

### Step 1: Content first (before release)
Publish one Korean-language article before promoting the tool:
- **Title:** "네이버 메일이 내 이메일을 차단하는 이유: 한국 발신자를 위한 기술 체크리스트"
- **Target platform:** 요즘IT or Velog
- **Content:** KISA RBL 설명, KISA 화이트도메인 등록 방법, SPF/DKIM/DMARC 기초, 실제 기업 도메인 진단 예시
- **CTA:** "이 도구로 귀사 도메인을 직접 검사하세요" → GitHub link

### Step 2: Release
- GitHub repo under operator's personal account
- README in Korean (primary) + English (secondary) — same bilingual pattern as kr-forensic-finance
- Include `barobill.co.kr` as a worked example in README (real scan output, no fabrication)

### Step 3: Distribution
1. **Stibee community** — Post in Stibee blog / community channels: "스티비 사용자를 위한 도메인 상태 점검 도구"
2. **Tax SaaS developer communities** — Korean developer communities (카카오 오픈채팅, 개발자 Discord)
3. **Cold email** — To Barobill/Ecount/Douzone IT team: "귀사 도메인(barobill.co.kr) 검사 결과를 공유합니다 — 전자세금계산서 발송 안정성 관련"
4. **LinkedIn** — Share scan results of publicly known Tax SaaS domains; "여기서 발견한 것들" framing

---

## 8. Success Metrics

| Metric | 30-day target | 90-day target |
|---|---|---|
| Unique domains scanned (GitHub clones as proxy) | 100 | 500 |
| GitHub stars | 50 | 200 |
| Inbound consulting inquiries | 1 | 5 |
| Stibee partnership conversation started | — | 1 |

---

## 9. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| KISA 화이트도메인 scrape breaks (site structure change) | Medium | Medium | Graceful fallback: mark as "확인 불가" rather than fail; document scrape method clearly |
| Naver opacity — score is misleading | High | Medium | Prominent disclaimer on every report; score labeled as "추정치" not "측정값" |
| KISA RBL DNS query format is wrong | Medium | High | Verify against KISA docs and test with known-listed IPs before release; document fallback |
| Low initial distribution | High | Medium | Content-first strategy; cold email with actual scan results as hook |
| Spamhaus rate-limits DNS queries | Low | Low | Cache DNS results per run; add delay between lookups |
| Misuse (scanning domains you don't own) | Low | Low | README disclaimer: "본인 소유 도메인 또는 허가받은 도메인만 검사하세요" |

---

## 10. Verification Checklist (PRD Complete When All Pass)

- [x] All 11 open questions answered
- [x] Stack confirmed consistent with kr-forensic-finance (Python, uv, no server, HTML output)
- [x] Feature list maps to "three missing layers" (KISA regulatory layer, inbox provider proxy signals, no existing Korean tool)
- [x] `barobill.co.kr` used as concrete test case throughout (sections 4.1, 4.4, 7)
- [x] Korean-language findings text specified for every check
- [x] Naver Mail score methodology and disclaimer documented
- [x] Post-MVP roadmap defined to avoid scope creep in MVP
- [x] Go-to-market tied to Tax SaaS vertical (Barobill/Ecount cold email strategy)
- [x] KISA URL field verification (2026-02-28): RBL zone active; whitedomain no public API
- [x] README written (2026-02-28)

---

## Appendix A: KISA RBL DNS Query Format

```
# Lookup format (to verify before implementation):
# IP: 1.2.3.4
# Query: 4.3.2.1.rbl.kisa.or.kr
# If resolves (any A record) → listed
# If NXDOMAIN → not listed

import dns.resolver
def check_kisa_rbl(ip: str) -> bool:
    reversed_ip = ".".join(reversed(ip.split(".")))
    query = f"{reversed_ip}.rbl.kisa.or.kr"
    try:
        dns.resolver.resolve(query, "A")
        return True  # listed
    except dns.resolver.NXDOMAIN:
        return False  # clean
```

**⚠️ Verify this DNS zone is active before release.** If inactive, fall back to HTTP scrape of `https://www.kisa.or.kr/` or `https://rbl.kisa.or.kr/`.

---

## Appendix B: Naver Mail Compatibility Score — Full Rationale

Naver Mail does not publish filtering criteria. The following proxy indicators are based on:
1. General email authentication best practices (RFC 7208, RFC 6376, RFC 7489)
2. KISA 화이트도메인 program documentation (which explicitly improves Korean ISP delivery)
3. Observed patterns in Korean email deliverability forums and ESP support documentation
4. Global inbox provider behavior (Naver's infrastructure shares characteristics with other major providers)

The score is explicitly labeled as an estimate. Users are told to treat it as a checklist, not a measurement. This is honest positioning — and it differentiates the tool from snake oil.

---

*PRD authored: 2026-02-28*
*Ready for implementation: proceed to src/ build*
