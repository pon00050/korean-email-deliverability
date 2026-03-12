# Phase 2 Manual Setup Guide

This document covers every step that cannot be automated — account creation,
DNS configuration, cloud deployment, and end-to-end verification.
All technical details have been verified against current state (March 2026).

**Current status:** All steps complete as of 2026-03-05. Email delivery confirmed.
Railway deploy live and green. Resend domain verified, credentials set, scan report
received in subscriber inbox with correct Korean text and working unsubscribe link.

---

## Prerequisites checklist

- [x] GitHub repo pushed and up to date on the `dev` branch
- [x] `uv.lock` committed (required for Railway to detect uv — see Step 1)
- [x] A domain you control where you can add DNS TXT records — `senderfit.kr` registered and verified
      *(required only for Resend email sending in Step 2; not needed for Railway deploy)*
- [x] Railway Hobby plan — $5/month, subscribed 2026-03-04

---

## Step 1 — Sync dependencies locally ✅ Done

The Phase 2 packages (FastAPI, psycopg, resend, etc.) were added to
`pyproject.toml`. `uv sync` was run to update the lockfile and local venv,
and `uv.lock` was committed.

<details>
<summary>Reference commands (already done)</summary>

```bash
uv sync --extra dev
git add uv.lock pyproject.toml
git commit -m "chore: add Phase 2 dependencies"
git push origin dev
```

> **Why this matters for Railway:** Railway's Railpack builder detects the
> presence of `uv.lock` and automatically runs `uv sync --no-dev --frozen`.
> If `uv.lock` is absent, Railpack falls back to pip and the build will fail.

</details>

---

## Step 2 — Create a Resend account and verify your sending domain

**Status: Partially verified (2026-03-05).** Domain `senderfit.kr` added in Resend
(Tokyo region, `ap-northeast-1`). All four DNS records added in Gabia and confirmed
present. Resend shows "partially verified" — DKIM and SPF (Enable Sending) are
verified; the "Enable Receiving" inbound MX (`@` root) is intentionally not added
(inbound email routing is not needed for this product). Sending is fully enabled.
`RESEND_API_KEY` and `FROM_EMAIL` still need to be updated in Railway Variables.

### 2-a. Sign up and get an API key

1. Go to **resend.com** and create a free account.
2. In the left sidebar, click **API Keys** → **Create API Key**.
3. Name it (e.g. `kr-email-monitor-prod`), set permission to **Sending access**.
4. **Copy the key value immediately** — Resend shows it only once.
   Store it somewhere safe; you will paste it into Railway in Step 3-d.

Free tier: 3,000 emails/month, 1 custom domain.

### 2-b. Add and verify your sending domain

1. In the Resend dashboard, click **Domains** → **Add Domain**.
2. Enter the domain you will send from (e.g. `yourdomain.com`).
3. **Select the Tokyo region** — this is the nearest Resend region to Korea
   and improves inbox placement at Naver/Kakao. Tokyo is available on the
   free tier as of March 2025.
4. Resend shows you a set of DNS records to add. Add all of them at your
   DNS registrar (Cloudflare, Route 53, Namecheap, etc.):

| Type | Name | Value |
|------|------|-------|
| MX   | `send.yourdomain.com` | Resend bounce server (shown in dashboard) |
| TXT  | `send.yourdomain.com` | SPF — `v=spf1 include:amazonses.com ~all` (exact value shown in dashboard) |
| TXT  | `resend._domainkey.yourdomain.com` | DKIM public key (exact value shown in dashboard) |
| TXT  | `_dmarc.yourdomain.com` | `v=DMARC1; p=quarantine; rua=mailto:<your-monitored-inbox>` |

> **Note on SPF:** Resend routes bounces through a `send.yourdomain.com`
> subdomain as the envelope-from. The SPF record goes on that subdomain,
> not on your root domain — so it does not conflict with any existing SPF
> record on `yourdomain.com`.

> **Note on DMARC:** Resend's dashboard suggests `p=none`. Set it to
> `p=quarantine` instead. Naver Mail scores senders with `p=none` lower
> than those with a stricter policy.

5. Click **Verify** in the Resend dashboard. With Cloudflare, verification
   typically completes in under 5 minutes. With other registrars allow up to
   24 hours for DNS propagation.

### 2-b-note — MX record for bounce handling (added 2026-03-05) ✅

The MX record required by Resend under "Enable Sending" was successfully added in
Gabia on 2026-03-05 (an earlier attempt was blocked by Gabia's client-side validator,
but the record saved correctly on retry):

| Type | Host | Value | Priority |
|---|---|---|---|
| MX | `send` | `feedback-smtp.ap-northeast-1.amazonses.com` | `10` |

**What this does:** Routes bounce notifications back to Amazon SES → Resend so
hard-bounced addresses are automatically suppressed from future sends.

### 2-b-note — DMARC rua address (updated 2026-03-05)

