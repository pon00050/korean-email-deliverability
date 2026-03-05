# NEXT_ACTIONS.md — Open Action Items

Last updated: 2026-03-05

This is the **only file in the project that tracks open work.**
All other files are history/vision. Add new tasks here, nowhere else.

This file answers "What are the next action open items?"
Organized by urgency, not product phase. For feature-phase context, see ROADMAP.md.

---

## Status: Phases 1–3a complete. Product works. Revenue requires the items below.

---

## Tier 1 — Required before first paid customer (1–2 weeks)

- [ ] **Landing page**
  `senderfit.kr` currently shows a bare signup form. A prospective buyer needs:
  what the product does, why it matters (KISA RBL silently blocks senders, Naver
  filtering is a black box), pricing, and a clear CTA. Even a single-page HTML works.

- [ ] **Pricing decision + public pricing page**
  No pricing is published anywhere. Outbound cannot reference a number.
  Draft exists in `content/pricing_strategy_research.md` (gitignored) — needs to be
  decided and published before any sales conversation.

- [ ] **Payment integration**
  No Stripe, no Toss Payments, no billing mechanism of any kind exists.
  For Korean B2B, Toss Payments or invoice-on-signup are the realistic paths.
  Without this, there is no route from "interested" to "paying".

- [ ] **Per-customer API keys for the batch endpoint**
  The batch API currently uses a single shared `BATCH_API_KEY` env var.
  Selling batch access to multiple customers requires per-customer keys.
  Minimum viable: `api_keys(key_hash, customer_id, created_at, active)` DB table +
  lookup in the `/batch` auth middleware. No UI required at first — manual provisioning is fine.

---

## Tier 2 — Required to retain customers (weeks)

- [ ] **Scan history / results dashboard**
  Subscribers receive email reports but cannot log in to see past scans.
  Without any history view, churn after the first automated email is high.

- [ ] **Batch API onboarding documentation**
  No public docs exist for POST /batch. A paying B2B customer needs:
  authentication, request/response schema, rate limits, and error codes.
  A single markdown page or README section is the minimum.

---

## Completed (context only)

- [x] 7-check scanner (SPF, DKIM, DMARC, PTR, KISA RBL, international blacklists, whitedomain)
- [x] Naver compatibility composite score
- [x] Hosted signup + scheduled monitoring (senderfit.kr, Railway, PostgreSQL, APScheduler)
- [x] Batch B2B API (POST /batch, ≤50 domains, JSON + CSV output)
- [x] Optional API key auth on /batch (single shared key via BATCH_API_KEY env var)
- [x] 90 tests passing, CI green (GitHub Actions)
- [x] senderfit.kr + senderfit.co.kr domains registered (Gabia, 2026-03-04)
- [x] GitHub repo public, bilingual README, CI badge
- [x] Resend email delivery end-to-end verified (2026-03-05) — scan report received in inbox, Korean text correct, unsubscribe link working
