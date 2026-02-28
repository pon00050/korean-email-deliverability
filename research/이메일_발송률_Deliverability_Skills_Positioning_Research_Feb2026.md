# 이메일 발송률 / Email Deliverability — Skills, Market, and Positioning Research
**Date:** 2026-02-28
**Status:** Deep research session — synthesis of 4 parallel agents
**Purpose:** Answer three questions: (1) minimum skill set to win first gigs, (2) how existing background creates positioning advantages, (3) what separates $15/hr from $150/hr and how to close the gap faster

---

## Table of Contents
1. [Minimum Skill Set — Korean Market Context](#1-minimum-skill-set)
2. [Korean Job Market — Titles, Employers, Salary Signals](#2-korean-job-market)
3. [The $15/hr vs. $150/hr Gap](#3-the-gap)
4. [Background Leverage Map](#4-background-leverage)
5. [Recommended Positioning Statement](#5-positioning-statement)
6. [Suggested Learning Sequence](#6-learning-sequence)
7. [Sources](#7-sources)

---

## 1. Minimum Skill Set

### 1A. Korean Market Context First

Korean-language internet covers deliverability at **Tier 1** (basic DNS configuration) reasonably well. Tiers 2–3 are nearly absent in Korean. This is both the competitive gap and the opportunity.

**Korean-specific inbox providers to know (no English guide covers these):**
| Provider | Market Role | Deliverability Tool |
|---|---|---|
| **Gmail** | Dominant for Korean business email | Google Postmaster Tools (free) |
| **Naver Mail** | Largest Korean consumer inbox | No public postmaster tool — Naver Mail filtering logic is undocumented |
| **Kakao Mail** | Secondary consumer | No public postmaster tool |
| **Naver Works** | B2B groupware (SMBs) | Enterprise IT-managed |
| **Daou Office** | Korean enterprise groupware | NDR error codes specific to this platform |

**Key Korean-specific fact:** Gmail AND Naver Mail simultaneously tightened sender policies in 2024 — a dual-ISP policy event with no equivalent in English-language deliverability writing. 스티비 published the only Korean-language guidance. Understanding both simultaneously is a uniquely Korean practitioner skill.

**Korean ESP ecosystem:**
- **스티비 (Stibee)** — dominant for Korean newsletters; has its own domain status checker at [lab.stibee.com](https://lab.stibee.com/)
- **오즈메일러 (OzMailer)** — secondary Korean ESP
- **Mailchimp** — international brands in Korea
- **Braze** — enterprise Korean CRM platforms (Braze email module, not pure ESP)

**Korean hosting deliverability risk:** Cafe24, Gabia, Hosting.kr — cPanel-based shared IP. Individual customers share sender reputation. This is a pain point specific to Korean SMBs that no Western deliverability guide addresses.

**No standardized Korean term for "deliverability":**
- 전달성 / 발송 성공률 / 수신률 / 도달률 — all used interchangeably
- No single term has won
- This is a content/SEO opportunity: whoever defines the terminology becomes the reference

---

### 1B. Tiered Skill Map

| Tier | Skills | Korean Coverage | English Coverage | Time to Learn |
|---|---|---|---|---|
| **Tier 1 (Entry — table stakes)** | SPF/DKIM/DMARC setup; MXToolbox blacklist check; mail-tester.com score; hard vs. soft bounce classification; spam complaint rate thresholds | Well covered (스티비, petsonthego, velog) | Saturated | 2–4 weeks |
| **Tier 2 (Intermediate — differentiated in Korea)** | DMARC report parsing (RUA XML); inbox placement testing (GlockApps seed lists); Google Postmaster Tools interpretation; bounce forensics; engagement segmentation; list hygiene strategy | Sparse in Korean | Well covered | 2–4 months |
| **Tier 3 (Advanced — uncontested in Korean market)** | ISP-specific behavior (Naver Mail, Gmail, Outlook nuances); IP warmup architecture; FBL (Feedback Loop) setup; dedicated vs. shared IP strategy; MTA configuration; spam trap forensics; Validity/CSA certification navigation | Not covered in Korean | Practitioner/consultant level only | 1–2 years of practice |

**Minimum for first paid audit (Tier 1 + partial Tier 2):**

```
Authentication Layer:
  ✓ Read and write SPF record syntax (include:, -all vs ~all)
  ✓ Verify DKIM DNS TXT record; read DKIM header in raw email source
  ✓ Configure DMARC p=none → quarantine → reject progression
  ✓ Read DMARC aggregate (RUA) XML reports

Reputation Layer:
  ✓ Run IP + domain through 100+ RBL blacklists (MXToolbox + Spamhaus)
  ✓ Interpret Google Postmaster Tools (domain reputation trend, spam rate)
  ✓ Know Microsoft SNDS for Outlook/Hotmail IP reputation
  ✓ Distinguish inbox placement rate from delivery rate

List and Program Layer:
  ✓ Classify bounce types; know acceptable thresholds (<2% hard bounce)
  ✓ Understand spam complaint rate thresholds (<0.1% Gmail)
  ✓ Basic list hygiene concepts (double opt-in, sunset policy)

Content Layer:
  ✓ Run mail-tester.com and interpret score
  ✓ Text-to-image ratio check (60/40 rule)
  ✓ Verify List-Unsubscribe header presence (RFC 8058 one-click)
```

**Free tool stack for a first audit:**
| Tool | Function |
|---|---|
| [MXToolbox](https://mxtoolbox.com) | DNS lookup, blacklist check (basic) |
| [Mail-tester.com](https://www.mail-tester.com/) | Send test email, get scored diagnosis (3/day free) |
| [GlockApps](https://glockapps.com) | Inbox placement test across 20+ providers (freemium) |
| [Google Postmaster Tools](https://postmaster.google.com) | Gmail domain/IP reputation — free |
| [Microsoft SNDS](https://sendersupport.olc.protection.outlook.com/snds/) | Outlook IP reputation — free |
| [Spamhaus Check](https://check.spamhaus.org/) | Most impactful blacklist — free |
| [스티비 실험실](https://lab.stibee.com/) | Korean-localized domain status checker — unique to Korean market |

**Standard 7-step audit process:**
1. Establish baseline metrics (delivery rate, bounce rate, complaint rate, open rate)
2. Verify authentication (SPF/DKIM/DMARC alignment)
3. Check sender reputation (Google Postmaster Tools, SNDS)
4. Blacklist scan (domain + sending IP)
5. Inbox placement test (GlockApps seed list)
6. Content and technical audit (mail-tester, link hygiene, header check)
7. List hygiene review (bounce suppression, inactive segmentation)

---

## 2. Korean Job Market

### 2A. Job Titles That Cover Deliverability Work

Email deliverability **does not exist as a standalone job title in Korea**. Deliverability skills are embedded inside:

| Korean Title | Deliverability Exposure | Notes |
|---|---|---|
| **CRM 마케터** | Low-to-moderate | Email is 1 of 8 channels; 앱 푸시 + 알림톡 dominate |
| **이메일 마케터 / 담당자** | Moderate | 발송성공률 rising as tracked KPI (스티비 2025 report) |
| **그로스 마케터 / 그로스 해커** | Variable | Deliverability surfaces only at scale |
| **마케팅 자동화 / Marketing Ops** | Higher | SPF/DKIM setup is practical prerequisite for ESP onboarding |
| **디지털 마케터 (general)** | Low | Incidental |

**No Korean job posting explicitly requires** SPF/DKIM/DMARC, "이메일 도달률 전문가," or "deliverability" in the job title. Zero found on Wanted, 사람인, 잡코리아.

**Why:** Korea's CRM stack is push-heavy (앱 푸시 + 카카오 알림톡 dominate retention). Email is supplementary in most Korean consumer apps. Deliverability is handled inside the ESP's managed infrastructure — companies don't configure it themselves.

### 2B. Skills Korean Employers Actually List (CRM 마케터)

**Required (공통 자격요건):**
- SQL for data extraction
- Braze (most common), Salesforce Marketing Cloud, HubSpot, or Stibee
- A/B test design and interpretation
- Amplitude or Mixpanel for behavioral analytics
- All channels: email + 앱 푸시 + 카카오 알림톡 + in-app

**Preferred / Bonus (우대사항):**
- Braze or SFMC hands-on experience (often required, not just preferred)
- 정보통신망법 수신동의 opt-in compliance understanding
- SQL proficiency for self-service data pulls

**What is NOT listed in Korean postings:** SPF/DKIM/DMARC, IP reputation, bounce forensics, blocklist management, inbox placement testing.

### 2C. Korean Salary Ranges (CRM 마케터)

Source: 그룹바이 블로그, 아이보스, 잡플래닛

| Level | Experience | Annual Salary |
|---|---|---|
| 신입 | 0–1 yr | ~₩3,000만 |
| 주니어 | 1–3 yr | ₩3,657만–₩4,003만 |
| 미들 | 3–5 yr | ₩5,403만 |
| 시니어 | 5+ yr | ₩6,591만 |
| 팀장급 | 7+ yr | ₩9,786만 |
| **그로스 마케터 평균** | — | **₩6,672만** (highest among marketers) |
| CRM 마케터 평균 | — | ₩5,123만 |

No dedicated "이메일 deliverability" salary band exists in Korean data. Deliverability expertise is unpriced in the Korean market — making it simultaneously a positioning gap and a rate-setting opportunity for the first mover.

### 2D. Global Deliverability Specialist Salaries (USD, for reference)

| Role | Median | P75 | P90 |
|---|---|---|---|
| Email Deliverability Specialist (US) | $64,246 | $72,500 | $78,500 |
| Senior Email Deliverability Specialist | ~$82,000 | $98,500 | — |
| Email Deliverability Consultant (Glassdoor) | ~$120,000 | $163,287 | — |

**Remote availability:** 257 of ~654 US-listed deliverability positions are remote — significant freelance/contract opportunity accessible from Seoul.

### 2E. Where Deliverability Skills Would Create Differentiation in Korea

- **B2B SaaS** with heavy transactional email (세금계산서 notifications, invoices, OTPs) — deliverability is infrastructure-critical, not just marketing
- **핀테크 / 금융** where email is a compliance channel
- **글로벌 진출 스타트업** where Korean ESP assumptions don't hold internationally
- **ESP/MarTech vendors in Korea** (Stibee, Mailplug) — most likely to hire someone with technical deliverability skills

---

## 3. The $15/hr vs. $150/hr Gap

### 3A. Full Pricing Spectrum

| Tier | Rate | Who They Are |
|---|---|---|
| Commodity / Upwork bottom | $15–$40/hr | Follow checklists; know SPF/DKIM basics; no proprietary insight |
| Competent practitioner | $50–$100/hr | 3–8 yr in-house or ESP experience; tool-proficient; diagnoses common issues |
| Senior specialist | $100–$150/hr | Deep pattern recognition; ISP-relationship experience; has rescued major disasters |
| Top-tier / named expert | $150–$300+/hr | Published, conference-speaking, community authority; can negotiate with mailbox providers |
| Agency (managed) | $2,000–$12,000+/month | Full program management, mid-market to enterprise |

### 3B. The Most Expensive Problems (= Where Premium Rates Are Justified)

**1. Major Blacklist Listings (Spamhaus SBL/DBL)**
- Blocks email to millions of mailboxes overnight; delivery can drop from 95% → near 0%
- Revenue link: $500K/month email-driven revenue × 23% drop = $115K/month lost → a $10K consultant is trivially justified
- *What separates $15 from $150:* Low-rate consultants submit a web form. Senior practitioners diagnose *why* (spam trap hits vs. complaint spike vs. snowshoe detection), know escalation paths at each RBL, and prevent recurrence.

**2. Gmail Bulk Folder Routing at Scale**
- Gmail doesn't communicate blacklisting — emails silently go to spam
- A sender at "Low" domain reputation with 5M subscribers loses access to ~60–70% of recipients
- Marketing teams blame subject lines; deliverability consultants read Postmaster Tools and find the real cause
- *Diagnostic expertise:* Domain vs. IP reputation split, spam rate curves over time, authentication failure rate by sending domain

**3. DMARC Rollout for Enterprise Senders**
- Large companies with 50–200 sending domains + multiple ESPs + third-party SaaS (CRMs, helpdesks, billing) have complex SPF/DKIM alignment problems
- A botched rollout can break all transactional email (receipts, password resets) simultaneously
- Enterprise DMARC project engagements: **$5,000–$50,000** are normal

**4. IP Warmup Failures for ESP Migrations**
- Switching ESPs without proper warmup = immediate reputation damage to new IP ranges before migration completes
- High-volume SaaS and fintech (10M+ emails/month) have enormous exposure

**5. Spam Trap Acquisition**
- Even 0.01% spam trap hit rate can trigger Spamhaus SBL listing
- Diagnosis requires Validity Everest or GlockApps combined with list audit — not just "run an email verifier"

### 3C. What $15/hr vs. $150/hr Actually Know

**$15/hr knows:**
- SPF/DKIM/DMARC basics (can set records, run MXToolbox)
- Run GlockApps and read a score
- Repeat generic advice: "clean your list," "warm your IP," "avoid spam words"
- Follow a checklist
- **Cannot diagnose when the checklist doesn't explain the problem**

**$150/hr+ knows:**

*Infrastructure-level:*
- SPF record flattening for large senders with >10 include mechanisms
- DKIM key rotation strategy, selector management across multiple ESPs
- DMARC RUA/RUF XML report analysis (not just checking policy)
- BIMI deployment including VMC (Verified Mark Certificate) via DigiCert/Entrust
- MTA configuration: Postfix, Exim, PowerMTA queue management and per-domain throttling
- Dedicated vs. shared IP strategy by sending volume and use case

*Mailbox provider-specific:*
- Gmail Postmaster Tools: domain vs. IP reputation split — knows which levers move it
- Microsoft SNDS: IP range complaint visualization
- Yahoo Postmaster feedback loop registration and thresholds
- Apple MPP impact on open rate measurement and warmup strategy
- Naver Mail filtering logic (undocumented — Korean specialist differentiator)

*The $150/hr pattern:* Looks at a non-obvious problem ("our transactional password resets go to spam for AOL/Verizon users only, but marketing emails are fine") → forms an immediate hypothesis → identifies it as a DKIM alignment issue on a specific subdomain → fixes it in one session. This is pattern recognition from having seen that exact failure before, not checklist execution.

### 3D. Named Expert Cohort — What They Have in Common

| Name | Affiliation | Credentials |
|---|---|---|
| **Laura Atkins** | Word to the Wise | Co-founded MAPS abuse desk; 20+ yr; M3AAWG active; Spamhaus contributor |
| **Matthew Vernhout** | Email Industries | 20 yr; M3AAWG Training Co-Chair; CAUCE Director; CIPP/C; helped write CASL + BIMI standards |
| **Al Iverson** | Spam Resource | 25+ yr; 4M+ pageviews; DELIVTERMS glossary; covers RBL policy changes in real time |
| **Kevin "KAM" McGrail** | Apache SpamAssassin | Open-source contributor to the primary spam filter engine; Deliverability Summit keynote |

**Universal patterns in the named expert cohort:**
1. Tenure 10–25 years
2. Active M3AAWG participation (the industry body where ISPs + ESPs set policy together)
3. Public writing with durable body of work (blog, conference talks, whitepapers)
4. Both-sides experience (worked at ISP or ESP — knows how filters *actually* work)
5. Named in conference programs (Deliverability Summit, M3AAWG, Litmus Live)
6. Community reputation in EmailGeeks Slack (#deliverability)

### 3E. Building Credibility Without a Portfolio

In email deliverability, clients cannot evaluate work the way they evaluate a designer's portfolio — the work is invisible. Credibility signals substitute:

**1. Public writing (highest leverage)**
- A blog with technically accurate content is the single most leverageable asset
- Word to the Wise (Atkins) and Spam Resource (Iverson) built their practices almost entirely on public writing
- Topics that signal expert-level knowledge: analyzing specific RBL policy changes, dissecting a DMARC aggregate report, explaining Gmail Postmaster Tools interpretation, writing about ISP-specific filtering nuances
- **Korean opportunity:** Writing technically accurate Korean-language deliverability content creates a category of one — no Korean practitioner is doing this

**2. EmailGeeks Slack (#deliverability channel)**
- 22,000+ member community; the primary referral network for mid-to-high-end consulting
- Answering hard questions accurately in public builds reputation that translates to referrals

**3. M3AAWG participation**
- Members-only conferences 3x/year where ISPs, ESPs, and security researchers share intelligence
- Producing or contributing to Best Common Practices documents is a significant credibility marker
- Joining as an organization member is the path in

**4. Conference speaking (Deliverability Summit, Litmus Live, MailCon)**
- Deliverability Summit (Barcelona 2026) is the most focused event
- Speaking submission accepted = peer validation

**5. Open-source tools**
- `checkdmarc`, `parsedmarc`, custom blocklist monitoring scripts on GitHub
- Kevin McGrail's SpamAssassin contributions made him a keynote speaker

### 3F. Certifications That Exist

| Certification | What It Is | Career Value |
|---|---|---|
| **Validity Sender Certification** | Certifies a *sending program* meets quality standards; certified IPs get preferential ISP treatment | Navigating this for a client demonstrates high-bar expertise |
| **Certified Senders Alliance (CSA)** | European certification (eco + DDV); GDPR-aligned; whitelisted at GMX, Web.de, T-Online | Useful for EU-facing clients |
| **M3AAWG** | Not a certification — but active participation is the highest-tier industry credibility signal | Matthew Vernhout (Training Co-Chair) shows its career value |
| **CIPP/C** | Canadian privacy certification (PIPEDA/CASL) — Matthew Vernhout holds this | Privacy-compliance deliverability intersection |
| **No universal "deliverability consultant" credential exists** | The field has no industry-standard cert | Community reputation is the de facto credentialing system |

### 3G. High-Value Audit Deliverable Format

**Scope (1–2 weeks of work, not a 2-hour tool run):**
- Infrastructure layer: SPF, DKIM, DMARC, PTR/rDNS, MX, BIMI readiness
- Sending program: IP configuration, bounce handling, FBL setup, list hygiene
- Mailbox provider diagnostics: Postmaster Tools trend (30 days), SNDS, inbox placement (GlockApps)
- Content and practice review: headers, link hygiene, sending frequency patterns

**Deliverable format:**
- 15–40 page PDF
- Executive summary with severity-tiered findings (Critical / High / Medium / Low)
- Each finding: current state → business impact → recommended fix → estimated effort
- Prioritized remediation roadmap with timelines
- Screenshots as evidence (Postmaster Tools, blacklist checks)
- 60-minute debrief call

**Pricing:**
| Type | Range |
|---|---|
| Basic / automated check | $200–$750 |
| Standard single-program audit | $1,500–$5,000 |
| Comprehensive enterprise (multi-domain, multi-ESP) | $5,000–$20,000+ |
| Ongoing managed retainer | $1,000–$12,000/month |

---

## 4. Background Leverage Map

### 4A. Asset → Positioning Advantage Table

| Background Asset | Specific Deliverability Positioning Advantage | Premium Tier Unlocked |
|---|---|---|
| **MAcc degree** | Regulatory compliance documentation; audit trail logic; WORM storage requirements (SEC 17a-4: 2yr immediate + 6yr total); no technical specialist has this baseline | Regulated industries (financial services, securities) |
| **US CPA firm experience** | FINRA/SEC context; can speak to CFOs, controllers, compliance officers; credible in US accounting technology | US fintech, accounting SaaS vendors |
| **Bilingual Korean/English** | Only bilingual deliverability specialist in a 1.8%-DMARC-adoption Korean market; can produce Korean-language reports (no commercial tool does this); understands Naver Mail behavior — the one major ISP with zero English documentation | Korean market monopoly position |
| **Functional Chinese** | Pan-East-Asia advisory (China at 4.2% DMARC adoption); Japan, Korea, China have fundamentally different email frequency norms, opt-in standards, ISP behavior | Secondary market expansion |
| **Python/pytest/Postman** | Automated monitoring pipelines; batch DNS validation (`checkdmarc`); DMARC report processing (`parsedmarc`); CI/CD integration; custom alert thresholds; scalable to 30–50 clients vs. 5–10 for manual | Technical differentiation; scalable practice |
| **ISTQB CTFL (in progress)** | Formal QA methodology applied to deliverability: testable acceptance criteria ("95% delivered in 5 min; spam rate <0.1%; DMARC pass rate >99%"); risk-based prioritization; professional audit structure | Credibility with technical organizations; enterprise buyers |
| **Korean tax software ecosystem (전산법인/세무사)** | Understands notification failure consequences in context (missed 가산세 avoidance = legal liability for platform); 17,000+ member 세무사회 notification infrastructure; 부가세 SaaS product context | Korean tax SaaS vertical — entirely unserved |
| **1형당뇨 사협 이사장 (healthcare social cooperative)** | Firsthand PIPA + patient communication experience; founder credibility with Korean health startups; appointment/test result email failure = patient harm | Korean healthcare SaaS vertical |

### 4B. What Python Specifically Enables (vs. Non-Technical Consultants)

| Task | Non-Technical Consultant | Python-Capable Consultant |
|---|---|---|
| DNS validation | Manual, one domain at a time | `checkdmarc` batch validates hundreds; JSON output for client reports |
| DMARC report processing | Manual XML reading | `parsedmarc` full pipeline; aggregate statistics in minutes |
| Blocklist monitoring | Manual MXToolbox checks | API + cron job → instant alert on any of 200+ blocklists |
| Postmaster data | Weekly screenshots | Daily API pull → time-series trend; anomaly detection |
| Email flow testing | Manual send + visual check | pytest + MailSlurp: CI/CD integrated; assertion-based; runs on every deploy |
| Client monitoring scale | 5–10 clients maximum | 30–50 clients with automated threshold alerts |
| Korean-language reports | Not possible for foreign tools | Custom output in Korean — no commercial tool offers this |

**ISTQB framework advantage:** Structures deliverability audits as formal QA projects with defect lifecycle tracking and risk-based prioritization — producing audit reports that enterprise buyers can present internally, not informal advisory memos.

### 4C. The Two Industries with Maximum Asset Stack Overlap

**1. Korean Tax SaaS Platforms**

Email types with specific deliverability failure consequences:

| Email Type | Failure Consequence |
|---|---|
| Filing confirmation | Duplicate filing; penalty risk |
| Deadline reminder | 가산세 (late filing penalty) — legal liability for platform |
| 세금계산서 issuance notification | Missed 매입세액공제 window |
| OTP / Account security | Failed login; security breach |
| 경정청구 result | Missed refund opportunity |
| 세무사 delegation notification | Workflow breakdown |

A 기획자 at 전산법인 who can articulate "if DMARC is misconfigured, members miss regulatory change 공지사항 via Gmail or Naver Mail" is demonstrably differentiated from other candidates who see this as an IT infrastructure problem.

**2. Korean Fintech / Korean B2B SaaS Expanding Internationally**

Korea's deliverability position globally:
- South Korea: **1.8% DMARC adoption** among Global 2000 companies — dead last in APAC
- APAC overall: **78.2% inbox placement rate** — lowest globally (2025)
- A bilingual Korean/English deliverability consultant job posting exists on Salary.com — confirming demand exists but is unfilled

Four compounding problems for Korean B2B SaaS going global:
1. Zero sender reputation on Korean IP ranges with US/EU ISPs
2. Korean character encoding (UTF-8/EUC-KR/MIME headers for Korean subject lines) triggering Western spam filters
3. Naver Mail outbound reputation issues with non-Korean ISPs
4. High-frequency broadcast culture without Western list hygiene practices (ISPs read as spam signals)

**3. Regulated Financial Services (US-facing)**

SEC Rule 17a-4: Broker-dealers must retain all email for 2 years (immediate access) + 6 years total, in WORM non-erasable format.
- JPMorgan fined $4M in 2023 for deleting 47 million messages
- 12 FINRA member firms fined $14.4M combined in 2017

**The combined-assets moat:** A regulated financial firm needs email to (a) reach inboxes AND (b) be archivable and compliant. A pure-technical consultant doesn't understand WORM storage. A pure-compliance consultant doesn't understand SPF/DKIM/DMARC repair. A MAcc-trained QA-capable bilingual consultant covers both — and is the only practitioner in that position.

### 4D. All-Assets-Stack Niches (Uncontested Positioning)

| Niche | Why Uncontested |
|---|---|
| Korean fintech expanding to US | CPA compliance knowledge + Korean bilingual + QA automation + Korean sender reputation expertise — no other consultant has all four |
| Korean tax SaaS platforms (전산법인, 세금계산서 vendors) | Tax ecosystem knowledge + Korean bilingual + QA/API + MAcc — only person who understands product context AND builds monitoring AND advises in Korean AND understands financial-legal significance |
| US accounting/CPA firm technology vendors | CPA firm background makes you credible to the buyer (controllers, CPAs) + QA methodology delivers structured audits they can present internally |
| Korean healthcare SaaS / digital health startups | 사협 founder experience + PIPA knowledge + Korean bilingual + QA/API — no one else in this position |
| Pan-East-Asian B2B SaaS going global | Korean + Chinese bilingual + market knowledge — no Western consultant serves this; no Korean consultant has the technical depth |

---

## 5. Recommended Positioning Statement

### Version 1 — Technical Buyer (English)

> "I help Korean and East Asian B2B companies fix email deliverability failures when entering global markets — a problem that costs companies in inbox placement, customer trust, and regulatory compliance, and that generic technical consultants can't diagnose without understanding your local sending infrastructure. With a background in US CPA-firm financial compliance, QA automation engineering, and direct expertise in the Korean email ecosystem (Naver Mail, Stibee, KISA anti-spam policy), I build programmatic monitoring systems in Python that provide ongoing deliverability visibility — not a one-time audit that goes stale in 90 days."

### Version 2 — Korean Market (한국어)

> "US CPA 자격을 가진 QA 엔지니어로서, 저는 한국 기업이 글로벌 이메일 발송에서 겪는 스팸 처리 문제를 기술적으로 진단하고 자동화된 모니터링 시스템으로 해결합니다. 특히 국세청 연동 플랫폼, 세무사 협회, 핀테크 기업의 거래 메일 발송률 문제에서 국내에 비교 가능한 전문가가 없는 영역을 다룹니다."

### Version 3 — Professional Bio / Positioning Statement (Full)

> "I operate at the intersection of financial compliance, QA engineering, and the Korean B2B email ecosystem — a combination that does not otherwise exist as a consulting specialty. My accounting background (MAcc, US CPA firm experience) allows me to advise regulated-industry clients on the compliance dimensions of email infrastructure that pure-technical specialists miss. My QA/API engineering skills (Python, pytest, Postman, ISTQB CTFL) allow me to build automated deliverability monitoring systems rather than delivering static audits. And my bilingual Korean/English position in Seoul, with direct experience in the Korean tax software ecosystem, means I serve the Korean market — where DMARC adoption is 1.8% and no local specialist class exists — without the language and market-knowledge barriers that exclude all other deliverability consultants."

### Consulting Rate Guidance

Based on research:
- Korea-specialist tier alone: $100–$200/hr
- Regulated-industry specialist alone: $150–$300/hr
- QA automation tier alone: $150–$250/hr
- **Combined assets target: $150–$300/hr** — the only practitioner combining all four positioning factors

---

## 6. Suggested Learning Sequence

Given existing QA/API track (Python, pytest, Postman, ISTQB CTFL in progress):

### Phase 1 — Foundation (Weeks 1–4, alongside existing QA study)

**Goal:** Complete first self-audit and understand all Tier 1 concepts

| Task | Resource |
|---|---|
| Read 스티비 help docs end-to-end | help.stibee.com — SPF, DKIM, DMARC sections |
| Run Gmail + Naver Mail tests via mail-tester.com | mail-tester.com |
| Set up Google Postmaster Tools for a test domain | postmaster.google.com |
| Do MXToolbox blacklist check walkthrough | mxtoolbox.com |
| Read Al Iverson's DELIVTERMS glossary | spamresource.com |
| Read 스티비 2025 이메일 마케팅 리포트 | report.stibee.com |

### Phase 2 — Technical Deepening (Months 2–3)

**Goal:** Tier 2 competency; first Python automation; first pro bono audit

| Task | Resource |
|---|---|
| Install and run `checkdmarc` on 10 domains | pip install checkdmarc |
| Install and run `parsedmarc` on sample DMARC RUA XML | pip install parsedmarc |
| Build a simple blocklist monitoring script (MXToolbox API) | mxtoolbox.com/api |
| Complete a GlockApps inbox placement test with a test send | glockapps.com |
| Do a pro bono audit for one Korean SMB or startup | EmailGeeks Slack or personal network |
| Join EmailGeeks Slack — lurk #deliverability for 30 days | email.geeks.chat |

### Phase 3 — Credibility Building (Months 3–6)

**Goal:** First published Korean-language deliverability content; first paid engagement

| Task | Resource |
|---|---|
| Write and publish first Korean-language deliverability explainer (target: Brunch or 요즘IT) | Choose 1 topic: "Naver Mail 발송률 완전정복" or "DMARC 리포트 읽는 법" |
| Answer 3 questions in EmailGeeks #deliverability accurately | email.geeks.chat |
| Complete first paid audit ($500–$1,500 range, Korean B2B target) | Network via 전산법인 or 세무사 ecosystem |
| Build GitHub repo with Korean-language deliverability automation tools | checkdmarc wrapper, parsedmarc pipeline, blocklist monitor |
| Publish GitHub tools publicly — link from blog post | |

### Phase 4 — Premium Positioning (Month 6+)

**Goal:** Establish Korean-market authority; target $100–$200/hr rate for subsequent engagements

| Task | Resource |
|---|---|
| Submit to Deliverability Summit (Barcelona 2026) speaker application | deliverabilitysummit.com |
| Write case study from Phase 3 audit (anonymized) | Publish on personal blog |
| Evaluate M3AAWG organizational membership | m3aawg.org |
| Target second engagement in Korean fintech or tax SaaS vertical | Use tax ecosystem relationships |

### Integration with Existing Tracks

- **ISTQB CTFL**: directly applicable — formal test design methodology → structured audit scope and acceptance criteria
- **Postman**: directly applicable — email API testing (SendGrid/Mailgun APIs, webhook testing)
- **pytest**: directly applicable — `parsedmarc` pipeline automation, inbox placement assertion testing
- **전산법인 기획자**: this deliverability expertise is a direct differentiator in the interview ("as a 기획자 I would own notification deliverability as a product quality metric, not just an IT concern")

---

## 7. Sources

### Korean Sources
- [SPF, DKIM 설정 이해하기 — 스티비 도움말](https://help.stibee.com/email/managing-sender/spf-dkim)
- [DMARC 설정 이해하기 — 스티비 도움말](https://help.stibee.com/email/managing-sender/dmarc)
- [G메일, 네이버 메일 수신 정책 변경 (1) — 스티비 블로그](https://blog.stibee.com/gmail-sender-guidelines/)
- [G메일, 네이버 메일 수신 정책 변경 (2) — 스티비 블로그](https://blog.stibee.com/gmail-sender-guidelines-2/)
- [스티비 실험실 도메인 상태 조회](https://lab.stibee.com/)
- [스티비 2025 이메일 마케팅 리포트](https://report.stibee.com/)
- [이메일 보안 DKIM, SPF, DMARC — Velog (개발자 블로그)](https://velog.io/@totw5701/%EC%9D%B4%EB%A9%94%EC%9D%BC-%EB%B3%B4%EC%95%88-DKIM-SPF-DMARC)
- [SPF/DKIM/DMARC 스팸 신뢰도 개선 — petsonthego](https://petsonthego.com/%EC%8A%A4%ED%8C%B8-%EC%8B%A0%EB%A2%B0%EB%8F%84-%EC%A7%80%EC%88%98-%EA%B0%9C%EC%84%A0/)
- [이메일 전달성이란? — Poptin KO](https://www.poptin.com/blog/ko/what-is-email-deliverability-tips-and-best-practices/)
- [메일 발송실패 NDR — 다우오피스](https://care.daouoffice.co.kr/hc/ko/articles/38030317161113)
- [이메일 전달 가능성 — OneSignal KO](https://documentation.onesignal.com/docs/ko/email-deliverability)
- [내 메일 블랙리스트 올라가지 않는 8가지 방법 — ITWorld Korea](http://www.itworld.co.kr/print/50638)
- [메일 스팸 해결 — HiSEON](https://hiseon.me/server/how-to-solve-spam-mail-problem/)
- [MXToolbox 블랙리스트 모니터링 — thundermail.co.kr](https://blog.thundermail.co.kr/133)
- [MXToolbox MX 레코드 진단 — IDCHOWTO](https://idchowto.com/mxtoolbox-mx-record-blacklist-check/)
- [스팸함에서 벗어나기 위해서 — OpenAds](https://www.openads.co.kr/content/contentDetail?contsId=6869)
- [이메일 마케팅? 초보도 전문가처럼 — OpenAds](http://openads.co.kr/content/contentDetail?contsId=4231)
- [이메일 쫌 아는 마케터 — Google Books KO](https://books.google.com/books/about/%EC%9D%B4%EB%A9%94%EC%9D%BC_%EC%AB%8C_%EC%95%84%EB%8A%94_%EB%A7%88%EC%BC%80%ED%84%B0.html?id=FwXN0AEACAAJ)
- [DMARC 설정 — Microsoft Learn KO](https://learn.microsoft.com/ko-kr/defender-office-365/email-authentication-dmarc-configure)
- [크리니티 스팸 차단 제품](https://www.crinity.com/main/product/product_spam.html)
- [이메일 마케팅 툴 시장 보고서 — GII Korea](https://www.giikorea.co.kr/report/go1733512-email-deliverability-tools.html)
- [잡코리아 — CRM 마케터 채용](https://www.jobkorea.co.kr/Search/?stext=CRM+%EB%A7%88%EC%BC%80%ED%84%B0)
- [그룹바이 — 2025 마케터 연봉 분석](https://groupby.careers/%EC%A7%81%EB%AC%B4%EB%B3%84-%EC%84%B8%EB%B6%80-%EC%97%B0%EB%B4%89-%EB%B6%84%EC%84%9D-2%ED%83%84-2025-%EB%A7%88%EC%BC%80%ED%84%B0-%EC%98%81%EC%97%85-%EC%84%B8%EC%9D%BC%EC%A6%88-%EC%97%B0%EB%B4%89/)
- [아이보스 — 마케터 연봉 2025](https://www.i-boss.co.kr/ab-6141-67729)
- [잡플래닛 — 연차별 마케터 평균 연봉](https://www.jobplanet.co.kr/contents/news-7805)
- [이메일 마케팅 KPI — CLVS](https://www.clvs.co.kr/post/email-marketing-kpi-email-deliverability)
- [SPF, DKIM이 뭔가요? — Medium KO](https://medium.com/@ionniu/spf-dkim%EC%9D%B4-%EB%AD%94%EA%B0%80%EC%9A%94-from-%EC%8A%A4%ED%8B%B0%EB%B9%84-ed31c5852040)
- [2025년 B2C 이메일 마케팅 완벽 가이드 — 마켓핏랩](https://www.mfitlab.com/solutions/blog/moengage-email-marketing)

### English Sources — Market and Pricing
- [Glassdoor — Email Deliverability Consultant Salary](https://www.glassdoor.com/Salaries/email-deliverability-consultant-salary-SRCH_KO0,31.htm)
- [ZipRecruiter — Email Deliverability Specialist Salary](https://www.ziprecruiter.com/Salaries/Email-Deliverability-Specialist-Salary)
- [Upwork — Email Deliverability Freelancers](https://www.upwork.com/hire/email-deliverability-consulting-freelancers/)
- [Email Vendor Selection — Pricing Guide](https://www.emailvendorselection.com/email-marketing-cost-pricing-guide/)
- [Suped.com — Deliverability Job Titles](https://www.suped.com/knowledge/email-deliverability/basics/what-are-some-appropriate-job-titles-for-someone-who-specializes-in-email-deliverability)
- [emaillistvalidation.com — Deliverability Specialist Guide](https://emaillistvalidation.com/blog/email-deliverability-specialist-job-a-comprehensive-guide-to-the-role-and-responsibilities/)
- [Railsware — Email Deliverability Specialist Job](https://railsware.com/careers/email-deliverability-specialist/)
- [Heroify — Email Deliverability Specialist Job Description](https://heroify.co/job-descriptions/email-deliverability-specialist-job-description/)
- [Warmy.io — Role, Courses & Certificates](https://www.warmy.io/blog/email-deliverability-manager-role-courses-certificates-jobs/)
- [Attentive — Messaging Strategy & Operations Analyst (Built In NYC)](https://www.builtinnyc.com/job/messaging-strategy-operations-analyst-deliverability/6313488)

### English Sources — Practitioner / Expert Community
- [Word to the Wise — Laura Atkins](https://www.wordtothewise.com/)
- [Spam Resource — Al Iverson](https://www.spamresource.com/)
- [EmailGeeks Community](https://email.geeks.chat/)
- [M3AAWG](https://www.m3aawg.org/)
- [Deliverability Summit](https://deliverabilitysummit.com/)
- [Matthew Vernhout — Email Industries](https://www.emailindustries.com/email-industries-matthew-vernhout/)
- [Matthew Vernhout — PR Newswire Profile](https://www.prnewswire.com/news-releases/matthew-vernhout-industry-leading-expert-on-deliverability-privacy-and-compliance-joins-netcore-as-vp--deliverability-north-america-301111200.html)
- [Laura Atkins — Deliverability Summit Speaker](https://deliverabilitysummit.com/speaker/laura-atkins/)

### English Sources — Tools and Technical
- [Validity Sender Certification](https://www.validity.com/sender-certification/)
- [Certified Senders Alliance (CSA)](https://certified-senders.org/certification-process/)
- [GlockApps](https://glockapps.com/)
- [MXToolbox](https://mxtoolbox.com/)
- [Google Postmaster Tools](https://postmaster.google.com)
- [Microsoft SNDS](https://sendersupport.olc.protection.outlook.com/snds/)
- [Spamhaus Check](https://check.spamhaus.org/)
- [dmarcian](https://dmarcian.com)

### English Sources — Audit Methodology
- [Email Deliverability Audit — Saleshandy](https://www.saleshandy.com/blog/email-deliverability-audit/)
- [Email Deliverability Audit — Mailgun](https://www.mailgun.com/blog/email/email-deliverability-audit/)
- [Email Deliverability Audit — Litmus](https://www.litmus.com/blog/email-deliverability-audit)
- [Email Deliverability Audit — Bouncer](https://www.usebouncer.com/email-deliverability-audit/)
- [16-step Audit — Sparkle.io](https://sparkle.io/blog/email-deliverability-audit/)
- [InboxArmy Audit Service](https://www.inboxarmy.com/email-deliverability-audit/)
- [Email Industries Audit](https://www.emailindustries.com/email-deliverability-audit/)
- [MailSoar Audit](https://www.mailsoar.com/services-solutions/infrastructure-audit/)

### English Sources — Industry Data and Background Leverage
- [MailReach — Deliverability Statistics 2025](https://www.mailreach.co/blog/email-deliverability-statistics)
- [GlobeNewsWire — $1.9B Email Deliverability Tools Market](https://www.globenewswire.com/news-release/2026/01/06/3213911/0/en/Trends-Strategies-Shaping-the-1-9-Billion-Email-Deliverability-Tools-Market-2026-Beyond.html)
- [DMARC Report — Hidden Costs for SaaS](https://dmarcreport.com/blog/the-hidden-costs-of-poor-email-deliverability-for-saas-businesses/)
- [Intradyn — FINRA/SEC 17a-4 Compliance](https://www.intradyn.com/guidelines-for-finra-sec-17a-4-email-compliance/)
- [Finance Monthly — Fintech Transactional Email](https://www.finance-monthly.com/building-trust-in-fintech-best-practices-for-transactional-email-sending/)
- [Stripo — Email Marketing in East Asia](https://stripo.email/blog/email-marketing-in-east-asia-how-to-adapt-strategies-to-the-market-realities-of-japan-south-korea-and-china/)
- [Salary.com — Bilingual Korean/English Deliverability Consultant posting](https://www.salary.com/job/easyrecrue/deliverability-consultant-bilingual-korean-and-english/852b1078-5dc4-4af4-bcb3-e534611c0ea8)
- [Warmforge — Blacklisted IPs Impact](https://www.warmforge.ai/blog/blacklisted-ips-impact-email-deliverability)
- [Mailpool — Hidden Costs for Agencies](https://www.mailpool.ai/blog/the-hidden-costs-of-poor-email-deliverability-for-agencies)
- [SmartLead — Email Spam Traps](https://www.smartlead.ai/blog/email-spam-traps)
- [MailerSend — Email for Banks/Fintech](https://www.mailersend.com/solutions/email-banks-financial-services)
- [HIPAA Journal — Email Compliance](https://www.hipaajournal.com/hipaa-compliance-for-email/)