The DMARC record added in Gabia uses a personal monitored inbox as the `rua`
aggregate report recipient. This is intentional — the `noreply@senderfit.kr`
address does not have an active mailbox, so reports would be silently discarded.
DMARC aggregate reports (weekly XML digests from major receiving servers) will
arrive at the configured address and can be reviewed for authentication failures.

> To change the `rua` address: update the `_dmarc` TXT record in Gabia.
> No Railway or Resend changes are needed.

### 2-b-note — Inbound MX (`@` root) — not added, not needed

Resend's dashboard shows a third DNS section, "Enable Receiving", which requests:

| Type | Host | Value | Priority |
|---|---|---|---|
| MX | `@` | `inbound-smtp.ap-northeast-1.amazonaws.com` | `10` |

This record is **only needed if you want to receive email at `senderfit.kr` addresses**
(e.g. `hello@senderfit.kr`, `noreply@senderfit.kr`). It is not required for sending.
The monitoring product only sends outbound scan reports — it does not receive email —
so this record has been intentionally omitted.

**Add this record in Gabia if you later want to:**
- Create real inboxes at `@senderfit.kr` (requires also configuring Resend's inbound
  routing or a separate mail host)
- Receive replies to scan report emails at a `senderfit.kr` address

---

### 2-c. Decide your FROM_EMAIL value

Either plain address or display-name format is accepted:

```
noreply@yourdomain.com
이메일 건강도 모니터 <noreply@yourdomain.com>
```

Use plain ASCII in the display name — special characters cause a 422 error
from the Resend API.

### 2-d. Update Railway Variables

Once Resend is set up, go to your app service **Variables** tab and update:

| Key | Value |
|-----|-------|
| `RESEND_API_KEY` | Your real Resend API key |
| `FROM_EMAIL` | Your verified sender address |
| `BASE_URL` | `https://senderfit.kr` |

Railway will redeploy automatically after saving.

---

## Step 3 — Create a Railway project ✅ Done

All sub-steps below are complete as of 2026-03-02.

### 3-a. Create the project ✅

Project is connected to GitHub. Railway auto-picks the `dev` branch
(the repo default branch) — no manual branch selection needed in the
current UI flow.

### 3-b. Add PostgreSQL ✅

Managed Postgres container is provisioned and running.

### 3-c. Wire DATABASE_URL into your app service ✅

`DATABASE_URL` is auto-injected by Railway because both services are in the
same project. No manual action needed.

> **Fallback:** If `DATABASE_URL` is ever missing, add it manually:
> **Variables** → **New Variable** → Key: `DATABASE_URL`,
> Value: `${{Postgres.DATABASE_URL}}`.

> To connect from your local machine (e.g. `psql`), look for
> `DATABASE_PUBLIC_URL` in the Postgres service's own Variables tab.

### 3-d. Add the remaining environment variables ✅

Placeholders were added. Update `RESEND_API_KEY` and `FROM_EMAIL` after
completing Step 2.

| Key | Current value | Action needed |
|-----|--------------|---------------|
| `RESEND_API_KEY` | *(real key set 2026-03-05)* | ✅ Done |
| `FROM_EMAIL` | `noreply@senderfit.kr` | ✅ Done |
| `BASE_URL` | `https://senderfit.kr` | ✅ Set |
| `BATCH_API_KEY` | *(unset)* | **Legacy.** Per-customer keys (Phase 4) preferred. If set, accepted as fallback for `POST /batch`. |
| `SECRET_KEY` | *(required for Phase 4)* | Signing key for session cookies. Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |

### 3-d-update — BASE_URL updated to custom domain (2026-03-05) ✅

`BASE_URL` updated in Railway Variables to `https://senderfit.kr` so that
unsubscribe links in scan report emails point to the public domain, not the
raw Railway subdomain.

### 3-e. Get your public URL ✅

Internal Railway URL: `https://senderfit.kr`
Public URL: `https://senderfit.kr` (custom domain wired 2026-03-05 — see 3-f)

Railway assigns a `<name>.up.railway.app` subdomain with automatic SSL.

### 3-f. Wire custom domain `senderfit.kr` to Railway ✅ (2026-03-05)

**In Railway:** app service → Settings → Networking → Custom Domains → Add `senderfit.kr`.
Railway provided a CNAME target and a verification token. Two DNS records were added
in Gabia to complete wiring:

| Type | Host | Value | Purpose |
|------|------|-------|---------|
| CNAME | `@` | `*(Railway-assigned CNAME target — see Railway dashboard)*` | Routes `senderfit.kr` → Railway app |
| TXT | `_railway-verify` | `*(Railway-assigned verification token — see Railway dashboard)*` | Domain ownership verification |

> **Port:** When adding the custom domain in Railway, select the FastAPI app port
> (not 5432 — that is Postgres and must never be exposed publicly).

After DNS propagation, `https://senderfit.kr` serves the signup form directly.

<details>
<summary>How to generate a domain on a new Railway service</summary>

**Option A — Canvas prompt (fastest):** After a successful deploy, Railway may
show a button or prompt directly on the service tile on the project canvas.

