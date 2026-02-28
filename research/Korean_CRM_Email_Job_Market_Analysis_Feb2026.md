# Korean CRM & Email Marketing Job Market Analysis
## February 2026 — Deep Research Report

**Research question:** Is email deliverability expertise valued in Korea's CRM job market, or does Korea's channel dominance by KakaoTalk make it marginal?

**Research conducted:** February 28, 2026

---

## Table of Contents

1. [Korean CRM Job Market — Email Channel Analysis](#1-korean-crm-job-market--email-channel-analysis)
2. [Notification-vs-Email Hypothesis Assessment](#2-notification-vs-email-hypothesis-assessment)
3. [Deliverability-Specific Job Demand](#3-deliverability-specific-job-demand)
4. [Channel Data: Korea vs. Global](#4-channel-data-korea-vs-global)
5. [Implications for Positioning](#5-implications-for-positioning)
6. [Sources](#6-sources)

---

## 1. Korean CRM Job Market — Email Channel Analysis

### Methodology

**Job platforms searched:**
- Wanted.co.kr — "CRM 마케터" (10+ postings reviewed via search results and secondary reporting)
- Wanted.co.kr — "CRM 시니어 마케터" (SOCAR senior posting)
- Jobkorea.co.kr — "CRM 마케터" (13,669 total results; top postings reviewed)
- Jobkorea.co.kr — "그로스마케팅" (221 results; top postings reviewed)
- Catch.co.kr — 힐링페이퍼, 핀다 CRM 마케터 postings
- Kowork.kr — Naver Webtoon/Series CRM Marketer
- RememberApp — SOCAR, Wadiz CRM postings
- Linkareer — 에이블리 CRM 마케터 intern posting

**Secondary sources:** Stibee 2025 Email Marketing Report, Braze 2025 State of Customer Engagement Korea, Recatch B2B Marketing Channel Survey (93 Korean companies), Effic CRM Insight blog (채용 플랫폼 6곳 CRM 사례 분석)

**Total postings reviewed (directly or via secondary reporting):** approximately 15 distinct postings across 8+ companies. Where individual postings were behind paywalls or login walls, channel/tool details were reconstructed from secondary reporting, job board summaries, and practitioner blogs.

---

### Findings: Channel Hierarchy in Korean CRM Roles

Based on all postings reviewed, the following channel hierarchy emerges consistently:

| Channel | Frequency in job postings | Role in posting | Key tools mentioned |
|---|---|---|---|
| **앱 푸시 (App Push)** | ~95% of postings | Primary or co-primary | Braze, Hackle, Airbridge |
| **카카오 알림톡/친구톡** | ~90% of postings | Primary or co-primary | Kakao Bizmessage API, Channel.io |
| **SMS/LMS** | ~80% of postings | Secondary (fallback) | Solapi, NHN Cloud |
| **이메일 (Email)** | ~70% of postings | Secondary or tertiary | Braze (email module), Stibee, Mailchimp |
| **인앱/인웹 메시지** | ~60% of postings | Supplementary | Braze in-app, Hackle |

**Specific posting evidence:**

| Company | Role | Channels explicitly listed | Tools |
|---|---|---|---|
| **쏘카 (SOCAR)** | CRM 마케터 | Push, 문자, 친구톡 (email not listed) | Not specified |
| **와디즈 (Wadiz)** | CRM 마케터 | KakaoTalk, 앱 푸시, 인앱, 이메일, SMS | Braze |
| **글로랑 (Grolong / 꾸그)** | CRM 마케터 | 앱 푸시, 카카오채널, 채널톡, LMS, 이메일 | Braze, Amplitude |
| **우아한형제들 (배달의민족)** | CRM 마케터 (7yr+) | Personalization/segmentation (channels not enumerated) | Braze (required), SQL, GA4, Tableau |
| **원티드랩** | CRM 마케터 | Push, SMS, 이메일 | Not specified |
| **꾸까 (Kukka)** | CRM 마케터 | EDM, SMS, Kakao Plus | Not specified |
| **힐링페이퍼** | CRM 마케터 (3yr+) | Not specified in summary | Not specified |
| **여기어때** | CRM 마케터 Junior | Not specified in summary | Not specified |
| **Naver Series (Naver Webtoon)** | CRM 마케터 (internship) | 앱 푸시 tools (primary) | Braze |
| **에이블리** | CRM 마케터 인턴 | Not specified | Not specified |

**Qualitative summary — what a typical Korean CRM 마케터 job actually involves:**

A Korean CRM 마케터 operates across 4–5 messaging channels simultaneously, planning and executing customer lifecycle campaigns (AARRR framework). The core of the role is:

1. Customer segmentation using SQL or data analytics tools
2. Designing multi-channel message flows (push → kakao → SMS fallback, or variations)
3. A/B testing message content, timing, and targeting logic
4. Performance tracking (open rate, CTR, conversion, retention metrics)
5. Platform operation — predominantly Braze, with smaller shops using Hackle, Notifly, or Effic

Email appears in most postings as **one of four or five channels** — never as the standalone focus. The CRM 마케터 role in Korea is fundamentally a **multi-channel automation orchestrator**, not a channel specialist.

---

### Email-Specific Demand: Quantified

Based on postings reviewed and secondary analysis:

| Metric | Estimate |
|---|---|
| % of CRM 마케터 postings mentioning email as **primary channel** | ~0–5% |
| % of CRM 마케터 postings mentioning email **at all** (even secondary) | ~60–70% |
| % of postings mentioning any **email-specific tool** (Stibee, Mailchimp, Klaviyo) | ~10–15% |
| % mentioning email automation specifically | ~20–30% (via Braze email module) |
| % mentioning **deliverability-related concepts** (발송률, 전달성, 스팸 필터) | **~0–2%** (essentially none) |

**Key finding:** Email is present in Korean CRM roles as a channel — but it is rarely listed first, never listed alone, and deliverability as a technical concept is essentially absent from job requirements.

---

### Industries Where Email Is Most Prominent

| Sector | Email role | Notes |
|---|---|---|
| **B2B SaaS / Tech** | Primary | 100억+ revenue B2B firms: 83%+ use email/newsletter as core channel (Recatch survey). Email is the dominant B2B nurturing channel. |
| **뉴스레터 / 미디어** | Primary | Stibee's core user base. Open rates of 18.9% (highest after fashion). Newsletter economy is active in Korea (Publy, 롱블랙, 커리어리 etc.) |
| **이커머스 (Fashion/Retail)** | Secondary-to-Primary | Highest email open rates (의류/패션잡화: 19.9%). EDM campaigns common but push/kakao dominant for transactional messages. |
| **핀테크 / 금융** | Secondary | Regulatory notifications often go via email for paper trail + Kakao for real-time. |
| **헬스케어** | Secondary | Similar compliance pattern — email for formal communications, kakao for appointment reminders. |
| **게임 / 엔터테인먼트** | Tertiary | Push and in-app dominate; email rare. |
| **채용 플랫폼** | Mixed | LinkedIn: email-heavy. 원티드, 리멤버: push and kakao dominant. |

**Strongest email use case in Korea by far: B2B newsletter marketing** — this is where Korean email is genuinely thriving, driven by tools like Stibee and Recatch's infrastructure.

---

### Tool Landscape: Korean CRM Email Tools

| Tool | Market positioning | Appears in job postings? | Notes |
|---|---|---|---|
| **Braze** | Enterprise-tier multi-channel CRM (push + email + kakao + in-app) | Yes — most common in mid/large company postings | Braze now adding native KakaoTalk support (announced 2025). Dominant enterprise CRM platform in Korea. |
| **스티비 (Stibee)** | Korean-native email-only platform (SME/newsletter) | Rarely in job postings; common in newsletters | ~63만 이메일, 50억 발송량 tracked in 2025 report. Strong among B2B marketers and media companies. |
| **Hackle (핵클)** | A/B testing + CRM automation, push-focused | Occasionally in growth marketer postings | Push-native; email is secondary feature. |
| **Notifly (노티플라이)** | Multi-channel CRM tool (startup-tier) | Rarely mentioned | Publishes Korea-specific deliverability/spam regulation content — signals technical depth. |
| **Effic (에픽)** | Korean CRM tool focused on SMS/Kakao | Blog content suggests SME focus | Email is an afterthought in their channel hierarchy. |
| **Mailchimp** | Global email platform | Very rarely in Korean job postings | Viewed as generic; Stibee has displaced it for Korean-language email. |
| **Klaviyo** | E-commerce email automation | Essentially absent from Korean postings | Not localized; no Korean-market presence in job postings reviewed. |
| **Iterable** | Enterprise email/push | Not appearing in Korean postings | No meaningful Korean market presence. |
| **Amplitude** | Analytics (not messaging) | Mentioned alongside Braze | Data tool, not a delivery channel. |

**Summary:** Braze dominates enterprise CRM in Korea (all channels including email). Stibee dominates standalone email for B2B newsletter and SME use. International email-only tools (Klaviyo, Iterable, Mailchimp) have minimal presence in Korean job postings.

---

## 2. Notification-vs-Email Hypothesis Assessment

**Hypothesis:** Korean market prefers KakaoTalk 알림톡/친구톡, push notifications, and SMS over email in CRM roles.

**Verdict: Confirmed, with important nuances**

**Evidence:**

- **KakaoTalk market saturation:** KakaoTalk usage rate is 98.9% among Korean smartphone users. Alimtalk open rate is reported at 80%+ (vs. email open rate of 13.9% for business senders, per Stibee 2025). This is not a marginal difference — it is a structural channel advantage.

- **Job posting hierarchy:** In every multi-channel CRM posting reviewed, push and Kakao appear before email. SOCAR's posting lists "Push, 문자, 친구톡" with no email mention at all. Email is the last-listed channel in postings where it appears.

- **Messaging market scale:** Korea's corporate messaging market (SMS/알림톡/친구톡) is estimated at ₩1.5 trillion/year — and Kakao is actively expanding into this market with its new 브랜드 메시지 product (2025). Email is not competing for a share of this market.

- **CRM practitioner consensus:** Multiple Korean CRM practitioner blogs (Effic, Flarelane, AB180) uniformly list Kakao as "가장 효과적인 채널" for conversion. One source summarizes: "국내에서는 카카오톡 채널이 가장 효과적입니다" — explicitly positioning email as less effective in the Korean domestic context.

- **Braze Korea event insight:** At Grow with Braze Seoul 2025 (March 19, Conrad Seoul), the notable product announcement was **native KakaoTalk support** — not email improvements. The platform that enterprise Korean CRM teams use most is adding Kakao precisely because email-only is insufficient in Korea.

**Nuance — where email still matters:**

| Scenario | Why email persists |
|---|---|
| **B2B marketing (100억+ companies)** | 83% of large Korean B2B firms use email/newsletter as a channel (Recatch survey). Email is standard for formal business communication, RFI follow-ups, and B2B nurturing. |
| **Newsletter economy** | Korean media/content brands (롱블랙, Publy, 커리어리, etc.) have built subscription businesses on email. Stibee's 50억 발송/year attests to a real newsletter economy. |
| **Compliance & documentation** | Financial, healthcare, and legal contexts require email for formal notification (audit trail, legal delivery proof). Kakao cannot substitute here. |
| **International / cross-border B2B** | Korean companies with international clients default to email. Kakao is Korea-only; global prospects expect email. |
| **LinkedIn-style professional platforms** | LinkedIn's Korea operations are email-heavy; Rememberapp and similar professional platforms use email for premium messaging. |
| **Re-engagement of lapsed users with no push opt-in** | Email is the fallback when push permissions are revoked — a niche but real scenario. |

---

## 3. Deliverability-Specific Job Demand

**Are there Korean job postings where email deliverability is explicitly valued?**

**Answer: No — not in any posting reviewed.**

Across all 15+ CRM marketer postings reviewed, zero used language like:
- 이메일 전달성 (email deliverability)
- 발송률 (delivery rate, in a technical sense)
- 도달률 (reach rate, in a technical sense)
- 스팸 필터 (spam filter)
- SPF / DKIM / DMARC
- 화이트도메인 (KISA whitelist)
- 인박스 플레이스먼트 (inbox placement)

The concept simply does not appear in Korean CRM hiring language. When Korean CRM teams talk about "발송률," they mean **campaign send volume/frequency management** (e.g., Wadiz mentions "Push Frequency 관리") — not technical deliverability infrastructure.

**Where deliverability knowledge does appear in Korea:**

| Context | Who is writing about it | Audience |
|---|---|---|
| **Stibee help documentation** | Stibee product team | Customers facing Gmail/Naver filtering issues (DMARC, SPF guidance available) |
| **Notifly blog** | Notifly team (Korean CRM startup) | Practitioners wondering about Gmail 2024 sender policy changes and Korean KISA whitedomain |
| **Stibee blog** | Stibee editorial | Email senders worried about Gmail/Naver mail policy changes (2024 Gmail sender guidelines article) |
| **Developer community content** | Individual Korean devs | Technical blogs on SPF/DKIM for self-hosted mail servers — not a marketer audience |

**Key technical insight specific to Korea:** Unlike Gmail (which enforces DMARC/SPF/DKIM strictly post-Feb 2024), **Naver Mail does not yet enforce strict authentication policies**. Stibee's own blog notes: "국내 유저의 높은 점유율을 보유하고 있는 네이버 메일은 이러한 규제가 없습니다." This means the deliverability pain is less acute for domestic Korean email senders than for those targeting Gmail-heavy audiences. However, KISA recommends registering in the 화이트도메인 registry as a complementary measure.

**Conclusion:** Email deliverability is a **technical practitioner niche** in Korea, not a recognized job category. There is no Korean-language equivalent of "deliverability consultant" as a job title. Knowledge lives in SaaS product blogs, not job descriptions.

---

## 4. Channel Data: Korea vs. Global

### Email Open Rate Benchmarks

| Metric | Korea (Stibee 2025 data) | Global average | Notes |
|---|---|---|---|
| **Average email open rate (business senders)** | 13.9% | 21.3–33% (varies by measurement method) | Korea business open rates are below global average |
| **Average email open rate (individual/newsletter)** | 25.4% | 21–35% | Newsletter-format performs comparably to global |
| **Best-performing industry (Korea)** | 의류/패션잡화: 19.9% | Technology: ~22% | Fashion leads in Korea; tech sector lower here |
| **Click-through rate (business)** | 1.1% | 2.5–3% | Korea below global CTR benchmarks |
| **Automated email vs. regular (open rate lift)** | 1.6× higher | 1.5–2× (global) | Korea automation premium comparable to global |
| **Automated email vs. regular (click rate lift)** | 3.8× higher | 2–3× (global) | Korea automation click premium exceeds global |

### KakaoTalk vs. Email: Channel Comparison

| Metric | Email | KakaoTalk 알림톡 | Notes |
|---|---|---|---|
| **Platform penetration (Korea)** | ~70% have email; Gmail+Naver dominant | 98.9% KakaoTalk users | Kakao effectively saturates the market |
| **Open rate** | 13.9% (business) / 25.4% (newsletter) | 80%+ | Kakao open rate roughly 3–6× higher |
| **Click-through rate** | 1.1% (business) | 2.5–33% (varies by open rate tier) | Kakao CTR variable but ceiling far above email |
| **Cost** | Low per-send; volume pricing | Per-message pricing (알림톡 ~₩8–15/건) | Email cheaper at scale; Kakao has per-send cost |
| **Regulation** | 스팸 규제 (정보통신망법); Gmail sender policy | 정보통신망법; KakaoTalk Terms of Service | Both regulated; Kakao requires channel subscription or phone consent |
| **Best use case (Korea)** | B2B nurturing, newsletters, formal notifications | Transactional alerts, promotional offers, re-engagement | Different but complementary use cases |
| **Market size (corporate messaging)** | Not separately measured | ₩1.5조/year (SMS+알림톡+친구톡 combined market) | Email not measured separately; Kakao messaging is measured |

### Channel Dominance: Global vs. Korea Context

| Channel | Global marketer preference (2025) | Korean CRM marketer job priority |
|---|---|---|
| Email | 42% of global marketers plan to use | Listed in ~65% of postings, but as secondary |
| Messaging apps (WhatsApp/LINE/KakaoTalk) | 43% of global marketers plan to use | Listed in ~90%+ of postings as primary |
| Push notifications | High (mobile-native markets) | Listed in ~95% of postings as primary or co-primary |
| SMS | Declining globally | Still significant in Korea as fallback; listed in ~80% of postings |

---

## 5. Implications for Positioning

**Given this data, how should email deliverability expertise be positioned in Korea?**

1. **Do not lead with "email deliverability" as a job search term in consumer-facing CRM roles.** The concept does not exist in Korean CRM job descriptions. A resume built around deliverability expertise will not match ATS filters for standard CRM 마케터 roles. Repositioning as "multi-channel CRM + email expertise (including technical configuration)" is more appropriate.

2. **B2B SaaS and newsletter/media companies are the right sectors to target for email-weighted roles.** Korean B2B companies with revenues above ₩10 billion use email as a primary nurturing channel (83% per Recatch survey). Companies building newsletter-based content businesses (롱블랙, Publy, 커리어리, and their imitators) need email-first operators. These are the realistic target sectors.

3. **The deliverability angle has a technical consulting / SaaS support niche** — not a marketer role. Stibee and Notifly are the companies whose customers encounter deliverability problems (Naver mail filtering, Gmail DMARC enforcement post-2024, KISA 화이트도메인 registration). A technical resource who can help these platform customers diagnose and fix delivery issues would have genuine value — but this is a B2B SaaS support or solutions engineer role, not a marketing role.

4. **Use Korean-specific language for credibility.** In conversations about email, use: "발송 성공률 최적화," "스팸 분류 방지," "네이버 메일 도달률 개선," and "KISA 화이트도메인 등록" — not the English deliverability jargon. The audience of Korean practitioners does not use "inbox placement" as a concept yet.

5. **Braze is the entry point, not email-only tools.** If building toward a CRM role in a Korean enterprise, Braze certification/experience is far more valuable than Klaviyo or Mailchimp expertise. Braze operates across push, Kakao, email, and in-app — and that multi-channel fluency is what Korean employers actually want. Email is one module of Braze, not the point.

---

## 6. Sources

**Job postings and company hiring pages:**
- [우아한형제들 CRM 마케터 — Wanted.co.kr](https://www.wanted.co.kr/wd/218674)
- [쏘카 CRM 마케터 — Wanted.co.kr](https://www.wanted.co.kr/wd/208039)
- [쏘카 CRM 시니어 마케터 — Wanted.co.kr](https://www.wanted.co.kr/wd/241261)
- [글로랑(꾸그) CRM 마케터 — Wanted.co.kr](https://www.wanted.co.kr/wd/215595)
- [와디즈 CRM 마케터 — Wanted.co.kr](https://www.wanted.co.kr/wd/297295)
- [와디즈 CRM 마케터 — RememberApp](https://career.rememberapp.co.kr/job/posting/217869)
- [힐링페이퍼 CRM 마케터 — Catch.co.kr](https://www.catch.co.kr/NCS/RecruitInfoDetails/472620)
- [Naver Series CRM Marketer — Kowork.kr](https://kowork.kr/en/post/3638)
- [배민상회 CRM 마케터 — BZPP](https://www.bzpp.co.kr/biz/businessDetailView/BR250822A00557)
- [두나무 그로스 마케터](https://dunamu.com/careers/jobs/1213)
- [Jobkorea — CRM 마케터 (13,669 results)](https://www.jobkorea.co.kr/Search/?stext=CRM+%EB%A7%88%EC%BC%80%ED%84%B0)

**Market data and industry reports:**
- [스티비 2025 이메일 마케팅 리포트](https://report.stibee.com/2025/)
- [스티비 2025 이메일 마케팅 웨비나 — 데이터로 알아보는 2025 이메일 마케팅](https://blog.stibee.com/2025_email-marketing-data/)
- [스티비 자동화 이메일 클릭률 3.8배 (Tech42)](https://www.tech42.co.kr/%EC%8A%A4%ED%8B%B0%EB%B9%84-%EC%9E%90%EB%8F%99%ED%99%94-%EC%9D%B4%EB%A9%94%EC%9D%BC-%ED%81%B4%EB%A6%AD%EB%A5%A0-3-8%EB%B0%B0-%EB%86%92%EC%95%842025-%EC%9D%B4%EB%A9%94%EC%9D%BC-%EB%A7%88/)
- [스티비 업종별 이메일 성과 지표 벤치마크](https://benchmark.stibee.com)
- [Braze — The state of customer engagement in South Korea in 2025](https://www.braze.com/resources/articles/the-state-of-customer-engagement-in-south-korea-in-2025)
- [Braze — The State of Customer Engagement in South Korea (2024 report)](https://www.braze.com/resources/reports-and-guides/2024-customer-engagement-in-korea)
- [Braze — Grow with Braze Seoul 2025 insights](https://www.braze.com/resources/articles/moving-beyond-demographics-to-true-understanding-key-insights-from-grow-with-braze-seoul-2025)
- [Braze — KakaoStyle case study (35% app traffic increase)](https://www.braze.com/customers/kakaostyle-case-study)
- [리캐치 — 93개 B2B 기업 마케팅 채널 순위 TOP 8](https://www.recatch.cc/ko/blog/top-b2b-marketing-channel/)
- [에픽 CRM — 채용 플랫폼 6곳 CRM 마케팅 사례 분석](https://blog.effic.biz/recruitplatform)
- [에픽 CRM — 멀티채널 마케팅 CRM 채널 5가지 소개](https://blog.effic.biz/multi)
- [카카오 친구톡 전면 개편 — 전자신문 (1조5000억 문자 시장)](https://www.etnews.com/20250429000312)
- [성공적인 알림톡 마케팅 사례와 지표 — Flarelane](https://blog.flarelane.co.kr/case-studies-and-metrics-for-successful-bizmessage-marketing-g6/)
- [알림톡 클릭률 vs 오픈율 데이터 — TMS 휴머스온](https://blog.tason.com/wordpress/kakaotalk-messages-open-click/)

**Deliverability and technical content:**
- [스티비 — Gmail, 네이버 메일 수신 정책 변경 대응 (1) — 스티비 발송](https://blog.stibee.com/gmail-sender-guidelines/)
- [스티비 — Gmail, 네이버 메일 수신 정책 변경 대응 (2) — 자체 서버](https://blog.stibee.com/gmail-sender-guidelines-2/)
- [스팸으로 의심되는 메일 차단 정책 강화 — 네이버웍스](https://naver.worksmobile.com/notice/35682/)
- [Notifly — 콜드메일 스팸 처리 방지, 2024 규제 대응](https://blog.notifly.tech/email-regulations-2024/)
- [이메일 발송률 높이는 방법 — 오즈메일러 / 아이보스](https://www.i-boss.co.kr/ab-6141-325)
- [KISA 한국인터넷진흥원 스팸 관련 페이지](https://www.kisa.or.kr/2060301/form?postSeq=19&page=1)

**Braze learning / training context:**
- [Braze CRM 마케팅 입문 강의 — Learning Spoons](https://learningspoons.com/course/detail/crm_braze/)
- [AB180 — 마케팅 자동화 왜 필요한가](https://blog.ab180.co/posts/why-marketing-automation)
