# NEXT_ACTIONS.md — Open Action Items

Last updated: 2026-03-13

This is the **only file in the project that tracks open work.**
All other files are history/vision. Add new tasks here, nowhere else.

This file answers "What are the next action open items?"
Organized by urgency, not product phase. For feature-phase context, see ROADMAP.md.

---

## Status: Phases 1–4 complete (web UI, dashboard, PDF, DMARC upload). Revenue requires the items below.

---

## Tier 1 — Required before first paid customer (1–2 weeks)

- [x] **Landing page** *(Phase 4.3 — 2026-03-13)*
  HTMX-powered Korean landing page with inline scan, value props, and CTAs.

- [ ] **Pricing decision + public pricing page**
  No pricing is published anywhere. Outbound cannot reference a number.
  Draft exists in `content/pricing_strategy_research.md` (gitignored) — needs to be
  decided and published before any sales conversation.

- [ ] **Payment integration**
  No Stripe, no Toss Payments, no billing mechanism of any kind exists.
  For Korean B2B, Toss Payments or invoice-on-signup are the realistic paths.
  Without this, there is no route from "interested" to "paying".

- [x] **Per-customer API keys for the batch endpoint** *(Phase 4.1 — 2026-03-13)*
  `sf_live_` prefixed keys, SHA-256 hashed in DB, admin CLI provisioning via `admin.py`.
  Legacy `BATCH_API_KEY` env var accepted as fallback.

---

## Tier 2 — Required to retain customers (weeks)

- [x] **Scan history / results dashboard** *(Phase 4.4 — 2026-03-13)*
  Multi-domain dashboard with session auth, login/register, scan history per domain.

- [x] **Batch API onboarding documentation** *(2026-03-17)*
  `docs/batch-api.md` — Korean-language, covers auth, request/response schema,
  rate limits, error codes, and key management CLI.

---

## Tier 3 — Required for data-driven scoring and research output (longer-term)

- [ ] **Collect labelled delivery outcome data**
  All supervised ML approaches (logistic regression, random forests, Lasso) that could
  validate or replace the current hand-tuned scoring weights in `src/scorer.py` require
  ground-truth labels: "did this domain's email reach the Naver inbox, or was it
  spam-filtered / blocked?"

  Without this data, the scoring model remains heuristic and the statistical work in
  `research/ISLR_relevant_topics_for_scoring_model_Mar2026.md` cannot be executed.

  Three paths to acquiring labels, in order of feasibility:

  1. **Customer feedback loop (nearest term):** Add an optional `delivery_rate` field
     to the batch API response schema now, before customers exist, so the habit and
     the data contract are in place from day one. Ask early batch customers to report
     their actual delivery rates back via a lightweight endpoint or survey.

  2. **ESP data partnership:** Approach Stibee, TasOn, or NHN Cloud for a data-sharing
     arrangement — they hold delivery rate data for thousands of Korean domains.
     Positioning: their data improves a scoring model that makes their customers
     better senders, which reduces their own spam complaints.

  3. **Naver seed account inbox test (Phase 6):** Build internally — own seed Naver
     accounts, send test emails, classify inbox vs. spam. High operational cost;
     deferred until there is clear paying demand for inbox placement data specifically.

---

## Completed (context only)

- [x] 7-check scanner (SPF, DKIM, DMARC, PTR, KISA RBL, international blacklists, whitedomain)
- [x] Naver compatibility composite score
- [x] Hosted signup + scheduled monitoring (senderfit.kr, Railway, PostgreSQL, APScheduler)
- [x] Batch B2B API (POST /batch, ≤50 domains, JSON + CSV output)
- [x] Optional API key auth on /batch (single shared key via BATCH_API_KEY env var)
- [x] 156 tests passing, CI green (GitHub Actions)
- [x] senderfit.kr + senderfit.co.kr domains registered (Gabia, 2026-03-04)
- [x] GitHub repo public, bilingual README, CI badge
- [x] Resend email delivery end-to-end verified (2026-03-05) — scan report received in inbox, Korean text correct, unsubscribe link working
- [x] Security hardening pass (2026-03-13) — 16 findings addressed, `docs/SECURITY_HARDENING.md`
