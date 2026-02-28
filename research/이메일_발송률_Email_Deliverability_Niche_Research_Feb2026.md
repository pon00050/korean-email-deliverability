# Email Deliverability — Niche Career & Side Income Research
## February 2026

**Research trigger:** Reddit post (r/learnprogramming) — "I fix email deliverability issues regularly and most web developers have no idea how email authentication actually works"

**Research status:** Initial scan complete. Deeper research deferred.

---

## Table of Contents

1. [Is It Legit?](#1-is-it-legit)
2. [The Global Market — Not Low-Balling Yourself](#2-the-global-market--not-low-balling-yourself)
3. [The Korea Opportunity](#3-the-korea-opportunity-a-near-uncontested-market)
4. [Skill Overlap with QA/API Track](#4-skill-overlap-with-your-qaapi-track)
5. [How It Fits Existing Career Tracks](#5-how-it-fits-existing-career-tracks)
6. [Certifications & Communities](#6-certifications--communities)
7. [Verdict & Next Steps](#7-verdict--next-steps)
8. [Raw Research: Career Demand](#8-raw-research-career-demand)
9. [Raw Research: Skill Overlap Detail](#9-raw-research-skill-overlap-detail)
10. [Raw Research: Korea Market](#10-raw-research-korea-market)

---

## 1. Is It Legit?

**Yes, unambiguously.** This became mandatory infrastructure in 2024–2025 — not a trend.

- Google/Yahoo enforced SPF/DKIM/DMARC for bulk senders in **Feb 2024**. Microsoft followed **May 2025**. All three now enforce it.
- **16.9% of legitimate marketing emails globally never reach inboxes.** Microsoft/Outlook alone: 75.6% inbox placement rate with 14% going directly to spam.
- Global deliverability market: **$1.14B (2024) → $2.38B by 2033** at 8.47% CAGR.
- Every company that sends email at any real volume has this problem. It is not niche — it is universal.

---

## 2. The Global Market — Not Low-Balling Yourself

The market is deeply bifurcated. The commodity tier is flooded; the expert tier is undersupplied.

| Tier | What they do | Who does it | Rate |
|---|---|---|---|
| **Commodity** | Set up SPF/DKIM/DMARC records, basic warmup | Fiverr/Upwork workers globally | $15–$50/hr; $25–$170 fixed |
| **Mid-market** | Deliverability audits, ESP migration, bounce management | Freelance generalists with track record | $50–$100/hr |
| **Expert** | Blocklist removal, ISP postmaster relations, sender reputation repair, multi-domain architecture, DMARC report interpretation at scale | ~50 named practitioners globally | $150–$300/hr |

**The commodity tier is where you'd compete with low-cost Upwork workers. That is not where to play.**

What AI is automating (commodity end):
- Basic SPF/DKIM/DMARC record generation and validation
- Spam score testing (now built into most ESPs)
- Email warmup (Warmy, Mailreach, Lemwarm automate this)
- Bounce/complaint rate monitoring and alerting

What AI is NOT replacing:
- ISP postmaster relationship management
- Blocklist removal negotiations (Spamhaus, Barracuda, Microsoft SNDS)
- Sender reputation strategy across domain/IP architecture
- Diagnosing systemic deliverability failures (list hygiene collapse, engagement signal problems)
- Enterprise infrastructure design for high-volume senders

**AI is commoditizing the entry-level work and raising the floor for expert work. The niche is growing, not shrinking.**

### Demand Numbers

- **438** open email deliverability consultant jobs on Upwork (Jan 2026)
- **20,555** email deliverability-related jobs on ZipRecruiter
- In-house salary: $64K/yr (entry, ZipRecruiter) → $117K/yr (consultant-level, Glassdoor)
- Senior freelance: $150–$300/hr

---

## 3. The Korea Opportunity: A Near-Uncontested Market

This is the most striking finding. Korean businesses are among the worst-prepared globally, and no Korean specialist class exists to serve them.

### DMARC Adoption: South Korea vs. APAC

| Country | DMARC Adoption (Global 2000) |
|---|---|
| Australia | 71% |
| India | 50% |
| Singapore | 46.2% |
| Thailand | 17.6% |
| Japan | 7.4% |
| China | 4.2% |
| **South Korea** | **1.8% — dead last in APAC** |

Source: Proofpoint data via CybersecAsia / Red Sift Global DMARC Adoption Guide.

Over half of Korean public companies lack any DMARC record. Only 10.1% have implemented `p=reject`.

### Why It's Urgent Now

Gmail + Naver Mail = **70–80% of all Korean email recipients**. Both now enforce authentication:

| Provider | SPF Required | DKIM Required | DMARC Required | Enforcement |
|---|---|---|---|---|
| Gmail | Yes (bulk) | Yes (bulk) | p=none minimum (bulk) | High; escalating |
| Naver Mail | Yes | Yes | Recommended | Medium |
| Daum/Kakao Mail | Yes (SPF primary) | Not documented | Not documented | Low-medium |

Naver independently tightened policy in 2024 following Gmail's lead. Stibee (Korea's Mailchimp equivalent) explicitly states: "Gmail and Naver Mail combined account for 70–80% of domestic recipients — implementing these measures is strongly recommended."

### The Supply Gap

- **No Korean email deliverability specialists exist** as an identifiable professional class
- No deliverability service category on Kmong or Wishket — white space
- Only Korean-language deliverability resource: Stibee's blog (vendor content, not independent consulting)
- No Korean equivalent of Email Geeks Slack, MAAWG, or Word to the Wise

### Your Positioning Advantage

As a bilingual (EN/KR) person in Seoul with QA/API technical skills and a business background:

- **No Korean competition** to undercut you
- **Western consultants** at $150–$300/hr don't speak Korean and don't know Naver Mail's filtering
- **Korean generalist IT consultants** don't have the deliverability technical depth
- The pitch: *"I help Korean B2B companies fix email deliverability for both Gmail and Naver Mail audiences"* — a problem nobody in Korea is specifically solving

### Korean Email Ecosystem

| Platform | Role | Notes |
|---|---|---|
| **Naver Mail** | ~40–50% of domestic consumer inboxes | Tightened receiving policy 2024; requires SPF + DKIM |
| **Daum/Kakao Mail** | Large consumer base | SPF-gated; DMARC enforcement softer |
| **Stibee (스티비)** | Korea's dominant email marketing SaaS | Most proactive on deliverability education; only real Korean-language resource |
| **Channel.io** | B2B customer messaging + email | Significant transactional email sender for Korean businesses |
| **Naver Works** | B2B/enterprise email | Enhanced spam blocking announced 2024 |

No dedicated Korean deliverability tooling exists — no Korean Postmark, SendGrid, or Valimail equivalent.

---

## 4. Skill Overlap with Your QA/API Track

This is not adjacent to what you're learning — **it is the same thing applied to a different domain.** Near 1:1 mapping.

| Your QA/API Skill | Directly Maps To |
|---|---|
| REST API calls (requests, Postman) | SendGrid v3 API, Postmark API, SES API — all standard REST/JSON with Bearer auth |
| pytest | MailSlurp/Mailtrap pytest integration — `assert email.subject == "Reset your password"` |
| Python scripting | `parsedmarc`, `checkdmarc`, `dnspython` — mature PyPI packages |
| JSON parsing | ESP webhook payloads, SES SNS notifications |
| XML parsing | DMARC aggregate reports are gzip XML |
| Webhook consumption | SendGrid Event Webhook, SES→SNS→HTTP — identical to payment/CRM webhooks |
| ISTQB acceptance criteria | "95% of emails delivered in 5 min; spam rate < 0.1%; DMARC pass rate > 99%" |
| Monitoring/alerting design | Google Postmaster Tools API + MXToolbox REST API → threshold alerts |

The QA/API learning path already in progress produces the skills needed here with essentially zero wasted effort. No separate track required.

### Python Libraries

| Library | Function |
|---|---|
| `dnspython` | DNS record lookup (SPF, DKIM, DMARC, MX, PTR) |
| `checkdmarc` | Validates and parses SPF and DMARC records with structured output |
| `parsedmarc` | Full pipeline: fetch DMARC reports from IMAP → decompress → parse XML → JSON/Elasticsearch |
| `mailslurp-client` | Create disposable inboxes programmatically; pytest integration for email flow testing |

### Key APIs

| API | Auth | What it exposes |
|---|---|---|
| **SendGrid v3** | Bearer token | Send, bounce management, complaint list, event webhooks, stats |
| **Postmark** | X-Postmark-Server-Token | Bounces, webhooks, suppressions |
| **Amazon SES v2** | AWS SigV4 / boto3 | Suppression list, bounce/complaint handling, sending stats |
| **MXToolbox REST** | API key (paid) | SPF/DKIM/DMARC validation, blacklist checks, DNS propagation |
| **Google Postmaster Tools** | OAuth2 | Spam rate, domain reputation, DMARC/SPF/DKIM pass rates, per-day data |

### QA Concept Mapping

| ISTQB / Software QA Concept | Email Deliverability Equivalent |
|---|---|
| Acceptance criteria | "95% delivery in 5 min; spam rate < 0.1%; DMARC pass rate > 99%" |
| Functional testing | Send test email; assert correct headers, DKIM signature, From: address |
| Regression testing | After any DNS/ESP change, re-run DNS validation + delivery test suite |
| Integration testing | App code → SendGrid/SES API → correct error handling + webhook processing |
| Monitoring / alerting | Scheduled probes to seed addresses; Postmaster API for spam rate thresholds |
| Defect reporting | Document that `550 5.7.26` = DMARC rejection; which MTA; what DNS fix resolves it |
| Test environment management | Mailtrap sandbox = mock server for email (intercepts in staging) |
| CI/CD integration | pytest + MailSlurp email flow tests in CI pipeline on every deploy |

---

## 5. How It Fits Existing Career Tracks

| Track | Relevance |
|---|---|
| **전산법인 기획자** | 플랫폼세무사회 sends notification emails to 17,000 세무사 members. Deliverability settings being wrong = members miss 공지. You'd be the only 기획자 candidate who could flag this as a product quality concern. |
| **Embassy** | Irrelevant. |
| **사협 (1형당뇨 협동조합)** | Member newsletters and transactional emails will need proper authentication anyway. Learn it properly rather than outsourcing. |
| **SaaS (부가세 점검 도구)** | Any SaaS built will need transactional email (signup, report delivery, alerts). Own the infrastructure; don't outsource it. |
| **QA/API track (ISTQB, pytest, Postman)** | Direct overlap — skills reinforce each other, not competing for learning time. |

---

## 6. Certifications & Communities

### Certifications (all free)

| Program | Provider | Notes |
|---|---|---|
| Warmy Deliverability Certificate | Warmy.io | Open access; assessment required |
| Klaviyo Deliverability Certificate | Klaviyo Academy | ESP-specific but respected |
| Braze Email Deliverability Skills Badge | Braze Learning | Enterprise ESP focused |
| Proofpoint Certified Email Authentication Specialist | Proofpoint | Authentication/security angle |

No universally recognized credential exists (no CISSP equivalent). MAAWG membership is the closest to a professional body — an industry association, not a certification. Reputation and results matter more than credentials in this space.

### Communities

| Community | Platform | Notes |
|---|---|---|
| **Email Geeks** | Slack | Largest community; primary on-ramp; all major ESPs have official channels |
| **Litmus Community** | Web forum | Design + deliverability peer help |
| **MAAWG** | Industry association | Senior practitioners + ISP engineers; invite/membership only |
| **Word to the Wise blog** | wordtothewise.com | Laura Atkins — industry bible; read by ISP engineers |
| **Spam Resource** | spamresource.com | Al Iverson — practitioner-level reference |

---

## 7. Verdict & Next Steps

| Question | Answer |
|---|---|
| **Is it legit?** | Yes. Mandatory infrastructure, $1.14B→$2.38B market, enforced by Gmail/Yahoo/Microsoft. |
| **Enough global demand?** | Yes. 20,555+ job listings, 438 Upwork postings, $64K–$117K in-house salary range. |
| **Can you avoid competing on price?** | Yes — Korea-market bilingual specialist or QA-methodology-driven auditor = different tier from Fiverr setup workers entirely. |
| **Korea-specific opportunity?** | Strong. 1.8% DMARC adoption, zero local specialist competition, both Gmail + Naver Mail now enforcing, no Korean-language professional resource. |
| **Skill overlap with QA/API track?** | Near 1:1. Same APIs, same pytest patterns, same Python tooling, same ISTQB test thinking. No new track required. |
| **Primary career track?** | No — Embassy/전산법인/사협 are better defined. Hold as natural byproduct of QA/API skills + Korea-market side income option. |

### When to revisit

- After ISTQB CTFL pass — then you have a credential + technical depth to combine
- If 전산법인 role materializes — email deliverability of 플랫폼세무사회 becomes a concrete internal application
- If freelance income needed during Embassy wait period (May–July 2026) — Korea-market consulting angle is the entry point

### Potential demonstration project (when ready)

A Python script using `parsedmarc` + `checkdmarc` + `dnspython` that:
1. Accepts a domain as input
2. Validates SPF, DKIM, DMARC records and flags issues
3. Parses a DMARC aggregate report XML and outputs human-readable summary
4. Generates a structured audit report (Markdown or JSON)

This would be a natural follow-on to `kr-forensic-finance` — same pattern (open data + Python pipeline + structured output) in a different domain.

---

## 8. Raw Research: Career Demand

*Source: Agent search, Jan–Feb 2026 data*

### Freelance Rates (Upwork/Fiverr)

- Upwork: 438 open jobs; $15–$40/hr (lower end) → $50–$150/hr (portfolio consultants) → $95–$300/hr (agency-level)
- Fixed-price audits: basic ~$750; comprehensive $1,500+
- Fiverr: basic packages ~$25; comprehensive up to $170; 12 vetted freelancers listed

### In-House Salaries

- ZipRecruiter average: **$64,246/yr** (Email Deliverability Specialist, entry-to-mid)
- Glassdoor: **$117,694/yr** average (Email Deliverability Consultant; 25th–75th: $88K–$163K)

### Market Size

- 2024: **$1.14B** → 2025: **$1.24B** → 2033: **$2.38B** (8.47% CAGR)
- Source: Business Research Insights

### Inbox Placement Stats

- Global average inbox placement: **83.1%** (16.9% of legitimate email fails)
- US/Canada: **20%+** of commercial emails do not reach subscribers
- Microsoft/Outlook inbox placement: only **75.6%** (spam rate > 14%)
- Source: MailReach 2025 stats; Validity 2025 Benchmark Report

### AI Impact

| Automates (commodity) | Does not replace (expert) |
|---|---|
| Basic record generation/validation | ISP postmaster relationship management |
| Spam score testing | Blocklist removal negotiations |
| Email warmup | Sender reputation strategy |
| Bounce/complaint rate monitoring | Diagnosing systemic failures |

---

## 9. Raw Research: Skill Overlap Detail

*Source: Agent search, Jan–Feb 2026 data*

### SendGrid v3 API Key Endpoints

| Endpoint | Method | Function |
|---|---|---|
| `/mail/send` | POST | Send transactional email |
| `/suppression/bounces` | GET/DELETE | Retrieve or remove bounced addresses |
| `/suppression/spam_reports` | GET/DELETE | Manage spam complaint list |
| `/v3/user/webhooks/event/settings` | GET/PATCH | Configure Event Webhook |
| `/stats` | GET | Delivery, open, click metrics |

SendGrid Event Webhook fires HTTP POST of JSON array for every event (`delivered`, `bounce`, `spam_report`, `click`, `open`, `unsubscribe`) — standard webhook pattern.

### Amazon SES v2 Python (boto3)

```python
import boto3
client = boto3.client('sesv2', region_name='us-east-1')

# List suppressed destinations
response = client.list_suppressed_destinations(
    Reasons=['BOUNCE', 'COMPLAINT'],
    StartDate=datetime(2026, 1, 1),
    EndDate=datetime(2026, 2, 28)
)

# Remove from suppression
client.delete_suppressed_destination(EmailAddress='user@example.com')
```

### pytest Email Flow Test (MailSlurp)

```python
def test_password_reset_email_delivered():
    # Create disposable inbox
    inbox = inbox_controller.create_inbox()

    # Trigger system to send email to inbox
    trigger_password_reset(inbox.email_address)

    # Assert on received email
    email = wait_controller.wait_for_latest_email(
        inbox_id=inbox.id,
        timeout=30000,
        unread_only=True
    )

    assert email.subject == "Reset your password"
    assert "reset-link" in email.body
    assert email.from_ == "noreply@yourdomain.com"
```

### DMARC Report Parsing (parsedmarc)

```python
import parsedmarc

with open('google.com!yourdomain.com!...xml.gz', 'rb') as f:
    report = parsedmarc.parse_aggregate_report_file(f)

for record in report['records']:
    print(record['source']['ip_address'],
          record['count'],
          record['policy_evaluated'])
```

### DNS Checking (dnspython)

```python
import dns.resolver

# SPF
answers = dns.resolver.resolve('yourdomain.com', 'TXT')
for rdata in answers:
    if 'v=spf1' in str(rdata):
        print(f"SPF: {rdata}")

# DMARC
answers = dns.resolver.resolve('_dmarc.yourdomain.com', 'TXT')
for rdata in answers:
    print(f"DMARC: {rdata}")
```

### Google Postmaster Tools API

- Base: REST with Discovery Document; OAuth2 auth
- `domains.trafficStats`: spam rate, domain reputation, DMARC/SPF/DKIM pass rates, TLS encryption rate — per-day granularity
- Use case: pull daily → alert when spam rate exceeds 0.1% threshold

---

## 10. Raw Research: Korea Market

*Source: Agent search, Jan–Feb 2026 data*

### DMARC Adoption Data

- South Korea Global 2000 DMARC adoption: **1.8%** (Proofpoint/CybersecAsia/Red Sift)
- Only 10.1% of Korean public companies have implemented `p=reject`
- Over 50% have no DMARC record at all

### Naver Mail Policy (2024)

- Tightened receiving policy to require SPF and DKIM following Gmail's lead
- Applies aggressive rate-limiting to international senders without Korean IP reputation
- Bans using @naver.com as sender address from non-Naver servers

### Stibee (스티비) as Primary Resource

- Korea's dominant email marketing SaaS; effectively the only deliverability educator in the Korean market by default
- Published two dedicated blog posts on 2024 policy changes for domestic senders
- 2025 Email Marketing Report analyzed 636,000 emails; automated emails achieve 3.8x higher click rates

### Freelance/Job Market in Korea

- Only 17 email marketing jobs on Glassdoor Korea (Jan 2026) — generalist roles, not deliverability specialists
- No "email deliverability" service category on Kmong or Wishket
- No identified Korean deliverability consultants or communities

### KISA (Korea Internet Security Agency)

Handles anti-spam regulation under Korea's Act on Promotion of Information and Communications Network Utilization. Publishes spam-blocking guidelines focused on legal compliance, not deliverability optimization. Materials are technical/regulatory, not marketer-friendly.

---

## 11. Background Asset Positioning Research — Deep Synthesis (Feb 28, 2026)

*This section was produced as a deep research pass specifically answering: which background assets create which deliverability positioning advantages, where assets stack for maximum advantage, and how to articulate the combined positioning.*

---

### Research Area 1: Industries with the Most Severe and Expensive Deliverability Problems

The highest-pain deliverability problems are concentrated in industries where a failed email has an immediate, measurable financial or trust consequence — not just a marketing metric.

**Fintech / Financial SaaS** is the clearest example. The deliverability failure mode is specific: OTPs (one-time passwords), fraud alerts, new device login notifications, and transaction confirmations must arrive within seconds. A delayed OTP = failed login = abandoned transaction = lost revenue and lost trust. Fintech companies often experience deliverability crises during volume spikes (market events, tax periods, product launches) precisely when reliability matters most. Even a few seconds of delay is unacceptable. Because these are transactional (not marketing) emails, standard email marketing logic (open rates, click rates) does not apply — the test is pure delivery speed and inbox placement. Sources: [MailerSend — Email for Banks, Fintech](https://www.mailersend.com/solutions/email-banks-financial-services); [Finance Monthly — Building Trust in Fintech](https://www.finance-monthly.com/building-trust-in-fintech-best-practices-for-transactional-email-sending/); [Mailgun — Fintech Email](https://www.mailgun.com/industries/fintech/).

**Tax and Accounting SaaS** is the second tier. Tax SaaS platforms (TurboTax equivalents; Korean platforms like 홈택스 연동 tools) send filing confirmations, deadline reminders, assessment notifications, and e-signature requests. These emails are legally significant. A missed deadline reminder is not a missed marketing email — it is a missed 가산세 avoidance opportunity worth real money to the recipient. The 삼쩜삼 추징 scandal (1,423 taxpayers, ₩41억 clawback) shows how trust-critical tax notification infrastructure is: if users had received clearer, timely notifications, complaint volumes would have been lower. Deliverability failure in tax SaaS is directly tied to user loss and legal liability exposure.

**Healthcare SaaS** compounds deliverability with compliance. Appointment confirmations, prescription notifications, and test result alerts that land in spam cause missed appointments and patient anxiety. In the US, HIPAA compliance adds a second dimension: any email containing PHI requires a BAA with the email service provider, end-to-end encryption, and audit logging. In Korea, the 개인정보보호법 (PIPA) imposes analogous obligations on health data. The 1형당뇨 사협 context is directly relevant: a healthcare social cooperative that sends member communications, service alerts, or 건보공단 payment notifications will face both deliverability and regulatory requirements simultaneously. Sources: [Mailgun — HIPAA Email Compliance](https://www.mailgun.com/blog/email/email-hipaa-compliance/); [HIPAA Journal — Email Compliance](https://www.hipaajournal.com/hipaa-compliance-for-email/).

**SaaS generically** suffers a well-documented revenue impact from transactional email failure. When billing alerts, plan expiration notices, or usage notifications fail to arrive: support ticket volume spikes, churn increases, and conversion from trial decreases. The [DMARC Report analysis of hidden SaaS deliverability costs](https://dmarcreport.com/blog/the-hidden-costs-of-poor-email-deliverability-for-saas-businesses/) quantifies this: a 10% spam placement rate = a direct 10% reduction in potential revenue touchpoints before any engagement occurs.

**Key finding:** The most expensive deliverability problems are not in email marketing — they are in transactional email for regulated, time-sensitive, or trust-critical industries. These industries pay premium consulting rates because the cost of failure is not abstract.

---

### Research Area 2: Regulated Industries — Compliance + Deliverability as a Combined Premium

Securities, insurance, and banking operate under email compliance obligations that go far beyond deliverability optimization — creating a combined consulting need that generic deliverability specialists cannot serve.

**US regulatory framework (FINRA/SEC):**
- **SEC Rule 17a-4** requires broker-dealers to retain all electronic correspondence (including email) for minimum 2 years with immediate accessibility, 6 years total, in WORM (write-once, read-many) non-erasable format.
- **FINRA Rule 4513** requires records of customer complaints to be retained for 4 years.
- Email must be encrypted end-to-end when containing sensitive client data or PII.
- Multi-factor authentication is required on all email accounts.
- **Enforcement is real:** JPMorgan was fined $4M in 2023 for accidentally deleting 47 million messages. In 2017, FINRA fined 12 firms a combined $14.4M for WORM format violations. Source: [Bluetie — FINRA Email Compliance Guide](https://bluetie.com/finra-email-compliance-guide-for-financial-services/); [Intradyn — FINRA/SEC 17a-4](https://www.intradyn.com/guidelines-for-finra-sec-17a-4-email-compliance/).

**The combined deliverability + compliance opportunity:** A regulated financial firm needs emails to (a) reach inboxes reliably and (b) be compliant, archived, and auditable. These are separate problems but the same client has both. A consultant who understands both deliverability mechanics and the compliance context can charge for integrated advice that no pure-deliverability or pure-compliance consultant can provide alone. An accountant-trained consultant understands regulatory documentation requirements, record retention logic, and audit trails in a way that a technical deliverability specialist never would.

**Korean regulated financial context:** Korea's 금융위원회 and 금융감독원 regulate financial communications. Korea's personal data law (PIPA / 개인정보보호법) applies to all personally identifiable communications. Korean financial institutions expanding internationally (sending emails to US or EU recipients) face the additional layer of CAN-SPAM, GDPR, and CASL compliance simultaneously. No Korean specialist exists to advise on the intersection of Korean sender reputation + international regulatory compliance + deliverability mechanics.

**Insurance:** Insurance companies send policy renewal notices, premium payment reminders, and claims status notifications — all of which are legally significant communications that must demonstrably reach the insured. Failure to deliver a cancellation notice has resulted in litigation. Premium consulting rates reflect this. Source: [Inxmail — Banks and Insurance Email](https://www.inxmail.de/en/solutions/industry-solutions/banks-insurance/).

---

### Research Area 3: Korean Companies Expanding Internationally — Specific Deliverability Challenges

This is the single most differentiated positioning opportunity because the supply gap is documented and the problem is structural.

**The DMARC adoption data** (Section 3 of this document) establishes South Korea at 1.8% DMARC adoption among Global 2000 companies — dead last in APAC, behind Japan (7.4%), China (4.2%), Thailand (17.6%), Singapore (46.2%), and Australia (71%). This is not a minor gap. It means Korean companies sending email to Gmail or Outlook recipients globally are operating without the authentication infrastructure that Google and Microsoft now require.

**The international expansion email problem is structural, not just technical:**

A Korean B2B SaaS company expanding to the US or Japan faces compounding problems that most deliverability consultants cannot diagnose:

1. **Sender reputation starting from zero:** Korean IP ranges and domains have no established reputation with US ISPs. Cold sending from Korean infrastructure into Gmail/Outlook without warmup will result in mass spam placement or rejection.

2. **Korean character encoding:** Emails with Korean-language content (UTF-8, EUC-KR), Korean sender names, or Korean domain names can trigger spam filters trained on Western sending patterns. MIME encoding of Korean subject lines (ISO-2022-KR or UTF-8 with proper MIME header encoding) is a specific technical challenge that non-bilingual consultants cannot diagnose by reading the email content.

3. **Naver Mail / Daum outbound reputation:** Korean companies accustomed to using Naver Works or Kakao for internal communication often lack proper outbound email infrastructure entirely. When they need to send to international recipients, they may be sending from shared infrastructure with poor reputation.

4. **Cultural mismatch in list management:** As the research found, Korean business email is primarily used as a broadcast channel rather than a relationship channel. Korean companies expanding internationally often send at high frequency without the list hygiene practices (engagement-based suppression, re-permission campaigns) that Western ISPs use as spam signals. This results in engagement rate collapse, which ISPs read as spam behavior, which triggers filtering.

5. **No local specialist:** The search found a job posting for a "Deliverability Consultant — Bilingual (Korean and English)" on Salary.com, confirming that bilingual Korean deliverability expertise is being searched for by employers. The supply is thin enough that an individual job posting surfaces as a result. Source: [Salary.com — Deliverability Consultant Bilingual Korean/English](https://www.salary.com/job/easyrecrue/deliverability-consultant-bilingual-korean-and-english/852b1078-5dc4-4af4-bcb3-e534611c0ea8).

**The East Asia email marketing adaptation problem** (confirmed by Stripo research) is that Japan, Korea, and China have fundamentally different email usage patterns than Western markets. Korean B2B companies expanding to Japan face a second-order localization problem: not just translation, but email frequency norms, opt-in standards, and ISP behavior in the Japanese market are entirely different from Korean norms. A bilingual Korean/English consultant with functional Chinese has a unique position to advise on pan-East-Asia outbound email strategy. Source: [Stripo — Email Marketing in East Asia](https://stripo.email/blog/email-marketing-in-east-asia-how-to-adapt-strategies-to-the-market-realities-of-japan-south-korea-and-china/).

**Asia-Pacific deliverability rate data** from MailReach 2025 shows APAC at the lowest regional inbox placement rate globally at 78.2%, with high variance: India at ~69.8%, Korea not independently broken out but contextually similar to India given the authentication gap. This confirms that Korean companies sending internationally are likely experiencing materially worse inbox placement than their US counterparts without understanding why. Source: [MailReach — Email Deliverability Statistics 2025](https://www.mailreach.co/blog/email-deliverability-statistics).

---

### Research Area 4: QA-to-Deliverability Career Path — Precedent and Python Advantage

**Precedent exists for the path.** ZipRecruiter lists job titles including "Email Deliverability Engineer" as a distinct career category, and the skill requirements map directly to QA/API testing: knowledge of email protocols (SMTP, IMAP, MIME), spam filter mechanics, authentication standards (SPF, DKIM, DMARC), data analysis, troubleshooting methodology, and ISP policy understanding. Sources: [Indeed — Email Deliverability Engineer Jobs](https://www.indeed.com/q-Email-Deliverability-Engineer-jobs.html); [ZipRecruiter — Email Deliverability Jobs](https://www.ziprecruiter.com/Jobs/Email-Deliverability).

The "Email Campaign QA Specialist" role exists as a distinct job category on Indeed — using tools like Litmus and Email on Acid to test rendering, deliverability, and compliance before send. This is essentially QA applied to email infrastructure, with the same methodology: test cases, acceptance criteria, pass/fail assertions, regression after changes.

**What Python enables that non-technical consultants cannot:**

| Capability | Non-Technical Consultant | Python-Capable Consultant |
|---|---|---|
| DNS record validation | Manual; one domain at a time | `checkdmarc` batch-validates hundreds of domains; outputs structured JSON |
| DMARC report processing | Opens XML in a browser; manual reading | `parsedmarc` ingests entire months of DMARC aggregate reports; outputs aggregate statistics showing which IPs are failing and why |
| Blocklist monitoring | Checks MXToolbox manually | MXToolbox REST API + scheduled Python cron → alert when any of 200+ blocklists flag a domain |
| Sender scoring trend | Screenshots Postmaster Tools weekly | Google Postmaster Tools API → daily pull → time-series dashboard; anomaly detection |
| Email flow integration testing | Manual send + manual check | pytest + MailSlurp: automated assertion that the password reset email arrives with correct subject, sender, and link within 30 seconds — runs on every CI/CD deploy |
| Deliverability audit report | Word document with screenshots | Python script accepts domain → outputs structured Markdown/JSON audit report covering SPF, DKIM, DMARC, MX, PTR, blacklist status, and DMARC report summary |
| Multi-client monitoring | Client-by-client manual checks | Single script monitors 50 client domains with threshold alerting — scalable without proportional time cost |

**The ISTQB framework advantage** is positioning-specific. ISTQB CTFL certifies that the practitioner understands test design technique (equivalence partitioning, boundary value analysis), test planning, defect lifecycle management, and risk-based testing prioritization. These concepts apply directly to deliverability audit methodology:
- Equivalence partitioning: what classes of authentication configuration are equivalent in their deliverability impact?
- Risk-based prioritization: which deliverability issues pose the highest probability × impact for this specific client's send volume and industry?
- Acceptance criteria definition: writing testable deliverability SLAs (e.g., "95% of transactional emails delivered within 5 minutes; spam rate < 0.1%; DMARC pass rate > 99%") is identical in structure to ISTQB-trained acceptance criteria for software features.

This allows a QA-background deliverability consultant to produce deliverability audit reports that look like professional QA test reports — structured, traceable, with defined pass/fail criteria — rather than the informal advisory documents that generalist deliverability consultants produce.

---

### Research Area 5: Email Deliverability Monitoring Tools and Custom Automation Advantage

**The commercial tool landscape (2025–2026):**

| Tool | Function | Pricing Tier | Limitation |
|---|---|---|---|
| **GlockApps** | Inbox placement testing across ISPs; DMARC monitoring; blocklist monitoring; automatic scheduled tests | Paid (freemium); paid tier ~$59–$249/mo | Results are aggregate; no custom logic or client-specific alerting without API integration |
| **Litmus** | Email rendering + inbox preview; spam testing; analytics | Enterprise pricing; ~$99–$399/mo | Focused on design/rendering, not authentication or reputation |
| **Email on Acid** | Rendering tests; spam filter checks; accessibility | ~$86–$399/mo | Similar to Litmus; limited on authentication/reputation depth |
| **MXToolbox** | DNS lookup; blacklist monitoring; SPF/DKIM/DMARC validation; REST API available | Free (limited) + $129–$399/mo paid | Not a deliverability monitoring platform; a diagnostic tool |
| **MailReach / Warmup Inbox** | Email warmup automation; reputation scoring | $25–$79/mo | Warmup-focused; not audit/monitoring |
| **EasyDMARC** | DMARC management; aggregate report visualization | Freemium + paid | Solid DMARC management; limited non-DMARC scope |
| **Google Postmaster Tools** | Gmail-specific: domain reputation, spam rate, DMARC pass rate | **Free; Google account required** | Gmail only; no Outlook/Yahoo data; requires OAuth |

Sources: [GlockApps — Automatic Email Spam Test Tutorial](https://glockapps.com/tutorials/automatic-email-spam-test/); [EmailVendorSelection — 9 Best Email Deliverability Tools 2026](https://www.emailvendorselection.com/email-deliverability-tools/); [TrulyInbox — 6 Best Email Deliverability Tools](https://www.trulyinbox.com/blog/email-deliverability-tools/).

**What building custom Python monitoring scripts enables beyond these tools:**

1. **Multi-source aggregation:** A custom script can simultaneously pull from Google Postmaster Tools API (Gmail data), MXToolbox API (DNS + blacklist), SendGrid/SES webhooks (event stream), and GlockApps API (inbox placement) into a single dashboard or alert system. No commercial tool spans all of these.

2. **Client-specific business logic:** Commercial tools alert on absolute thresholds. A custom script can alert based on client-specific SLAs, seasonal expectations (a tax platform's spam rate during 5월 종합소득세 filing season vs. off-season should have different alerting thresholds), or integration with the client's ticketing system.

3. **DMARC aggregate report pipeline:** `parsedmarc` processes the full DMARC report XML pipeline (fetch from IMAP/HTTPS → decompress → parse → structured output) with zero manual effort. Commercial DMARC tools charge $50–$200/month for this; a custom script running on a $5/month VPS does it for free with more customization. This is a direct cost reduction for clients at small to mid scale, and positions the consultant as the operator of the client's deliverability infrastructure rather than just an advisor.

4. **Korean-language diagnostic output:** Commercial tools produce English-only reports. A consultant who builds Korean-language deliverability audit report templates has a hard-to-replicate advantage with Korean clients.

5. **Scalability advantage for consulting business:** A consultant who manually checks clients is limited to ~5–10 clients before the monitoring work overwhelms them. A consultant running automated monitoring scripts can monitor 30–50 clients simultaneously with threshold-based alerts, profitably serving mid-market clients at lower price points than manual-monitoring competitors.

---

### Research Area 6: Tax SaaS and Korean Tax Ecosystem Deliverability Needs

This connects directly to the 전산법인 and SaaS product track.

**Tax SaaS transactional email types and their failure consequences:**

| Email Type | Consequence of Non-Delivery |
|---|---|
| Filing confirmation | Taxpayer has no record of submission; re-files → duplicate; penalty risk |
| Deadline reminder | Missed filing → 가산세 (late filing penalty); potential legal liability for platform |
| 세금계산서 issuance notification | Business recipient misses 매입세액공제 (VAT input deduction) window |
| Account security / OTP | Failed login; security breach if account unprotected |
| Payment notification (국민건강보험, 4대보험) | Missed payment → 연체 가산금; compliance failure |
| Assessment / 경정청구 result | Taxpayer misses refund opportunity |
| Agent assignment notification (세무사 delegation) | Workflow breakdown between taxpayer and 세무사 |

**전산법인 specific application:** 플랫폼세무사회 sends operational notifications to 17,000+ member 세무사. If DMARC is not configured and Naver Mail or Gmail classifies these as spam, members miss 공지사항 about regulatory changes, software updates, or system maintenance — directly impacting the platform's credibility. The 기획자 who understands this problem and can articulate it in terms of product quality (not just IT infrastructure) is meaningfully differentiated from other candidates.

**홈택스 연동 / 세금계산서 (전자세금계산서) platforms** like 더존 위하고, 세무사랑, and the 국세청 e세금계산서 system all generate transactional emails at the moment of document issuance and receipt. These are legally significant tax documents. A deliverability failure is a potential tax record failure. No Korean specialist currently advises these platforms on deliverability.

**The 부가세 SaaS product connection:** The planned 부가세 사전 점검 SaaS will itself need a transactional email infrastructure: report delivery, user account management, billing notifications. Building this with proper authentication from day one (rather than retrofitting it) is a $0 investment with ongoing value. Knowing the deliverability layer deeply means the product never ships broken email infrastructure — and the founder can credibly advise other Korean tax SaaS founders on the same problem.

---

### Synthesis: Background Asset → Positioning Advantage Mapping

| Background Asset | Deliverability Positioning Advantage | Tier It Unlocks |
|---|---|---|
| **MAcc degree** | Understands regulatory record retention, audit trails, and compliance documentation requirements that pure-technical deliverability consultants cannot articulate; can advise regulated industry clients (financial services, accounting firms) on the intersection of compliance obligations and delivery infrastructure | Premium (regulated industries) |
| **US CPA firm experience** | Familiarity with US financial services regulatory environment (SEC, FINRA, IRS); understands what "legally significant email" means from the sender's perspective; credible to CFOs and controllers who are the budget owners for regulated-industry email infrastructure | Premium (US-registered financial companies, accounting technology vendors) |
| **Bilingual English/Korean** | Only bilingual deliverability specialist in a market with 1.8% DMARC adoption and no Korean specialist class; can serve Korean companies expanding internationally AND Western companies targeting Korean-language audiences; can produce Korean-language audit reports; understands Naver Mail filtering behavior; can read Stibee/KISA documentation in Korean | Korea-market monopoly (effectively uncontested) |
| **Functional Chinese** | Adds Chinese-language SaaS and fintech company context; China has 4.2% DMARC adoption (higher than Korea but still low); Chinese fintech expanding globally (WeChat Pay international, etc.) faces identical problems | Secondary market expansion; Chinese company BD |
| **QA/API testing (Python/pytest/Postman)** | Enables automated, programmatic deliverability testing that non-technical consultants cannot provide; can integrate email flow testing into clients' CI/CD pipelines; can build custom monitoring dashboards; can produce structured audit reports with defined pass/fail criteria | Technical differentiation; scalable consulting operations |
| **ISTQB CTFL (in progress)** | Provides professional framework for deliverability audit methodology: test design, risk-based prioritization, acceptance criteria, defect lifecycle; allows structuring deliverability engagements as formal QA projects rather than informal advice | Credibility with technical organizations; positions work as QA methodology not just ad-hoc troubleshooting |
| **Korean tax software ecosystem knowledge (전산법인, 세무사랑, 세금계산서 platforms, 홈택스)** | Specific product knowledge of Korean tax SaaS sending patterns; understands 세무사 workflow and what notification failures cost them operationally; direct access as an insider if 전산법인 role materializes; competitive intelligence on which platforms have authentication gaps | Korean tax SaaS vertical — currently unserved by any deliverability specialist |
| **Healthcare social cooperative founding (1형당뇨 사협, 이사장)** | Firsthand experience building a regulated healthcare communication infrastructure; understands patient communication sensitivity; credible to Korean healthcare SaaS vendors on PIPA compliance + deliverability intersection; bootstrap proof-of-concept lab for own email deliverability implementation | Healthcare SaaS vertical; founder-credibility with early-stage Korean health startups |

---

### Industries and Niches Where All Assets Stack for Maximum Positioning

| Niche | Assets That Apply | Why This Combination Is Uncontested |
|---|---|---|
| **Korean fintech companies expanding to the US** | MAcc + CPA firm + Korean bilingual + QA/API + functional Chinese | Can advise on: US financial email compliance (FINRA/SEC context), Korean sender reputation repair for US ISPs, SPF/DKIM/DMARC buildout with Python automation, Korean-language client communication. No other consultant has all four. |
| **Korean tax SaaS platforms (전산법인, 세금계산서 vendors)** | Korean tax ecosystem + Korean bilingual + QA/API + MAcc | The only person who understands the platform product context AND can build the monitoring infrastructure AND can advise in Korean AND understands the financial/tax significance of email non-delivery. |
| **US accounting/CPA firm technology vendors** | MAcc + CPA firm experience + QA/API + ISTQB | Can speak the language of the buyer (CPAs and controllers) + deliver structured QA-methodology-based deliverability audits + automate ongoing monitoring. |
| **Korean healthcare SaaS / digital health startups** | 사협 founder experience + Korean bilingual + PIPA knowledge + QA/API | Healthcare deliverability with Korean regulatory compliance + technical implementation capability. 사협 provides founder credibility ("I run a Korean healthcare cooperative and solved this problem for our own infrastructure"). |
| **East Asian B2B SaaS companies going global (Korean + Japanese + Chinese markets)** | Korean bilingual + functional Chinese + QA/API + Korean market knowledge | Pan-East-Asia deliverability advisory — outbound email from Korean/Japanese/Chinese infrastructure into Western inboxes — no Western consultant can serve this; no Korean consultant has the technical depth. |

---

### Draft Positioning Statement

**Version 1 (Consulting pitch — technical buyer):**

"I help Korean and East Asian B2B companies fix email deliverability failures when entering global markets — a problem that costs companies in inbox placement, customer trust, and regulatory compliance, and that generic technical consultants can't diagnose without understanding your local sending infrastructure. With a background in US CPA-firm financial compliance, QA automation engineering, and direct expertise in the Korean email ecosystem (Naver Mail, Stibee, KISA anti-spam policy), I build programmatic monitoring systems in Python that provide ongoing deliverability visibility — not a one-time audit that goes stale in 90 days."

**Version 2 (Client-facing — Korean language context, translated for positioning clarity):**

"US CPA 자격을 가진 QA 엔지니어로서, 저는 한국 기업이 글로벌 이메일 발송에서 겪는 스팸 처리 문제를 기술적으로 진단하고 자동화된 모니터링 시스템으로 해결합니다. 특히 국세청 연동 플랫폼, 세무사 협회, 핀테크 기업의 거래 메일 발송률 문제에서 국내에 비교 가능한 전문가가 없는 영역을 다룹니다."

**Version 3 (Positioning statement for professional bio):**

"I operate at the intersection of financial compliance, QA engineering, and the Korean B2B email ecosystem — a combination that does not otherwise exist as a consulting specialty. My accounting background (MAcc, US CPA firm experience) allows me to advise regulated-industry clients on the compliance dimensions of email infrastructure that pure-technical specialists miss. My QA/API engineering skills (Python, pytest, Postman, ISTQB CTFL) allow me to build automated deliverability monitoring systems rather than delivering static audits. And my bilingual Korean/English position in Seoul, with direct experience in the Korean tax software ecosystem, means I serve the Korean market — where DMARC adoption is 1.8% and no local specialist class exists — without the language and market-knowledge barriers that exclude all other deliverability consultants."

---

### Consulting Rate Guidance by Niche Tier

Based on market data: [Upwork — Email Deliverability Freelancers](https://www.upwork.com/hire/email-deliverability-consulting-freelancers/); [Glassdoor — Deliverability Consultant Salary](https://www.glassdoor.com/Salaries/email-deliverability-consultant-salary-SRCH_KO0,31.htm).

| Positioning Tier | Rate Range | Justification |
|---|---|---|
| Commodity (avoid) | $15–$50/hr | SPF/DKIM/DMARC setup only; competed on Fiverr/Upwork globally |
| Mid-market (baseline) | $75–$125/hr | Deliverability audit + ESP migration + monitoring setup |
| Korea-specialist (differentiated) | $100–$200/hr | Bilingual Korean/English; Naver Mail expertise; Korean sender reputation — no comparable supply |
| Regulated-industry specialist (premium) | $150–$300/hr | Financial services (FINRA/SEC compliance intersection); Healthcare (HIPAA/PIPA); accounting technology |
| QA-methodology + automation (premium) | $150–$250/hr | Programmatic monitoring build; CI/CD integration; custom DMARC report pipelines |
| All assets combined (target) | $150–$300/hr | Korean regulated fintech/tax SaaS; quantifiable as the only practitioner combining these assets |

---

### Additional Sources (Research Area 1–6)

**Research Area 1 — Industry Severity:**
- [MailerSend — Email for Banks, Fintech and Financial Services](https://www.mailersend.com/solutions/email-banks-financial-services)
- [Finance Monthly — Building Trust in Fintech: Transactional Email](https://www.finance-monthly.com/building-trust-in-fintech-best-practices-for-transactional-email-sending/)
- [Mailgun — Sinch Email for Fintech](https://www.mailgun.com/industries/fintech/)
- [DMARC Report — Hidden Costs of Poor Email Deliverability for SaaS](https://dmarcreport.com/blog/the-hidden-costs-of-poor-email-deliverability-for-saas-businesses/)
- [Mailgun — State of Email Deliverability 2025 Key Takeaways](https://www.mailgun.com/blog/deliverability/state-of-deliverability-takeaways/)
- [Clearout — 10 Reasons Your Transactional Emails Won't Deliver](https://clearout.io/blog/transactional-email-deliverability/)
- [Mailgun — HIPAA Email Compliance](https://www.mailgun.com/blog/email/email-hipaa-compliance/)
- [HIPAA Journal — HIPAA Compliance for Email](https://www.hipaajournal.com/hipaa-compliance-for-email/)

**Research Area 2 — Regulated Industry Compliance:**
- [Bluetie — FINRA Email Compliance Guide for Financial Services](https://bluetie.com/finra-email-compliance-guide-for-financial-services/)
- [MirrorWeb — SEC and FINRA Email Archiving Policy](https://www.mirrorweb.com/blog/sec-and-finra-email-archiving-policy)
- [Intradyn — Guidelines for FINRA SEC 17a-4 Compliance](https://www.intradyn.com/guidelines-for-finra-sec-17a-4-email-compliance/)
- [Mimecast — FINRA Compliance and Regulations](https://www.mimecast.com/content/finra-compliance-and-regulations/)
- [Inxmail — Email for Banks and Insurance Companies](https://www.inxmail.de/en/solutions/industry-solutions/banks-insurance/)
- [EmailVendorSelection — Email Marketing for Financial Services](https://www.emailvendorselection.com/email-marketing-financial-services-banks/)

**Research Area 3 — Korean International Expansion:**
- [Stripo — Email Marketing in East Asia: Japan, South Korea, China](https://stripo.email/blog/email-marketing-in-east-asia-how-to-adapt-strategies-to-the-market-realities-of-japan-south-korea-and-china/)
- [The Marketing Student — Digital Marketing in South Korea](https://www.themarketingstudent.com/marketing-korea/)
- [Salary.com — Deliverability Consultant Bilingual Korean and English (job posting)](https://www.salary.com/job/easyrecrue/deliverability-consultant-bilingual-korean-and-english/852b1078-5dc4-4af4-bcb3-e534611c0ea8)
- [MailReach — Email Deliverability Statistics 2025](https://www.mailreach.co/blog/email-deliverability-statistics)
- [Suped — Country-Specific Email Domains for International Sending](https://www.suped.com/knowledge/email-deliverability/technical/what-are-the-pros-and-cons-of-using-country-specific-email-domains-for-international-sending)
- [LinkedIn — Asia Pacific Email Deliverability Software Market](https://www.linkedin.com/pulse/asia-pacific-email-deliverability-software-market-xwnge/)
- [Korea Times — Why Korean Firms Struggle to Become Global Players](https://www.koreatimes.co.kr/business/companies/20250708/why-korean-firms-struggle-to-become-global-players)

**Research Area 4 — QA-to-Deliverability Path:**
- [Indeed — Email Deliverability Engineer Jobs](https://www.indeed.com/q-Email-Deliverability-Engineer-jobs.html)
- [ZipRecruiter — Email Deliverability Jobs](https://www.ziprecruiter.com/Jobs/Email-Deliverability)
- [Indeed — Email Campaign QA Specialist Jobs](https://www.indeed.com/q-email-campaign-qa-specialist-jobs.html)
- [Mailosaur — How to Test Email and SMS in Python](https://mailosaur.com/docs/languages/python)
- [Mailtrap — Python Test Email Tutorial](https://mailtrap.io/blog/python-test-email/)
- [Woteq — How to Test Email Sending in Python with pytest](https://woteq.com/how-to-test-email-sending-functionality-in-python-with-pytest/)

**Research Area 5 — Monitoring Tools and Automation:**
- [GlockApps — Next-Level Email Deliverability Testing](https://glockapps.com/)
- [GlockApps — How to Create Automatic Tests](https://glockapps.com/tutorials/automatic-email-spam-test/)
- [EmailVendorSelection — 9 Best Email Deliverability Tools 2026](https://www.emailvendorselection.com/email-deliverability-tools/)
- [TrulyInbox — 6 Best Email Deliverability Tools 2026](https://www.trulyinbox.com/blog/email-deliverability-tools/)
- [Mailgun — Inbox Placement Testing](https://www.mailgun.com/features/email-inbox-placement/)
- [GlobeNewsWire — $1.9 Billion Email Deliverability Tools Market 2026](https://www.globenewswire.com/news-release/2026/01/06/3213911/0/en/Trends-Strategies-Shaping-the-1-9-Billion-Email-Deliverability-Tools-Market-2026-Beyond.html)
- [Emercury — Which Email Infrastructure Solutions Offer Best Deliverability for Python](https://www.emercury.net/blog/email-marketing-tips/which-email-infrastructure-solutions-offer-the-best-deliverability-rates-for-python-applications/)

**Research Area 6 — Tax SaaS Deliverability:**
- [MailerSend — Email Solution for SaaS and Developers](https://www.mailersend.com/solutions/email-for-saas)
- [Postmark — Transactional Email Providers Compared](https://postmarkapp.com/blog/transactional-email-providers)
- [Mailtrap — Best Transactional Email Services 2026](https://mailtrap.io/blog/transactional-email-services/)
- [Journal of Accountancy — 2025 Tax Software Survey](https://www.journalofaccountancy.com/issues/2025/sep/2025-tax-software-survey.html)
- [AI SEO Accountants — Email Marketing for Accounting and Tax Firms 2025](https://aiseoaccountants.com/blog/email-marketing-for-accounting-and-tax-firms/)

---

## Sources

**Career Demand:**
- [Upwork — Email Deliverability Freelancers](https://www.upwork.com/hire/email-deliverability-consulting-freelancers/)
- [ZipRecruiter — Email Deliverability Specialist Salary](https://www.ziprecruiter.com/Salaries/Email-Deliverability-Specialist-Salary)
- [Glassdoor — Email Deliverability Consultant Salary](https://www.glassdoor.com/Salaries/email-deliverability-consultant-salary-SRCH_KO0,31.htm)
- [Business Research Insights — Email Deliverability Market Size 2033](https://www.businessresearchinsights.com/market-reports/email-deliverability-market-102810)
- [MailReach — Email Deliverability Statistics 2025](https://www.mailreach.co/blog/email-deliverability-statistics)
- [Validity — 2025 Email Deliverability Benchmark Report](https://www.validity.com/resource-center/2025-email-deliverability-benchmark-report/)
- [ExpertSender — Email Deliverability in 2026](https://expertsender.com/blog/email-deliverability-in-2026-key-observations-trends-challenges-for-marketers/)
- [Word to the Wise](https://www.wordtothewise.com/categories/best-practices/)
- [Warmy — Become a Certified Deliverability Expert](https://support.warmy.io/knowledge/become-a-certified-deliverability-expert)
- [Klaviyo Academy — Deliverability Certificate](https://academy.klaviyo.com/en-us/collections/deliverability-certificate)

**Skill Overlap:**
- [SendGrid v3 API Reference](https://www.twilio.com/docs/sendgrid/api-reference)
- [Postmark Bounce API](https://postmarkapp.com/developer/api/bounce-api)
- [Amazon SES Suppression List — AWS Docs](https://docs.aws.amazon.com/ses/latest/dg/sending-email-suppression-list.html)
- [SESV2 — Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html)
- [parsedmarc documentation](https://domainaware.github.io/parsedmarc/)
- [checkdmarc — PyPI](https://pypi.org/project/checkdmarc/)
- [MxToolbox API](https://mxtoolbox.com/c/products/mxtoolboxapi)
- [Google Postmaster Tools API](https://developers.google.com/workspace/gmail/postmaster)
- [PyTest email test — MailSlurp](https://www.mailslurp.com/examples/pytest-read-email/)
- [Automated Email Testing — Mailtrap](https://mailtrap.io/automated-email-testing/)

**Korea Market:**
- [스티비 — SPF/DKIM 설정 이해하기](https://help.stibee.com/email/managing-sender/spf-dkim)
- [스티비 — DMARC 설정 이해하기](https://help.stibee.com/email/managing-sender/dmarc)
- [스티비 블로그 — G메일, 네이버 메일 수신 정책 변경 (1)](https://blog.stibee.com/gmail-sender-guidelines/)
- [스티비 블로그 — G메일, 네이버 메일 수신 정책 변경 (2)](https://blog.stibee.com/gmail-sender-guidelines-2/)
- [스티비 2025 이메일 마케팅 리포트](https://report.stibee.com/)
- [DMARC adoption lags in Asia-Pacific — CybersecAsia](https://cybersecasia.net/news/despite-exponentially-rising-email-fraud-threats-dmarc-adoption-lags-in-the-largest-firms/)
- [Red Sift Global DMARC Adoption Guide](https://redsift.com/guides/red-sifts-guide-to-global-dmarc-adoption)
- [EasyDMARC 2025 DMARC Adoption Report](https://easydmarc.com/blog/ebook/easydmarc-dmarc-adoption-report-2025/)
- [카카오메일 정책](https://mail.kakao.com/static/policy/policy3.html)
