# Revenue Model — Korean Email Deliverability Scanner
_Date: 2026-03-02 | Status: Working draft, private_

All figures in KRW. USD conversions at ₩1,380/$.

---

## Channel 1 — Direct SaaS Subscription

Recurring revenue model enabled by Phase 2 (hosted scheduler + email delivery).

```
MRR = subscribers × ARPU

Conservative tier assumption: ₩30,000/mo per domain
(below Stibee Standard; zero Korean-language competition at any price)
```

| Scenario | Subscribers | MRR | ARR |
|---|---|---|---|
| Early traction | 30 | ₩900,000 | ₩10.8M (~$7,800) |
| 100 subscribers | 100 | ₩3,000,000 | ₩36M (~$26,000) |
| 300 subscribers | 300 | ₩9,000,000 | ₩108M (~$78,000) |
| 1,000 subscribers | 1,000 | ₩30,000,000 | ₩360M (~$261,000) |

**Unit economics:**
- Railway hosting: ~$10–25/mo (Hobby plan, scales with DB size)
- Resend: free tier covers 3,000 emails/mo; $20/mo above that
- COGS per subscriber: ~₩0 marginal at < 300 subscribers
- Gross margin at scale: ~95%+

**TAM context:** DMARC adoption in Korea is 1.8% (APAC lowest), meaning ~98% of the
target market is broken by default. Every Korean company sending transactional email
is a potential subscriber.

---

## Channel 2 — Consulting / Remediation (Services Revenue)

The free scan report is a sales tool. The engagement funnel:

```
Tier 0 (free scan) → Tier 1 (report) → Tier 2 (fix) → Tier 3 (retainer)
```

| Tier | Price | Billable hours | Effective hourly rate |
|---|---|---|---|
| Tier 1 — Scan report + written summary | ₩30,000–80,000 | ~1h | ₩30–80k/h |
| Tier 2 — Setup + remediation (SPF/DKIM/DMARC) | ₩200,000–500,000 | 3–8h | ~₩60–70k/h |
| Tier 3 — Annual retainer (4× quarterly scans) | ₩150,000–300,000/yr | ~4h/yr | ~₩50–75k/h |
| Full remediation (SPF+DKIM+DMARC none→reject+PTR) | ₩900,000–2,100,000 | 15–30h | ~₩60–70k/h |

Pricing is calibrated just below the Korean senior IT security consultant day rate
(₩475,000–600,000/day). High perceived value, no sticker shock.

**Steady-state monthly model (solo operator, month 12+):**

```
2 × Tier 2 engagements/mo:   2 × ₩300,000 = ₩600,000
Retainer base (12 signed):   12 × ₩225,000/yr ÷ 12 = ₩225,000/mo
────────────────────────────────────────────────────────
Total:                        ₩825,000/mo (~$600/mo)
```

Consulting is primarily a conversion mechanism — paid engagements convert prospects
into long-term SaaS subscribers.

---

## Channel 3 — KISA 공급기업 Pool (Primary Revenue Strategy)

Government-subsidized B2B. Not volume-driven — per-engagement, premium pricing.

```
Per-SME client economics:
  Solution price:      ₩5,000,000
  Government pays:     80% = ₩4,000,000  (up to ₩4.4M SECaaS cap)
  SME co-pay:          20% = ₩1,000,000
  Revenue per engagement: ₩5,000,000 (~$3,600)
```

| Engagements/year | Revenue per engagement | Annual revenue |
|---|---|---|
| 5 | ₩5,000,000 | ₩25M (~$18,000) |
| 10 | ₩5,000,000 | ₩50M (~$36,000) |
| 20 | ₩5,000,000 | ₩100M (~$72,000) |

**Program constraints:**
- ~430 total beneficiary SMEs program-wide across all approved vendors (2025; shrinking)
- Not a volume play — a premium channel with a capped ceiling
- 5–10 engagements/year is realistic for a new entrant in the pool
- Requires legal entity registration (사업자등록증 minimum, 1인 법인 preferred)
- Application window: late April – May 28, 2026. Earliest subsidy revenue: 2026 하반기

**Key pricing dynamic:** At 80% subsidy, the SME buyer's effective cost drops to ₩1M
for a ₩5M service. The sales conversation shifts from "is this affordable?" to
"when can we start?"

---

## Combined Model — 12-Month Projection

```
Month 1–3  (Q1): Resend live, first organic subscribers, first consulting engagements
Month 4–6  (Q2): KISA application filed, content published, cold email to Tax SaaS targets
Month 7–9  (Q3): First KISA-subsidized engagements (earliest possible subsidy revenue)
Month 10–12 (Q4): SaaS ARR growing, retainer base accumulating
```

| Revenue stream | Conservative (Year 1) | Optimistic (Year 1) |
|---|---|---|
| SaaS subscriptions | ₩6M (~30 subs avg) | ₩18M (~100 subs avg) |
| Consulting / remediation | ₩12M (2 engagements/mo) | ₩36M (6 engagements/mo) |
| KISA subsidized engagements | ₩25M (5 × ₩5M) | ₩50M (10 × ₩5M) |
| **Total Year 1** | **₩43M (~$31,000)** | **₩104M (~$75,000)** |

---

## Key Leverage Points

1. **Zero Korean-language competition at any price point.** The entire global tool set
   (dmarcian, EasyDMARC, MXToolbox) has no Korean-language UI. Korean IT managers will
   not use English-only tooling for compliance decisions.

2. **1.8% DMARC adoption** means ~98% of the target market is broken by default. Every
   cold email with a real scan result is a live demonstration of the problem.

3. **Tax SaaS delivery failures carry legal penalties (0.3–0.5% surcharge per transaction).**
   The pain is quantifiable and the liability is personal for the CTO. Unusually strong
   willingness-to-pay signal.

4. **KISA channel inverts the pricing conversation.** 80% government subsidy makes the
   effective SME cost ₩1M for a ₩5M service. Objection to price largely disappears.

5. **Phase 2 architecture was the KISA eligibility gate.** A CLI tool alone would not
   qualify as SECaaS. The hosted scheduler + email delivery architecture directly unlocks
   the highest-value revenue channel.
