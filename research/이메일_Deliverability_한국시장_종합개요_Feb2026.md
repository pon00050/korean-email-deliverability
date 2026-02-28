# 이메일 Deliverability — 한국 시장 종합 개요
## Industry Overview · The Profession · Minimum Skills · Minimum Viable Service · Market Demand · Entry Strategy

**Date:** 2026-02-28
**Purpose:** Single-document overview for someone building into email deliverability in the Korean market. Synthesizes all research files created in this project. All information cross-checked for currency as of Feb 2026 — stale data from earlier files is explicitly flagged and corrected.

**Source files synthesized:**
- `이메일_발송률_Email_Deliverability_Niche_Research_Feb2026.md`
- `이메일_발송률_MinimumSkills_DeepDive_Feb2026.md`
- `이메일_발송률_Deliverability_Skills_Positioning_Research_Feb2026.md`
- `한국_이메일_Deliverability_생태계_지도_Feb2026.md`
- `Korean_CRM_Email_Job_Market_Analysis_Feb2026.md`
- `이메일_발송률_KoreanJobMarket_EmailVsNotification_Feb2026.md`
- `이메일_Deliverability_Hub_기술스택_FeasibilityStudy_Feb2026.md`

---

## Table of Contents

1. [What Is Email Deliverability](#1-what-is-email-deliverability)
2. [The Global Industry](#2-the-global-industry)
3. [The Profession](#3-the-profession)
4. [Minimum Skill Set — Layer by Layer](#4-minimum-skill-set--layer-by-layer)
5. [The Korean Market](#5-the-korean-market)
6. [The Korean Ecosystem — Who Exists and Who Is Missing](#6-the-korean-ecosystem--who-exists-and-who-is-missing)
7. [What the Market Is Demanding](#7-what-the-market-is-demanding)
8. [Minimum Viable Service](#8-minimum-viable-service)
9. [Entry Strategy — How to Complement and Enter](#9-entry-strategy--how-to-complement-and-enter)
10. [Background Asset Stack — Where Everything Stacks for Maximum Advantage](#10-background-asset-stack)
11. [Rate and Revenue Guidance](#11-rate-and-revenue-guidance)
12. [Cross-Check Notes — What Changed Since Earlier Files](#12-cross-check-notes)

---

## 1. What Is Email Deliverability

Email deliverability is the discipline of ensuring that emails sent by a legitimate organization actually reach recipients' inboxes — as opposed to landing in spam folders, being blocked at the server level, or being silently discarded.

It is not the same as email marketing. A deliverability specialist does not write subject lines or design campaigns. They work on the infrastructure, authentication, and reputation layer that determines whether any email — marketing, transactional, or operational — gets through at all.

**The core problem:** 16.9% of legitimate marketing emails globally never reach inboxes. For Microsoft/Outlook specifically, inbox placement is only 75.6%, with 14% going directly to spam. A company can have perfectly written emails, a well-designed ESP setup, and still have 15–20% of their send volume disappearing.

**Why it became urgent 2024–2025:**
- Google enforced SPF/DKIM/DMARC for all bulk senders in **February 2024**
- Yahoo/AOL enforced the same in **February 2024**
- Microsoft followed for senders of 5,000+ messages/day in **May 2025**
- Naver Mail independently tightened authentication requirements in **2024**, requiring SPF + DKIM + DMARC + PTR for bulk senders
- These are enforced mandates, not recommendations. Non-compliant senders have mail rejected, not just filtered.

This shift converted deliverability from a specialist concern into a universal infrastructure requirement for any organization sending email at volume.

---

## 2. The Global Industry

### Market Size

| Year | Market Size | Notes |
|---|---|---|
| 2024 | $1.14B | Established baseline |
| 2025 | $1.24B | Post-enforcement acceleration |
| 2033 | $2.38B (projected) | 8.47% CAGR |

Source: Business Research Insights.

### The Bifurcated Market

The market is not a single tier. There is a deep structural split between commodity and expert work.

| Tier | What They Do | Rate |
|---|---|---|
| **Commodity** | Copy-paste SPF/DKIM/DMARC records per ESP docs; basic warmup | $15–$50/hr |
| **Mid-market** | Deliverability audits, ESP migration, bounce management | $50–$125/hr |
| **Expert** | Blocklist removal, ISP postmaster relations, sender reputation strategy, multi-domain architecture, DMARC report forensics, regulated-industry compliance | $150–$300/hr |

**AI is automating the commodity tier.** Basic record generation, spam score testing, email warmup (Warmy, Mailreach), and bounce/complaint rate monitoring are now built into most ESPs or automated by tools. This does not eliminate the profession — it eliminates the entry-level work and raises the baseline for expert work.

**What AI is NOT replacing:**
- ISP postmaster relationship management
- Blocklist removal negotiations (Spamhaus SBL is a human review process)
- Diagnosing systemic failures — why a specific domain at a specific volume to a specific inbox provider is failing
- Sender reputation strategy across complex domain/IP architectures
- Enterprise infrastructure design for high-volume, high-compliance senders

### Demand Data (as of Jan–Feb 2026)

- 438 open email deliverability consultant jobs on Upwork
- 20,555 email deliverability-related listings on ZipRecruiter
- In-house salaries: $64K/yr (entry, ZipRecruiter) → $117K/yr (consultant-level, Glassdoor)
- Senior freelance: $150–$300/hr

---

## 3. The Profession

### Who Practitioners Are

There is no formal credential for email deliverability. No CISSP equivalent, no national certification. Reputation is de facto credential — built through public writing, community contribution, documented results, and recognition by ISP engineers.

The professional body is **MAAWG (M3AAWG)** — the Messaging, Malware and Mobile Anti-Abuse Working Group. Membership is by invitation/application and includes both ISP-side engineers and sender-side specialists. For a Korean practitioner, MAAWG membership signals international-tier credibility.

**Secondary credentials (all minor, industry-specific):**
- Warmy Deliverability Certificate (open access, free)
- Klaviyo Deliverability Certificate (ESP-specific, respected for Klaviyo-ecosystem work)
- Braze Email Deliverability Skills Badge (enterprise-focused)

**Communities:**
- Email Geeks Slack — the primary on-ramp; largest community; all major ESPs have official channels
- Word to the Wise (wordtothewise.com, Laura Atkins) — the industry bible; read by ISP engineers
- Spam Resource (spamresource.com, Al Iverson) — practitioner-level reference
- Litmus Community — design + deliverability peer help

### Job Titles

Email deliverability does not yet have a standardized job title. Practitioners appear under:
- Email Deliverability Specialist / Consultant / Engineer
- Email Operations Specialist
- CRM Engineer (with deliverability scope)
- Marketing Technologist
- Email Platform Manager

**In Korean job postings:** The term does not exist explicitly. Deliverability knowledge is embedded in roles titled 마케팅 자동화, CRM 마케터, 이메일 마케팅 담당, 그로스 마케터. No Korean job posting has been found that uses 이메일 발송률 or 이메일 전달성 as a job requirement. This is both a gap and an opportunity.

### Career Entry Points

There are three realistic paths into deliverability professionally:

**1. From ESP customer support / operations**
Practitioners who worked inside an ESP (Mailchimp, SendGrid, Klaviyo) as support engineers or technical account managers, and developed domain expertise through repetitive exposure to deliverability incidents. This is the most common path globally.

**2. From email marketing generalist**
Marketers who became the de facto deliverability expert at their organization because nobody else handled it. They developed diagnostic skills from necessity. Many Korean CRM/이메일 마케터 roles work this way by default.

**3. From QA/systems engineering**
Technical practitioners who applied testing and systems methodology to email infrastructure. This path produces the most rigorous diagnosticians because they approach it like a QA engineer: define test cases, assert expected outcomes, investigate failures. Python scripting ability converts this into a scalable consulting operation.

Path 3 is the relevant one here and is the most underpopulated — especially in Korea.

---

## 4. Minimum Skill Set — Layer by Layer

Email deliverability knowledge is organized in three technical layers. Each layer builds on the previous. A Tier 1 practitioner executes checklists. A Tier 2 practitioner diagnoses failures. A Tier 3 practitioner designs architecture and manages ISP relationships.

The following covers what a practitioner needs to know at each tier, with emphasis on where Tier 1 and Tier 2 diverge — because the consulting value is entirely in Tier 2+.

---

### Layer 1: Authentication (SPF / DKIM / DMARC)

#### SPF (Sender Policy Framework)

**What it is:** A DNS TXT record that tells receiving servers which IP addresses are authorized to send email for your domain.

**Tier 1 checklist:** Publish the record, include your ESP's authorized range, verify with MXToolbox, confirm `~all` vs. `-all` softfail/hardfail designation.

**What separates Tier 2:**

The **10-lookup limit** (RFC 7208): SPF evaluation allows at most 10 DNS-querying mechanism lookups across the entire evaluation chain, including recursive `include:` statements. Many organizations publish a valid-looking SPF record that actually exceeds 10 lookups when fully resolved — triggering `permerror`, which most receivers treat as a hard fail. A tool that shows only the top-level record gives a false sense of compliance. Diagnosis requires walking the entire lookup tree.

The **void lookup limit of 2**: Almost entirely unknown. DNS queries returning NXDOMAIN or empty results are capped at 2 in the RFC. Exceeding this also triggers permerror.

**SPF forwarding failure**: Forwarding servers re-transmit using their own IP, not the original sender's. SPF always fails for forwarded mail. This is not a misconfiguration — it is a spec limitation. The correct mitigation is DKIM authentication plus DMARC alignment.

**Subdomain blind spot**: SPF policies do not cascade to subdomains. Each sending subdomain needs its own record. Subdomains that never send: `v=spf1 -all`.

**SPF flattening**: Converts `include:` chains to explicit `ip4:` ranges, reducing lookup count near zero. Risk: ESPs change their IP pools; flattened records go stale. Requires automated sync (AutoSPF, DMARCLY Safe SPF) to remain current.

#### DKIM (DomainKeys Identified Mail)

**What it is:** A cryptographic signature attached to outgoing messages. Unlike SPF, DKIM signatures travel with the message and survive forwarding as long as signed content is not modified.

**Tier 1 checklist:** Add the DKIM public key TXT record provided by the ESP, verify with MXToolbox, send a test and confirm `dkim=pass` in the Authentication-Results header.

**What separates Tier 2:**

**DKIM alignment — the DMARC connection**: DMARC checks whether the `d=` domain in the DKIM-Signature matches the visible `From:` header domain. Many ESPs sign with their own domain by default (e.g., `d=amazonses.com`), which passes raw DKIM but fails DMARC alignment for your domain. Custom DKIM signing (under your domain) must be configured explicitly — a step most users skip.

**Key rotation procedure (no-downtime, 6-step method):**
1. Generate new keypair with new selector name
2. Publish new public key to DNS — do NOT remove old key
3. Lower TTL on old selector to 300s several days before rotation
4. Configure sending system to sign with new selector
5. Monitor DMARC aggregate reports 24–48 hours to confirm new selector passes
6. After minimum 5–7 days grace period, remove old selector's DNS record

The grace period is critical: messages in MTA retry queues (up to 5 days) carry the old selector. Deleting the old DNS record within 24 hours — as most operators do — causes `dkim=permerror (no key for signature)` on perfectly valid in-flight messages.

**Key length**: 1024-bit RSA is computationally deprecatable; NIST deprecated it; Gmail prefers 2048+. 2048-bit keys can exceed DNS TXT record length limits — solution: split into multiple quoted strings in the TXT record.

**DKIM failure diagnosis — reading the header:**

| Header text | Meaning |
|---|---|
| `dkim=fail (body hash did not verify)` | Message body was modified in transit (link rewriter, antivirus gateway, mailing list software) |
| `dkim=permerror (no key for signature)` | Selector does not exist in DNS — key removed prematurely |
| `dkim=neutral (message not signed)` | ESP did not sign — signing not configured on sender side |

#### DMARC

**What it is:** Adds alignment requirement on top of SPF/DKIM; establishes sender policy (none/quarantine/reject); enables aggregate reporting.

**Tier 1 checklist:** Publish `_dmarc.yourdomain.com` TXT record with `p=none; rua=mailto:dmarc@yourdomain.com`. Use a commercial tool (EasyDMARC, dmarcian) to view reports.

**What separates Tier 2:**

The most common Tier 1 failure: `p=none` + `pct=5` is NOT a "soft start." The `pct=` tag only applies during the quarantine/reject phase. Setting `pct=5; p=none` does nothing different than `p=none` alone. Many practitioners believe they are gently ramping policy when they are not.

**Reading DMARC aggregate XML — the key distinction:**

The `policy_evaluated.dkim` and `policy_evaluated.spf` fields show DMARC **alignment** results, not raw SPF/DKIM protocol results. A source IP can have raw `dkim=pass` in `auth_results` but `dmarc dkim=fail` in `policy_evaluated` if the `d=` domain does not align to the `From:` domain. This is the single most misread field in DMARC reports.

**The alignment trap (most common Tier 1 failure mode):**
- SPF passes at protocol level (ESP authorized for your Return-Path domain)
- DKIM passes at protocol level (ESP signed with their domain)
- DMARC fails — neither result aligns to your visible `From:` domain
- A Tier 1 practitioner checks MXToolbox, sees SPF and DKIM both green, concludes "authentication is working." It is not.

**parsedmarc**: Open-source Python package. Parses RUA aggregate reports: IMAP fetch → decompress XML → structured JSON output. Replaces $50–$200/month commercial DMARC monitoring tools for small/medium senders. This is the primary tool in any self-built Korean deliverability dashboard.

---

### Layer 2: Reputation & Blacklists

#### Google Postmaster Tools (GPT) — ⚠️ CRITICAL UPDATE: v1 RETIRED SEPTEMBER 2025

**This is the most important currency cross-check in this document.** Google Postmaster Tools v1 was retired on **September 30, 2025**. The Domain Reputation and IP Reputation dashboards — the core diagnostic tools of the platform — **no longer exist in v2.**

v2 retains: spam rate dashboard, authentication pass rates, TLS encryption rate.
v2 does NOT have: domain reputation (High/Medium/Low/Bad), IP reputation, inbox vs. spam breakdown.

A practitioner who still talks about "checking domain reputation in Postmaster Tools" is demonstrably out of date. The v2 API (launching end of 2025) will eventually restore v1 functionality.

**Spam Rate thresholds (the primary remaining v2 signal):**

| Rate | Status | Action |
|---|---|---|
| < 0.08% | Safe zone | Monitor |
| 0.08–0.10% | Approaching ceiling | Watch trend |
| 0.10–0.30% | Danger zone | Immediate hygiene and content audit |
| ≥ 0.30% | Policy violation | Emergency remediation |

**Critical non-obvious point:** Gmail calculates spam rate against inbox-delivered mail only — spam-foldered mail is excluded from the denominator. A clean-looking GPT spam rate can mask a severe inbox placement crisis. If 40% of your mail is going to spam folder, those complaints are excluded from GPT rate calculation.

#### Microsoft SNDS

IP-centric reputation monitoring for Outlook.com, Hotmail, and Microsoft 365. Unlike GPT (domain-centric), SNDS centers on IP addresses — essential for dedicated IP infrastructure. 2025 update: Microsoft now requires Microsoft account authentication to manage IP ranges.

**Enforcement:** May 2025 — Microsoft began actively enforcing bulk sender requirements for 5,000+ msg/day senders.

SNDS and GPT used in combination give coverage of Gmail + Outlook/Hotmail — the two inbox providers with the most structured feedback. Naver and Kakao provide neither equivalent.

#### Blacklists — What a Practitioner Must Know

The blacklist landscape is not a single list. There are different list types by operator, by listing criterion, and by delisting difficulty.

| Blacklist | What Triggers Listing | Delisting |
|---|---|---|
| **Spamhaus SBL** | Known spam operations | Manual human review — hardest |
| **Spamhaus CSS** | High-volume spam, snowshoe patterns | Manual review; auto-expires sometimes |
| **Spamhaus XBL** | Compromised machines, botnet | Fix exploit; often auto-delists 24–48hr |
| **Spamhaus PBL** | End-user/broadband IPs (not for direct-to-MX) | Self-service — policy-based, not punitive |
| **Spamhaus DBL** | Domains in spam content/URLs | Manual contact |
| **Barracuda BRBL** | User-reported spam at Barracuda-protected networks | Self-service |
| **SpamCop** | Aggregated user reports | Auto-expires 24–48hr |
| **SURBL/URIBL** | Domain used in spam URLs | Manual contact |

**Korean enterprise relevance**: Barracuda hardware is prevalent in Korean enterprise and government mail gateways. A sender blocked by Barracuda may be blocked from reaching a disproportionate share of Korean enterprise inbox targets. No Korean-language Barracuda reputation management content exists.

**Non-obvious listing triggers:**
- Snowshoe patterns (rotating IPs to distribute volume) are themselves the signature Spamhaus CSS detects
- Reverse DNS mismatch (PTR not matching A record) is an automatic PBL candidate — a common problem with Korean cloud infrastructure
- Recycled spam traps: formerly active addresses converted to traps after 6–12 months of inbox provider inactivity — do not bounce, absorb mail silently; the signature is zero bounces AND zero engagement on a cohort

---

### Layer 3: List Hygiene & Sending Program

#### Bounce Management — 4 Categories, Not 2

Most practitioners know: hard bounce = bad address; soft bounce = temporary. There is a third category that separates Tier 2 practitioners:

**Block bounce**: Rejection based on sender reputation, blocklist, content filter, or authentication failure. Returns a 5xx or 4xx code, but the problem is with the **sender**, not the **recipient address**. Treating a block bounce as a hard bounce and suppressing the recipient address hides the real problem. A Tier 1 practitioner creates a growing suppression list masking an infrastructure failure. A Tier 2 practitioner reads the enhanced SMTP status code and diagnoses the sender-side issue.

**Key SMTP enhanced status codes:**

| Code | Meaning |
|---|---|
| `550 5.1.1` | User unknown → suppress address |
| `550 5.7.1` | Policy rejection → **investigate first** (may be block bounce, not bad address) |
| `550 5.7.26` | Gmail DMARC rejection → fix authentication, not the list |
| `451 4.7.0` | Gmail: reputation not yet established → reduce send volume, do not retry aggressively |

#### Gmail February 2024 Enforcement — Binary Requirements

**These are hard gates, not recommendations:**
- SPF or DKIM authentication — failure = rejection
- DMARC at minimum `p=none`
- Valid PTR (rDNS) for sending IP
- One-click unsubscribe (RFC 8058 List-Unsubscribe-Post header)
- TLS for all transmission

**One-click unsubscribe is widely misunderstood:** The requirement is not just an unsubscribe link in the email body. It requires the `List-Unsubscribe-Post` header so that inbox clients can present a one-click "Unsubscribe" button. Senders who lack this header have recipients who cannot easily unsubscribe — and those recipients hit "spam" instead, directly inflating complaint rate.

#### Engagement Segmentation — the Foundation of List Health

| Segment | Definition | Action |
|---|---|---|
| Tier A — Active | Opened or clicked within last 90 days | Full send cadence |
| Tier B — Warm | Last engagement 91–180 days ago | Full send; monitor complaint rate separately |
| Tier C — At Risk | Last engagement 181–365 days ago | Reduced frequency; trigger re-engagement |
| Tier D — Lapsed | No engagement in 365+ days | Do not mail until re-engagement attempted |

**Apple Mail Privacy Protection caveat (since iOS 15, 2021):** Open tracking is unreliable for Apple Mail users. "Active" segments defined purely by opens use inflated data. Cross-reference click data, purchase activity, or login events for accurate engagement measurement.

**Sunset policy:** Only ~24% of email programs have a formal sunset policy. For a Korean consulting context, this is both a diagnostic question and a consulting entry point. Default recommendation: 180-day re-engagement trigger, 365-day suppression.

#### The 2년 수신동의 재확인 Obligation (Korean-specific, almost universally unknown)

Under 정보통신망법 시행령, bulk email senders to Korean recipients must re-confirm consent every **2 years**. Penalty: up to ₩30M. Research indicates this obligation is broadly unknown and almost universally violated by Korean bulk senders. This is a significant regulatory consulting entry point — the obligation is real, the violation rate is near-total, and no Korean service currently helps senders manage it.

---

## 5. The Korean Market

### DMARC Adoption — South Korea vs. APAC

| Country | DMARC Adoption (Global 2000) |
|---|---|
| Australia | 71% |
| Singapore | 46.2% |
| Thailand | 17.6% |
| Japan | 7.4% |
| China | 4.2% |
| **South Korea** | **1.8% — dead last in APAC** |

Source: Proofpoint / Red Sift Global DMARC Adoption Guide.

Over 50% of Korean public companies have no DMARC record at all. Only 10.1% have implemented `p=reject`. This is the structural backdrop for everything else.

### Naver Mail Policy — July 2024 Update

Following Gmail's February 2024 enforcement, Naver Mail tightened its own bulk sender policy in 2024:

- **SPF**: Required
- **DKIM**: Required
- **DMARC**: Required (recommended `p=none` minimum)
- **PTR/rDNS**: Required

Naver Mail also:
- Applies aggressive rate-limiting to international senders without Korean IP reputation
- Bans using @naver.com as sender address from non-Naver servers
- Operates opaque spam filtering with no equivalent to Google Postmaster Tools — zero public visibility into why mail fails at Naver

Naver Mail + Gmail together = 70–80% of all Korean email recipients. Both now enforce authentication. A Korean bulk sender who fails either has lost the majority of their deliverable market.

### Kakao/Daum Mail

- IMAP supported: **yes** — `imap.kakao.com:993`; mandatory app passwords since January 2025
- Published bounce code: `554 5.7.1 DAS50 [IP]` = Daum Anti-Spam rejected the sending IP
- No published DMARC/DKIM enforcement documentation; SPF-gated

### Korean Channel Hierarchy (CRM Job Postings, Jan–Feb 2026)

Email is not the primary channel in Korean CRM — it is fifth. This shapes the market:

| Channel | Approximate effectiveness signal | Korean CRM job prevalence |
|---|---|---|
| 앱 푸시 (App push) | ~95% open rate | High |
| 카카오 알림톡 | ~90% conversion rate | Very high |
| SMS/LMS | ~80% open rate | High |
| 이메일 | ~65–70% inbox (when working) | Low — embedded in CRM 마케터 role |

**Implication:** Korean job postings rarely emphasize email deliverability because email is not the primary revenue channel. But **automated email achieves 3.8× click rate above baseline** (Stibee 2025 data on 636,000 emails). The channel is underused and underperforming — not because it doesn't work, but because no one in Korea is optimizing the infrastructure. This is the latent demand.

---

## 6. The Korean Ecosystem — Who Exists and Who Is Missing

### Regulatory Layer

| Institution | Role | What They Do | Gap |
|---|---|---|---|
| **KISA (한국인터넷진흥원)** | Anti-spam, 화이트도메인 registry (until June 2024), RBL operator | Publishes spam guidelines, operates `spamlist.or.kr` RBL, coordinates with MBPs | No managed services for senders; entirely self-serve |
| **방통위 (방송통신위원회)** | 정보통신망법 enforcement | Can fine senders for spam violations | No proactive compliance advisory |
| **PIPC (개인정보보호위원회)** | 개인정보보호법 enforcement | Consent management, data protection | No guidance specifically on email consent management |

**⚠️ CRITICAL UPDATE — 화이트도메인 TERMINATED:**
KISA's 화이트도메인 registry, which allowed Korean bulk senders to register their domains for spam filter bypass at domestic inbox providers, was **terminated on June 28, 2024**. Earlier files in this project (`한국_이메일_Deliverability_생태계_지도_Feb2026.md`) describe 화이트도메인 as an active institutional bridge — this is stale. As of mid-2024, senders must contact Naver and Kakao individually to address deliverability issues; there is no central clearinghouse.

Post-termination gap: The institutional managed service that a private entity could build is now more needed than before — the one mechanism that helped bulk senders navigate Korean inbox providers has been removed, leaving only self-serve paths.

**KISA RBL (`spamlist.or.kr`)**: Still operational as a standard DNSBL. Queryable with 3 lines of Python using `dnspython`. Korean senders appearing on this list will be blocked by most Korean enterprise mail gateways and ISPs.

### Domestic ESPs

| ESP | Role | Deliverability Support |
|---|---|---|
| **스티비 (Stibee)** | Korea's dominant email marketing SaaS (~Mailchimp equivalent) | Most proactive on deliverability education; only real Korean-language deliverability resource by default; vendor content, not independent consulting |
| **타손 (TasOn)** | Marketing automation platform | No documented deliverability support depth |
| **NHN Cloud (Naver Cloud)** | Cloud infrastructure including SMTP/SES equivalent | No deliverability advisory layer |
| **Channel.io** | B2B messaging + transactional email | Significant transactional email sender; no deliverability specialty |
| **Naver Works** | Enterprise mail platform | Enhanced spam blocking announced 2024 |

**The pattern across all domestic ESPs:** "Sending tools only." None offer inbox placement monitoring, blacklist alerts, DMARC reporting, or proactive deliverability advisory. Support responses to deliverability problems stop at "check your SPF/DKIM records."

### Global Deliverability Tools — Korean Coverage Gap

| Tool | Function | Naver Coverage | Kakao Coverage |
|---|---|---|---|
| GlockApps | Inbox placement testing (seed panel) | **ZERO seed accounts** | **ZERO seed accounts** |
| Validity/Everest | Inbox placement, sender certification | **None** | **None** |
| Litmus | Email rendering + spam filter testing | **None** | **None** |
| Google Postmaster Tools | Gmail reputation + spam rate | Not applicable | Not applicable |
| Microsoft SNDS | Outlook reputation | Not applicable | Not applicable |

No existing commercial tool anywhere in the world can test whether a message reaches Naver Mail or Kakao inbox vs. spam. This is the single largest structural gap. A provider with Korean seed accounts — actual @naver.com and @kakao.com email addresses registered to real accounts — would provide data that no global competitor can replicate without local presence.

### Missing Layers — The Three Structural Gaps

**Missing Layer 1: Between Regulators and Senders**
KISA/방통위/PIPC publish rules and can levy fines. No private entity translates these regulatory requirements into actionable, managed technical services. The "get compliant" journey is entirely self-serve. The 화이트도메인 termination made this worse. Examples of what doesn't exist: managed 화이트도메인 registration service (now defunct but the institutional relationship work is similar); 2년 수신동의 재확인 management; pre-audit compliance checking before 방통위 complaints trigger formal investigation; DMARC policy ramp-up advisory for senders trying to reach `p=reject`.

**Missing Layer 2: Between ESPs and Senders**
When a Korean ESP user has a deliverability problem the ESP support team cannot solve, there is no escalation path. No ESP deliverability partner program exists in Korea. Globally, deliverability consultants fill this role as official or unofficial ESP partners — Mailchimp, Klaviyo, and SendGrid all have partner directories. No Korean ESP (Stibee, TasOn, NHN Cloud) has an equivalent.

**Missing Layer 3: Between Inbox Providers and Senders**
Gmail has Google Postmaster Tools (though v2 has reduced scope — see Section 12). Microsoft has SNDS. Naver and Kakao have nothing. The feedback loop between Korean inbox providers and Korean senders is effectively broken — senders have no idea why mail fails at Naver until they see open rate collapse. DMARC aggregate reports from Naver and Kakao (if they send RUA reports) are an underutilized proxy signal that most Korean senders ignore.

---

## 7. What the Market Is Demanding

### Explicit vs. Latent Demand

Korean market demand is almost entirely **latent** — the problem exists and is growing, but the buyer does not yet have a named category for the solution. This has implications for how to enter (education-led) and how to price (value-based, not market-rate).

### Explicit demand signals

1. **Gmail + Naver Mail enforcement (2024)**: Korean companies receiving 550/DMARC rejection codes from Gmail are actively trying to fix this. The search is "why is Gmail blocking my email" not "I need a deliverability consultant" — but the underlying need is deliverability consulting.

2. **Korean B2B SaaS expanding internationally**: Korean tech companies entering US/Japanese/European markets face inbox placement failures from zero IP/domain reputation, encoding issues with Korean character sets, and authentication gaps. This is a real operational pain point for companies in Series B+ growth mode.

3. **Stibee's content strategy**: The only Korean-language deliverability content that exists is Stibee's blog. They have published multiple pieces on Gmail/Naver policy changes. Their content is vendor-focused; independent advisory content has zero competition.

4. **Tax/legal notification email**: Korean tax SaaS platforms (세금계산서 issuance, 국세청 연동, 세무사랑) send legally significant transactional emails. A missed tax deadline notification or e-invoice receipt is not a missed marketing email — it has legal and financial consequences. These senders have high willingness to pay for reliability.

5. **Enterprise Korean companies**: Large 그룹웨어 users (Samsung, Hyundai, SK affiliates) using internal mail relays plus marketing email systems have the same authentication gaps as SMBs, plus the Barracuda enterprise gateway concern. No Korean consultant addresses this.

### What Korean CRM Job Postings Actually Signal

Analysis of 15+ Korean CRM job postings (Jan–Feb 2026):
- Email deliverability terminology: absent from 100% of postings
- Email channel prioritization: lower than 앱 푸시, 카카오 알림톡, SMS in nearly all postings
- But: B2B SaaS sectors show 83% of postings requiring email channel competency
- Newsletter/media companies: email remains the primary channel

**The B2B SaaS sector is the best entry market** for email-focused work in Korea: decision-makers speak English, understand global best practices, have Gmail-heavy recipient bases, and measure deliverability impact directly in product metrics.

### The Content Gap

No Korean-language practitioner content exists at diagnostic depth on any of the following:
- SPF lookup tree diagnosis
- DKIM key rotation procedure
- DMARC aggregate XML parsing
- Multi-ESP selector management
- Alignment failure forensics
- Google Postmaster Tools v2 changes (Sep 2025 reputation dashboard retirement)
- Spam trap taxonomy (pristine/recycled/typo)
- IP warming methodology
- Blacklist removal beyond clicking "delist"
- Sunset policy design
- Bounce code reference with enhanced status codes
- Naver Mail filtering behavior
- Barracuda enterprise gateway reputation management (Korean enterprise-specific)

Publishing Korean-language content on any of these topics fills a space that is currently completely empty.

---

## 8. Minimum Viable Service

What can be offered immediately with current skills, with zero client history?

### Tier 0 — The Demonstration Project (precedes paid work)

A Python script using `parsedmarc` + `checkdmarc` + `dnspython` that:
1. Accepts a domain as input
2. Validates SPF, DKIM, DMARC records and flags issues
3. Parses a DMARC aggregate report XML and outputs human-readable summary
4. Queries KISA RBL (`spamlist.or.kr`) and major global blacklists (Spamhaus ZEN)
5. Outputs structured Markdown audit report

This is the proof-of-concept that establishes Python-capable deliverability positioning. No equivalent tool exists in Korean.

### Service 1 — The Deliverability Audit (₩300K–₩800K per engagement)

A structured assessment of a single organization's current authentication, reputation, and list health status. Deliverable: a Korean-language audit report with specific remediation steps, prioritized by risk.

**Components:**
- SPF record analysis: lookup tree, void lookup count, flattening recommendation
- DKIM: key length, selector architecture, signing domain alignment
- DMARC: current policy, rua/ruf configuration, report interpretation (if reports are available)
- DNS hygiene: PTR/rDNS, MX configuration, DMARC subdomain policy
- Blacklist check: Spamhaus ZEN, Barracuda, KISA RBL, SpamCop, MXToolbox 200+ list scan
- Google Postmaster Tools review (if Gmail traffic exists)
- Microsoft SNDS check (if applicable)
- List hygiene assessment: bounce rate, complaint rate, last engagement segmentation, unsubscribe infrastructure
- One-click unsubscribe compliance (Gmail Feb 2024 requirement)
- 2년 수신동의 재확인 compliance status (Korean legal requirement)

**Minimum viable delivery:** One-person, 4–8 hours work per audit. Can begin with no staff.

### Service 2 — Authentication Implementation (₩500K–₩1.5M per engagement)

For clients who need SPF/DKIM/DMARC configured from scratch or repaired:
- Custom DKIM signing configuration on their ESP
- SPF record rebuild with lookup optimization
- DMARC policy ramp plan (`p=none` → `p=quarantine` → `p=reject` over 60–90 days)
- parsedmarc setup for ongoing DMARC report monitoring
- Documentation and handoff in Korean

### Service 3 — Ongoing Monitoring Retainer (₩150K–₩500K/month)

Automated monitoring using Python scripts + parsedmarc + MXToolbox API:
- Daily blacklist check (any listing triggers alert)
- Weekly DMARC aggregate report processing (summary of pass/fail rates, unauthorized senders, new sending IPs)
- Monthly deliverability health report in Korean
- Incident response for any blocking events

**Scalable:** A monitoring script running on a ₩5,000/month VPS can cover 20–30 clients simultaneously. This is where the consulting practice scales without proportional time cost.

### Service 4 — Naver/Kakao Inbox Placement Testing (uniquely Korean)

Using a panel of seed accounts at Naver Mail and Kakao Mail (minimum: 5 accounts each), checked via IMAP (Naver: `imap.naver.com:993`; Kakao: `imap.kakao.com:993`; app passwords required since Nov 2024 for Naver, Jan 2025 for Kakao):

For each test send:
- Inbox vs. spam folder placement at Naver Mail
- Inbox vs. spam folder placement at Kakao/Daum Mail
- Authentication-Results header extraction (DKIM/SPF pass/fail as seen by Naver/Kakao)
- Time-to-delivery measurement

**This is the data no global tool can provide.** A 10-account panel (5 Naver + 5 Kakao) is a buildable MVP for a single developer. No commercial competitor anywhere in the world offers this.

### Service 5 — The Regulatory Compliance Layer (₩500K–₩2M per engagement)

Managed compliance for 정보통신망법 + 개인정보보호법:
- Audit of current email consent records and documentation
- 2년 수신동의 재확인 workflow implementation
- 옵트아웃 (opt-out) mechanism compliance review
- Pre-audit checklist before 방통위 complaint-triggered investigation
- Documentation package for PIPC review if data breach or complaint occurs

This requires no technology beyond document management and process design. The value is knowing what the regulation requires and translating it into operational workflow.

---

## 9. Entry Strategy — How to Complement and Enter

### Phase 1: Foundation (Now — 3 months)

**Goal:** Be findable and credible before acquiring first client.

**Actions:**
1. **Publish Korean-language content on Medium, Velog, or personal blog**
   - Topic 1: "한국 기업의 이메일이 스팸함으로 가는 진짜 이유 — DMARC란 무엇인가"
   - Topic 2: "네이버 메일 2024년 정책 변경이 이메일 마케터에게 미치는 영향"
   - Topic 3: "SPF 레코드 10개 제한 — 한국 마케터가 모르는 이메일 발송 장애물"
   - Topic 4: "구글 포스트마스터 툴즈 v2 변경사항 — 2025년 9월 이후 무엇이 달라졌나"
   - Topic 5: "이메일 반송 코드 완전 해설 — 550 5.7.26이 뭘 의미하는지 아는가"
   - These topics have zero Korean-language coverage. First-mover captures all search traffic.

2. **Build the demonstration tool**
   - Python script: domain → audit report (SPF tree walk, DMARC policy, KISA RBL check, blacklist check)
   - Publish on GitHub; link from blog posts
   - This creates a tangible artifact that demonstrates Python-capable deliverability work

3. **Naver contact outreach**
   - Initial contact to understand Naver Mail's current deliverability documentation and policy for bulk senders
   - This is ISP relationship development — the single most differentiated skill at Tier 3

4. **Email Geeks Slack**: Join; introduce as Korean-market specialist; begin building international peer network

### Phase 2: First Clients (3–9 months)

**Entry targets:**
- Korean B2B SaaS companies with Gmail-heavy customer bases (target: 20–50 employees, Series A–B)
- Newsletter operators on Stibee who have seen open rate decline post-2024 policy changes
- Korean ESPs or digital agencies as referral partners (pitch: you handle deliverability issues their team cannot resolve)
- Companies that recently received Gmail 550 5.7.26 rejection codes — they are actively searching for a solution

**First client acquisition:**
- A free mini-audit (15-minute scan using the demonstration tool) generates the first conversation
- First paid audit (₩300K–₩500K) produces the first written case study
- One successful case study in Korean is sufficient to unlock referral-based growth

### Phase 3: Institutional Positioning (12–36 months)

**Goal:** Position as the entity that fills the structural gap left by 화이트도메인 termination.

**CSA model analog:** Germany's Certified Senders Alliance (CSA), founded by eco + DDV in 2004, operates a whitelist that German inbox providers (GMX, Web.de, T-Online) honor. Korean analog: a private certification body with KISA as institutional partner + Naver + Kakao as whitelist recipients. This is a 2–3 year institutional project, not a 90-day consulting play — but it begins with the Phase 1 public reference assets.

**Key institutional steps:**
1. Establish KISA relationship — start as a public contributor to anti-spam policy discussion
2. Become the reference point for Korean-language deliverability content (Phase 1 content → SEO → inbound)
3. Develop ESP partnerships (Stibee, TasOn) — formalized referral/escalation relationship
4. Naver/Kakao inbox placement panel — the proprietary data asset that no competitor can replicate
5. Certification layer — once institutional trust is established with MBPs and KISA, formalize sender certification program

---

## 10. Background Asset Stack

Where existing background assets create compounding advantages:

| Asset | Deliverability Advantage | Tier Unlocked |
|---|---|---|
| **MAcc degree** | Understands regulatory record retention, audit trails, compliance documentation — can advise regulated-industry clients on the intersection of compliance obligations and delivery infrastructure | Premium regulated industries |
| **US CPA firm experience** | Understands US financial regulatory environment (SEC, FINRA); credible to CFOs and controllers who are budget owners for enterprise email infrastructure | US-registered financial companies, accounting technology vendors |
| **Bilingual Korean/English** | Only bilingual deliverability specialist in a market with 1.8% DMARC adoption and zero specialist supply; can serve Korean companies expanding internationally AND western companies targeting Korean audiences; can produce Korean-language audit reports; understands Naver Mail filtering behavior | Korea-market monopoly — effectively uncontested |
| **Functional Chinese** | China has 4.2% DMARC adoption; Chinese fintech expanding globally faces identical problems | Secondary East Asian market |
| **QA/API testing (Python/pytest/Postman)** | Enables automated programmatic deliverability testing; CI/CD email flow integration; custom monitoring dashboards; scalable multi-client operations (50+ clients on one script) | Technical differentiation; premium for automation delivery |
| **ISTQB CTFL** | Provides professional framework for audit methodology: risk-based prioritization, acceptance criteria, defect lifecycle; deliverability audit reports structured as formal QA documents vs. informal advisory | Credibility with technical organizations |
| **Korean tax software ecosystem knowledge** | Specific product knowledge of Korean tax SaaS sending patterns; understands 세무사 workflow; direct insider access if 전산법인 role materializes | Korean tax SaaS vertical — unserved |
| **Healthcare social cooperative (이사장)** | Firsthand regulated healthcare communication infrastructure; PIPA compliance context; founder credibility with Korean health startups | Healthcare SaaS vertical |

### Niches Where All Assets Stack

| Niche | Why Uncontested |
|---|---|
| Korean fintech → US market expansion | MAcc + CPA firm + Korean bilingual + QA/API: advises on US financial email compliance + Korean sender reputation repair + Python automation. No other consultant combines all four. |
| Korean tax SaaS platforms (전산법인, 세금계산서) | Korean tax ecosystem + bilingual + QA/API + MAcc: only person who understands both the product context AND can build monitoring AND can advise in Korean AND understands the legal significance of email non-delivery. |
| Korean healthcare SaaS / digital health | 사협 founder experience + Korean bilingual + PIPA knowledge + QA/API: healthcare deliverability with Korean regulatory compliance + technical build capability. |
| East Asian B2B SaaS going global | Korean + functional Chinese + QA/API + Korean market knowledge: pan-East-Asia deliverability advisory. No Western consultant can serve this; no Korean consultant has the technical depth. |

---

## 11. Rate and Revenue Guidance

| Positioning | Rate | Notes |
|---|---|---|
| Commodity (avoid) | $15–$50/hr | SPF/DKIM/DMARC setup only; global Fiverr/Upwork competition |
| Mid-market baseline | $75–$125/hr | Deliverability audit + monitoring setup |
| Korea-specialist | $100–$200/hr | Bilingual Korean/English; Naver Mail expertise; no comparable supply |
| Regulated-industry specialist | $150–$300/hr | Financial services, healthcare; compliance overlay |
| QA-methodology + automation | $150–$250/hr | Programmatic monitoring build; CI/CD integration; DMARC pipelines |
| All assets combined (target tier) | $150–$300/hr | Korean regulated fintech/tax SaaS; unique combination cannot be replicated |

**Korean market conversion (assuming $150–$200/hr at ~130 KRW/USD):**
- Deliverability audit: ₩400K–₩800K per engagement
- Implementation project: ₩800K–₩2M per engagement
- Monthly retainer: ₩200K–₩600K/month
- Naver/Kakao inbox placement test: ₩150K–₩300K per test

At 3–4 clients/month at audit rates, this is a viable side income during the Embassy waiting period (May–July 2026). At 8–10 ongoing retainer clients, this is a standalone income stream.

---

## 12. Cross-Check Notes — What Changed Since Earlier Files

The following table documents where earlier project files contained information that has since been superseded. The synthesis above uses the corrected information throughout.

| Topic | Earlier File | Stale Information | Corrected Status |
|---|---|---|---|
| **KISA 화이트도메인** | `한국_이메일_Deliverability_생태계_지도_Feb2026.md` | Describes 화이트도메인 as an active institutional bridge between bulk senders and Naver/Kakao | **Terminated June 28, 2024.** Post-termination, senders contact Naver/Kakao individually. No central clearinghouse. |
| **Google Postmaster Tools domain/IP reputation** | `이메일_발송률_Deliverability_Skills_Positioning_Research_Feb2026.md` | References domain reputation (High/Medium/Low/Bad) as a diagnostic tool | **Retired September 30, 2025** in GPT v2. Domain reputation and IP reputation dashboards no longer exist. |
| **Gmail enforcement level** | `이메일_발송률_Email_Deliverability_Niche_Research_Feb2026.md` | Describes enforcement as tightening | **November 2025 update**: Gmail now issues active rejection codes (4.7.x temporary, 5.7.x permanent) for non-compliant senders — no longer warnings only |
| **Microsoft enforcement** | Earlier files general | Describes enforcement as forthcoming/announced | **Active since May 5, 2025** for senders of 5,000+ messages/day |
| **Naver IMAP app passwords** | Hub feasibility study | Mentions app passwords as a configuration option | **Mandatory since November 2024** for all IMAP access to Naver Mail. No alternative. |
| **Kakao IMAP app passwords** | Hub feasibility study | Same | **Mandatory since January 2025** for all IMAP access to Kakao Mail. |

---

## Summary: The One-Page Version

**The industry:** Email deliverability is a $1.14B → $2.38B market built on the universal enforcement (2024–2025) of email authentication standards by Google, Yahoo, Microsoft, and Naver. 16.9% of legitimate commercial email globally fails to reach inboxes. The expert consulting tier (ISP relationship management, blocklist removal, authentication architecture, programmatic monitoring) is undersupplied globally and essentially nonexistent in Korea.

**The Korean opportunity:** South Korea has 1.8% DMARC adoption — dead last in APAC. No Korean-language email deliverability specialist exists. No Korean job title names this skill. The only Korean-language deliverability content comes from Stibee (vendor blog, not independent advisory). KISA's 화이트도메인 registry was terminated June 2024 — removing the one institutional mechanism that helped senders navigate Korean inbox providers. Naver Mail + Gmail together = 70–80% of Korean email recipients, and both now enforce authentication.

**The minimum skill set:** Authentication (SPF/DKIM/DMARC) at diagnostic depth (not just checklist), reputation monitoring (GPT v2 + SNDS + blacklist taxonomy), list hygiene (4-category bounce management, engagement segmentation, sunset policy), plus Python scripting for automation. The QA/API track already in progress produces the exact toolset needed.

**The minimum viable service:** A deliverability audit (authentication + blacklist + list health + Korean regulatory compliance status), deliverable as a Korean-language report. ₩300K–₩800K per engagement. Buildable immediately. The Naver/Kakao inbox placement panel (10 seed accounts checked via IMAP) is the uniquely Korean component that no global competitor can offer.

**The entry:** Public Korean-language content on topics with zero existing coverage → builds findability → generates inbound from Korean senders experiencing Gmail/Naver blocking events → first free mini-audit → first paid audit → first retainer → referral-based growth. Phase 1 (content + demonstration tool) can begin now, in parallel with Embassy/전산법인 primary tracks.

**The long-term structural play:** The 3-layer gap (regulatory ↔ senders, ESP ↔ senders, inbox providers ↔ senders) plus the 화이트도메인 termination creates the conditions for a Korean Certified Senders Alliance equivalent — a private certification body operating between KISA, Naver/Kakao, and Korean bulk senders. This is a 2–3 year institutional project, not a 90-day consulting play. The Phase 1 content assets are the first step.

---

*Synthesized from 7 research files created Feb 2026. All information cross-checked as of Feb 28, 2026. Key updates reflected: KISA 화이트도메인 termination (June 2024), Naver Mail authentication policy (July 2024), Google Postmaster Tools v2 retirement of reputation dashboards (September 2025), Gmail active enforcement codes (November 2025), Microsoft enforcement effective date (May 2025).*