**Option B — Settings tab:**
1. Click your app service tile → **Settings** tab.
2. Scroll down to **Networking** → **Public Networking**.
3. Click **Generate Domain**. Railway injects `$PORT` automatically — no port
   number needs to be entered.

**Option C — Railway CLI:**
```bash
railway domain
```

</details>

### 3-f. Verify the builder detects uv ✅

Railpack detects `uv.lock` and runs `uv sync --no-dev --frozen` during the
build — confirmed in build logs.

### 3-g. Start command ✅

`railway.toml` sets:

```toml
[deploy]
startCommand = "uv run uvicorn app:app --host 0.0.0.0 --port $PORT"
```

`uv run` is required — bare `uvicorn` fails because the venv is not on PATH
in Railpack's runtime environment.

---

## Step 4 — Health check endpoint ✅ Done

`/health` is already implemented in `app.py` and `railway.toml`:

```python
# app.py
@app.get("/health")
async def health():
    return {"status": "ok"}
```

```toml
# railway.toml
[deploy]
startCommand = "uv run uvicorn app:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 300
```

`healthcheckTimeout = 300` is needed because the app initialises a DB
connection on startup — 30 s is too short.

---

## Step 5 — Verify the live deployment

**Status: Fully verified ✅ (2026-03-05)**

```
[x] Build log shows "uv sync" (not pip install)
[x] Deployment succeeds (green tick on Railway canvas)
[x] https://senderfit.kr returns the signup form
[x] https://senderfit.kr/docs shows FastAPI Swagger UI
[x] https://senderfit.kr/health returns {"status": "ok"}
[x] https://senderfit.kr returns the signup form (custom domain live)
[x] Submit the signup form with a real .co.kr domain and your email address
[x] Scan report email arrives in your inbox — confirmed 7:38 AM GMT+9, 2026-03-05
[x] Email displays correctly (Korean text, scores, check results, unsubscribe link)
[x] Railway Postgres: row confirmed in subscribers table
```

Naver compatibility 53/100. SPF ✅ DKIM ❌ DMARC p=none ⚠️ PTR ✅ KISA RBL ✅ 국제 블랙리스트 ✅

To inspect the database directly:

```bash
# Get the public URL from Railway dashboard → Postgres service → Variables
psql "$POSTGRES_PUBLIC_URL" -c "SELECT id, domain, email, active, next_scan_at FROM subscribers;"
```

---

## Step 6 — CI workflow ✅ Done (updated 2026-03-02)

`.github/workflows/tests.yml` now triggers on pushes and PRs to both `main`
and `dev`:

```yaml
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]
```

All 90 tests run in CI on every push to `dev`:
- 17 Phase 1 tests
- 27 Phase 2 tests (mocked Resend, SQLite for DB — no external services needed)
- 7 Phase 3a tests (batch API)

---

## Phase 4 — Database Migration

If upgrading from Phase 2/3 to Phase 4, the existing `subscribers` table needs a new
nullable column to optionally link subscribers to customer accounts:

```sql
ALTER TABLE subscribers ADD COLUMN customer_id INT REFERENCES customers(id);
```

The new tables (`customers`, `api_keys`, `scans`, `scan_checks`, `dmarc_uploads`) are
created automatically on app startup by `create_tables()` in `src/db.py`.

---

## Troubleshooting

**App unreachable at the public URL despite a green deploy**
→ Railway injects `$PORT` automatically — no manual configuration of the PORT
variable is needed. If the app is not reachable despite a green deploy, check
the Railway deploy logs for startup exceptions (e.g. a missing env var causing
an import error). Fix the underlying issue and redeploy.

**Build fails: `uvicorn: command not found`**
→ The start command is missing `uv run`. Railway's Railpack runtime does not
put the venv on PATH. The correct command is:
`uv run uvicorn app:app --host 0.0.0.0 --port $PORT`

**Build fails: packages not found despite successful `uv sync` step**
→ `uv.lock` is stale. Railway runs `uv sync --locked` (strict mode) — a
lockfile that does not match `pyproject.toml` causes packages to be skipped
silently during build. Run `uv sync --extra dev` locally and commit the
updated `uv.lock`.

**`DATABASE_URL` not found at runtime**
→ Auto-injection normally works for same-project services. If missing, add
manually: Key `DATABASE_URL`, Value `${{Postgres.DATABASE_URL}}` in the app
service Variables tab. See Step 3-c.

**Resend returns 422 `Invalid 'from' field`**
→ Special characters in `FROM_EMAIL` display name. Use plain ASCII or
just a bare address: `noreply@yourdomain.com`.

**Resend returns 403 `Domain not verified`**
→ DNS records have not propagated yet, or you clicked Verify before they
propagated. Wait and click Verify again in the Resend dashboard.

**Scheduler not running scans**
→ APScheduler starts inside the `lifespan` handler. If the app fails to
start (e.g. missing env var causes an import error), the scheduler never
starts. Check the Railway deploy logs for startup exceptions.

**Multiple scan emails per subscriber per cycle**
→ You scaled to more than 1 worker. APScheduler is not safe with multiple
processes without a shared job store. Keep `--workers 1`.
