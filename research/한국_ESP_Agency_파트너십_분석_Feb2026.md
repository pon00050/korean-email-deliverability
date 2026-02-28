# 한국 ESP·디지털 에이전시 파트너십 분석
## Email Deliverability Consulting — Partner & Client Assessment

**Date:** 2026-02-28
**Purpose:** Assess Korean ESPs and digital agencies as partners or clients for a deliverability consulting practice
**Research scope:** ESP partner programs, agency gap analysis, global commercial benchmarks, revenue model design

---

## Table of Contents

1. [Korean ESP Landscape — Overview](#1-korean-esp-landscape--overview)
2. [ESP Partner Program Assessment](#2-esp-partner-program-assessment)
3. [ESP Escalation Paths — What Happens When Deliverability Breaks?](#3-esp-escalation-paths--what-happens-when-deliverability-breaks)
4. [Korean Digital Agency Gap Analysis](#4-korean-digital-agency-gap-analysis)
5. [Global Commercial Structures — Benchmarks](#5-global-commercial-structures--benchmarks)
6. [Revenue Model Design — Korean ESP Partnerships](#6-revenue-model-design--korean-esp-partnerships)
7. [Named Contact Research — Approachability](#7-named-contact-research--approachability)
8. [Strategic Sequencing](#8-strategic-sequencing)

---

## 1. Korean ESP Landscape — Overview

| ESP | Type | Primary Market | Estimated Scale | Deliverability Depth |
|---|---|---|---|---|
| **스티비 (Stibee)** | Newsletter / marketing email SaaS | SMB, media, startups, B2C | ₩3.5B ARR (2025); 14 employees; 5yr profitable | Basic (SPF/DKIM/DMARC setup guide; KISA 화이트리스트 등록) |
| **타손 (TasOn / 타스온)** | Bulk email + SMS + big-data targeting | Mid-market, performance marketers | Private; bulk/transactional focus | Very basic (FAQ-level support; 02-552-3874 support line) |
| **NHN Cloud Mail** | Cloud email API (transactional + marketing) | Enterprise, dev teams | 230+ partners in NHN Cloud ecosystem | Infrastructure-focused; deliverability advisory absent |
| **Naver Cloud (Cloud Outbound Mailer)** | Cloud bulk/transactional email API | Enterprise, government | Naver ecosystem; government cloud available | No deliverability advisory layer evident |
| **비즈메일러 (Bizmailer)** | Bulk email; KOSPI-listed parent | Mid-to-large enterprise | Listed company; legacy player | KISA-registered IPs; no advisory services |

**Key structural finding:** All five Korean ESPs are "sending infrastructure" providers. None have a deliverability advisory, consulting, or monitoring layer. Support escalation is handled by phone/FAQ with no named deliverability expert.

---

## 2. ESP Partner Program Assessment

### 2.1 스티비 (Stibee)

| Dimension | Finding |
|---|---|
| **Formal partner program** | None publicly documented. No agency/reseller page on stibee.com as of Feb 2026 |
| **Agency pricing** | No published agency discount or volume tier for agencies managing multiple accounts |
| **Multi-account management** | No evidence of an agency dashboard or sub-account structure (unlike Mailchimp & Co) |
| **Current deliverability support** | KISA 화이트도메인 등록 complete for all Stibee sending IPs; SPF/DKIM/DMARC setup guides in help docs; escalation = 1:1 chat or email to support team |
| **Revenue** | ₩3.5B ARR (2025); seed-only funded (Sopoong Ventures, 2020); bootstrapped growth; 5 consecutive profitable years |
| **Pricing tiers** | Free → Standard (₩8,900/mo) → Pro (₩29,000/mo) → Enterprise (₩57,000/mo); subscriber-based |
| **Partnership contact** | No dedicated partnerships page; support+sponsorship@stibee.com for sponsorship inquiries; recruit@stibee.com for team queries |
| **Assessment** | Stibee is small (14 employees), profitable, and self-sufficient. No partner program exists — meaning the **first-mover opportunity** is to propose one. Stibee customers who encounter inbox placement problems have no escalation path beyond Stibee's generalist support team. |

### 2.2 타손 / 타스온 (TasOn)

| Dimension | Finding |
|---|---|
| **Formal partner program** | Not publicly documented; website (tason.com / mkt.tason.com) shows no partner/reseller section |
| **Agency pricing** | No evidence; pricing appears volume-based (CPM/CPC for big-data targeting; per-send for email) |
| **Deliverability support** | FAQ-only; customer support line (02-552-3874); basic DMARC guidance mentioned |
| **Product profile** | Postman (email bulk-send), PushPia (push), TAS TAG (big-data DMP + targeting); marketing automation angle |
| **Deliverability advisory** | None. A customer with inbox placement problems receives FAQ-level guidance only |
| **Assessment** | Larger scale than Stibee for bulk/transactional. Deliverability expertise gap is equally large. Less brand-forward — partnership approach would be more B2B/technical than with Stibee. |

### 2.3 NHN Cloud Email

| Dimension | Finding |
|---|---|
| **Formal partner program** | Yes — NHN Cloud has a documented partner program (nhncloud.com/kr/partner). ~230 partner companies. Tiers include reseller, MSP, and technology partners |
| **Email-specific partner program** | Not specifically for email; email (Cloud Email) is one product among many cloud services |
| **Notable NHN Cloud MSP partners** | Samsung SDS, LG CNS, Megazone Cloud, Didim365, Nuricloud — all infrastructure/cloud MSPs |
| **Deliverability support** | None beyond API documentation (docs.nhncloud.com); no deliverability advisory |
| **Entry path** | NHN Cloud's email product is API-first; customers are typically developers/DevOps, not marketers. Partnership approach would be as a **technology partner** or **managed service layer** on top of their email API |
| **Assessment** | NHN Cloud has a real partner program but it is cloud-infrastructure-oriented. An email deliverability specialist who helps NHN Cloud email API customers configure authentication, monitor reputation, and warm IPs would fill a genuine gap — but the buyer (DevOps engineer) is not the same as Stibee's buyer (marketer). |

### 2.4 Naver Cloud (Cloud Outbound Mailer)

| Dimension | Finding |
|---|---|
| **Partner program** | Yes — ncloud.com/partner (general cloud partner program) |
| **Email-specific program** | No dedicated email partner tier |
| **Deliverability support** | Docs-only; SENS (notification service) and Cloud Outbound Mailer are API products with no advisory layer |
| **Strategic value** | Naver Mail is the primary Korean inbox provider; Naver Cloud runs sending infrastructure. This creates a **dual relationship opportunity**: Naver Cloud as ESP partner AND Naver Mail team as inbox-provider partner (the inbox-panel data gap identified in existing research) |
| **Assessment** | Same structural gap as NHN Cloud. The Naver Cloud email product customer is a developer. Partnership value is highest if you can document Naver Mail filtering behavior and offer that as a premium consulting service to Naver Cloud customers. |

---

## 3. ESP Escalation Paths — What Happens When Deliverability Breaks?

This is the core market validation question. What actually happens when a Korean ESP customer has a deliverability problem the ESP cannot solve?

### Current Escalation Flow (All Korean ESPs)

```
Customer notices low open rate / bounce rate spike / spam folder complaints
  ↓
Contacts ESP support (chat / phone / email)
  ↓
ESP support checks: account status, bounce rate, unsubscribe rate
  ↓
ESP gives generic advice: "clean your list," "check your content," "set up DMARC"
  ↓
Customer implements basic fixes; problem may or may not resolve
  ↓
IF UNRESOLVED → Customer either (a) switches ESP, (b) reduces send volume, or (c) gives up on email
```

**What does NOT happen in Korea:**
- Referral to a third-party deliverability specialist
- IP reputation analysis using Validity/Everest (which has no Naver/Kakao seed accounts)
- Naver Mail postmaster contact or whitelist application
- KISA 화이트도메인 registration assistance (self-serve only; no managed service exists)
- Inbox placement testing specific to Korean mailboxes

### Gap Summary

| Problem Type | ESP Support Capability | Specialist Needed? |
|---|---|---|
| SPF/DKIM/DMARC misconfiguration | Basic guidance available | No (DIY possible) |
| IP warming strategy | No expertise | Yes |
| Naver Mail spam folder mystery | No relationship with Naver Mail team | Yes — unique value |
| KISA 화이트도메인 registration | Stibee IPs are registered; customer domain is not | Yes — managed service gap |
| List hygiene / engagement segmentation | Generic advice only | Yes for complex cases |
| Reputation recovery after blacklist | No expertise | Yes |
| Bulk-sender authentication (Google Feb 2024 requirements) | Basic docs | Yes for large senders |

---

## 4. Korean Digital Agency Gap Analysis

### 4.1 Major Korean Digital Marketing Agencies — Email Deliverability Offering

| Agency | Type | Email Marketing Services | Deliverability Offering |
|---|---|---|---|
| **나스미디어 (KT Nasmedia)** | Media buying; DSP/SSP; KT subsidiary | No email marketing listed; focus is display/video/adtech | None confirmed |
| **이노레드 (Innored)** | Creative/campaign agency; international awards | Campaign concept and execution | None confirmed |
| **펜타브리드 (Pentavid)** | Mid-size digital agency | Multi-channel digital marketing | None confirmed |
| **AB180** | MarTech consultancy; Braze Korea distributor; Amplitude partner | Braze onboarding, CRM automation, multi-channel campaign setup | No dedicated deliverability; Braze's own premium deliverability service is sold separately by Braze (not by AB180) |
| **모리엔티드** | Growth marketing; CRM marketing | CRM 마케팅 + 프로모션 | None found |

**Finding:** Zero Korean digital marketing agencies publicly offer email deliverability consulting as a named service. This is confirmed by:
1. No Korean job posting contains "deliverability" as a standalone skill requirement
2. No agency website lists "이메일 발송률 컨설팅" or "도달률 최적화" as a service
3. The largest Korean CRM consultancy (AB180) relies on Braze's own premium deliverability team for inbox issues — it does not offer this itself

### 4.2 What AB180's Braze Relationship Reveals

Braze explicitly sells **Premium Deliverability Services** (separate paid add-on):
- Named Braze deliverability expert; 3 check-ins/week during onboarding, 2/month ongoing
- Custom IP warming plan
- Whitelabel IP configuration
- This service is sold **by Braze directly**, not through Braze agency partners like AB180

**Implication:** AB180 closes Braze deals but outsources deliverability expertise back to Braze. When a Braze customer in Korea has a deliverability problem beyond AB180's scope, AB180 either escalates to Braze's US team (English-language; timezone gap; no Naver/Kakao knowledge) or has no answer. A Korean bilingual deliverability specialist who understands Braze architecture AND Naver Mail filtering is a gap AB180 would pay to fill — either as a subcontractor or referral partner.

---

## 5. Global Commercial Structures — Benchmarks

### 5.1 ESP Agency Partner Programs — Global Models

| ESP | Program Name | Commission Type | Rate | Notes |
|---|---|---|---|---|
| **Mailchimp** | Mailchimp & Co | Referral + managed revenue | 25% new customer; 5% managed MRR | Quarterly payout; requires 2+ connected accounts; no minimum |
| **Klaviyo** | Klaviyo Partner Program | Recurring referral | 20% recurring (standard); negotiable at volume | 30-day cookie; agency partner tiers (Silver/Gold/Master) |
| **Braze** | Braze Partner Program | Agency implementation fee | Project-based (implementation fees, not recurring SaaS %) | Deliverability Premium Service sold separately by Braze at $X/mo |
| **SendGrid** | Expert Services | Consulting retainer | $150–300/hr; one-time audit packages | Braze-style model — deliverability expertise is a paid premium, not bundled |
| **Campaign Monitor** | Agency Program | Revenue share | 20–30% on referred accounts | Sub-account management dashboard for agencies |

### 5.2 Deliverability Consultant Business Models — Global Benchmarks

| Model | Description | Price Range | Applicability to Korea |
|---|---|---|---|
| **One-time audit** | DNS check, reputation score, content analysis, actionable report | $500–$2,500 | High — no Korean alternative exists |
| **Retainer / monitoring** | Ongoing inbox placement monitoring, blacklist alerts, monthly report | $500–$3,000/mo | High — no Korean tool monitors Naver/Kakao inbox |
| **ESP referral fee** | Consultant recommends ESP; receives % of referred customer MRR | 15–25% | Feasible once Stibee/TasOn establish program |
| **White-label** | Agency resells your deliverability service under their brand | Custom | Very feasible — AB180, Braze partners would buy |
| **ISP relationship brokerage** | Facilitate whitelisting, complaint feedback loop setup | Project fee | High value — KISA 화이트도메인 managed-service gap |
| **Training / workshop** | ESP customer education; agency staff training | ₩500K–₩2M/session | Low barrier to entry; credibility building |

### 5.3 The EmailIndustries Model (US Reference)

EmailIndustries (emailindustries.com) is a specialist deliverability agency that does not offer creative or campaign services. Key structural elements applicable to Korea:

- **Core differentiation from ESP support:** Depth vs. breadth. ESP support handles platform UX, billing, automation setup. Deliverability agencies handle reputation scoring, ISP relationships, authentication troubleshooting, and complex recovery — skills that require cross-ESP, cross-mailbox expertise.
- **Service packages:** Audits, ongoing monitoring packages, infrastructure consulting — all productized with fixed pricing
- **Revenue:** Recurring > project; clients who solve a deliverability crisis stay as monitoring clients

---

## 6. Revenue Model Design — Korean ESP Partnerships

### 6.1 Proposed Stibee Partnership — Referral Model

Stibee has no partner program. You would be proposing its creation, specific to deliverability.

**Proposed Structure:**

| Element | Proposed Terms |
|---|---|
| **Your value to Stibee** | You handle escalated deliverability cases Stibee's 14-person team cannot. You prevent churn from customers who would leave due to inbox problems. You make Stibee's product stickier. |
| **Your value to Stibee customers** | Stibee refers customers to you when they have inbox placement problems. Customer pays you directly for an audit or retainer. |
| **Referral direction 1** | Stibee → you: Stibee refers a struggling customer. You provide service. You pay Stibee a referral acknowledgment (optional; or Stibee simply benefits from reduced churn). |
| **Referral direction 2** | You → Stibee: You advise a company to use Stibee as their ESP. Stibee pays you 15–20% of first-year subscription as referral commission. |
| **Partnership framing** | "공식 이메일 발송률 파트너 (Official Deliverability Partner)" — Stibee lists you in their help center as the recommended specialist for advanced inbox issues |
| **Revenue estimate (Year 1)** | 3–5 referred clients from Stibee × ₩500K–₩1.5M audit = ₩1.5M–₩7.5M from audits; plus ongoing retainers if they continue monitoring |

**Why Stibee is the right first call:**
- Small team (14 people) — decisions move fast; no corporate procurement process
- CEO (임호열, Im Hoyeol) is reachable on LinkedIn
- Profitable, so they are not under pressure to cut costs — but also small enough that adding a deliverability partner costs them nothing and benefits their product reputation
- Their customer base (media companies, startups, SMBs) is exactly the buyer who would pay ₩300K–₩1M for an audit

### 6.2 Proposed TasOn Partnership — Technical Referral

TasOn's customer profile is different from Stibee's: larger B2C senders, performance marketers, bulk email. Deliverability problems at TasOn tend to be:
- High bounce rates from dirty lists
- IP reputation degradation from high-volume sends
- Naver Mail filtering affecting campaign ROI

**Proposed Structure:**

| Element | Proposed Terms |
|---|---|
| **Entry point** | Contact TasOn's business development or enterprise sales team; position as a technical partner who helps their large customers optimize sends |
| **Value proposition** | "Your customers lose revenue when emails go to spam. I diagnose and fix that. You retain the customer; I bill them separately." |
| **Commercial model** | Subcontractor arrangement: TasOn refers, you deliver, customer pays you; TasOn benefits from retention |
| **Alternative** | White-label: TasOn packages your audit as a premium "발송률 최적화 서비스" and marks up |
| **Revenue estimate** | TasOn customer spend is higher (bulk senders); audit pricing ₩1M–₩3M; retainer ₩500K–₩2M/mo |

### 6.3 Proposed NHN Cloud / Naver Cloud — Technology Partner

These are API-first cloud products. The partnership model is different:
- Register as a **technology partner** in their partner programs
- Offer a complementary managed service: "Email Authentication & Deliverability Layer for NHN Cloud Email API customers"
- Target their enterprise customers (companies using NHN Cloud email API at scale)

**Revenue model:** Project-based consulting; retainer for monitoring. Not a referral-fee model — the ESP cannot easily track which customers you influenced.

### 6.4 Proposed AB180 / Braze Korea — Subcontractor Model

AB180 cannot solve Braze email deliverability problems that require Naver Mail expertise. You can:

| Structure | Description |
|---|---|
| **Subcontractor** | AB180 identifies a Braze customer with Korean inbox placement problems; subcontracts to you; you bill AB180 a wholesale rate; AB180 marks up and bills client |
| **White-label** | You operate as "AB180 Email Deliverability Specialist" on the project; client-facing under AB180's brand |
| **Referral** | AB180 simply refers the client directly to you; you pay AB180 a 10–15% referral fee |

**Revenue estimate:** Braze customers are enterprise; project fees ₩3M–₩10M per engagement.

---

## 7. Named Contact Research — Approachability

### 7.1 Stibee

| Person | Role | Contact |
|---|---|---|
| **임호열 (Im Hoyeol)** | CEO / Co-founder | LinkedIn: linkedin.com/in/imhoyeol/ — reachable; active profile |
| **임의균 (Im Uigyun)** | Co-founder / Representative | Listed as co-representative in corporate filings |
| **Support / general** | — | support+sponsorship@stibee.com (sponsorship/partnership inquiries) |
| **Team page** | — | team.stibee.com |

**Recommended approach:** LinkedIn DM to 임호열, framing as a deliverability specialist who wants to help Stibee customers succeed. Reference a specific, observable deliverability problem (e.g., "I've noticed Stibee customers in Naver Mail are seeing X pattern — I'd like to explore whether a formal partnership makes sense").

**Do NOT cold-email support.** CEO-direct is appropriate given company size (14 people, flat structure).

### 7.2 TasOn (타스온)

| Contact Method | Details |
|---|---|
| **Phone** | 02-552-3874 (customer support / business) |
| **Website** | tason.com / mkt.tason.com |
| **Entry point** | Request an enterprise/partnership conversation through the general business inquiry form; no named BD contact is publicly listed |

**Recommended approach:** Call or email asking for a 기업 파트너십 담당자 (business partnership contact). Frame as: "저는 이메일 발송률 전문 컨설턴트입니다. 타손 고객사 중 수신률 문제를 겪는 기업을 위해 협업 가능성을 논의하고 싶습니다."

### 7.3 NHN Cloud

| Contact Method | Details |
|---|---|
| **Partner program page** | nhncloud.com/kr/partner |
| **Partner registration** | Formal online application process; requires company registration |
| **Entry point** | Apply as a technology/consulting partner; specify email deliverability as the specialization |

### 7.4 AB180

| Contact Method | Details |
|---|---|
| **LinkedIn** | linkedin.com/company/ab180 — team is publicly listed |
| **Entry point** | Identify the Braze practice lead or Head of Customer Success at AB180; LinkedIn DM |
| **Framing** | "I specialize in Korean inbox placement — specifically Naver Mail and Kakao filtering behavior. When your Braze clients have deliverability issues in Korean inboxes, I can help. Open to a subcontractor or referral arrangement." |

---

## 8. Strategic Sequencing

### Recommended Partnership Priority Order

| Priority | Target | Rationale | Timeline |
|---|---|---|---|
| **1** | Stibee (스티비) | Fastest decision cycle (14 people); most marketer-friendly customer base; CEO reachable; no competing partner exists | Contact Q2 2026; informal first |
| **2** | AB180 | Enterprise budget; Braze deliverability gap is documented and proven globally; subcontractor path is established practice | Contact after you have 1 reference case |
| **3** | TasOn | Larger sender base; bulk deliverability problems; less brand-forward | Q3 2026 |
| **4** | NHN Cloud | Formal partner program exists; longer sales cycle; API-buyer profile | Q3–Q4 2026 |
| **5** | Naver Cloud | Highest strategic value (inbox provider relationship); hardest to access; requires credibility first | 2027+ |

### Pre-Partnership Prerequisites

Before approaching any ESP or agency as a partner, you need:

1. **A public reference asset** — at least one Korean-language article or case study demonstrating Naver Mail filtering behavior or KISA 화이트도메인 process; this is your credibility proof
2. **A productized audit offering** — a fixed-scope, fixed-price deliverability audit (e.g., ₩490,000 for a 3-day audit covering DNS, reputation, inbox placement test, KISA status) that an ESP can recommend without hesitation
3. **One paying client** — even if small; proof that the market buys this

### Revenue Model Summary

| Model | When | Annual Revenue Potential (conservative) |
|---|---|---|
| Deliverability audits (direct) | Phase 1 | ₩5M–₩15M (10–30 audits × ₩490K–₩500K) |
| Stibee referral partnership | Phase 1–2 | ₩2M–₩6M (referral commissions + referred clients) |
| AB180 subcontractor | Phase 2 | ₩5M–₩20M (2–5 enterprise projects) |
| TasOn white-label | Phase 2–3 | ₩3M–₩12M (retainers) |
| Total (Phase 1 target) | Year 1 | **₩10M–₩30M** (part-time; compatible with full-time employment) |

---

## Sources

- [Stibee pricing and help documentation](https://help.stibee.com/pricing/understanding/type)
- [Stibee CEO LinkedIn — 임호열 Im Hoyeol](https://www.linkedin.com/in/imhoyeol/)
- [Stibee company profile — THE VC](https://thevc.kr/stibee)
- [Stibee 5-consecutive-year profitability analysis — 아이보스](https://www.i-boss.co.kr/ab-6141-67386)
- [NHN Cloud partner program](https://www.nhncloud.com/kr/partner?lang=ko)
- [Naver Cloud partner program](https://ncloud.com/partner)
- [TasOn email platform](https://mkt.tason.com/report/new_report/report_email_info.jsp)
- [Mailchimp & Co — commission structure](https://mailchimp.com/help/earn-commission/)
- [Mailchimp & Co — partner benefits](https://mailchimp.com/andco/benefits/)
- [Klaviyo partner program — become a partner](https://www.klaviyo.com/partners/become-a-partner)
- [Braze email deliverability premium services](https://www.braze.com/resources/articles/email-deliverability)
- [Braze deliverability services documentation](https://www.braze.com/docs/user_guide/message_building_by_channel/email/best_practices/email_services)
- [AB180 Braze solutions Korea](https://www.ab180.co/solutions/braze)
- [EmailIndustries — deliverability agencies vs ESP support](https://www.emailindustries.com/random/how-do-deliverability-agencies-differ-from-esp-support-teams/)
- [White-label email marketing for agencies — InboxArmy](https://www.inboxarmy.com/agencies/)
- [How switching ESPs impacts deliverability — SmartrMail](http://docs.smartrmail.com/en/articles/1481148-how-switching-esps-impacts-your-deliverability)
- [Return Path / Validity certification and whitelist model](https://www.validity.com/everest/returnpath/)
