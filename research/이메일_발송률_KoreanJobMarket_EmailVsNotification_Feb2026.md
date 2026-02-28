# 이메일 발송률 — 한국 취업시장 분석 & 콘텐츠 전략
## Korean Job Market: Email vs. Notification + Public Writing Strategy

**Date:** 2026-02-28
**Purpose:** (1) Quantify email-specific demand in Korean CRM job market and assess notification-over-email hypothesis; (2) Map Korean deliverability content gaps and build a public writing strategy for authority positioning.
**Source research:** 2 dedicated deep-research agents (Agent 4: job market; Agent 5: writing strategy), Feb 28 2026.

---

## Table of Contents

1. [Korean CRM Job Market — Email Channel Analysis](#1-korean-crm-job-market--email-channel-analysis)
2. [Notification-vs-Email Hypothesis: Verdict](#2-notification-vs-email-hypothesis-verdict)
3. [Deliverability-Specific Job Demand](#3-deliverability-specific-job-demand)
4. [Channel Data: Korea vs. Global](#4-channel-data-korea-vs-global)
5. [Content Gap Map: Korean-Language Deliverability](#5-content-gap-map-korean-language-deliverability)
6. [Existing Korean Email Writers — Competitive Landscape](#6-existing-korean-email-writers--competitive-landscape)
7. [First 5 Recommended Korean Article Topics](#7-first-5-recommended-korean-article-topics)
8. [Best Publishing Platforms for Korean Deliverability Authority](#8-best-publishing-platforms-for-korean-deliverability-authority)
9. [English-Language Authority Building](#9-english-language-authority-building)
10. [Naver Contact Strategy](#10-naver-contact-strategy)
11. [Positioning Implications](#11-positioning-implications)
12. [Sources](#12-sources)

---

## 1. Korean CRM Job Market — Email Channel Analysis

### Methodology

Searched Wanted.co.kr, Jobkorea.co.kr (13,669 "CRM 마케터" results), Catch.co.kr, RememberApp, and Kowork.kr. Approximately 15 distinct postings reviewed directly or via secondary reporting. Secondary data from Stibee 2025 Report, Braze 2025 Korea report, and Recatch's 93-company B2B survey.

### Channel Hierarchy in Korean CRM Roles

| Channel | Frequency in postings | Primary vs. Secondary | Key tools mentioned |
|---|---|---|---|
| **앱 푸시 (App Push)** | ~95% | Primary or co-primary | Braze, Hackle, Airbridge |
| **카카오 알림톡/친구톡** | ~90% | Primary or co-primary | Kakao Bizmessage API, Channel.io |
| **SMS/LMS** | ~80% | Secondary (fallback) | Solapi, NHN Cloud |
| **이메일** | ~65–70% | Secondary or tertiary | Braze (email module), Stibee |
| **인앱/인웹 메시지** | ~60% | Supplementary | Braze in-app, Hackle |

### Specific Posting Evidence

| Company | Role | Channels explicitly listed | Tools |
|---|---|---|---|
| **쏘카 (SOCAR)** | CRM 마케터 | Push, 문자, 친구톡 — **email not listed** | Not specified |
| **와디즈 (Wadiz)** | CRM 마케터 | KakaoTalk, 앱 푸시, 인앱, 이메일, SMS | Braze |
| **글로랑 (꾸그)** | CRM 마케터 | 앱 푸시, 카카오채널, 채널톡, LMS, 이메일 | Braze, Amplitude |
| **우아한형제들** | CRM 마케터 (7yr+) | Segmentation/personalization focus | Braze (required), SQL, GA4, Tableau |
| **원티드랩** | CRM 마케터 | Push, SMS, 이메일 | Not specified |
| **꾸까 (Kukka)** | CRM 마케터 | EDM, SMS, Kakao Plus | Not specified |
| **Naver Series** | CRM 마케터 (intern) | App push (primary) | Braze |

**Profile of a typical Korean CRM 마케터 role:** Multi-channel automation orchestrator running 4–5 channels simultaneously using the AARRR framework. Email is one of those channels — never the solo focus.

### Email-Specific Demand: Quantified

| Metric | Estimate |
|---|---|
| Email listed as **primary channel** | ~0–5% of postings |
| Email mentioned at all (even secondary) | ~65–70% of postings |
| Any email-specific tool (Stibee, Mailchimp, Klaviyo) | ~10–15% of postings |
| Email automation mentioned (via Braze email module) | ~20–30% |
| **Deliverability concepts (발송률, 전달성, 스팸, SPF/DKIM)** | **~0% — essentially absent** |

### Industries Where Email Is Most Prominent

| Sector | Email role | Key evidence |
|---|---|---|
| **B2B SaaS / Tech** | Primary channel | 83% of Korean B2B firms (revenue ₩10B+) use email/newsletter (Recatch survey, 93 companies) |
| **뉴스레터 / 미디어** | Primary | Stibee tracking 50억 발송/year; 롱블랙, Publy, 커리어리 as examples |
| **이커머스 / 패션** | Secondary-to-primary | Highest email open rate sector: 의류/패션잡화 at 19.9% (Stibee 2025) |
| **핀테크 / 금융** | Secondary | Email for compliance/documentation; Kakao for real-time alerts |
| **헬스케어** | Secondary | Similar compliance pattern |
| **채용 플랫폼** | Mixed | LinkedIn-style platforms: email-heavy; 원티드/리멤버: push + kakao dominant |

### Tool Landscape: Korean CRM Email Tools

| Tool | Market positioning | In job postings? |
|---|---|---|
| **Braze** | Enterprise multi-channel CRM (push+kakao+email+in-app) | Yes — most common enterprise CRM tool; added native KakaoTalk support in 2025 |
| **스티비 (Stibee)** | Korean-native email-only (SME/newsletter) | Rarely in job postings; dominant for newsletters |
| **Hackle** | A/B testing + CRM, push-native | Occasional appearance in growth marketer postings |
| **Notifly** | Multi-channel CRM (startup tier) | Rarely mentioned |
| **Mailchimp** | Global email | Very rarely in Korean postings; displaced by Stibee |
| **Klaviyo** | E-commerce email automation | Essentially absent from Korean postings |
| **Iterable** | Enterprise email/push | No meaningful Korean presence |

---

## 2. Notification-vs-Email Hypothesis: Verdict

**Hypothesis:** Korean market prefers KakaoTalk 알림톡/친구톡, push notifications, and SMS over email in CRM roles.

### Verdict: **Confirmed, with nuance**

**Supporting evidence:**

- **KakaoTalk penetration:** 98.9% among Korean smartphone users. 알림톡 open rates reach 80%+ vs. email's 13.9% for business senders (Stibee 2025) — a 5–6x open rate differential
- **SOCAR's CRM posting** lists "Push, 문자, 친구톡" with no email mention at all
- **Korean corporate messaging market** (SMS + 알림톡 + 친구톡): estimated ₩1.5 trillion/year; Kakao expanding with new 브랜드 메시지 product (launched 2025)
- **Korean CRM practitioner consensus:** Effic, Flarelane, AB180 blogs uniformly describe KakaoTalk as "가장 효과적인 채널." One source explicitly: "국내에서는 카카오톡 채널이 가장 효과적입니다."
- **Grow with Braze Seoul 2025:** The headline product announcement for the Korean market was **native KakaoTalk support** — confirming enterprise CRM teams needed Kakao integration more than email improvements

**Where email persists in Korea (the nuance):**
- B2B nurturing at large companies (83% usage, Recatch)
- Newsletter/media subscription economy (Stibee, Publy, 롱블랙)
- Compliance and legal documentation contexts (fintech, healthcare)
- International/cross-border B2B (Kakao doesn't work outside Korea)
- Fallback for users who have revoked push permissions

**Korea-specific deliverability note:** Naver Mail (dominant domestic email provider) **does not yet enforce DMARC/SPF/DKIM as strictly as Gmail**. Stibee's blog states this explicitly. This reduces the urgency of deliverability pain for domestic Korean email senders compared to global senders — the Gmail enforcement squeeze driving deliverability consulting demand globally has softer domestic impact where Naver Mail dominates.

**Critical Korea-specific tool:** KISA (Korea Internet Security Agency) maintains a **화이트도메인 registry** that legitimate bulk senders can register with. No global equivalent. This is the key Korean-specific deliverability knowledge item with no foreign-language competition.

---

## 3. Deliverability-Specific Job Demand

**Answer: Zero postings found with deliverability language.**

Across all postings reviewed, none used: 이메일 전달성, 발송률 (in technical sense), 도달률 (technical), 스팸 필터, SPF, DKIM, DMARC, 화이트도메인, or inbox placement.

**Where deliverability knowledge does exist in Korea:**
- **Stibee's blog and help docs** — published Korea-specific guidance on Gmail's Feb 2024 sender policy changes and Naver Mail filtering behavior
- **Notifly's blog** — wrote about 2024 cold email spam regulations
- **Korean developer community** — SPF/DKIM content exists for self-hosted mail server operators, not marketers
- **ThunderMail blog** — documented July 2024 Naver bulk policy change (the most detailed Korean Naver-specific content found)

**Where deliverability expertise maps in Korea:**
- Not a standalone CRM marketing role (confirmed: zero postings)
- Closest role type: **B2B SaaS support / solutions engineer** — Stibee and Notifly customers encounter deliverability problems; there is a narrow niche closer to technical support or email infrastructure consulting than CRM marketer
- Alternatively: **independent consulting** to Korean SMEs and enterprises who send bulk email and don't know why it fails

---

## 4. Channel Data: Korea vs. Global

### Email Open Rate Benchmarks

| Metric | Korea (Stibee 2025) | Global average | Gap |
|---|---|---|---|
| Business email open rate | 13.9% | 21–33% | Korea below global |
| Newsletter/individual open rate | 25.4% | 21–35% | Comparable |
| Best industry open rate | Fashion/apparel: 19.9% | Tech: ~22% | Sectors differ |
| Business click-through rate | 1.1% | 2.5–3% | Korea below global |
| Automated email open rate lift | 1.6× | 1.5–2× | Comparable |
| **Automated email click rate lift** | **3.8×** | 2–3× | **Korea exceeds global — automated email works here** |

### KakaoTalk vs. Email: The Channel Comparison

| Metric | Email (Korea) | KakaoTalk 알림톡 |
|---|---|---|
| Platform penetration | ~70% have email | **98.9%** KakaoTalk users |
| Open rate | 13.9% (business) / 25.4% (newsletter) | **80%+** |
| Click-through rate | 1.1% | 2.5–33% (varies by open rate tier) |
| Cost | Low per-send | ~₩8–15/건 per-message |
| Corporate messaging market size | Not separately measured | **₩1.5조/year** |

**The opportunity hiding in the data:** Korea's automated email click rate is **3.8× above baseline** (vs. 2–3× globally). This means properly set-up automated email programs perform disproportionately well in Korea — the channel is underused, not ineffective. This is a positioning argument for deliverability consulting.

---

## 5. Content Gap Map: Korean-Language Deliverability

### What Exists (by Platform)

| Platform | Topics Covered | Depth | Who's Writing |
|---|---|---|---|
| **Velog** | SPF/DKIM/DMARC concept overviews; "why emails go to spam"; Google Workspace setup walkthroughs | Shallow to medium — developer setup notes, no strategic depth | Individual developers documenting their own configurations |
| **Brunch** | Email marketing automation intros; one SPF/DKIM post | Very shallow — lifestyle/startup framing | Marketing generalists |
| **Tistory** | DMARC setup copied from Google/Cloudflare docs; SPF record creation; Gmail 2024 compliance | Medium on setup steps, zero on strategy or diagnosis | IT system admins |
| **스티비 Blog** | Gmail/Naver policy changes; spam folder tips; DMARC setup guide; bounce metrics | Medium — ESP-oriented, product-focused | Stibee content team (vendor, product-driven) |
| **ThunderMail Blog** | Naver/Daum bulk policy changes (July 2024); Naver sending guide | Medium — most detailed Korean Naver-specific content found | One-off policy update posts; no systematic framework |
| **CLVS Blog** | "Email marketing terminology" series: Email Deliverability (post 1), SPF & DKIM (post 3) | Medium — most systematic Korean independent coverage found, but still intro-level | CRM/email marketing agency |
| **요즘IT (yozm.wishket.com)** | General IT content (MAU 460K); **no dedicated deliverability articles found** | Gap — high-traffic platform, underserved on this topic | IT generalists |
| **Naver Blog** | Mostly reposts of vendor help-doc content | Very shallow | Marketers reposting vendor content |

### The Gaps — What Does NOT Exist in Korean

| Topic | Current Korean Content Status | Gap Size |
|---|---|---|
| **DMARC report reading** (RUA/RUF XML parsing, alignment failures diagnosis) | Zero dedicated content — Stibee/Tason say "set up DMARC" but nothing explains how to read reports | **Critical gap — highest value** |
| **Naver Mail filtering behavior** (PTR, KISA White Domain, connection limits, what Naver rejects) | Partial — Stibee wrote 2 posts about Gmail+Naver 2024 policy; ThunderMail documented July 2024 change. No deep analysis | **Very large — unique Korea opportunity** |
| **Bounce code reference for Korean ISPs** (SMTP 5xx from naver.com, kakao.com, daum.net) | Near zero | **Very large — unique Korea opportunity** |
| **Google Postmaster Tools practitioner guide** (register, interpret, act on dashboards) | Official Google Korean docs exist but are dry translation; no practitioner-written Korean guide | **Large — very high search intent** |
| **IP warming strategy** | Zero in Korean | Very large |
| **DKIM key management and rotation** | Near zero — one Velog post covers concept; nothing on rotation, selectors, key compromise | Very large |
| **Engagement segmentation for deliverability** | Near zero — Stibee's KPI guide mentions open rate; nothing on proactive segmentation | Large |
| **Blacklist diagnosis + removal (global + KISA)** | Global blacklists (Spamhaus, Barracuda): zero Korean practitioner coverage; KISA White Domain: some hosting company posts exist | Large |
| **List verification tools comparison (Korean)** | Zero Korean-language tool comparison | Large |
| **Daum/Kakao Mail filtering behavior** | Zero dedicated content; Daum has a spam policy page but no practitioner analysis | Very large |
| **SPF syntax deep dive** (include chains, 10-lookup limit, softfail vs hardfail) | Exists at entry level only — "add this TXT record"; no diagnostic guides | Large |
| **Sunset policy design** | Near zero — entirely absent from Korean practitioner discourse | Large |
| **BIMI implementation guide** | Zero in Korean | Medium |
| **FBL (Feedback Loop) setup** | Zero in Korean | Medium |
| **Transactional vs. marketing email separation** | Near zero | Large |

### Korean Deliverability Content Status Summary

**Key finding:** There is no identifiable individual in Korea who has established public authority specifically as an email deliverability specialist. Stibee's content team is the closest — but they are a vendor with product-driven motivation, not an independent authority. **The position of "Korea's email deliverability expert" is entirely open.**

---

## 6. Existing Korean Email Writers — Competitive Landscape

| Writer / Publisher | Platform | Technical Depth | Deliverability Coverage Gap |
|---|---|---|---|
| **스티비 (Stibee) Team** | blog.stibee.com + help.stibee.com | Medium — setup-focused, not diagnostic | Does NOT cover: DMARC report reading, GPT deep dives, blacklist removal, IP warm-up, bounce codes, Naver-specific filtering signals |
| **타손 (TasOn) Marketing** | blog.tason.com | Shallow — vendor marketing | Surface only; no diagnostic or advanced strategy |
| **CLVS** (CRM/marketing agency) | clvs.co.kr/post | Medium — most systematic independent Korean coverage, but still intro-level | Does NOT cover: DMARC reports, IP warming, Naver-specific content, blacklists, bounce codes |
| **가비아 (Gabia) Library** | library.gabia.com | Medium DNS mechanics, no strategy | Infrastructure-only; no marketing-side deliverability |
| **ThunderMail Blog** | blog.thundermail.co.kr | Medium — most detailed Korean Naver-specific content found | One-off policy update posts; no systematic framework |
| **Velog individual devs** | velog.io | Low to medium — personal reference | No strategic deliverability thinking |
| **No identifiable individual Korean deliverability specialist** | — | — | **The position is entirely vacant** |

---

## 7. First 5 Recommended Korean Article Topics

Ranked by gap size + positioning value for a deliverability specialist.

---

### #1 — DMARC 리포트 읽는 법
**Title:** `DMARC 리포트 읽는 법: XML 집계 보고서로 이메일 인증 실패 원인 찾기`

- **Why this gap:** DMARC setup guides exist in Korean; zero Korean content explains what to do with the reports after setup. This is the practitioner skill that separates real specialists from config admins.
- **Target reader:** Marketing ops, IT managers, developers who set up DMARC but get XML reports they don't understand
- **Key angle:** Walk through a real aggregate report XML; identify specific failure patterns (SPF misalignment vs. DKIM failure vs. forwarding); map to actionable fixes
- **Best platform:** 요즘IT — 460K MAU, IT practitioners, no competition on this topic
- **SEO terms:** `DMARC 리포트`, `DMARC XML 읽는 법`, `이메일 인증 실패 원인`, `이메일 발송률 개선`

---

### #2 — 네이버 메일 발송 실패 원인
**Title:** `네이버 메일에 이메일이 안 들어가는 진짜 이유: PTR 레코드, 화이트도메인, 연결 제한까지`

- **Why this gap:** Naver + Gmail cover 70–80% of Korean email recipients; while Gmail documentation is everywhere, Naver-specific filtering logic has never been comprehensively documented by an independent practitioner
- **Target reader:** Developers and marketing IT teams sending bulk email to Korean consumers; e-commerce operators, SaaS companies with Korean user bases
- **Key angle:** Consolidate all publicly available Naver Mail filtering signals (PTR/reverse DNS requirement, KISA White Domain registration, simultaneous connection limits, July 2024 policy changes) into one diagnostic framework; add "what Naver does that Gmail doesn't" comparison
- **Best platform:** Velog (developer audience for technical depth) + cross-post summary to 요즘IT
- **SEO terms:** `네이버 메일 발송 실패`, `네이버 메일 스팸`, `화이트도메인 등록`, `대량 발송 네이버`, `PTR 레코드 이메일`

---

### #3 — 이메일 블랙리스트 진단과 해제
**Title:** `이메일 블랙리스트에 올라갔을 때 하는 일: Spamhaus부터 KISA RBL까지 진단과 해제 실전 가이드`

- **Why this gap:** When a sender hits a blacklist, it is a crisis — urgency drives search. No Korean practitioner has written a systematic guide covering both global blacklists (Spamhaus SBL/XBL/PBL, Barracuda, URIBL) and Korea-specific KISA RBL, including White Domain registration as a preventive tool
- **Target reader:** Marketers or IT managers who suddenly see delivery rates drop and suspect a blacklist
- **Key angle:** Checklist-driven diagnostic (how to check 5 relevant blacklists in sequence); specific delisting procedures for each; ending with KISA White Domain as the Korean-specific prophylactic measure
- **Best platform:** Brunch (crisis/story format) or Tistory (strong SEO on Korean search terms)
- **SEO terms:** `블랙리스트 이메일 해제`, `Spamhaus 등록 해제`, `KISA RBL 화이트도메인`, `이메일 스팸 차단 해제`

---

### #4 — Google Postmaster Tools 완전 정복
**Title:** `Google Postmaster Tools 완전 정복: 도메인 평판 '나쁨'에서 '높음'으로 올리는 단계별 전략`

- **Why this gap:** Gmail 2024 sender guidelines sent thousands of Korean marketers scrambling; Google's Korean documentation exists but reads like a translated manual; no Korean practitioner has written a GPT guide from the user's perspective
- **Target reader:** Email marketers at Korean companies sending to Gmail addresses; any marketer who got rejection notices after February 2024
- **Key angle:** Walk through GPT dashboards with annotated screenshots; what healthy vs. problematic looks like; 30-day recovery plan for a sender with "low" domain reputation. Include the critical Sep 2025 v2 change (Domain Reputation and IP Reputation dashboards were retired).
- **Best platform:** 요즘IT — practitioner audience, high distribution, strong SEO
- **SEO terms:** `Google Postmaster Tools 사용법`, `도메인 평판 개선`, `Gmail 발송률`, `이메일 스팸 비율 낮추기`

---

### #5 — Sunset Policy (비활성 구독자 관리)
**Title:** `구독자 30%가 6개월째 이메일을 안 읽는다면: 발송률을 지키는 Sunset Policy 설계법`

- **Why this gap:** Korean email marketing discussion focuses almost entirely on content strategy and open rate — the concept of proactively suppressing cold subscribers to protect sender reputation is essentially absent from Korean-language content
- **Target reader:** Email marketers and newsletter operators who have been sending for 1+ years and notice declining open rates; particularly relevant for Stibee users
- **Key angle:** Why inactive subscribers are a reputation threat (not just a vanity metric issue); engagement segment definitions (30/60/90/180-day windows); concrete re-engagement and sunset sequence; Korean market benchmarks from Stibee's annual report
- **Best platform:** Brunch (newsletter/marketing community); also suitable for 요즘IT
- **SEO terms:** `이메일 구독자 관리`, `발송률 개선`, `이메일 스팸 신고율`, `뉴스레터 수신 거부`, `이메일 세그멘테이션`

---

## 8. Best Publishing Platforms for Korean Deliverability Authority

| Platform | Audience | Content Format | Discovery Mechanism | Recommendation |
|---|---|---|---|---|
| **요즘IT (yozm.wishket.com)** | IT practitioners, developers, product managers (MAU 460K; newsletter 85K) | Long-form technical articles | Platform curation + Naver search + weekly newsletter (PICKKIT, Thurs) | **Primary platform.** Best reach among people managing email infrastructure. Submit articles directly. |
| **Velog** | Korean developers; strong in backend, DevOps, infrastructure | Technical posts with code/config snippets | GitHub-linked discovery; Naver search | **Best for deeply technical posts** (DMARC XML, SPF syntax, DNS config). Developer credibility platform. |
| **Brunch** | Startup founders, marketers, general tech-literate readers | Essay and narrative format | Kakao search; Brunch internal curation | **Good for marketing-audience topics** (Sunset Policy, blacklist crisis stories, "why deliverability matters"). Not best for config tutorials. |
| **Tistory** | Broad Korean internet users | Any format; strong Naver/Google crawl indexing | Naver/Google search (strongest SEO of all platforms) | **Good as owned SEO hub** — publish here for search discovery, link to deeper content on Velog/요즘IT. |
| **LinkedIn (Korean)** | Enterprise IT, B2B marketers, startup ecosystem | Short posts + link to full articles | LinkedIn feed; professional network | Growing. Korean LinkedIn becoming relevant for B2B authority. Use for commentary and article promotion. |
| **스티비 User Community / Slack** | Stibee ESP users; Korean newsletter operators | Q&A, tips, mini-guides | In-community discovery | **Tactical:** Answer deliverability questions in Stibee's user community; builds reputation directly with email practitioners. |
| **Naver Blog** | Broadest Korean internet audience | Any format | Naver search almost exclusively | **SEO play only** — Naver Blog ranks well for Korean searches. Use for repurposed content. Not a credibility-builder. |

**Summary recommendation:** Lead with 요즘IT for practitioner reach. Use Velog for technical depth that signals expertise to developers. Use Brunch for marketing-side narrative pieces. Build an owned Tistory or personal domain as SEO anchor. Establish consistent Korean presence before pursuing English.

---

## 9. English-Language Authority Building

### Top 3 Communities to Participate In

**1. Email Geeks Slack (email.geeks.chat)**
The primary global community for email professionals — thousands discussing code, design, deliverability, and tools. The #deliverability channel is active. Key behavior: answer questions publicly, especially niche ISP-specific questions. A well-researched answer about Naver Mail filtering in the #deliverability channel would immediately differentiate a Korean specialist — no one else in the community has that knowledge.

**2. M3AAWG (Messaging, Malware and Mobile Anti-Abuse Working Group)**
Industry standards body for anti-abuse and deliverability. Writing Korean-language summaries of M3AAWG conference sessions is a legitimacy signal; no Korean practitioner currently does this.

**3. Only Influencers (OI)**
Original community of email industry professionals; more marketing-practitioner oriented than M3AAWG. Useful for establishing presence among ESP marketers and email consultants.

### Content Format That Works

- **Diagnostic tutorials** (here is a real problem, step-by-step investigation) outperform generic "best practices" posts — this is how Laura Atkins / Word to the Wise built authority over 15+ years (2,500+ posts, many ISP-specific error message explanations)
- **Case studies with numbers** drive highest engagement — deliverability case studies with quantified outcomes achieve ~14% CTR vs. average ~2%
- **Tools and checklists** become reference material and attract ongoing links — a "Korean ISP deliverability checklist" in English would be a unique, linkable resource
- **ISP-specific deep dives** are highest-value authority content — Gmail and Outlook are covered by everyone; **Naver Mail is covered by essentially nobody writing in English**

### The Unique English-Language Position Available

Being the English-language authority on Korean ISP behavior (Naver Mail, Kakao Mail) is a completely open position. No one holds it. A single well-researched English post on "How to send email to Naver Mail addresses" would be the only such resource in existence.

---

## 10. Naver Contact Strategy

### What Is Publicly Known About Naver Mail Filtering

1. **Authentication requirements (2024):** Naver Mail now enforces SPF, DKIM, and DMARC on bulk senders. Aligned with Gmail's February 2024 requirements. July 2024 policy change. Source: Stibee blog, ThunderMail blog.
2. **PTR/reverse DNS requirement:** Naver requires a valid PTR record for sending IPs. Required for servers sending directly; not required when using a compliant ESP. Source: Stibee blog.
3. **KISA RBL:** Naver checks KISA and Spamhaus RBLs against sending IPs. Being on KISA RBL = outright rejection.
4. **KISA White Domain registration:** Naver participates in the KISA White Domain program (kisarbl.or.kr). Preferential treatment. Free to register; requires clean sending history (1–2 week monitoring period), valid SPF record.
5. **Simultaneous connection limits:** Naver's attack-detection system temporarily blocks IPs that open too many simultaneous SMTP connections.
6. **No public FBL:** Naver does not have a publicly documented Feedback Loop (no "Naver Postmaster Tools" equivalent). No feedback channel for bulk senders.
7. **Content signals:** KISA guidelines require "광고" in subject line, unsubscribe mechanisms, and sender identification; Naver enforces these as spam criteria.
8. **Naver.com spoofing restriction:** Using `@naver.com` as sender address from non-Naver infrastructure is explicitly blocked (post-2024).

### What Is NOT Publicly Known (The Gap = The Opportunity)

- Naver's specific domain reputation scoring system and thresholds (Gmail's 0.3% spam rate threshold — Naver's equivalent is unpublished)
- Whether Naver uses engagement signals (opens, clicks, deletions-without-reading) in filtering
- IP warm-up recognition — whether Naver tracks new-domain senders differently
- Specific SMTP error codes and rejection messages Naver returns for different block reasons
- Whether Naver has rate limits varying by sender reputation
- Whether BIMI is supported or planned
- How Naver handles forwarded email (DMARC/SPF alignment complication)
- The Daum/Kakao Mail equivalent (entirely undocumented)

### 10 Questions to Ask a Naver Employee in Email / Messaging Infrastructure

*Frame: "I'm building Korean-language technical content on email deliverability and want to make sure what I publish about Naver Mail is accurate. I'm not asking for proprietary systems documentation — I want to make sure legitimate senders are guided correctly."*

1. "I'm writing a guide for Korean businesses on sending email reliably to Naver Mail users. Is KISA White Domain registration still actively used and recommended, or has the 2024 policy change superseded it?"

2. "For senders doing everything right on authentication (SPF/DKIM/DMARC, PTR record, KISA White Domain) but still seeing delivery delays to naver.com addresses — what's the most common actual cause you see? Reputation-based? Volume-based?"

3. "Gmail has Google Postmaster Tools for sender visibility into domain reputation, spam rate, and authentication. Is there anything comparable for Naver Mail, or is feedback purely through delivery/bounce rates?"

4. "Are there common mistakes Korean businesses make when setting up email infrastructure to reach Naver Mail users that you see repeatedly — things that aren't well-documented publicly?"

5. "When Naver Mail blocks or delays email from a legitimate sender, what's the typical path for investigation and resolution? Is there a formal process?"

6. "I've seen that KISA RBL and Spamhaus are checked. Are there other blacklists or reputation systems Naver Mail checks that Korean senders should know about?"

7. "For e-commerce companies sending transactional vs. marketing email — does Naver Mail treat these differently at the infrastructure level, or is it entirely reputation/IP-based?"

8. "I'm curious about the DMARC policy for naver.com itself — currently set to `p=none`. Is there a roadmap toward `p=quarantine` or `p=reject`, and what would that mean for Naver Mail users with alias addresses?"

9. "Are there publicly available developer resources about Naver Mail's SMTP behavior — perhaps in the Naver Cloud developer docs — that I might have missed?"

10. "I'm thinking about the 광고 header requirement under Korean law — are there edge cases in how Naver's filters interpret legal labeling requirements that trip up legitimate senders?"

### How to Frame the Conversation with a Non-Mail-Owning Naver Contact

Most productive framing: **"I'm writing something public that will either correctly or incorrectly represent Naver Mail's behavior — you can influence which outcome happens."**

Specifically:
- Position as someone producing Korean-language technical content (blog series, practitioner guide) — not someone extracting operational secrets
- Ask who would be the right person to fact-check technical claims about Naver Mail deliverability — the contact may not know but may provide a warm introduction
- Reference Stibee (the leading Korean ESP) as having already written about Gmail/Naver policy changes — gives a recognizable frame of reference
- **Best entry point:** Naver Cloud Outbound Mailer product team — they have public documentation and a developer community. Approaching via that channel lands closer to the right stakeholders than going through Naver's consumer mail support.
- If contact is in developer relations or Naver Works (which has the most public mail documentation), those are also viable pathways

---

## 11. Positioning Implications

**Five conclusions from this research:**

1. **Do not lead with "email deliverability" in Korean CRM job searches.** The concept does not appear in Korean CRM job descriptions; it will not match ATS keywords. Reframe as: "multi-channel CRM automation with email expertise including technical configuration (SPF/DKIM/DMARC, 발송 성공률 최적화)."

2. **B2B SaaS and newsletter/media are the correct target sectors for email-weighted roles.** Korean B2B firms above ₩10B revenue use email as a primary channel (83% per Recatch). The growing Korean newsletter economy (Stibee, 롱블랙, Publy) runs on email.

3. **Deliverability expertise maps to a B2B SaaS support/solutions engineer role, not a marketing role.** Stibee and Notifly's customers encounter deliverability problems. The niche is closer to technical support or email infrastructure consulting than CRM marketer.

4. **Use Korean-specific language in practitioner conversations:** "발송 성공률 최적화," "스팸 분류 방지," "네이버 메일 도달률 개선," "KISA 화이트도메인 등록." The English deliverability vocabulary is not yet normalized in Korea.

5. **Braze certification is the high-leverage credentialing move for Korean CRM roles.** Braze covers push, Kakao (native support 2025), email, in-app, and SMS — exactly the multi-channel stack Korean employers want. Email is one module of Braze. Multi-channel Braze fluency is far more marketable in Korea than email-only expertise.

**The consulting angle:** Korea's automated email click rate is 3.8× above baseline (Stibee 2025) — disproportionately better than global. Properly set-up automated email programs work well in Korea. The channel is underused, not ineffective. This is the positioning argument: "your email isn't working because of deliverability problems, not because email doesn't work in Korea."

---

## 12. Sources

### Korean Job Market Sources
- [우아한형제들 CRM 마케터 — Wanted](https://www.wanted.co.kr/wd/218674)
- [쏘카 CRM 마케터 — Wanted](https://www.wanted.co.kr/wd/208039)
- [글로랑 CRM 마케터 — Wanted](https://www.wanted.co.kr/wd/215595)
- [와디즈 CRM 마케터 — Wanted](https://www.wanted.co.kr/wd/297295)
- [Naver Series CRM Marketer — Kowork](https://kowork.kr/en/post/3638)
- [힐링페이퍼 CRM 마케터 — Catch](https://www.catch.co.kr/NCS/RecruitInfoDetails/472620)
- [에픽 CRM — 채용 플랫폼 6곳 CRM 사례 분석](https://blog.effic.biz/recruitplatform)
- [에픽 CRM — 멀티채널 CRM 채널 5가지](https://blog.effic.biz/multi)
- [리캐치 — 93개 B2B 기업 마케팅 채널 순위 TOP 8](https://www.recatch.cc/ko/blog/top-b2b-marketing-channel/)

### Korean Channel Data Sources
- [스티비 2025 이메일 마케팅 리포트](https://report.stibee.com/2025/)
- [스티비 자동화 이메일 클릭률 3.8배 (Tech42)](https://www.tech42.co.kr/%EC%8A%A4%ED%8B%B0%EB%B9%84-%EC%9E%90%EB%8F%99%ED%99%94-%EC%9D%B4%EB%A9%94%EC%9D%BC-%ED%81%B4%EB%A6%AD%EB%A5%A0-3-8%EB%B0%B0-%EB%86%92%EC%95%842025-%EC%9D%B4%EB%A9%94%EC%9D%BC-%EB%A7%88/)
- [카카오 친구톡 개편 — 전자신문 (₩1.5조 문자 시장)](https://www.etnews.com/20250429000312)
- [알림톡 마케팅 사례와 지표 — Flarelane](https://blog.flarelane.co.kr/case-studies-and-metrics-for-successful-bizmessage-marketing-g6/)
- [Braze — State of Customer Engagement South Korea 2025](https://www.braze.com/resources/articles/the-state-of-customer-engagement-in-south-korea-in-2025)
- [Braze — Grow with Braze Seoul 2025 Insights](https://www.braze.com/resources/articles/moving-beyond-demographics-to-true-understanding-key-insights-from-grow-with-braze-seoul-2025)

### Korean Content Gap Sources
- [스티비 — Gmail, 네이버 메일 수신 정책 변경 (1)](https://blog.stibee.com/gmail-sender-guidelines/)
- [스티비 — Gmail, 네이버 메일 수신 정책 변경 (2)](https://blog.stibee.com/gmail-sender-guidelines-2/)
- [ThunderMail — 2024년 07월 네이버, 한메일 대량발송 변경 내용](https://blog.thundermail.co.kr/368)
- [CLVS — 이메일 마케팅 용어 바로알기(3) — SPF & DKIM](https://www.clvs.co.kr/post/%EC%9D%B4%EB%A9%94%EC%9D%BC-%EB%A7%88%EC%BC%80%ED%8C%85-%EC%9A%A9%EC%96%B4-%EB%B0%94%EB%A1%9C%EC%95%8C%EA%B8%B0-3-spf-dkim)
- [CLVS — 이메일 마케팅 용어 — Email Deliverability](https://www.clvs.co.kr/post/email-marketing-kpi-email-deliverability)
- [Notifly — 콜드메일 스팸 처리 방지 2024 규제](https://blog.notifly.tech/email-regulations-2024/)
- [요즘IT magazine](https://yozm.wishket.com/magazine/)

### Naver Mail Sources
- [네이버웍스 — 대량 메일 수신 정책 변경 (PTR레코드 등록 필수)](https://naver.worksmobile.com/notice/3568/)
- [ThunderMail — 네이버 대량메일 발송 가이드](https://blog.thundermail.co.kr/9)
- [KISA RBL 화이트도메인 등록 — IDCHOWTO](https://idchowto.com/29260/)
- [Naver Cloud — DKIM 인증 문제](https://guide.ncloud-docs.com/docs/cloudoutboundmailer-troubleshoot-auth)

### English-Language Authority Sources
- [Email Geeks Slack community](https://email.geeks.chat/)
- [Word to the Wise — Laura Atkins blog](https://www.wordtothewise.com/)
- [Only Influencers (OI)](https://www.onlyinfluencers.com/top-email-consultants-and-freelancers/entry/laura-atkins)
- [M3AAWG — Email Deliverability](https://www.m3aawg.org/blog/-/140)
- [Validity — 2025 Email Deliverability Benchmark Report](https://www.validity.com/resource-center/2025-email-deliverability-benchmark-report/)
- [Email on Acid — Naver Webmail Testing Guide](https://www.emailonacid.com/blog/article/email-development/naver-webmail-testing-what-you-need-to-know/)
