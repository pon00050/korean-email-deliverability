# Phase 2 Manual Setup Guide

This document covers every step that cannot be automated — account creation,
DNS configuration, cloud deployment, and end-to-end verification.
All technical details have been verified against current documentation (March 2026).

---

## Prerequisites checklist

- [ ] GitHub repo pushed and up to date on the `dev` branch
- [ ] `uv.lock` committed (required for Railway to detect uv — see Step 1)
- [ ] A domain you control where you can add DNS TXT records
- [ ] A credit card (Railway Hobby plan is $5/month minimum after the 30-day trial)

---

## Step 1 — Sync dependencies locally

The Phase 2 packages (FastAPI, psycopg, resend, etc.) were added to
`pyproject.toml`. Run `uv sync` to update your lockfile and local venv.
`uv sync` automatically re-resolves and updates `uv.lock` when
`pyproject.toml` has changed — no separate `uv lock` step is needed.

```bash
uv sync --extra dev
```

Then **commit the updated `uv.lock`**:

```bash
git add uv.lock pyproject.toml
git commit -m "chore: add Phase 2 dependencies"
git push origin dev
```

> **Why this matters for Railway:** Railway's Railpack builder detects the
> presence of `uv.lock` and automatically runs `uv sync --no-dev --frozen`.
> If `uv.lock` is absent, Railpack falls back to pip and the build will fail
> because `pyproject.toml` does not have a `[project.scripts]` entry or
> `requirements.txt`.

---

## Step 2 — Create a Resend account and verify your sending domain

### 2-a. Sign up and get an API key

1. Go to **resend.com** and create a free account.
2. In the left sidebar, click **API Keys** → **Create API Key**.
3. Name it (e.g. `kr-email-monitor-prod`), set permission to **Sending access**.
4. **Copy the key value immediately** — Resend shows it only once.
   Store it somewhere safe; you will paste it into Railway in Step 4.

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
| TXT  | `_dmarc.yourdomain.com` | `v=DMARC1; p=quarantine; rua=mailto:you@yourdomain.com` |

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

### 2-c. Decide your FROM_EMAIL value

Either plain address or display-name format is accepted:

```
noreply@yourdomain.com
이메일 건강도 모니터 <noreply@yourdomain.com>
```

Use plain ASCII in the display name — special characters cause a 422 error
from the Resend API.

---

## Step 3 — Create a Railway project

Railway no longer has a permanent free tier. A **Hobby plan** ($5/month)
is required for services to keep running beyond the 30-day trial.
The $5/month subscription includes $5 of usage credit.

### 3-a. Create the project

1. Log in at **railway.com** → **New Project**.
2. Select **Deploy from GitHub repo**.
3. Authorise the GitHub App if prompted, then select your repository.
4. Choose the **`dev`** branch (this is your Phase 2 development branch).
5. Railway triggers an initial build immediately. It will likely fail at
   this point because the database and environment variables are not yet
   configured — that is expected. Continue to the next steps.

### 3-b. Add PostgreSQL

1. On the project canvas, press **Cmd+K** (macOS) or **Ctrl+K** (Windows)
   and type "PostgreSQL", or click **+ New** → **Database** →
   **Add PostgreSQL**.
2. Railway provisions a managed Postgres container as a service inside your
   project. This takes ~30 seconds.

### 3-c. Wire DATABASE_URL into your app service

Railway automatically injects the Postgres connection variables into your app
service when both services are in the same project. Check your app service's
**Variables** tab — you should already see `DATABASE_URL` populated with a
value like `postgresql://postgres:...@postgres.railway.internal:5432/railway`.
No manual action needed.

> If `DATABASE_URL` is not present, add it manually: **Variables** →
> **New Variable** → Key: `DATABASE_URL`, Value: `${{Postgres.DATABASE_URL}}`.

> To connect from your local machine (e.g. `psql`), look for
> `DATABASE_PUBLIC_URL` in the Postgres service's own Variables tab —
> this is the externally-routable address.

### 3-d. Add the remaining environment variables

Still in your app service's **Variables** tab, add these — use placeholder values
for now if you have not set up Resend yet (you will update them later):

| Key | Value |
|-----|-------|
| `RESEND_API_KEY` | Your Resend key, or `placeholder` for now |
| `FROM_EMAIL` | e.g. `noreply@yourdomain.com`, or `placeholder@example.com` for now |
| `BASE_URL` | Leave blank for now — fill in after Step 3-e |

