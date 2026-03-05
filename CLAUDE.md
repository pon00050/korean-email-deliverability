# CLAUDE.md — Development Guidelines

## Workflow
- **Test-driven development:** Write failing tests before implementing features or fixes.
  Every check, scorer change, and report feature requires a test first.
- **Bug documentation:** When a bug is discovered that existing tests did not anticipate,
  document the full investigation and resolution in local `BUGS.md` before closing.
  (`BUGS.md` is gitignored — never commit it.)
- **`content/`**: Go-to-market article drafts (Korean-language blog posts). Not shipped with the tool.

## Commands
- Run tests: `uv run pytest tests/ -v`
- Run scan: `uv run check.py <domain>`
- Install deps: `uv sync --extra dev`
- E2E scan (use a real domain — see Privacy rules): `uv run check.py <실제도메인>.co.kr`
  Expected: all 7 checks complete in <15s, HTML report saved to `reports/`

## Claude Code Shell

`uv` is **not on PATH** in Claude Code's bash sandbox. Use these equivalents instead:

| Human command | Claude Code equivalent |
|---|---|
| `uv run pytest tests/ -v` | `python -m pytest tests/ -v` |
| `uv run uvicorn app:app --port 8000` | `.venv/Scripts/python -m uvicorn …` (Win) / `.venv/bin/python -m uvicorn …` (macOS/Linux) |
| `uv run check.py <domain>` | `.venv/Scripts/python check.py …` (Win) / `.venv/bin/python check.py …` (macOS/Linux) |

**Local batch API dev** (no Postgres needed):
```bash
# Windows
SENDERFIT_SKIP_DB=1 .venv/Scripts/python -m uvicorn app:app --host 127.0.0.1 --port 8000
# macOS / Linux
SENDERFIT_SKIP_DB=1 .venv/bin/python -m uvicorn app:app --host 127.0.0.1 --port 8000
```
With `SENDERFIT_SKIP_DB=1` set, the lifespan skips DB/scheduler init and `/health` returns
`"ok"`. The `/batch` endpoint works fully; `/subscribe` will error (requires DB).

**E2E batch test** (run after server is up):
```bash
time curl -s -X POST http://127.0.0.1:8000/batch \
  -H "Content-Type: application/json" \
  -d '{"domains": ["<실제도메인>.co.kr"], "format": "json"}' \
  | python -m json.tool --no-ensure-ascii
```
Expected: HTTP 200, all 7 checks present, completes in ~5s. `--no-ensure-ascii` renders
Korean characters correctly in the terminal instead of `\uXXXX` escapes.

**Unicode JSON pretty-print** — always use `python -m json.tool --no-ensure-ascii` when
inspecting API responses that contain Korean strings. Raw `curl` output will show mojibake
without it.

**Stopping a background server** — `kill $(...)` and `xargs kill` are unreliable on this
Windows/Cygwin shell. Use `TaskStop` with the background task ID instead (the ID is returned
when you launch with `run_in_background=True`).

## Privacy — No Real Company Data in Public Files

**Never use real company names, domains, or scan results in any public-facing file.**
This includes: `README.md`, `sample/`, `content/` articles, code comments, test fixtures,
and any file tracked by git (unless it is explicitly gitignored).

- Use `example.co.kr` as the canonical dummy domain in all **display** examples and
  sample output (README, article screenshots, HTML sample report).
- When a comparison table or multi-domain example is needed, use anonymised labels:
  "세금계산서 SaaS A", "이커머스 B2B SaaS B", etc. — never real brand names.
- Prospect intelligence files (`content/outreach_emails.md`, `content/target_list.md`,
  `content/cold_email_template.md`) are gitignored and must never be committed.
- If real scan data is needed for research or drafting, keep it in a local-only file
  that is covered by `.gitignore` before writing anything.

**Live / end-to-end scan testing must use a real domain.**
`example.co.kr` has no DNS records and will produce all-fail results, which is useless
for verifying scanner behaviour. Use any live `.co.kr` domain you have access to when
running `uv run check.py` locally to validate real output.
Never commit those local run results to a public file.

