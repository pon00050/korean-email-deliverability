# 이메일 Deliverability Hub — 기술 스택 및 한국 인박스 패널 타당성 연구
**Korean Email Deliverability Hub: Technology Stack & Feasibility Study**
*Compiled: Feb 28, 2026 | 7-agent parallel research*

---

## Contents

1. [Novel Value Proposition — The Missing-Layer Map](#1-novel-value-proposition)
2. [Technical Feasibility: Naver/Kakao Inbox Panel](#2-technical-feasibility-naverkakao-inbox-panel)
3. [Open-Source and API Building Blocks](#3-open-source-and-api-building-blocks)
4. [Missing Layer 1 — Regulatory Compliance Managed Service](#4-missing-layer-1--regulatory-compliance-managed-service)
5. [Missing Layer 2 — ESP Partner Integration](#5-missing-layer-2--esp-partner-integration)
6. [Missing Layer 3 — Inbox Provider Feedback Reconstruction](#6-missing-layer-3--inbox-provider-feedback-reconstruction)
7. [The CSA Institutional Layer](#7-the-csa-institutional-layer)
8. [MVP Concept: 1–3 Month Single-Developer Build](#8-mvp-concept-13-month-single-developer-build)
9. [Sources](#9-sources)

---

## 1. Novel Value Proposition

### The Structural Gap

A Korean bulk email sender — a cosmetics e-commerce company, a fintech SaaS, a hospital group — sends 500,000 emails per month. Roughly 60–70% of their recipients have Naver or Kakao/Daum email addresses. They have no way to know whether those emails are landing in the inbox or the spam folder. None. Not from their ESP. Not from any commercial tool. Not from Naver or Kakao directly.

This is not a niche problem. It is a systematic absence of an entire feedback layer.

### The Three Missing Layers

```
[Korean Regulatory Bodies]          [Naver Mail / Kakao Mail]         [Korean ESPs]
 KISA / 방통위 / PIPC                  (Inbox Providers)                Stibee / TasOn
         |                                     |                        NHN Cloud / Naver Cloud
         |                                     |                               |
    [GAP: Layer 1]                       [GAP: Layer 3]                 [GAP: Layer 2]
 No managed compliance             No feedback to senders           No deliverability partner
  service translating              on inbox placement,              when support closes
   regulations into                filtering reasons,               the ticket
   technical action                or sender reputation
         |                                     |                               |
         v                                     v                               v
                    [BULK EMAIL SENDERS — entirely on their own]
```

**Layer 1 gap (between regulators and senders):** KISA publishes 정보통신망법 guidance. 방통위 issues fines. PIPC governs consent. But no private entity translates these into a managed compliance service. The 화이트도메인 registry — the one institutional bridge — was terminated June 28, 2024. The self-serve vacuum is now complete.

**Layer 2 gap (between ESPs and senders):** When a Korean ESP user (Stibee / TasOn / NHN Cloud customer) has a deliverability problem, support runs through the SPF/DKIM checklist and closes the ticket. There is no preferred deliverability partner, no escalation path, no deeper diagnostic resource. The gap between "support closes ticket" and "Naver postmaster contact" is entirely empty.

**Layer 3 gap (between inbox providers and senders):** Gmail has Google Postmaster Tools. Microsoft has SNDS. Naver and Kakao have nothing. No dashboard. No FBL. No sender reputation signal. No published bounce code reference. Korean senders discover inbox collapse only when their open rates collapse.

### The Korean Inbox Data Asset

Every global inbox placement testing tool — GlockApps, Validity Everest, Litmus, Mailgun inbox testing, Mailtrap — has the same blind spot:

| Provider | GlockApps | Validity Everest | Litmus | Korea-Specific Tool |
|---|---|---|---|---|
| Gmail | ✓ | ✓ | ✓ | ✓ |
| Outlook/Hotmail | ✓ | ✓ | ✓ | ✓ |
| Yahoo | ✓ | ✓ | ✓ | ✓ |
| **Naver Mail** | ✗ | ✗ | ✗ | **✓** |
| **Kakao/Daum Mail** | ✗ | ✗ | ✗ | **✓** |

GlockApps explicitly lists its providers: Gmail, Outlook, Yahoo, AOL, Yandex, Zoho, GMX, laposte.net — no Korean providers. Validity Everest claims 140 ISPs globally; no Korean provider appears in any documentation, review, or user report.

Naver Mail: ~40M active accounts. Kakao/Daum Mail: ~15–20M combined. These are the dominant Korean consumer inboxes. They are entirely unrepresented in every commercial inbox placement tool on the market.

The operational barrier that creates the moat: building a Naver/Kakao seed panel requires Korean phone numbers for account creation. A US-based SaaS vendor cannot replicate this. A Korea-based operator can.

---

## 2. Technical Feasibility: Naver/Kakao Inbox Panel

### Feasibility Table

| Provider | IMAP Supported? | Auth Method | Server / Port | Rate Limits | ToS Risk | Verdict |
|---|---|---|---|---|---|---|
| **Naver Mail** (@naver.com) | Yes — must enable per account in settings | App password (mandatory since ~Nov 2024; requires 2FA first) | `imap.naver.com:993` SSL | Not documented; ~15 concurrent sessions assumed | Medium — no explicit prohibition on reading your own email; 3 accounts max per phone | **Feasible** |
| **Kakao Mail** (@kakao.com) | Yes — must enable per account | App password (mandatory since Jan 2, 2025; requires KakaoTalk 2FA) | `imap.kakao.com:993` SSL | Not documented | Medium — each account requires real KakaoTalk-linked phone number | **Feasible, higher setup friction** |
| **Daum Mail** (@daum.net) | Yes — same infrastructure as Kakao | App password (same Jan 2025 policy) | `imap.daum.net:993` SSL | Same as Kakao | Medium — unified under Kakao accounts | **Feasible** |
| **Naver Works Mail** | Yes (B2B enterprise) | Works admin credentials | `imap.worksmobile.com:993` | N/A | Low for API use; but requires enterprise subscription | **Not relevant** — enterprise only; not consumer addresses |
| **Naver Cloud Platform** | **No** — outbound only | Send API (key-based) | REST API only | N/A | N/A | **Dead end** for inbox reading |

### Working IMAP Configuration

**Naver Mail (@naver.com):**
```
IMAP Host:  imap.naver.com
IMAP Port:  993
Security:   SSL/TLS
Username:   yourname@naver.com
Password:   Application Password (NOT login password)
SMTP Host:  smtp.naver.com
SMTP Port:  587 (STARTTLS)
```

Setup per account (manual, one-time):
1. Log in to mail.naver.com
2. Settings > POP3/IMAP Settings > Enable IMAP
3. Enable 2-step verification at nid.naver.com
4. Generate App Password: nid.naver.com > Security > 2-step Verification > App Passwords

**Kakao Mail (@kakao.com) / Daum Mail (@daum.net):**
```
IMAP Host (Kakao):  imap.kakao.com:993 SSL
IMAP Host (Daum):   imap.daum.net:993 SSL
Username:           yourname@kakao.com (or @daum.net)
Password:           App Password (from KakaoTalk 2FA settings)
SMTP Host (Kakao):  smtp.kakao.com:465 SSL
SMTP Host (Daum):   smtp.daum.net:465 SSL
```

Setup per account (manual, one-time):
1. Enable IMAP at mail.kakao.com > Settings > IMAP/POP3
2. Enable 2-step verification in KakaoTalk app
3. Generate App Password from KakaoTalk: Settings > Security > Kakao Account > App Password

### Python Code Pattern

Recommended library: `imap_tools` (MIT license, wraps `imaplib`, handles encoding, supports folder enumeration).

```python
from imap_tools import MailBox, AND
from datetime import datetime, timedelta
import time

SEED_ACCOUNTS = [
    {"id": "naver_01", "provider": "naver", "email": "seed01@naver.com",
     "imap_host": "imap.naver.com", "imap_port": 993, "app_password": "xxxx",
     "spam_folder": "스팸메일함"},  # Discovered on first run
    {"id": "kakao_01", "provider": "kakao", "email": "seed11@kakao.com",
     "imap_host": "imap.kakao.com", "imap_port": 993, "app_password": "xxxx",
     "spam_folder": "Junk"},  # Discovered on first run
    # ... 18 more accounts
]

def check_placement(acct, test_subject, lookback_minutes=60):
    """Returns: 'inbox', 'spam', 'not_found'"""
    since = datetime.now() - timedelta(minutes=lookback_minutes)
    with MailBox(acct["imap_host"], acct["imap_port"]).login(
            acct["email"], acct["app_password"]) as mailbox:
        # Discover folders on first run — store spam_folder name in config
        # folders = [f.name for f in mailbox.folder.list()]
        mailbox.folder.set("INBOX")
        if list(mailbox.fetch(AND(subject=test_subject, date_gte=since.date()))):
            return "inbox"
        mailbox.folder.set(acct["spam_folder"])
        if list(mailbox.fetch(AND(subject=test_subject, date_gte=since.date()))):
            return "spam"
    return "not_found"

def run_panel_check(test_subject, lookback_minutes=30):
    results = []
    for acct in SEED_ACCOUNTS:
        placement = check_placement(acct, test_subject, lookback_minutes)
        results.append({"account": acct["email"], "provider": acct["provider"],
                         "placement": placement, "checked_at": datetime.now().isoformat()})
        time.sleep(2)  # Polite delay between connections
    return results
```

**Important:** Naver's IMAP spam folder name is `스팸메일함` (Korean). Kakao/Daum likely uses English `Junk`. Run `mailbox.folder.list()` on first connection to each account and store the result — do not hardcode.

### 20-Account Panel Architecture

| Account # | Provider | Address | Notes |
|---|---|---|---|
| 1–10 | Naver | seed01–10@naver.com | 3 accounts max per phone; need ~4 phone numbers |
| 11–17 | Kakao | seed11–17@kakao.com | 1 per phone; KakaoTalk install required for 2FA |
| 18–20 | Daum | seed18–20@daum.net | Same Kakao account system |

**Critical operational constraints:**
- Naver: IMAP auto-disables after 90 days of non-use → schedule weekly keepalive cron
- Kakao: KakaoTalk must be installed on a real device (or emulator) for initial 2FA setup
- Account creation requires real Korean mobile numbers — budget 4–7 SIM cards total
- Naver account limit: 3 per phone number
- Do not hold all 20 IMAP connections simultaneously — poll serially with 2s delays

**Key risks and mitigations:**

| Risk | Severity | Mitigation |
|---|---|---|
| Naver IMAP auto-disable after 90 days | Medium | Weekly keepalive cron (login + logout) |
| App password invalidation | Medium | Alert on auth failure; re-generate manually |
| Kakao requires KakaoTalk for 2FA setup | High (setup friction) | One-time setup on dedicated device; done once per account |
| Korean spam folder name uses Korean characters | Low | imap_tools handles encoding; folder discovery step at setup |
| 3 accounts per phone limit (Naver) | Medium | Plan for 4+ unique Korean numbers |

---

## 3. Open-Source and API Building Blocks

### Component Inventory

| Component | What It Does | License / Cost | Building Block? | Notes |
|---|---|---|---|---|
| **parsedmarc** | Python CLI + library: parses DMARC aggregate (RUA) and forensic (RUF) reports; outputs JSON/CSV; can push to Elasticsearch/Splunk/Kafka | Apache 2.0 / Free | **Yes — core** | Data source: your DMARC report mailbox (XML zips from Gmail, Naver, etc.). Does NOT show inbox vs. spam — only auth pass/fail. |
| **imapclient** | Python IMAP wrapper over `imaplib`; `find_special_folder()` detects Spam/Junk by IMAP `\Junk` flag; supports `idle()` for push | BSD / Free | **Yes — preferred** for seed mailbox polling | Handles special folder detection across providers |
| **imap_tools** | High-level IMAP abstraction; Pythonic message parsing; folder iteration; search | MIT / Free | **Yes** | Faster to code basic folder-check logic; good for prototype |
| **dnspython** | Full DNS query library for any record type (A, TXT, MX, PTR); essential for DNSBL queries and SPF/DMARC record validation | ISC / Free | **Yes — foundational** | Used internally by parsedmarc |
| **authres** | Parses `Authentication-Results:` headers per RFC 7601 (DKIM, SPF, DMARC, ARC) | MIT/BSD / Free | **Yes** | Extracts DKIM/SPF/DMARC pass/fail from fetched seed emails without re-running auth |
| **pyemailprotectionslib** | Fetches and parses SPF and DMARC DNS records for a domain | MIT / Free | **Yes** | DNS record retrieval and parsing; not for email headers |
| **MXToolbox API** | REST API: blacklist check (100+ lists including KISA), DNS lookups, SMTP diagnostics, SPF/DMARC validation | Freemium — free tier 30 lists; paid for volume | **Yes** | `GET /api/v1/lookup/{type}/{target}`. Checks KISA-RBL and surfaces it as a named result |
| **Spamhaus DQS** | DNSBL service: SBL, XBL, PBL, DBL, ZEN (IP + domain blacklists). Standard DNS A-record query format | Free (non-commercial, registration required); paid commercial | **Yes** | Query format: `{reversed-IP}.{key}.{zone}.dq.spamhaus.net`. 3 lines of Python with dnspython |
| **KISA RBL** | Korea's national spam IP blacklist (불법스팸대응센터). Updated hourly. | Free public DNSBL | **Yes** | Zone: `spamlist.or.kr`. Query: `{reversed-IP}.spamlist.or.kr` — returns `127.0.0.2` if listed |
| **GlockApps API v2** | REST API for creating spam tests, retrieving results programmatically; Swagger-documented | Paid account required | **Conditional** | Automates test creation/result retrieval but doesn't expose their seed panel directly |
| **PowerDMARC API** | REST API for DMARC aggregate/forensic reports, domain security scoring | Paid; free tier for basic | **Conditional** | Most useful if client is already on PowerDMARC |
| **KISA WHOIS OpenAPI** | .kr domain registration info (registrant, creation date, expiry) via data.go.kr | Free; 100K requests/day | **Yes** | Domain age check for .kr domains; relevant for reputation analysis |
| **Cloudflare DoH API** | DNS-over-HTTPS: any record type (TXT for SPF/DMARC/DKIM, MX, A, PTR); JSON response | Free; no auth required | **Yes** | `GET https://cloudflare-dns.com/dns-query?name=&type=TXT`. For programmatic SPF/DKIM/DMARC record validation |
| **EmailEngine** | Self-hosted IMAP API; manages multiple accounts; IMAP sub-connections per folder for real-time monitoring without polling | Source-available; paid license after trial | **Conditional** | Correct architecture for production-scale seed mailbox backend |

### KISA RBL Query — 3 Lines of Python

```python
import dns.resolver

def check_kisa_rbl(ip: str) -> bool:
    reversed_ip = ".".join(reversed(ip.split(".")))
    query = f"{reversed_ip}.spamlist.or.kr"
    try:
        dns.resolver.resolve(query, 'A')
        return True  # LISTED
    except dns.resolver.NXDOMAIN:
        return False  # Clean
```

### Novel Value Stack: What No Existing Tool Does

| Capability | Global Tools | Korea-Specific Tool |
|---|---|---|
| Naver Mail inbox vs. spam placement | No coverage | Direct IMAP monitoring of seed @naver.com accounts |
| Kakao Mail inbox vs. spam placement | No coverage | Direct IMAP monitoring of seed @kakao.com accounts |
| Daum/Hanmail inbox vs. spam placement | No coverage | Direct IMAP monitoring of seed @daum.net accounts |
| KISA RBL check (`spamlist.or.kr`) | Not checked by any global tool | DNS query — 3 lines of Python |
| Korean bounce code interpretation | No reference exists | Localized reference: Naver 550/421, Kakao DAS50 |
| Korean-language UI and reports | English-only | Korean: 수신함/스팸함/수신률/발송 성공률 |
| Naver 화이트도메인 guidance | No awareness | Step-by-step managed workflow (historical; service terminated June 2024) |
| Korean ESP sending range in SPF check | Generic SPF validation | Check if Korean ESP sending IPs are correctly declared |

### Minimum Viable Python Stack

```
imapclient (or imap_tools)  # seed mailbox polling, folder detection
dnspython                   # DNSBL queries (KISA, Spamhaus DQS)
authres                     # Authentication-Results header parsing
requests                    # MXToolbox API calls
parsedmarc                  # DMARC report parsing (long-term monitoring layer)
```

All free/open-source. No licensing fee. Infrastructure cost under ₩50,000/month (VPS + domain).

---

## 4. Missing Layer 1 — Regulatory Compliance Managed Service

### The Regulatory Landscape

Korean bulk email senders face three overlapping frameworks administered by different bodies with no unified compliance interface:

| Framework | Governing Body | Primary Obligation for Email |
|---|---|---|
| 정보통신망법 제50조 | 방통위 / KISA 불법스팸대응센터 | Content format, consent, 수신거부, 발신자 정보 표시 |
| 개인정보보호법 (PIPA) | PIPC | Consent collection, records retention, purpose limitation |
| 화이트도메인 / KISA RBL | KISA (terminated June 2024) | Technical sender registration — now self-serve contact per MBP |

### 정보통신망법 제50조 Compliance Checklist

**Tier 1 — Must implement before first send (compliance gate):**

| Requirement | Specification | Penalty |
|---|---|---|
| **사전 동의** | Explicit opt-in before sending; marketing consent separate from service consent | ₩30M 이하 과태료 |
| **"(광고)" in subject** | Must be the very first characters of the subject line on all commercial emails | ₩30M 이하 과태료 |
| **전송자 명칭 표시** | Sender's company/individual name clearly displayed | Included in §50 violations |
| **수신거부 링크 ("무료수신거부")** | Functional unsubscribe at end of email; free to recipient; labeled "무료수신거부" | ₩30M 이하 과태료 |
| **전송자 연락처** | Company name, email, phone, physical address | Included in §50 violations |

**Tier 2 — Must implement within operational workflow:**

| Requirement | Specification | Penalty |
|---|---|---|
| **수신거부 처리** | Immediately stop sending on unsubscribe; confirm processing to recipient | ₩30M 이하 과태료 |
| **2년 주기 수신동의 재확인** | **CRITICAL GAP — almost universally violated.** Biennial re-confirmation of consent from all subscribers; must include original consent date; new consent or address must be removed | ₩30M 이하 과태료 |
| **야간 광고 전송 제한** | No commercial email 21:00–08:00 without separate nighttime consent | ₩30M 이하 과태료 |

**Tier 3 — Absolute prohibitions (criminal):**
- Sender spoofing / address falsification: 1년 이하 징역 or ₩10M 이하 벌금
- Automated recipient address harvesting: 1년 이하 징역 or ₩10M 이하 벌금
- Obstructing unsubscribe systems: 1년 이하 징역 or ₩10M 이하 벌금

**The 2년 재확인 gap is the single largest unknown compliance exposure.** KISA has not aggressively publicized enforcement, but the obligation exists under 정보통신망법 시행령. Most Korean companies running email marketing are in ongoing violation of this. No Korean ESP automates this workflow.

### PIPC Consent Management Requirements

| Requirement | Detail |
|---|---|
| Explicit consent for collection | Email collected under informed consent specifying marketing purpose |
| Separate marketing consent | Cannot bundle with essential service consent |
| Purpose limitation | Email for order confirmation cannot be used for marketing without separate consent |
| Consent records | Fact, date, and method of consent must be recorded and retained |
| Retention period | Retained until consent withdrawn or membership terminated |
| Withdrawal confirmation | Must confirm processing of withdrawal |

**Double opt-in:** Not legally mandated. But it is the strongest evidentiary proof of consent in a PIPC audit — timestamps confirmation receipt, eliminates "I never consented" disputes. Not required but compliance-optimal.

**Global CMP gap:** OneTrust, Cookiebot, Didomi, and CookieHub all cover Korean PIPA from a web cookie/tracking consent perspective. **None implement Korean email-specific requirements:**
- 2년 주기 수신동의 재확인 workflow
- "(광고)" subject line enforcement checking
- 방통위 complaint rate monitoring
- KISA RBL status monitoring

**No Korean-specific email marketing CMP exists.** The market runs on manual processes, generic ESP unsubscribe tools, and absence of any formal consent audit capability.

### 화이트도메인 — TERMINATED (Critical Update)

> **KISA 화이트도메인 service was formally terminated:**
> - New registrations closed: June 14, 2024
> - Service fully terminated: June 28, 2024
> - Reason stated: shift to managed ESPs (Naver Cloud, Kakao mail services) reduced practical effectiveness

**Post-termination situation:**
- No centralized Korean whitelist exists
- Senders must approach Naver and Kakao individually for whitelist consideration
- Naver implemented unilateral strengthened sender requirements July 19, 2024: mandatory SPF, DKIM, DMARC, PTR/rDNS for all bulk senders
- The managed 화이트도메인 registration service concept now reframes as: **Naver + Kakao individual compliance managed service** (pre-flight, submission, monitoring per provider)

### Pre-flight Checks Before Sending to Korean MBPs

| Check | Tool / Method |
|---|---|
| SPF record validity | MXToolbox SPF Check / dnspython |
| DKIM selector existence | `dig TXT selector._domainkey.domain.com` |
| DMARC record presence and policy level | MXToolbox DMARC Check |
| KISA RBL status | `{reversed-IP}.spamlist.or.kr` DNS query |
| International RBL status | Spamhaus ZEN + DBL via DQS |
| Reverse DNS (PTR record) for sending IP | `dig -x [IP]` |
| 수신거부 link functional test | Manual send + unsubscribe flow test |
| Bounce handling capability | Verify bounce address monitored and processed |
| Domain age and history | KISA WHOIS OpenAPI + historical blacklist lookups |

### Managed Service Specification (3 Phases)

**Phase 1 — Onboarding Audit (Weeks 1–2):**
DNS authentication audit (SPF/DKIM/DMARC), KISA RBL check, international RBL check, 정보통신망법 template audit (subject line, 수신거부 footer, 전송자 정보), consent records audit (CRM review for timestamps, source records, 2년 재확인 workflow existence), 수신거부 system functional test, bounce handling review.

**Phase 2 — Remediation (Weeks 2–4):**
SPF record rewrite, DKIM implementation (2048-bit), DMARC deployment (p=none → p=quarantine → p=reject over 60–90 days), PTR coordination with hosting provider, template remediation for 정보통신망법 compliance, 2년 재확인 workflow build, Naver/Kakao individual registration if eligible (replacing 화이트도메인 path).

**Phase 3 — Ongoing Monitoring (Monthly Retainer):**

| Task | Frequency | Alert Threshold |
|---|---|---|
| KISA RBL status | Weekly | Immediate alert on listing |
| International RBL status | Weekly | Alert if entering Spamhaus/Barracuda |
| DMARC aggregate report analysis (Naver/Kakao rows) | Weekly | Alert if SPF/DKIM alignment <95% |
| 수신거부 system uptime | Monthly functional test | Alert if unsubscribe flow breaks |
| Consent database audit | Quarterly | Flag addresses without consent; flag approaching 2년 re-confirmation due date |
| Template compliance check | On any template change | Review against 정보통신망법 checklist |
| Korean inbox placement test | Monthly | Send to seed panel; report inbox vs. spam |

### The 7 Gaps the Private Compliance Layer Fills

| Gap | What KISA/방통위 Does | What Private Service Adds |
|---|---|---|
| **Translation gap** | Legal/regulatory document (불법스팸방지 안내서 6th ed.) | Translates legal requirements into per-company implementation checklist |
| **Pre-flight gap** | No pre-submission diagnostic | Pre-flight checks catch ~60% of applications that would fail before submission |
| **2년 재확인 gap** | Requirement exists; enforcement unpublicized | Builds and operates the automated biennial re-confirmation workflow |
| **Monitoring gap** | Passive removal without warning | Monitors RBL, DMARC, complaint rate, 수신거부 uptime on client's behalf |
| **Consent records gap** | No audit of individual consent infrastructure | Builds/audits consent record infrastructure; ensures PIPC audit defensibility |
| **Cross-law coordination gap** | Three frameworks, three bodies, no unified interface | Single point of coordination for 정보통신망법 + 개인정보보호법 + technical config |
| **Market education gap** | Publishes guides; no proactive alerting on changes | Ongoing education; alerts as requirements change (e.g., Naver's July 2024 policy shift) |

---

## 5. Missing Layer 2 — ESP Partner Integration

### How Global ESP Partner Programs Work

**Mailchimp & Co:**
- 25% commission on referred customer's first paid plan; 5% ongoing revenue share on connected client accounts (quarterly, no minimum)
- Expert Directory listing (searchable by service category including deliverability)
- White-label dashboards for agency partners
- Deliverability escalation: passive — support may suggest finding a Mailchimp Expert; no formal warm handoff protocol

**Klaviyo K:Partners:**
- Tiered: Basic → Silver → Gold → Platinum → Elite
- Elite tier: roadmap steering sessions, exclusive focus groups
- Technology Partner track (separate) launching H2 2025 with dedicated portal
- No standalone "deliverability partner" category; bundled within agency services

**Twilio SendGrid Expert Services:**
- Expert Consultation (50-day engagement) and Expert Partnership (ongoing named expert) — **staff-delivered, not partner-referral**
- Reveals the gap: small Korean ESPs with no deliverability staff cannot offer this
- Commercial lesson: ESPs that monetize deliverability expertise internally demonstrate the market demand

**Braze:**
- Premium Deliverability Services: named consultant, 3x/week during onboarding, 2x/month ongoing — **staff-delivered**
- AB180 = Braze's Korea partner; AB180 does NOT have documented deliverability expertise
- Korean Braze client with Naver inbox collapse: AB180 → Braze support → US-based Braze deliverability team with no Naver/KISA expertise

### Korean ESP Gap Analysis

| ESP | Partner Program? | Deliverability Support Depth | Escalation Path When Stuck | Gap |
|---|---|---|---|---|
| **스티비 (Stibee)** | Creator Track only (newsletter sponsor program — not consultant/agency). No deliverability partner program. | Help center: soft/hard bounce categories, SPF/DKIM setup guides, list hygiene basics. No inbox placement diagnostics. | Email support; generic authentication checklist; ticket closes. | **Critical.** No consultant referral path. No partner directory. Customer with persistent Naver inbox issues has nowhere to go. |
| **타손 (TasOn)** | No public partner program. E-commerce affiliate/reseller implied via Cafe24. | Basic FAQ: bounce limits, spam filter guidance. Support hours weekdays 9–6 only. | 1:1 ticket system; basic bounce/spam filter guidance; no escalation beyond first-line. | **Critical.** Volume-first platform; zero deliverability expertise layer for enterprise clients. |
| **NHN Cloud** | General cloud partner program (resellers, ISVs). No email deliverability track. | Documentation covers SMTP endpoints, Gmail/Yahoo 2024 compliance notes, auth setup. Treats deliverability as technical configuration only. | SLA-based enterprise support; for deliverability beyond authentication, escalation path unclear. | **Significant.** Infrastructure-level product; clients building on NHN Cloud SMTP have no deliverability partner to call. |
| **Naver Cloud Platform** | General partner program (MSP/reseller tiers). No email deliverability track. | Documentation covers send limits, auth requirements. | Partner inquiry via proposal form. No documented deliverability escalation team. | **Ironic.** Naver Cloud sells outbound email infrastructure; their own mail platform (Naver Mail) is the hardest Korean inbox to reach; no specialist resource exists. |
| **AB180 (Braze Korea)** | AB180 is a partner (of Braze/Amplitude). No sub-partner program. | Implementation and strategy; email deliverability not documented as AB180 capability. | AB180 → Braze support → Braze US deliverability team (no Korea-specific expertise). | **Structural.** Korean enterprise clients get bounced through a chain ending at a US-based consultant with no Naver/KISA knowledge. |

### What the Current Escalation Path Looks Like

When a Korean B2B email sender (using Stibee for CRM marketing) experiences sudden Naver inbox collapse:

1. Call ESP support → "Your SPF, DKIM, DMARC are all correctly configured. Ticket closed."
2. Search Korean web → finds generic SPF/DKIM setup guides; no Naver-specific inbox placement guidance because it doesn't exist in Korean
3. Consider contacting Naver directly → most Korean businesses don't know this path exists; response is slow or absent
4. Accept the failure, switch ESPs hoping the new IP resolves it, or abandon email channel

**The gap between Step 1 and Step 3 is entirely empty. There is no Korean deliverability specialist in this chain.**

### ESP Partnership Proposal Structure

**Section 1 — Problem for the ESP:**
- Deliverability is a documented top-3 ESP churn driver globally
- Your support team has no escalation resource for complex Naver inbox placement issues or KISA-RBL listings
- No Korean-language specialist with Naver Mail expertise currently exists

**Section 2 — Three Arrangement Options:**

| Option | Structure | Commercial |
|---|---|---|
| A — Preferred Partner Listing | Listed on ESP website/help center as recommended resource; support agents use standard handoff script | No fee initially; value = churn reduction and ticket deflection |
| B — Formal Referral Agreement | Active referral by support team; specialist pays 10–20% referral fee or offers reciprocal referrals | Signed referral agreement; UTM tracking |
| C — White-Label Deliverability Service | ESP packages specialist services as premium "Pro Deliverability Support" tier; ESP retains brand; specialist delivers | Revenue share; highest trust requirement |

**Section 3 — Value to the ESP:**
- Churn reduction (deliverability failures resolved → subscriber stays)
- Premium tier differentiation ("we have a deliverability partner for complex issues")
- Support cost reduction (complex tickets absorbed externally)
- No capability investment required

**Section 4 — Pilot Proposal:** 90-day pilot; consultant takes 3 referred cases at no cost to ESP; documents outcomes; formalize on success.

### The Preferred Deliverability Partner Position

**Why first position is permanent in Korea:** Unlike global markets where multiple consultants compete for Mailchimp Expert Directory listings (hundreds of entries), the Korean market has zero consultants with explicit Naver Mail deliverability expertise. The first person to hold a formal preferred partner position with Stibee, TasOn, or NHN Cloud owns that channel entirely — no competing listing.

**Technical credibility requirements:**
- Ability to navigate KISA-RBL process and Naver's post-화이트도메인 individual contact path
- Documented Naver Mail inbox placement improvement (the hardest Korean inbox to reach)
- SPF/DKIM/DMARC, IP warming, bounce management, list hygiene
- Korean regulatory context (정보통신망법 opt-in, 개인정보보호법 data handling)

**Positioning requirement:** Korean-language public writing is the primary credibility path (no cert exists; community reputation = de facto credential). The analog: Laura Atkins (Word to the Wise) is cited by Spamhaus = highest global deliverability authority. A Korean consultant cited by or contributing to KISA materials holds the equivalent position.

**Case study — Email Industries (most direct model):**
- Founded 2008; Mailchimp Expert Directory listed from early days
- Built BlackBox (database used by ESPs to evaluate list threats) → became a vendor TO ESPs, not just a consultant, creating inbound referral
- Reached $3.4M revenue, 37-person team through ESP ecosystem embeddedness + content authority

---

## 6. Missing Layer 3 — Inbox Provider Feedback Reconstruction

### What Currently Exists at Naver Mail

| Mechanism | Status |
|---|---|
| Postmaster Tools (sender dashboard) | **None** |
| Feedback Loop (FBL) | **None** |
| Published SMTP error code reference | **None officially** — reconstructed from community posts: `550 5.7.1` (auth failure/IP block), `421 4.x.x` (rate limit/defer) |
| DMARC RUA reports sent to external senders | **Likely yes** (RFC 7489 compliant); `org_name` in reports unconfirmed — expected `naver.com` or `Naver Corp` |
| Naver's own DMARC record | `v=DMARC1; p=none; rua=mailto:dmarc_reports@worksmobile.com` (their own infra) |
| Postmaster contact (proactive) | **None** |
| Bulk sender unblock path | Reactive only: `help.naver.com` > 스팸 차단 해제 요청 (form requires: sending domain, IP, recipient address, timestamp) |
| Pre-approval program (화이트도메인) | **Terminated June 2024** |
| Naver July 2024 requirements | SPF + DKIM + DMARC + PTR mandatory for all bulk senders; use of @naver.com From on non-Naver infrastructure prohibited |

### What Currently Exists at Kakao/Daum Mail

| Mechanism | Status |
|---|---|
| Postmaster Tools | **None** |
| Feedback Loop (FBL) | **None** |
| Published bounce error codes | **Yes — partially.** `mail.daum.net/policy?category=bulk&tab=returnMessage`: `554 5.7.1 DAS50 [IP]` = IP auto-blocked by anti-spam; `554 5.7.1 DAS51` = domain-level block; `553 5.1.3` = invalid address; `550 5.1.1` = address doesn't exist |
| Bulk sender policy | Published at `mail.daum.net/policy?category=bulk` |
| DMARC RUA reports | **Unverified** — expected yes as RFC-compliant MBP; `org_name` unconfirmed |
| Postmaster contact | **None proactive** — `cs.daum.net` for reactive block disputes with full bounce DSN attached |
| Authentication requirements | SPF + PTR required (published); DKIM/DMARC de facto required but not in published policy |

The `DAS50` prefix = "Daum Anti-Spam" — the most actionable Korean-specific SMTP error. Embedding the blocking IP in the error (`DAS50 [203.0.113.42]`) allows precise diagnosis. No global tool surfaces or interprets this code.

### DMARC Reports as the Only Existing Korean MBP Feedback Channel

A sender with `rua=` in their DMARC record receives aggregate reports from receiving MBPs. These reports reveal, for Naver/Kakao:
- How many messages Naver/Kakao received from your domain per source IP
- SPF alignment pass/fail rate at Naver/Kakao specifically
- DKIM alignment pass/fail rate at Naver/Kakao specifically
- Disposition applied (none/quarantine/reject based on your policy + their enforcement)

**What DMARC reports do NOT reveal:** Whether messages landed in inbox or spam. A message can pass DMARC perfectly and still land in Naver's spam folder due to content scoring, sending IP reputation in Naver's proprietary system, or sender engagement history.

**The actionable insight from DMARC data that senders are ignoring:** A sudden drop in Naver/Kakao row volume in DMARC reports — even before open rates collapse — is an early warning signal that Naver/Kakao has stopped receiving your mail (silent reject or DNS block upstream). parsedmarc + time-series monitoring on Naver/Kakao rows catches this days before visible campaign impact.

### Three Independent Data Sources for the "Naver Postmaster Equivalent"

**Source 1 — DMARC Aggregate Reports (via parsedmarc)**
- What: SPF/DKIM pass rates per source IP; volume to Naver/Kakao per day; disposition applied
- Latency: once-daily report delivery
- Gap: no inbox/spam placement signal

**Source 2 — IMAP Panel Inbox Placement**
- What: Actual inbox vs. spam folder rate at Naver and Kakao for test sends
- Latency: near-real-time (minutes after send)
- Architecture: 20 seed accounts as specified in Section 2
- Unique value: the only way to know actual Korean inbox placement

**Source 3 — DSN/Bounce Code Analysis**
- What: Hard/soft bounce type; Naver 550/421 codes; Kakao DAS50/DAS51 codes with blocking IP
- Latency: immediate
- Gap: only captures non-delivered mail; no signal for mail accepted but spam-foldered

**Combined "Naver Postmaster Equivalent" dashboard:**

| Signal | Source | What It Tells You |
|---|---|---|
| SPF/DKIM/DMARC pass rate at Naver | parsedmarc + Naver RUA | Authentication is working |
| Volume trend to Naver (daily) | parsedmarc | Silent filtering upstream → volume drop precedes open rate collapse |
| KISA RBL status | Direct DNSBL query | Not on Korea's national blacklist |
| Spamhaus ZEN/DBL | DQS DNS query | Not on global IP/domain blacklist |
| Naver inbox placement % | IMAP seed panel | Actual delivery quality — the only real truth |
| Kakao inbox placement % | IMAP seed panel | Kakao/Daum delivery quality |
| Naver bounce code analysis | DSN parsing | IP/domain-level block signals; DAS50 pattern for Kakao |

Only when all signals are green AND inbox placement is high can a Korean sender confidently declare deliverability health.

### Realistic Naver/Kakao Partnership Entry Path

| Stage | Action | Rationale |
|---|---|---|
| **Stage 1: Public credibility** | Korean-language deliverability writing (Naver Blog, LinkedIn, email newsletter) | No credential exists; public writing = de facto credential in Korean market |
| **Stage 2: ESP introductions** | Stibee and Thundermail as entry points | These ESPs have deepest operational relationships with Naver/Kakao support channels; they can make introductions |
| **Stage 3: KISA registration** | Register with KISA 불법스팸대응센터 as email marketing operator | Regulatory credibility signal before any Naver cold outreach |
| **Stage 4: Naver developer ecosystem** | `developers.naver.com` partner inquiry channel | Not a postmaster channel but opens a technical dialogue |
| **Stage 5: KEMA** | Engage 한국이메일마케팅협회 (Korea Email Marketing Association) | Closest domestic equivalent of a sender-side industry body; has some ESP membership |

**Note on M3AAWG:** No public evidence of Naver or Kakao M3AAWG membership. No Korean equivalent of M3AAWG exists domestically. KISA 불법스팸대응센터 is regulatory/complaint-focused, not sender-relationship-focused.

---

## 7. The CSA Institutional Layer

### CSA Technical Architecture (The Direct Analog)

Germany's Certified Senders Alliance (2004, operated by eco — Association of the Internet Industry) is the direct institutional model.

**How CSA's whitelist works technically:**
1. CSA maintains a Certified IP List — a database of IP addresses belonging to certified commercial senders
2. Participating MBPs (GMX, Web.de, T-Online/Telekom) integrate the list into their MTA filtering stack
3. During SMTP delivery, the MTA checks the connecting IP against CSA's DNS zone (DNSBL-style lookup via reverse-IP DNS query; return `127.0.x.x` = trusted tier)
4. Listed IPs: bypass or reduce spam scoring, no throttling, no IP warming requirements
5. The `X-CSA-Complaints` header inserted by certified ESPs routes complaint data back to CSA and the sender — not siloed at the MBP

**CSA certification requirements (selected):**

| Requirement | Standard |
|---|---|
| SPF | Mandatory on MAIL FROM; `-all` or `~all` |
| DKIM | Mandatory; must sign `From`, `X-CSA-Complaints`, `List-Unsubscribe` headers |
| DMARC | Recommended for Standard tier; **mandatory** for Cyber Essentials Mark (as of 2026) |
| rDNS/PTR | Mandatory; must reference sending domain |
| Hard bounce rate | ≤1.0% per MBP |
| Spam complaint rate | ≤0.3% per MBP |
| List-Unsubscribe | Mandatory with RFC 8058 one-click POST |
| Opt-in documentation | Required at application |
| Annual fee | Required |

**How CSA solved the chicken-and-egg problem at founding:**
The solution was institutional, not technical. CSA is a service of eco — Europe's largest Internet industry association (1,000+ members). German MBPs (GMX, Web.de, T-Online) were already eco members. eco brought in DDV (German direct marketing association, representing senders) to co-author the quality criteria. When the whitelist launched, both sides of the market were already co-members of the same neutral organization. The trust anchor was eco's existing institutional credibility, not a new private party asking for trust.

**The key insight for Korea:** The chicken-and-egg problem is dissolved by using an **existing neutral membership organization** as the infrastructure host. In Korea, the candidates are: KISO (Korea Internet Self-governance Organization), 한국인터넷기업협회 (KICCA), or KEMA (한국이메일마케팅협회).

### KISA 화이트도메인 — What It Was Technically

KISA's whitelist was a hybrid: human-reviewed registration (not purely automated) but technically implemented as a DNS-queryable list sitting on top of the `kisarbl.or.kr` DNSBL. Participating portals queried `kisarbl.or.kr` for connecting IPs; whitelisted domains/IPs were exempted from RBL-based blocking.

**Critical: Terminated June 28, 2024.** The gap left by termination is now open. No centralized Korean certification mechanism exists.

### What a Private Certification Body Adds (Post-화이트도메인)

| KISA 화이트도메인 (what it was) | Private Korean Certification Body (what it adds) |
|---|---|
| Free public registry, minimal standards | Fee-based with rigorous standards |
| Binary: on list or not | Tiered certification (basic, premium, enterprise) with tiered MBP benefits |
| Passive registry | Active compliance monitoring with real-time dashboards |
| No sender feedback | Complaint feedback loop: complaints routed to certified sender in real time |
| No consulting layer | Pre-certification audit service (the commercial offering) |
| Government-operated | Private body with incentive to grow certified sender base |
| Korean portals only | Can pursue international MBP partnerships |
| No DMARC requirement | DMARC enforcement from launch (aligning with 2024 Naver/Google requirements) |

### Korean Minimum Viable Certification Infrastructure

**Technical components required:**

| Component | Function |
|---|---|
| IP/domain registry database | Certified sender IPs and domains; status flags; compliance metrics |
| DNS zone | Operated as DNSBL/RHSBL zone (e.g., `certified-senders.kr`); MBPs query at SMTP CONNECT time |
| Pre-certification scanner | Automated SPF/DKIM/DMARC/rDNS validation (MXToolbox-equivalent, run as part of application) |
| Monitoring ingestion | Receive bounce data and complaint data from MBP FBLs; calculate per-MBP rates; trigger alerts |
| Feedback loop routing | Negotiate FBL agreements with Naver/Kakao — hardest part, requires business development |
| Complaint header | `X-KCert-Complaints` equivalent; certified ESPs insert; complaints route to certification body |
| Web portal | Application management, sender lookup, compliance dashboard |

**Institutional partnership path:**

| Stage | Action |
|---|---|
| 1 | Position as private-sector successor to KISA 화이트도메인; brief KISA; seek endorsement |
| 2 | Naver integration: propose that certified senders' IPs are pre-vetted; Naver's MTA queries the DNS zone; Naver reduces spam complaint burden |
| 3 | Kakao integration: same pitch; demonstrate Naver value first |
| 4 | Major Korean ESP integration: Stibee, NHN Cloud, Cafe24 Mail certified sender tier |
| 5 | 방통위/KOFAC endorsement: recognize certification standard as industry self-regulatory mechanism |

**The hard problems (honest assessment):**
1. Getting Naver/Kakao to query a private DNS zone — requires business development, proof of value, time
2. Naver's self-interest conflict — Naver Cloud Outbound Mailer is a paid product; framing must be "reduce your spam complaint burden" not "help senders bypass your product"
3. FBL from Naver/Kakao — neither documents FBL programs; this is a negotiation, not a technical problem
4. Institutional anchor — CSA had eco; a Korean private body needs KISO or KEMA as the neutral host

**The DNS zone itself and monitoring software are commodity problems — they can be built with open-source components described in Section 3. The hard work is institutional.**

---

## 8. MVP Concept: 1–3 Month Single-Developer Build

### The Full Picture: What Combined Data Shows

```
INPUT: Korean sender sends test campaign
                    |
    ┌───────────────┼───────────────────────────┐
    |               |                           |
    v               v                           v
[DMARC layer]   [Blacklist layer]       [Inbox placement layer]
parsedmarc      KISA RBL (spamlist.or.kr)  IMAP seed panel
→ Naver/Kakao   Spamhaus ZEN/DBL           imap.naver.com:993
  volume trend  MXToolbox API             imap.kakao.com:993
  SPF/DKIM rates KISA WHOIS OpenAPI       imap.daum.net:993
  disposition   (domain age)
    |               |                           |
    └───────────────┴───────────────────────────┘
                    |
                    v
          [Korean Deliverability Dashboard]
          ┌────────────────────────────────┐
          │ Naver inbox rate: 71%          │
          │ Kakao inbox rate: 88%          │
          │ KISA RBL: CLEAN               │
          │ Spamhaus ZEN: CLEAN           │
          │ DMARC @ Naver: 98.3% pass     │
          │ Naver volume trend: ↓8% (!)   │
          │ SPF record: VALID             │
          │ DKIM: VALID                   │
          │ DMARC policy: p=quarantine    │
          └────────────────────────────────┘
```

### Month 1: Foundation (Free-tier only, no IMAP panel)

**Stack:** Python (FastAPI), PostgreSQL or SQLite, Streamlit prototype or simple HTML/JS frontend

**Features:**

**Feature 1 — Domain Health Check**
- Input: domain name
- Cloudflare DoH API → pull SPF TXT, DMARC TXT, DKIM selector TXT
- Parse and grade: SPF valid? DMARC policy level? DKIM selector reachable?
- Korean-specific flag: does SPF `include:` chain cover common Korean ESP sending ranges?

**Feature 2 — IP/Domain Blacklist Check**
- MXToolbox API (free tier) → blacklist lookup including KISA
- Spamhaus DQS (free non-commercial) → ZEN + DBL
- KISA RBL direct DNS query (`spamlist.or.kr`)
- Output: traffic-light status per blacklist with Korean priority ranking (KISA first)

**Feature 3 — DMARC Report Ingestion**
- parsedmarc configured to pull from dedicated mailbox (`dmarc-reports@yourtool.com`)
- Parse incoming reports; identify Korean reporters (naver.com, kakao.com, daum.net)
- Time-series: volume per Korean MBP, pass/fail rates
- Alert if Naver/Kakao pass rate drops below threshold or volume drops >20%

### Month 2: Korean-Specific Intelligence Layer

**Feature 4 — 화이트도메인 / Naver-Kakao Compliance Status Tracker**
- Store client's Naver/Kakao individual registration status (post-화이트도메인 termination)
- Guide: step-by-step walkthrough for Naver July 2024 requirements (SPF/DKIM/DMARC/PTR)
- Remind on any status change

**Feature 5 — Korean MBP Volume Dashboard**
- From DMARC data: chart daily volume to Naver vs. Kakao/Daum vs. Gmail vs. other
- Korean MBP share of total send volume
- Alert on sudden Korean MBP volume drop (may indicate silent filtering before DMARC even sees it)

**Feature 6 — Bounce Code Decoder**
- Parse DSN text from Korean MBPs
- Translate Naver 550/421 codes + Kakao DAS50/DAS51 codes into Korean-language action recommendations
- "DAS50 [203.0.113.42] = Kakao's anti-spam blocked your sending IP. Here are the steps to file an unblock request via cs.daum.net."

### Month 3: IMAP Panel (The Differentiator)

**Feature 7 — Naver/Kakao Inbox Placement Test**
- Maintain 20-account seed panel as specified in Section 2
- Client sends test message to panel addresses (unique subject line with test ID)
- IMAP poller checks inbox vs. spam folder per account (5 minutes after send, re-check at 30 minutes)
- Report: "Naver inbox rate: 71% (7/10 accounts), Kakao inbox rate: 88% (15/17 accounts)"
- Korean-language report template for client delivery
- Historical trend chart: inbox placement rate by campaign over time

### Cost Estimate

| Item | Monthly Cost |
|---|---|
| VPS (DigitalOcean / Vultr) | ~₩10,000 |
| Domain | ~₩3,000 |
| Spamhaus DQS (non-commercial) | Free |
| MXToolbox API (free tier) | Free |
| Cloudflare DoH | Free |
| parsedmarc | Free |
| Seed account creation (one-time: phone numbers) | ~₩50,000–₩100,000 one-time |
| **Total ongoing** | **<₩20,000/month** |

The only real cost is the seed accounts. The technical barrier is low. The moat is Korean local presence + institutional knowledge.

### What Makes the Korean-Specific Version Uniquely Valuable

1. **The data that doesn't exist anywhere else:** Naver and Kakao inbox placement rates, derived from real accounts
2. **The context that global tools miss:** KISA RBL as a first-class signal; Korean bounce code interpretation; 정보통신망법 compliance status
3. **The language:** Korean-language reports, Korean-language documentation, Korean-language public writing building authority
4. **The institutional knowledge:** Understanding Naver's July 2024 policy shift, the post-화이트도메인 contact path, the 2년 재확인 obligation that everyone is violating

No US-based tool can replicate items 1, 2, 3, or 4 without a Korea-based operator. The moat is local presence, not technical sophistication.

---

## 9. Sources

**Agent 1 — Inbox Placement Testing Architecture + Building Blocks:**
- [GlockApps — Seed list for email delivery testing](https://glockapps.zendesk.com/hc/en-us/articles/4412752079515)
- [GlockApps API v2 Documentation](https://glockapps.com/api-documentation-v2/)
- [250ok — Seedlist-based inbox monitoring the right way](https://250ok.com/blog/seedlist-based-inbox-monitoring-right-way/)
- [EmailEngine — Inbox Placement Testing architecture](https://learn.emailengine.app/docs/advanced/inbox-placement-testing)
- [parsedmarc Documentation](https://domainaware.github.io/parsedmarc/)
- [parsedmarc GitHub](https://github.com/domainaware/parsedmarc)
- [imapclient API Documentation](https://imapclient.readthedocs.io/en/2.1.0/api.html)
- [imap-tools PyPI](https://pypi.org/project/imap-tools/)
- [MXToolbox API Product Page](https://mxtoolbox.com/c/products/mxtoolboxapi)
- [Spamhaus Free Data Query Service](https://www.spamhaus.com/data-access/free-data-query-service/)
- [Spamhaus DQS Query Format](https://docs.spamhaus.com/datasets/docs/source/70-access-methods/data-query-service/040-dqs-queries.html)
- [MXToolbox — KISA Blacklist Problem Page](https://mxtoolbox.com/problem/blacklist/kisa)
- [MultiRBL — KISA-RBL / spamlist.or.kr](https://multirbl.valli.org/detail/spamlist.or.kr.html)
- [ValiMail authentication-headers GitHub](https://github.com/ValiMail/authentication-headers)
- [authres (Authentication-Results-Python) Launchpad](https://launchpad.net/authentication-results-python)
- [GitHub — ikvk/imap_tools](https://github.com/ikvk/imap_tools)
- [Domain Name System blocklist — Wikipedia](https://en.wikipedia.org/wiki/Domain_Name_System_blocklist)

**Agent 2 — Naver/Kakao IMAP Feasibility:**
- [Naver Mail IMAP settings — GetMailbird](https://www.getmailbird.com/setup/access-naver-com-via-imap-smtp)
- [Naver Mail app password setup — servertrix.com](https://servertrix.com/1879)
- [Naver IMAP app password policy — enterapps.kr](https://www.enterapps.kr/notice/?bmode=view&idx=168294489)
- [Kakao Mail IMAP FAQ — Kakao Customer Service](https://cs.kakao.com/helps_html/1073201883?locale=en)
- [Daum Mail IMAP FAQ — Daum 고객센터](https://cs.daum.net/faq/2482/67411.html)
- [Daum/Kakao IMAP 2FA change January 2025](https://hanmail-notice.daum.net/list/907?index=1)
- [LINE WORKS Mail API](https://developers.worksmobile.com/en/docs/mail)
- [Naver Cloud Outbound Mailer](https://www.ncloud.com/v2/product/applicationService/cloudOutboundMailer)
- [GitHub — Uks98/python_navermail](https://github.com/Uks98/python_navermail)
- [Wikidocs — imaplib IMAP4 이메일 확인](https://wikidocs.net/130371)

**Agent 3 — CSA + KISA 화이트도메인:**
- [Certified Senders Alliance](https://certified-senders.org/)
- [CSA Admission Criteria PDF](https://certified-senders.org/wp-content/uploads/2017/07/CSA_Admission_Criteria.pdf)
- [CSA — Wikipedia](https://en.wikipedia.org/wiki/Certified_Senders_Alliance)
- [CSA Requires DMARC for Cyber Essentials Mark — PowerDMARC](https://powerdmarc.com/csa-cyber-essentials-dmarc-requirement/)
- [RFC 8904 — DNS Whitelist (DNSWL) Email Authentication Method](https://datatracker.ietf.org/doc/rfc8904/)
- [Thundermail — 화이트도메인 서비스 종료 안내](https://blog.thundermail.co.kr/366)
- [Thundermail — 2024년 7월 네이버/한메일 대량발송 변경 내용](https://blog.thundermail.co.kr/368)
- [Cafe24 — 화이트 도메인 등록 방법](https://cafe24.zendesk.com/hc/ko/articles/18331893829913)
- [KISA 화이트도메인 — kisa.or.kr](https://www.kisa.or.kr/1020705)
- [Stibee — Gmail/Naver 수신 정책 변경](https://blog.stibee.com/gmail-sender-guidelines/)

**Agent 4 — Dashboard APIs and Data Sources:**
- [MXToolbox API Methods](https://knowledgebase.mxtoolbox.com/home/api-methods)
- [Spamhaus DQS Documentation](https://docs.spamhaus.com/datasets/docs/source/70-access-methods/data-query-service/000-intro.html)
- [Google Postmaster Tools API Overview](https://developers.google.com/workspace/gmail/postmaster)
- [parsedmarc Sample Outputs](https://domainaware.github.io/parsedmarc/output.html)
- [Cloudflare DoH API Documentation](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/)
- [KISA WHOIS OpenAPI 안내 (Witground)](https://witground.com/kisa-whois-api/)
- [KISA 화이트도메인 등록 안내 (Cafe24)](https://cafe24.zendesk.com/hc/ko/articles/18331893829913)
- [Validity Sender Score DNS Deprecation (Suped)](https://www.suped.com/knowledge/email-deliverability/sender-reputation/how-to-resolve-validity-sender-score-dns-lookup-deprecation)

**Agent 5 — Korean Regulatory Compliance:**
- [정보통신망법 제50조 — 국가법령정보센터](https://www.law.go.kr/법령/정보통신망이용촉진및정보보호등에관한법률/제50조)
- [불법스팸방지 정보통신망법 안내서 PDF (Gabia 호스트)](https://biz.gabia.com/assets/renew/files/spam_prevent_guide.pdf)
- [KISA 불법스팸대응센터](https://spam.kisa.or.kr)
- [개인정보보호법 — 국가법령정보센터](https://www.law.go.kr/LSW/lsInfoP.do?lsId=011357)
- [PIPC 개인정보 처리방침 작성지침 2025.04](https://www.pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS217&mCode=D010030000&nttId=11134)
- [Cookiebot — South Korea PIPA compliance overview](https://www.cookiebot.com/en/south-korea-pipa/)
- [ITEasy — 화이트도메인 등록 가이드](https://www.iteasy.co.kr/solution/whitedomain)
- [2년 주기 수신동의 확인 CELA Q&A](https://www.cela.kr/4/?bmode=view&idx=15400362)

**Agent 6 — ESP Partner Programs:**
- [Mailchimp & Co Benefits](https://mailchimp.com/andco/benefits/)
- [Mailchimp Expert Directory](https://mailchimp.com/experts/)
- [Klaviyo K:Partners introduction](https://www.klaviyo.com/blog/introducing-the-kpartners-program)
- [SendGrid Expert Services](https://sendgrid.com/en-us/solutions/expert-services/ongoing-consulting)
- [CINC / SendGrid Expert Partnership case study](https://customers.twilio.com/en-us/cinc)
- [Braze email deliverability services docs](https://www.braze.com/docs/user_guide/message_building_by_channel/email/best_practices/email_services)
- [AB180 as Braze solutions partner](https://www.braze.com/partners/solutions-partners/AB180)
- [InboxArmy Braze email marketing](https://www.inboxarmy.com/braze-email-marketing/)
- [Word to the Wise](https://www.wordtothewise.com/categories/delivery-improvement/)
- [Laura Atkins at Spamhaus](https://www.spamhaus.org/authors/laura-atkins/)
- [Email Industries about page](https://www.emailindustries.com/about-us/)
- [Email Industries revenue (Latka)](https://getlatka.com/companies/email-industries)
- [스티비 도움말](https://help.stibee.com/)
- [NHN Cloud Email Overview](https://docs.nhncloud.com/ko/Notification/Email/ko/Overview/)
- [Naver Cloud partner program](https://www.ncloud.com/v2/partner/program)

**Agent 7 — Naver/Kakao Inbox Provider Feedback:**
- [NAVER Cloud Outbound Mailer API](https://api.ncloud-docs.com/docs/en/ai-application-service-cloudoutboundmailer)
- [NAVER Works — Bulk Mail Reception Policy Change](https://naver.worksmobile.com/notice/3568/)
- [Daum/Kakao Bulk Email Sender Guidelines](https://mail.daum.net/policy?category=bulk&tab=guideline)
- [Daum/Kakao Bulk Email Return Message Codes](https://mail.daum.net/policy?category=bulk&tab=returnMessage)
- [KakaoMail Spam Policy (English)](https://mail.kakao.com/policy?lang=en)
- [Thundermail — 네이버 대량메일 발송 가이드](https://blog.thundermail.co.kr/9)
- [Stibee — Gmail and Naver Mail Reception Policy Changes](https://blog.stibee.com/gmail-sender-guidelines/)
- [Salesforce Trailblazer — Korea Naver Spam Filter Best Practices](https://trailhead.salesforce.com/trailblazer-community/feed/0D54S00000A8bhzSAB)
- [naver.com DMARC/SPF/DNS configuration — BulkEmailChecker](https://bulkemailchecker.com/verify/domain/naver.com/)
- [Cafe24 — Return Mail Error Codes 550/511/534](https://cafe24.zendesk.com/hc/ko/articles/18357442835353)
- [M3AAWG Registration Information](https://www.m3aawg.org/M3AAWGRegistrationInformation)
- [KLDP — Whitelist Registration Issue for Mail Servers](https://kldp.org/node/161283)

---
*Research compiled via 7 parallel agents, Feb 28, 2026.*
*Parent file: `이메일_발송률_Deliverability_Skills_Positioning_Research_Feb2026.md`*
*Ecosystem map: `한국_이메일_Deliverability_생태계_지도_Feb2026.md`*