Railway triggers a redeploy automatically each time you save variables.

### 3-e. Get your public URL

> **The Generate Domain option only appears after a successful deployment.**
> Set the env vars in Step 3-d first (even with placeholder values) so the
> app starts up, then come back here.

There are three ways to find it:

**Option A — Canvas prompt (fastest):** After a successful deploy, Railway may
show a button or prompt directly on the service tile on the project canvas.
Click it to generate a domain instantly.

**Option B — Settings tab:**
1. Click your app service tile → **Settings** tab.
2. Scroll down to the **Networking** section → **Public Networking**.
3. Click **Generate Domain** and enter port `8000`.

**Option C — Railway CLI:**
```bash
railway domain
```

Railway assigns a `<random-name>.up.railway.app` subdomain with automatic SSL.
No domain purchase needed.

Once you have the URL, go back to **Variables** and set:
`BASE_URL` = `https://<your-assigned-name>.up.railway.app`

Railway will redeploy automatically.

### 3-f. Verify the builder detects uv

Railway now defaults to **Railpack** (not Nixpacks) for new services.
Railpack automatically detects `uv.lock` and runs `uv sync --no-dev --frozen`
during the build — no configuration needed, as long as `uv.lock` is committed.

If the build log shows `pip install` instead of `uv sync`, it means `uv.lock`
is missing from the repo. Go back to Step 1.

### 3-g. Start command

The `railway.toml` in the repo sets the correct start command for Railpack:

```toml
[deploy]
startCommand = "uvicorn app:app --host 0.0.0.0 --port $PORT"
```

This is used automatically. No dashboard changes needed.

> **Note:** gunicorn is not used here because Railpack's start command
> detection works best with a single explicit uvicorn process. APScheduler
> runs as a background thread inside that single process, which is correct.

---

## Step 4 — Add a health check endpoint

Railway health checks run at deploy time to confirm the app started
successfully. Add this route to `app.py` (before the lifespan handler):

```python
@app.get("/health")
async def health():
    return {"status": "ok"}
```

Then update `railway.toml` to point the health check at it:

```toml
[deploy]
startCommand = "gunicorn app:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 1 --timeout 120"
healthcheckPath = "/health"
healthcheckTimeout = 300
```

Commit and push — Railway will redeploy.

---

## Step 5 — Verify the live deployment

Work through this checklist in order:

```
[ ] Build log shows "uv sync" (not pip install)
[ ] Deployment succeeds (green tick on Railway canvas)
[ ] https://<your-url>.railway.app returns the signup form
[ ] https://<your-url>.railway.app/docs shows the FastAPI Swagger UI
[ ] https://<your-url>.railway.app/health returns {"status": "ok"}
[ ] Submit the signup form with a real .co.kr domain and your email address
[ ] Scan report email arrives in your inbox within ~2 minutes
[ ] Email displays correctly (inline CSS, no broken images, Korean text renders)
[ ] Unsubscribe link in the email works (loads the unsubscribed confirmation page)
[ ] Railway Postgres: confirm a row exists in the `subscribers` table
    (use the Railway Postgres connect tab or a local psql with the PUBLIC_URL)
```

To inspect the database directly:

```bash
# Get the public URL from Railway dashboard → Postgres service → Variables
psql "$POSTGRES_PUBLIC_URL" -c "SELECT id, domain, email, active, next_scan_at FROM subscribers;"
```

---

## Step 6 — Update the CI workflow for Phase 2 tests

The GitHub Actions workflow currently runs `uv sync --extra dev` which will
now install the Phase 2 packages (FastAPI, psycopg, resend, etc.) in CI.
No changes to `.github/workflows/tests.yml` are needed — `uv sync --extra dev`
already handles new dependencies automatically via the updated `uv.lock`.

Confirm CI passes after pushing to `dev`:
- All 44 tests should pass (17 Phase 1 + 27 Phase 2)
- Phase 2 tests use mocks for Resend and SQLite for the DB — no external
  services needed in CI

---

## Troubleshooting

**Build fails: `uv: command not found`**
→ `uv.lock` is not committed. Run `uv sync --extra dev` locally and commit
the updated `uv.lock`.

**`DATABASE_URL` not found at runtime**
→ The variable reference `${{Postgres.DATABASE_URL}}` was not added to
the app service's Variables tab. See Step 3-c.

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