## Conventions
- Korean is the primary language for all user-facing strings (`message_ko`, `detail_ko`, `remediation_ko`).
- `status` values: `"pass"`, `"warn"`, `"fail"`, `"error"` — no others.
- Score range: 0–100 integers.
- All new checks must return a `CheckResult` (see `src/models.py`).
- Use `uv` for all package management — not pip directly.
- **Named constants over magic numbers:** Prefer dynamic, named constants (e.g. `MIN_DKIM_KEY_BITS`, `MAX_IPS_TO_CHECK`, `GRADE_THRESHOLDS`) over inline literals. Protocol-spec strings (`v=spf1`, `_dmarc.`, etc.) are exempt — they are fixed by the standard.
- **DNS queries must be parallelised and time-bounded:** Use `DNS_TIMEOUT = 5` (from
  `src/checks/_dns_cache.py`) as the `lifetime=` argument on every `dns.resolver.resolve()`
  call. Multiple independent DNS queries within a single check must use `ThreadPoolExecutor`.
  Top-level check execution in `check.py` must use `ThreadPoolExecutor`. Never add a
  sequential loop over DNS queries without justification.
  `get_sending_ips()` (in `src/checks/_dns_cache.py`) caps results to
  `_MAX_IPS = 3` IPs per domain. RBL and blacklist checks only test these IPs.

## Scoring

Overall score weights (defined in `src/scorer.py`, must sum to 100):

| Check | Weight |
|---|---|
| DMARC | 25 |
| SPF | 20 |
| KISA RBL | 15 |
| DKIM | 15 |
| PTR | 10 |
| 국제 블랙리스트 | 10 |
| KISA 화이트도메인 | 5 |

Naver compatibility score uses separate weights (see `src/scorer.py:NAVER_WEIGHTS`).
The Naver score is displayed as a secondary indicator and is NOT added to the overall score
to avoid double-counting.

## Privacy — Local Enforcement Hooks

Two local-only guards prevent accidental commits of private files: a git `pre-commit`
hook and a Claude Code `PreToolUse` hook. Neither travels with the repo — both must be
re-created manually on a new machine.

See **`HOOKS.md`** for full scripts and install instructions.

## Documentation Maintenance

After every significant work session, update the project's docs before closing.
This is what makes results reproducible across machines, agents, and time.

**Rules:**

1. **New operational knowledge → CLAUDE.md immediately.**
   Any friction point discovered and resolved (wrong shell path, env var behavior,
   timing expectation, test pattern, deployment gotcha) must be added to the
   relevant section of CLAUDE.md in the same session it is found.
   Do not leave it only in MEMORY.md — MEMORY.md is machine-local and does not
   travel with the repo.

2. **Bug fixed → local `BUGS.md` before closing.**
   Per the existing Workflow rule: every bug gets a BUGS.md entry with
   symptom · root cause · fix · tests added. This applies to dev-workflow bugs
   (state leaks, bad shell commands) as well as logic bugs.
   `BUGS.md` is **gitignored** — never commit it. Keep it as a local investigation log only.

3. **New env var or feature flag → .env.example + SETUP_PHASE2.md same session.**
   Any env var added to `app.py` must be reflected in `.env.example` (with an
   inline comment) and in the Railway variables table in `SETUP_PHASE2.md`.

4. **E2E timing changes → update CLAUDE.md `## Claude Code Shell` section.**
   If a timed scan run shows materially different results from the documented
   expectation (currently ~5s/domain), update the expected value.

5. **Promote MEMORY.md → CLAUDE.md on project-relevant knowledge — except competitive-intelligence items.**
   MEMORY.md is for session continuity on this machine. When an entry in
   MEMORY.md is clearly project-operational (not personal/session context),
   copy the substance into CLAUDE.md so it survives a machine change.
   Candidates: shell command equivalents, env var behavior, test patterns,
   known timing expectations.
   **Exception:** new-check checklists, debugging notes, and scoring rationale are
   competitive-intelligence items — keep those in MEMORY.md intentionally, not in the
   public CLAUDE.md.

**The test:** A Claude Code agent with an empty MEMORY.md and a fresh clone should
be able to read CLAUDE.md and reproduce any operation that has been done before,
without needing to rediscover anything documented in a prior session.
