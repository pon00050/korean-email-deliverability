# 이메일 발송률 / Deliverability — Minimum Skills Deep Dive
## Practitioner Knowledge Map: Layers 1–3

**Date:** 2026-02-28
**Purpose:** Building email deliverability consulting expertise for the Korean market. This document covers the minimum skill set at practitioner depth — distinguishing checklist execution (Tier 1) from diagnostic capability (Tier 2) from expert mastery (Tier 3).
**Source research:** 3 dedicated deep-research agents, 80+ primary sources, Feb 28 2026.

---

## Table of Contents

1. [Layer 1: Authentication (SPF / DKIM / DMARC)](#layer-1-authentication)
2. [Layer 2: Reputation & Blacklists](#layer-2-reputation--blacklists)
3. [Layer 3: List Hygiene & Sending Program](#layer-3-list-hygiene--sending-program)
4. [Cross-Layer: Top Non-Obvious Failure Modes](#cross-layer-top-non-obvious-failure-modes)
5. [Korean Market Gap Summary](#korean-market-gap-summary)
6. [Sources](#sources)

---

## Layer 1: Authentication (SPF / DKIM / DMARC)

*Source file: `06_Reference/Email_Authentication_SPF_DKIM_DMARC_Practitioner_Reference.md`*

---

### SPF — Practitioner Knowledge Map

**What SPF does:** SPF (Sender Policy Framework, RFC 7208) allows a domain owner to publish, via DNS TXT record, a list of authorized sending IP addresses. Receiving servers check the envelope sender (MAIL FROM / Return-Path) against this record.

#### Tier 1 (Checklist Executor)
- Adds a TXT record like `v=spf1 include:_spf.google.com include:sendgrid.net ~all`
- Knows `~all` = softfail, `-all` = hardfail
- Uses ESP docs to copy-paste `include:` statements
- Verifies via MXToolbox; knows only one SPF TXT record per domain is allowed

#### Tier 2 (Diagnostic)

**Mechanism lookup cost table:**

| Mechanism | What it does | DNS lookup cost |
|---|---|---|
| `ip4:x.x.x.x/cidr` | Directly authorizes IPv4 range | 0 |
| `ip6:x::/cidr` | Directly authorizes IPv6 range | 0 |
| `a` / `a:domain` | Resolves A/AAAA record | 1 |
| `mx` / `mx:domain` | Resolves MX records + A/AAAA for each host | 1 + N per MX host |
| `include:domain` | Evaluates target domain's SPF record recursively | 1 + recursive |
| `exists:domain` | A record lookup, matches if any A record exists | 1 |
| `redirect=domain` | Replaces entire SPF policy with target's policy | 1 + recursive |

**The 10-lookup limit and void lookups:**
- RFC 7208 caps DNS-querying mechanisms at 10 total across the entire evaluation chain, including recursive includes
- Exceeding 10 triggers **permerror** — most receivers treat as fail
- **Void lookup limit of 2** (almost entirely unknown secondary constraint): DNS queries returning NXDOMAIN or empty results are capped at 2; exceeding this also triggers permerror
- A single `include:salesforce.com` can internally consume 3–4 lookups; tools that show your record in isolation give a false sense of compliance

**SPF flattening:**
- Converts `include:` chains into explicit `ip4:` ranges, reducing lookup count to near zero
- Risk: ESPs change their IP pools without announcement — flattened records go stale
- Solution: automated flattening services (AutoSPF, DMARCLY Safe SPF) continuously sync ESP IP ranges
- Manual flattening without automation is a ticking clock

**Forwarding failure — structural design limitation:**
- Forwarding servers re-transmit using their own IP, not the original sender's → SPF fails
- Not a misconfiguration — a spec limitation; the correct mitigation is DKIM + DMARC relaxed alignment
- Different forwarding providers handle Return-Path differently (Outlook/iCloud preserve original; Gmail/Yahoo substitute their own)

**Subdomain blind spot:**
- SPF policies do NOT cascade to subdomains
- Each sending subdomain needs its own SPF record
- Subdomains that never send email: `v=spf1 -all` to prevent spoofing

#### Tier 3 (Expert)
- **Multiple SPF record conflict:** Two TXT records starting with `v=spf1` on same domain → immediate permerror per RFC 7208 §4.5
- **`redirect=` modifier trap:** If record includes both `redirect=` and `all` mechanism, `redirect=` is silently ignored — widely unknown spec detail
- **`ptr` mechanism:** Explicitly deprecated in RFC 7208; any record using `ptr:` should be migrated immediately
- **ESP IP drift:** Large senders with multiple ESPs discover via DMARC aggregate reports that a newly onboarded tool is sending without being in SPF — weeks after go-live
- **Macros in SPF:** RFC 7208 supports macros (`%{i}`, `%{s}`, `%{d}`) for dynamic per-sender resolution; used in SRS (Sender Rewriting Scheme) to survive forwarding

**Key tools:**

| Tool | What it does |
|---|---|
| MXToolbox SPF Lookup | Resolves and visualizes SPF chain, counts lookups, flags errors |
| dmarcian SPF Surveyor | Walks full SPF tree, shows lookup count with depth |
| AutoSPF | Automated flattening with continuous IP sync |
| DMARCLY Safe SPF | Automated SPF management with dynamic rewrite |
| `dig TXT domain.com` | Raw DNS query — ground truth |

---

### DKIM — Practitioner Knowledge Map

**What DKIM does:** DKIM (DomainKeys Identified Mail, RFC 6376) attaches a cryptographic signature to outgoing messages covering specified headers and body. Unlike SPF, DKIM signatures travel with the message and survive forwarding as long as signed content is not modified.

#### Tier 1 (Checklist Executor)
- Adds DKIM public key TXT record provided by ESP
- Verifies via MXToolbox or mail-tester.com
- Sends test email and checks Authentication-Results header for `dkim=pass`

#### Tier 2 (Diagnostic)

**Selector architecture — the key to multi-ESP management:**
- A DKIM selector namespaces the public key: `{selector}._domainkey.{domain}`
- You can have unlimited selectors — each ESP gets its own
- Naming convention best practice: `{purpose}-{date}-{keysize}` e.g., `mkt-20250101-2048`
- Example for three sending systems: `google._domainkey.example.com` / `mc._domainkey.example.com` / `transact20260301._domainkey.example.com`

**Alignment — the DMARC connection:**
- DKIM alignment checks whether `d=` domain in DKIM-Signature matches `From:` header domain
- **Relaxed (default `adkim=r`):** organizational domain must match — `mail.example.com` with `d=example.com` passes
- **Strict (`adkim=s`):** `d=` must exactly equal From domain
- Many ESPs sign with their own domain by default (`d=amazonses.com`) — does NOT pass DKIM alignment for DMARC; must configure custom signing with your domain

**Key length — 1024 vs. 2048 bit:**
- 1024-bit RSA computationally feasible to factor; NIST deprecated it; Gmail prefers 2048+
- 2048-bit keys can exceed DNS TXT record length limits (255 chars/string) — solution: split into multiple quoted strings in the TXT record
- `dig TXT selector._domainkey.domain.com` — 1024-bit key ≈ 216 chars; 2048-bit ≈ 392 chars

**DKIM key rotation procedure (no-downtime method):**
1. Generate new keypair with new selector name
2. Publish new public key to DNS — do NOT remove old key yet
3. Lower DNS TTL on old selector to 300s several days before rotation
4. Configure sending system to sign with new selector
5. Monitor DMARC aggregate reports 24–48 hours to confirm new selector passes
6. After grace period (minimum 5–7 days to allow for MTA retry queues), remove old selector's DNS record
- M3AAWG recommendation: rotate every 6 months minimum; high-volume every 1–3 months; 1024-bit every 3 months regardless

**DKIM failure diagnosis via headers:**

| Header text | Meaning |
|---|---|
| `dkim=fail (body hash did not verify)` | Message body modified in transit (link rewriters, antivirus gateways, mailing list software) |
| `dkim=fail (bad signature)` | Signed header fields were modified |
| `dkim=permerror (no key for signature)` | Selector does not exist in DNS — key never published or removed prematurely |
| `dkim=neutral (message not signed)` | ESP did not sign — signing configuration issue on sender side |
| `dkim=temperror` | Transient DNS failure during key lookup |

**Canonicalization:**
- `c=` field specifies relaxed or simple normalization
- Mailing lists and transit systems that reformat whitespace break `c=simple/simple`; `c=relaxed/relaxed` survives

#### Tier 3 (Expert)
- **DKIM replay attack:** A valid DKIM signature on one message can be replayed to different recipients — signature still verifies; DMARC does not prevent this
- **`l=` body length limit tag:** Security anti-pattern — allows injection of malicious content after signed portion; never use
- **Ed25519 DKIM keys (RFC 8463):** Shorter keys, faster verification, equivalent security; Google Workspace supports it; dual-sign approach (RSA 2048 + Ed25519) is forward-compatible
- **CNAME-based DKIM delegation:** Mailchimp, Salesforce use CNAME pointing to their infrastructure; they can rotate keys without customer DNS update — correct enterprise pattern, but reduces customer control over key material
- **Header field ordering attack:** Attacker prepends duplicate headers not in signed header list; legacy verifiers may check wrong header

---

### DMARC — Practitioner Knowledge Map

**What DMARC does:** DMARC (RFC 7489) adds: (1) alignment requirement — SPF/DKIM results must align to visible `From:` domain; (2) policy (`p=none/quarantine/reject`); (3) reporting (`rua=` aggregate, `ruf=` forensic).

#### Tier 1 (Checklist Executor)
- Publishes `_dmarc.domain.com` TXT: `v=DMARC1; p=none; rua=mailto:dmarc@domain.com`
- Knows three policy levels and ramp-up sequence: none → quarantine (small pct) → quarantine (100%) → reject
- Uses commercial tool (EasyDMARC, dmarcian) to read aggregate reports without touching XML

#### Tier 2 (Diagnostic)

**Reading DMARC aggregate report XML — key fields:**

```xml
<record>
  <row>
    <source_ip>209.85.220.41</source_ip>   <!-- sending IP -->
    <count>1542</count>                      <!-- messages from this IP -->
    <policy_evaluated>
      <disposition>none</disposition>        <!-- what receiver actually did -->
      <dkim>pass</dkim>                      <!-- DMARC alignment result (NOT raw DKIM) -->
      <spf>pass</spf>                        <!-- DMARC alignment result (NOT raw SPF) -->
    </policy_evaluated>
  </row>
  <auth_results>
    <dkim><domain>example.com</domain><selector>mkt-20250101</selector><result>pass</result></dkim>
    <spf><domain>bounce.example.com</domain><result>pass</result></spf>
  </auth_results>
</record>
```

**Critical field distinctions:**

| Field | What to look for |
|---|---|
| `policy_evaluated.dkim/spf` | DMARC **alignment** result — NOT raw SPF/DKIM. A source_ip can have raw DKIM=pass but DMARC dkim=fail if d= domain doesn't align to From: domain |
| `auth_results.spf.domain` | If this is ESP's domain (not yours), SPF alignment will fail for DMARC even if SPF passes raw |
| `disposition` | If `p=reject` but `disposition=none`, receiver applied a local override (forwarding, trusted sender list) — NOT a failure |
| `auth_results.dkim.selector` | Identifies which ESP/system sent the message |

**RUA vs. RUF reports:**

| | RUA (Aggregate) | RUF (Forensic) |
|---|---|---|
| Format | XML, compressed, daily | MIME email, near real-time |
| Content | IP, count, pass/fail statistics | Headers, subject, body snippets |
| Availability | Nearly universal | Limited — Google does not send RUF; many providers don't send due to privacy concerns |
| Practical use | Always the primary data source | Incident response only; cannot be relied upon as complete picture |

**DMARC policy mechanics:**
- `p=none`: Monitor only; reports sent; no action
- `p=quarantine`: Failed messages → spam folder
- `p=reject`: Failed messages → rejected at SMTP layer (550); message not delivered at all
- `pct=` tag: Apply quarantine/reject to N% of failing messages. **Zero effect with `p=none`** — many practitioners believe `pct=5; p=none` is a "soft start"; it is not; the pct ramp only applies to quarantine/reject phase
- `sp=` tag: Override subdomain policy — `p=none; sp=reject` monitors parent but hard-rejects spoofed subdomains immediately

**parsedmarc:**
- Open-source Python package; parses RUA/RUF; outputs to Elasticsearch/Kibana
- Setup: Python 3 + Elasticsearch + IMAP mailbox; install via `pip install parsedmarc`
- Use case: data residency requirements, high volume, budget constraints

#### Tier 3 (Expert)
- **DMARC "pass via SPF" alignment trap:** ESP sends using your domain in Return-Path → SPF passes AND aligns; but if they also sign with `d=esp.com`, DKIM alignment fails; message still passes DMARC (only one needs to align) — but if ESP SPF chain causes lookup limit breach, you lose SPF pass silently
- **Forwarding/override in aggregate reports:** Large volume of `disposition=none` when `p=reject` is in effect often indicates forwarding — not failures; misreading leads to incorrect remediation
- **Organizational domain vs. From domain:** DMARC evaluation always based on eTLD+1 of From header; understanding Public Suffix List necessary for edge cases (`.co.uk`, `.com.au`)
- **ARC (Authenticated Received Chain, RFC 8617):** Preserves authentication record through intermediaries like mailing lists; not universally checked

**DMARC tool comparison:**

| Tool | Best for | Key strength |
|---|---|---|
| dmarcian | Enterprises; consultants; complex multi-domain | Deepest data; co-founded by original DMARC authors |
| EasyDMARC | SMBs; non-technical stakeholders | Simple visual dashboard; solid free tier |
| Postmark DMARC | Small sites; quick verification | Free; clean UI |
| parsedmarc | Privacy-sensitive orgs; high volume; technical teams | Free; self-hosted; handles both RUA and RUF |
| Valimail | Large organizations with many sending services | Strong automation |

---

### Authentication Layer: Top Non-Obvious Failure Modes

These 7 scenarios trip up Tier 1 practitioners but are immediately diagnosable by Tier 2+:

**1. SPF passes, DKIM passes, DMARC fails — the alignment trap**
Both SPF and DKIM authenticate at protocol level, but DMARC alignment is a separate check. Return-Path `bounces.esp.com` passes SPF for that domain but does NOT align to `yourcompany.com` for DMARC. DKIM signing with `d=sendgrid.net` passes but doesn't align. Fix: configure ESP to use your domain as Return-Path and set up custom DKIM signing.

**2. SPF permerror from a hidden third-party include**
An `include:_spf.vendor.com` appears fine in isolation but the vendor's record itself contains 6 `include:` statements — combined tree exceeds 10. Fix: use a lookup-depth-aware tool (dmarcian SPF Surveyor) that walks the entire tree recursively.

**3. DKIM body hash failure after message modification**
A security gateway, antivirus, or mailing list software rewrites links or appends a disclaimer footer → body hash (`bh=`) no longer matches → `dkim=fail (body hash did not verify)`. Frequently misdiagnosed as configuration problem; it is a transit modification issue. Check if failure correlates with specific receiving domains running content-rewriting systems.

**4. Multiple SPF TXT records (the silent killer)**
During domain migration, a second `v=spf1` TXT record is left on the domain. Per RFC 7208: multiple SPF records = immediate permerror. Fix: `dig TXT domain.com` and count — there must be exactly one.

**5. DKIM "no key for signature" after premature key removal**
In-flight messages in retry queues (4xx retry, up to 5 days) carry the old `s=` selector. Deleting the old DNS record within 24 hours — as most operators do — causes `dkim=permerror (no key for signature)` on messages that were originally signed validly. Minimum grace period: 5–7 days.

**6. Subdomain spoofing when parent domain is at p=none**
Phishers use `payroll.example.com` or `invoice.example.com` — subdomains the organization owns but doesn't monitor — and these pass DMARC because `p=none` is inherited. Fix: use `sp=reject` even when `p=none` to protect unused subdomains immediately.

**7. ESP CNAME DKIM delegation — the invisible rotation**
When using CNAME-based DKIM (Mailchimp, Salesforce), the ESP can rotate keys without notifying the customer. If the ESP's rotation has a bug, DKIM fails for the customer domain with no warning. Diagnosis requires DMARC aggregate report data correlated with ESP maintenance windows.

---

## Layer 2: Reputation & Blacklists

*Source file: `06_Reference/Email_Deliverability_Layer2_Reputation_Blacklists.md`*

---

### Google Postmaster Tools — Practitioner Knowledge Map

#### Critical: September 2025 v1 Retirement

Google retired Postmaster Tools v1 on **September 30, 2025**. **Domain Reputation and IP Reputation dashboards no longer exist in v2.** This shifts GPT from a performance analysis platform into a compliance monitor. The v2 API (launching end of 2025) will maintain all v1 functionality except domain and IP reputation scores.

A practitioner who still talks about "checking domain reputation in Postmaster" without knowing about the v2 retirement is immediately identifiable as outdated.

#### Tier 1 — Spam Rate Dashboard (the primary remaining signal)

| Threshold | Meaning | Action Required |
|---|---|---|
| **< 0.08%** | Comfortable operating zone | Monitor; maintain list hygiene |
| **< 0.10%** | Recommended ceiling | Watch trend direction |
| **0.10%–0.30%** | Danger zone | Immediate list hygiene and content audit |
| **≥ 0.30%** | Policy violation — throttling or block | Emergency remediation; 7 consecutive days below 0.30% required for mitigation |

**Critical non-obvious point:** Gmail calculates spam rate against inbox-delivered mail only, not total sent volume. Emails delivered directly to spam folder are excluded from the denominator. A clean-looking GPT spam rate can mask a severe deliverability crisis.

#### Tier 2 — What Juniors Miss

- **FBL vs. Spam Rate:** GPT shows user-reported spam rate; does not show FBL complaint data — different measurement systems
- **Volume requirement:** ~100–250 emails/day to Gmail addresses before any dashboard populates; subdomain-level data requires consistent volume to that subdomain specifically
- **Domain registration:** Must match your DKIM signing domain (`d=` tag) or SPF envelope domain — not necessarily your From: header domain

#### Tier 3 — GPT v2 Structural Blind Spots

| Blind Spot | Why It Matters |
|---|---|
| No domain/IP reputation score | Removed in v2 — can no longer directly see Gmail's trust signal |
| No inbox vs. spam folder breakdown | Cannot see what % lands in spam vs. inbox |
| No engagement data | Open rates, click rates — invisible; yet heavily influence Gmail's ML |
| No send volume data | Cannot see how much volume Gmail received from you |
| No root cause for spam rate spikes | Tool tells you the outcome, not the cause |
| No data for non-Gmail MBPs | Outlook, Yahoo, Naver, Daum — zero coverage |

**Structural danger of v2:** Without domain/IP reputation scores, deliverability problems may only become visible once already severe — when the spam rate metric catches up to trust erosion that has been happening for weeks.

---

### Microsoft SNDS — Practitioner Knowledge Map

**What SNDS is:** Free, IP-centric reputation monitoring for Outlook.com, Hotmail, and Microsoft 365. Unlike GPT (domain-centric), SNDS centers around IP addresses — essential for senders on dedicated IP infrastructure.

**2025 update:** Microsoft now requires authentication (Microsoft account login) to manage IP ranges on SNDS.

#### Tier 2 — Interpretation

**Color-coded IP Health Status:**

| Color | Status | Action |
|---|---|---|
| Green | Good | Monitor |
| Yellow | Neutral/Caution | Investigate complaint rate and trap hits |
| Red | Poor | Immediate remediation |

**Key metrics:**
- **Complaint Rate:** Calculated against all delivered messages (unlike GPT which excludes spam-foldered mail); even 0.3–0.5% is high for Microsoft
- **Spam Trap Hits:** Correct number is zero. Any trap hit is a binary list hygiene failure signal
- **Minimum volume:** 100 messages/day to Microsoft-hosted addresses

**Critical nuance:** SNDS requires IP ownership (WHOIS verification). If using shared IP via ESP, you almost certainly cannot register — WHOIS belongs to the ESP.

#### Tier 3 — SNDS vs. GPT Comparison

| Dimension | Google Postmaster Tools | Microsoft SNDS |
|---|---|---|
| Reputation unit | Domain (DKIM signing domain) | IP address / IP range |
| Spam rate visibility | User-reported rate vs. inbox-delivered mail | Complaint rate vs. all delivered mail |
| Trap hits | Not shown | Directly reported |
| IP filter status | Removed in v2 | Color-coded per IP |
| Coverage | Gmail/Googlemail only | Outlook, Hotmail, MSN, Live, Microsoft 365 |
| Shared IP usability | Works (domain-level) | Requires IP ownership |

**Paired-tool discipline:** A senior specialist runs SNDS and GPT simultaneously. Spike in GPT spam rate without SNDS complaint data = Gmail-specific problem. Red SNDS IP with clean GPT = Microsoft-specific infrastructure issue.

---

### Blacklist Taxonomy & Delisting

| Blacklist | Type | What Triggers Listing | Removal Process | Difficulty |
|---|---|---|---|---|
| **SBL** (Spamhaus Blocklist) | IP | Known spam operations, bulletproof hosting, spam infrastructure | Manual review by Spamhaus team | High — human review |
| **CSS** (Combined Spam Sources) | IP | High-volume spam, snowshoe patterns | Manual review; often auto-expires | Medium |
| **XBL** (Exploits Blocklist) | IP | Compromised machines, botnet activity | Fix the exploit; often auto-delists 24–48hr | Low-Medium |
| **PBL** (Policy Blocklist) | IP | End-user/broadband IP ranges not for direct-to-MX sending | Self-service using domain-registered email | Low — policy-based |
| **DBL** (Domain Blocklist) | Domain | Domains in spam content, phishing, malware | Email request; manual review | High |
| **ZEN** | IP (combined) | Any combination of SBL, CSS, XBL, PBL | Delist from specific sub-lists individually | Varies |
| **BRBL** (Barracuda) | IP | User-reported spam at Barracuda-protected networks | Self-service at barracudacentral.org | Medium |
| **SpamCop** | IP | Aggregated user reports | Auto-expires 24–48hr; no manual removal | Low |
| **SURBL** / **URIBL** | Domain (URI) | Domain found in spam message bodies/URLs | Contact form; manually reviewed | High |

**ZEN return code system** (read the code, not just the listing):

| Return Code | Sub-list |
|---|---|
| `127.0.0.2` | SBL |
| `127.0.0.3` | SBL-CSS |
| `127.0.0.4–7` | XBL (CBL data) |
| `127.0.0.9` | DROP (hijacked netblocks) |
| `127.0.0.10–11` | PBL |

**Non-obvious listing triggers:**
1. **Snowshoe patterns:** Rotating sends across many IPs — Spamhaus CSS explicitly targets this; the distributed sending that senders think hides volume is itself the signature
2. **Reverse DNS mismatch:** PTR record not matching A record; or PTR pointing to generic ISP string — automatic PBL candidate
3. **Spam trap hits before complaint spikes:** Blacklist operators see trap data before you see complaint metrics
4. **Bulletproof hosting co-tenancy:** Sharing an IP range with known bulletproof hosts gets ranges pre-emptively SBL-listed
5. **Subdomain URL reuse:** DBL listings stick to subdomains used in URLs even after the spam campaign ends

---

### Spam Trap Intelligence

| Type | How Created | What Hit Signals | Severity |
|---|---|---|---|
| **Pristine (Honeypot)** | Created solely as traps; published on web pages, hidden form fields — never belonged to a real person | List was scraped, purchased, or harvested | Critical — can trigger immediate blacklisting |
| **Recycled** | Real addresses abandoned by users; inbox provider deactivates after 6–12 months inactivity, then converts to trap | Sender mailing contacts who never re-engaged — list hygiene failure | High — indicates stale list segments |
| **Typo** | Common misspellings of legitimate domains: `gnail.com`, `hotnail.com`, `yaho.com` | Signup form lacks real-time email validation | Medium — poor data quality at acquisition |

**Diagnostic signals you're hitting traps (without direct access):**

| Signal | What It Suggests |
|---|---|
| SNDS trap hit count > 0 | Directly reported — most explicit indirect signal |
| Blacklist listing with no corresponding complaint spike | Pristine trap hit |
| Deliverability drops concentrated in oldest inactive segments | Recycled traps concentrated in old/inactive cohorts |
| **Bounce rate suddenly drops to near-zero on a segment** | Recycled traps are "live" — they don't bounce, they absorb mail silently; suspiciously low bounces + zero engagement = trap-risk zone |
| Spam rate spikes without campaign volume change | Recycled trap converted from bounce to trap — your "bouncing" list now generates trap hits |
| Engagement rate collapses on a specific cohort | Zero opens + zero clicks across entire segment = non-human addresses |

---

### Sender Reputation Scoring Landscape (2026)

| Tool | Operator | 2026 Relevance | Notes |
|---|---|---|---|
| **Google Postmaster Tools** | Google | Essential | Free; domain-level; spam rate + auth (v2) |
| **Microsoft SNDS** | Microsoft | Essential for Outlook/Hotmail | Free; IP-level; requires IP ownership |
| **Validity Sender Score** | Validity (formerly Return Path) | Declining but not dead | DNS-based lookup tightened; registration required |
| **Validity Everest** | Validity | Active enterprise tool | Paid; combines Return Path + 250ok |
| **MXToolbox Blacklist Check** | MXToolbox | Useful for rapid triage | Free tier; checks 100+ blacklists simultaneously |
| **Talos Intelligence** | Cisco | Relevant for enterprise security stack | Free lookup |
| **Barracuda Central** | Barracuda Networks | **Relevant in Korean B2B** | Barracuda hardware prevalent in Korean enterprise and government mail gateways |

**Deprecated/diminished:**

| Tool/Concept | Status |
|---|---|
| GPT Domain Reputation (High/Medium/Low/Bad) | **Retired September 2025** |
| GPT IP Reputation | **Retired September 2025** |
| Return Path Certification | Significantly diminished; marginal benefit for Microsoft ecosystem only |
| DNS-based Sender Score lookup | Tightened — Validity restricted free DNS resolver access |

**BIMI and VMC:**
- BIMI allows brand logo display in supporting inbox providers (Gmail, Apple Mail, Yahoo)
- Prerequisites: SPF + DKIM + DMARC all pass (`p=quarantine` or `p=reject`); SVG Tiny PS format logo
- VMC (Verified Mark Certificate): required by Gmail; issued by DigiCert/Entrust; ~$1,500–$2,000/year
- BIMI is primarily brand trust signal; the deliverability prerequisite (DMARC enforcement) is what matters for deliverability

---

### Diagnostic Questions: Senior vs. Junior (Reputation Layer)

10 questions a senior reputation diagnostician asks that a junior doesn't:

1. **"Show me your DMARC aggregate (RUA) reports for the past 30 days — what % of mail is failing DKIM alignment, and from which sources?"** Junior checks if DMARC is published. Senior reads the XML to find unauthorized senders or misconfigured subdomains poisoning domain reputation.

2. **"What is your complaint rate specifically on the cohort acquired in the past 90 days, isolated from your legacy list?"** Junior looks at aggregate complaint rate. Senior segments by acquisition cohort to identify whether bad data enters at the top of the funnel vs. legacy list decay.

3. **"When did your PTR records last change, and do they match your A records and HELO domain?"** Junior checks if PTR exists. Senior validates three-way consistency (PTR → A → HELO).

4. **"What is your recycled-trap exposure window — when did you last run a sunset suppression on contacts who haven't engaged in 6+ months?"** Junior thinks spam traps only come from bad list purchases. Senior knows recycled traps are the most common silent killer in well-managed programs.

5. **"Your SNDS shows zero trap hits but your Spamhaus CSS listing is 3 days old — what changed in your sending pattern in the 7 days before the listing?"** Junior goes straight to delisting. Senior diagnoses root cause — delisting without diagnosis results in re-listing within 30 days.

6. **"What is the warm-up curve on this IP, and what was the volume on day 1 of sending?"** Junior checks if IP is blacklisted. Senior knows IP warming failure — sending too fast too early — is the most common cause of Microsoft red status and Spamhaus CSS listing for otherwise clean senders.

7. **"Is your unsubscribe link functional within 2 clicks and do you support List-Unsubscribe-Post (one-click RFC 8058)?"** Junior checks if unsubscribe link exists. Senior knows Google's 2024 mandate requires one-click unsubscribe; non-compliance amplifies complaint rate because users who can't unsubscribe hit "spam" instead.

8. **"What ESP are you using — shared or dedicated IPs?"** Junior treats all ESPs as equivalent. Senior knows on shared IP pools, a single bad co-tenant's trap hits affect every sender on that IP.

9. **"What domains are you using in email body URLs — are they on any DNSBL?"** Junior checks the sending domain. Senior knows DBL and URIBL check domains in the URLs within the email body.

10. **"In the 48 hours before your GPT spam rate spike, what campaigns went out and to which segments — specifically, was there a reactivation campaign to long-dormant subscribers?"** Junior treats spam rate spikes as uniform signals. Senior knows reactivation campaigns to cold subscribers (12+ months inactive) are the single most common trigger for spam rate spikes.

---

## Layer 3: List Hygiene & Sending Program

*Source file: `06_Reference/Email_Deliverability_Layer3_List_Hygiene_Sending_Program.md`*

---

### Bounce Management — Practitioner Knowledge Map

#### Tier Structure

| Tier | Knowledge Level |
|---|---|
| **Tier 1** | Binary mental model: hard bounce = bad address; soft bounce = temporary retry |
| **Tier 2** | Can read SMTP codes; understands suppression logic per ESP; knows when to escalate soft to permanent |
| **Tier 3** | Understands how bounce *patterns* signal list health before metrics degrade; reverse-engineers ISP scoring from bounce code distributions; builds suppression architecture with distinct failure modes |

#### Bounce Category Taxonomy (4-category, not 2)

| Category | Definition | Suppression Action |
|---|---|---|
| **Hard Bounce** | Permanent failure — invalid address, non-existent mailbox. SMTP 5xx. | Immediate permanent suppression |
| **Soft Bounce** | Temporary failure — full mailbox, server overloaded, greylisting. SMTP 4xx. | Queue and retry; after N consecutive failures, promote to hard suppression |
| **Block Bounce** | Rejection based on sender reputation, blocklist, content filter, or authentication failure. 4xx or 5xx. | **Investigate cause — do NOT suppress the recipient address.** This is a *sender* problem. |
| **Complaint Bounce** | Not a technical bounce — recipient marked as spam; FBL report. | Immediate suppression. Never re-mail a confirmed complainer. |

**Non-obvious point:** Block bounces are frequently conflated with hard bounces. Treating a block bounce as a hard bounce and suppressing the address hides the real problem — something is wrong with your sending infrastructure or reputation.

#### SMTP Bounce Code Reference

| Code | Class | Practitioner Action |
|---|---|---|
| **421** | 4xx Soft — Service Temporarily Unavailable | Retry. If persistent across one domain, you may be rate-limited — reduce send velocity to that domain. |
| **450** | 4xx Soft — Mailbox Unavailable (Temporary) | Retry. Greylisting resolves on second attempt from same IP. |
| **451** | 4xx Soft — Processing Error | Retry. 451 4.7.0 from Gmail = warming/reputation issue — reduce volume. |
| **452** | 4xx Soft — Insufficient Storage | Retry. If persistent 30+ days, consider permanent suppression (mailbox abandoned). |
| **500** | 5xx Hard — Syntax Error | Investigate your MTA configuration — not a list hygiene issue. |
| **550** | 5xx Hard — Mailbox Rejected | 5.1.1 = user unknown → suppress. 5.7.1 = policy rejection → **investigate first** — may be block bounce. |
| **551** | 5xx Hard — User Not Local | Suppress. |
| **552** | 5xx Hard — Message Too Large / Permanent Over Quota | If content: reduce message size. If mailbox quota permanent: suppress. |
| **553** | 5xx Hard — Mailbox Name Invalid | Suppress. Add real-time validation at point of capture. |
| **554** | 5xx Hard — Transaction Failed | Do NOT auto-suppress recipient. Diagnose: 5.7.26 = DMARC failure; reputation block; content filter. |

**Enhanced status codes (X.Y.Z) are the real diagnostic layer:**
- `5.1.1` — Address does not exist
- `5.7.1` — Policy rejection (content, IP reputation, or DMARC failure)
- `5.7.26` — Gmail-specific: DMARC policy violation
- `4.7.0` — Gmail: reputation not yet established (warming signal)

**ESP classification differences (important for migrations):**
- **SendGrid:** 7-bucket system including "Block" as a distinct category
- **Mailchimp:** Auto-promotes soft bounces to hard suppression without sender action
- **Klaviyo:** Requires 7 consecutive soft bounces before suppression
- Suppression gaps appear when migrating between ESPs with different classification logic

---

### Thresholds & Enforcement (2025–2026)

| Provider | Hard Bounce | Complaint — Caution | Complaint — Enforcement | What Happens |
|---|---|---|---|---|
| **Gmail** | ~2% (soft guideline) | < 0.10% recommended | 0.30% sustained | Nov 2025: active rejection codes (4.7.x temp, 5.7.x permanent) — no longer warnings only |
| **Yahoo / AOL** | ~2% | < 0.10% | 0.30% | TS01–TS04 throttling/rejection codes; requires Yahoo FBL registration |
| **Microsoft** | > 2% = problematic | < 0.10% | Unlisted specific rate | SNDS flags elevated rates; enforcement effective May 5, 2025 for 5,000+ msg/day senders |
| **Apple iCloud** | No published threshold | < 0.10% | Not disclosed | No formal FBL; no published sender guidelines |

**Gmail's February 2024 requirements — two-tier structure:**

**Enforced (binary compliance gate):**
- SPF or DKIM authentication — hard requirement; failure = rejection
- DMARC at minimum `p=none` — hard requirement
- Valid PTR (reverse DNS) for sending IPs — hard requirement
- One-click unsubscribe header — hard requirement
- TLS for transmission — hard requirement

**Recommended but not binary enforcement (yet):**
- Spam complaint rate below 0.10% — crossing 0.30% triggers enforcement; 0.10% is a reputation maintenance recommendation
- Bounce rate below 2% — treated as signal in domain reputation scoring, no enforcement mechanism published

---

### Engagement Segmentation Architecture

**Decision tree for building suppression strategy from scratch:**

```
START: You have an email list.

├─ Q1: How old is this list (or segments)?
│   ├─ < 6 months, continuously mailed → Proceed to Q2
│   ├─ 6–12 months, some gaps → Run list verification before next send
│   └─ > 12 months dormant → STOP. Verify first. Warm up to re-engagement
│       segment only. Full blast = reputation damage.

├─ Q2: Double opt-in on record?
│   ├─ Yes → Higher quality baseline. Lower spam trap risk.
│   └─ No (single opt-in, imported, purchased) → Treat as higher-risk.
│       NEVER send to purchased or scraped lists without verification.

├─ Q3: Engagement segments (opens + clicks):
│   ├─ Tier A — Active: Opened or clicked within last 90 days
│   ├─ Tier B — Warm: Last engagement 91–180 days ago
│   ├─ Tier C — At Risk: Last engagement 181–365 days ago
│   └─ Tier D — Inactive/Lapsed: No engagement in 365+ days

├─ Q4: What to do with each tier:
│   ├─ Tier A → Full send cadence
│   ├─ Tier B → Full send; monitor complaint rate separately; reduce frequency if rate spikes
│   ├─ Tier C → Reduced frequency (1x/month max); trigger re-engagement sequence
│   └─ Tier D → Do not mail until re-engagement attempted; if fails: suppression list

└─ Q5: Suppression list architecture (5 separate lists):
    ├─ Hard bounce list (permanent, never send)
    ├─ Complaint/FBL list (permanent, never send)
    ├─ Unsubscribe list (permanent, legally required)
    ├─ Inactive suppress list (operational, reviewable)
    └─ Block/role address list (postmaster@, admin@, noreply@)
```

**Proactive vs. Reactive decisions:**

| Decision | Proactive | Reactive |
|---|---|---|
| List quality | Double opt-in + real-time verification at signup | Run bulk verification after bounce rate exceeds 1.5% |
| Engagement management | Sunset policy applied automatically on schedule | Remove inactives after complaint rate climbs to 0.08% |
| Authentication | SPF/DKIM/DMARC set up before first send | Fix authentication after first Google rejection |
| Complaint monitoring | Register for Yahoo FBL and Microsoft JMRP on day 1 | Investigate complaint source after rates spike |

---

### Sunset Policy Framework

**Engagement window definitions by business type:**

| Business Type | "Active" Definition | Re-engagement Trigger | Sunset (Suppress) Trigger |
|---|---|---|---|
| Daily newsletter | Opened within 30 days | No open in 60 days | No open in 90–120 days |
| Weekly marketing (e-commerce) | Opened/clicked within 90 days | No engagement in 90–180 days | No engagement in 180–270 days |
| Monthly B2B / SaaS | Opened/clicked within 180 days | No engagement in 180–365 days | No engagement in 365–540 days |
| Infrequent / event-based | Any engagement past 12 months | No engagement in 12 months | No engagement in 18–24 months |

**Default for programs without a policy:** 180-day re-engagement trigger, 365-day suppression trigger.

**Re-engagement sequence before sunset:**
1. **Signal email (Week 1):** Personal, low-pressure; single CTA "Keep me subscribed"; no promotional content
2. **Escalation email (Week 2–3, if unopened):** Urgency framing — "Last chance — we'll remove you from our list soon"; directness improves deliverability (disinterested people unsubscribe rather than marking spam)
3. **Final confirmation (Week 3–4, optional):** "We've removed you from our list. Click here to resubscribe anytime."

After sequence: any non-respondent → inactive suppression list. Do not delete — suppress. Deletion removes opt-in history needed for regulatory compliance.

**Data point:** Only ~24% of email programs have a formal sunset policy — a significant market education gap and consulting entry point.

---

### List Verification Tool Comparison

| Tool | What It Checks | Best For | Pricing | Key Limitations |
|---|---|---|---|---|
| **ZeroBounce** | MX lookup, SMTP ping, domain existence, role addresses, abuse/spam complainer flags, toxic domain detection, spam trap detection (claimed) | Comprehensive bulk cleaning; large legacy lists | ~$0.004/email | 99.6% claimed accuracy; pristine spam trap detection is not independently verifiable |
| **NeverBounce** | MX lookup, SMTP ping, domain existence, catch-all, disposable address | API-first integrations; real-time signup verification | ~$0.004/email | Similar accuracy to ZeroBounce; acquired by ZoomInfo — data usage policy concerns |
| **BriteVerify (Validity)** | MX lookup, SMTP ping, domain existence, role address | Enterprise/Validity ecosystem buyers | ~$0.01/email (most expensive) | **Does NOT detect spam traps** (confirmed in documentation); usually purchased as part of Validity suite |
| **Kickbox** | MX lookup, SMTP ping, domain existence, role, disposable, "Sendex" proprietary score | Technical teams; SaaS signup flows; teams wanting a score vs. pass/fail | ~$0.008/email | No spam trap detection; Sendex score not externally validated; strong API docs |
| **Bouncer** | MX, SMTP, domain, disposable, role, catch-all, toxicity | EU/GDPR compliance requirements | ~$0.005–$0.008/email | Newer to market; smaller client base |

**When to use proactive verification:**
- Before migrating to new ESP
- List dormant for 6+ months
- Bounce rate already exceeded 1.5%
- Importing from new channel (trade show, partner)
- Before high-stakes campaign

**Cost-benefit:** At $0.004/email, verifying 100,000 addresses = $400. A single deliverability incident can require weeks of rehabilitation. Verification is almost always justified for lists over 50,000 addresses or unused for 6+ months.

---

### Feedback Loop Infrastructure

**What an FBL is:** A channel through which a mailbox provider sends the sender notification when a recipient marks a message as spam. Without FBL registration, you have no visibility into complaint events until they aggregate into a threshold breach detectable in Postmaster Tools.

| ISP | FBL Available | Format | Key Notes |
|---|---|---|---|
| **Yahoo / AOL** | Yes — Complaint Feedback Loop (CFL) | ARF | Self-service at Yahoo Sender Hub. Requires DKIM signing — reports tied to DKIM domain, not IP. The only domain-based (not IP-based) FBL among major ISPs. |
| **Microsoft (Outlook)** | Yes — JMRP (Junk Mail Reporting Program) | ARF | Register at Microsoft SNDS. Also register SNDS for IP reputation + trap hit data. Enforcement for non-registered senders effective May 2025. |
| **Comcast (Xfinity)** | Yes — migrating to Yahoo | ARF | Comcast migrating @comcast.net mailboxes to Yahoo Mail through 2026. Register for Yahoo FBL to capture this traffic going forward. |
| **Gmail** | No traditional ARF FBL | Dashboard (Postmaster Tools) | Google does not send individual complaint reports. Add `Feedback-ID` header to outgoing messages for campaign-level spam rate data. |
| **Apple iCloud** | No | — | No program available; complaint data is internal. |

**ESP FBL handling comparison:**
- **Mailchimp:** Processes Yahoo + Microsoft FBL automatically; complainers suppressed without sender action
- **SendGrid (dedicated IPs):** Sender responsible for FBL registration under their own domain/IP
- **Klaviyo:** Processes FBL automatically; visible in suppression list
- **Amazon SES:** Complaints handled via SNS webhooks — sender must configure and process complaint notifications manually
- **Self-hosted / dedicated MTA:** All FBL registrations fully manual — high consulting value for Korean enterprises running internal mail relay (common in 그룹웨어 environments)

---

### Diagnostic Questions: Senior vs. Junior (List Hygiene Layer)

1. **"What is your bounce rate, and how is your ESP classifying the bounce type distribution?"** Senior asks about the distribution — specifically how many 550 5.7.x (reputation/policy) vs. 550 5.1.1 (invalid address) codes appear. The distribution diagnoses list quality vs. reputation problem vs. content problem.

2. **"When were the subscribers on this list acquired, and through what channel — were any segments acquired differently?"** Senior segments risk by acquisition cohort before designing any hygiene intervention.

3. **"Have you registered for Yahoo's CFL and Microsoft's JMRP, and are you processing those reports within 24 hours?"** Most programs with "complaint rate problems" have never registered for FBL programs and are flying blind.

4. **"What does your suppression list architecture look like — are hard bounces, complainers, unsubscribes, and inactives kept in separate lists or merged into one?"** Merging suppression categories is a data governance problem that prevents both regulatory compliance and diagnostic visibility.

5. **"If you stopped mailing a segment today and restarted in 6 months, what would you do differently?"** Tests understanding of list decay risk. Correct answer: verify first, warm up, prioritize most-recently-engaged cohort.

6. **"What is your complaint-per-campaign breakdown — which specific campaigns or segments are generating disproportionate complaints?"** Aggregate rates hide which campaigns are the problem. A single poorly-targeted campaign to a lapsed segment can damage the domain for all other campaigns.

7. **"Are you accounting for Apple Mail Privacy Protection's impact on open rate inflation?"** Since iOS 15 (2021), open tracking is unreliable for Apple Mail users. "Active" defined purely by opens uses inflated data. Cross-reference click data or other engagement signals (site visits, purchase activity, login events).

8. **"What is the process when someone submits a spam complaint versus when someone unsubscribes — are those handled identically or differently?"** They should be handled differently. Unsubscribe = preference change. Spam complaint = trust breach requiring permanent suppression across all streams + investigation of which messages generated complaints.

---

## Cross-Layer: Top Non-Obvious Failure Modes

Summary of the 7 failure modes across all three layers most likely to separate Tier 1 from Tier 2 practitioners in a Korean consulting context:

| # | Failure Mode | Layer | Junior mistake | Senior diagnosis |
|---|---|---|---|---|
| 1 | SPF/DKIM pass but DMARC fail | Auth | "Authentication is working" | Alignment check is separate from protocol pass |
| 2 | SPF permerror from recursive includes | Auth | Record looks fine in isolation | Walk the entire lookup tree |
| 3 | DKIM key removed before retry queue drains | Auth | 24-hour key deletion | 5–7 day grace period minimum |
| 4 | GPT spam rate masks severity | Reputation | "Rate is clean" | Excludes spam-foldered mail from denominator |
| 5 | Recycled traps in low-bounce, zero-engagement segments | Reputation | "No bounces = clean list" | Traps don't bounce — they absorb mail silently |
| 6 | Block bounce treated as hard bounce | List Hygiene | Suppresses the address | Investigates the sending infrastructure |
| 7 | Single merged suppression list | List Hygiene | All suppressions in one list | 5 separate lists by type and reversibility |

---

## Korean Market Gap Summary

Korean-language practitioner content on email deliverability is effectively absent at diagnostic depth. What exists:

| Topic | Korean content status |
|---|---|
| SPF/DKIM/DMARC setup guides | Basic — translated Google Workspace admin docs; Stibee help pages |
| SPF lookup tree diagnosis | **Non-existent** |
| DKIM key rotation procedure | **Non-existent** |
| DMARC aggregate XML parsing | **Non-existent** |
| Multi-ESP selector management | **Non-existent** |
| Alignment failure forensics | **Non-existent** |
| GPT v2 changes (Sep 2025 retirement of reputation dashboards) | **Non-existent** |
| Spam trap taxonomy | **Non-existent** |
| IP warming methodology | **Non-existent** |
| Blacklist diagnosis and removal (beyond clicking "delist") | **Non-existent** |
| Sunset policy design | **Non-existent** |
| Bounce code reference with enhanced status codes | **Non-existent** |
| List verification tool comparison | **Non-existent** in Korean practitioner context |
| Naver Mail filtering behavior | **Non-existent** — Naver operates opaque filtering with no public equivalent to GPT |
| Barracuda (Korean enterprise mail gateway) | **Non-existent** — Barracuda hardware prevalent in Korean enterprise gateways; no Korean-language Barracuda reputation management content |
| KISA 화이트도메인 registry | Exists (official) but no practitioner guide to using it strategically |

**The Korea-specific gap:** Major Korean inbox providers (Naver, Kakao/Daum) operate opaque reputation systems with no public tools equivalent to GPT or SNDS. Naver Mail does not yet enforce DMARC/SPF/DKIM as strictly as Gmail. A consultant who can bridge international deliverability frameworks (GPT, SNDS, Spamhaus taxonomy) with Korean-specific MBP behavior (Naver Mail, Kakao Mail, Barracuda enterprise gateways, KISA 화이트도메인) occupies an uncrowded position.

---

## Sources

All sources are preserved in the source reference files. Key repositories:

- **Authentication sources (52 primary sources):** `06_Reference/Email_Authentication_SPF_DKIM_DMARC_Practitioner_Reference.md`
- **Reputation & Blacklist sources (20 primary sources):** `06_Reference/Email_Deliverability_Layer2_Reputation_Blacklists.md`
- **List Hygiene sources (30+ primary sources):** `06_Reference/Email_Deliverability_Layer3_List_Hygiene_Sending_Program.md`

Key institutional sources consulted: RFC 7208, RFC 6376, RFC 7489, RFC 8617, RFC 8463, Google Workspace Admin Help, Gmail Postmaster Tools, Microsoft SNDS, Spamhaus official documentation, M3AAWG DKIM Key Rotation BCP, Yahoo Sender Hub, dmarcian, EasyDMARC, Validity/Return Path, Suped, PowerDMARC, Mailtrap, Stibee (스티비), NHN Cloud Meetup, Google Korea support docs.
