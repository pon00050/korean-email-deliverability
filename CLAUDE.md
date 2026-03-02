# CLAUDE.md — Development Guidelines

## Workflow
- **Test-driven development:** Write failing tests before implementing features or fixes.
  Every check, scorer change, and report feature requires a test first.
- **Bug documentation:** When a bug is discovered that existing tests did not anticipate,
  document the full investigation and resolution in `BUGS.md` before closing.
- **`content/`**: Go-to-market article drafts (Korean-language blog posts). Not shipped with the tool.

## Commands
- Run tests: `uv run pytest tests/ -v`
- Run scan: `uv run check.py <domain>`
- Install deps: `uv sync --extra dev`
- E2E scan (use a real domain — see Privacy rules): `uv run check.py barobill.co.kr`
  Expected: all 7 checks complete in <15s, HTML report saved to `reports/`

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

## Adding a New Check

Seven steps, in order. Missing any one will cause a silent failure.

1. **Create `src/checks/<name>.py`**
   - Return `CheckResult` with `name` matching the string you'll use in `WEIGHTS`
   - Apply `lifetime=DNS_TIMEOUT` to every `dns.resolver.resolve()` call
   - Parallelize independent DNS queries with `ThreadPoolExecutor`

2. **Export from `src/checks/__init__.py`**
   - Add `from src.checks.<name> import check_<name>`

3. **Add to `WEIGHTS` in `src/scorer.py`**
   - Adjust other weights so the dict still sums to 100
   - Add rationale comment

4. **Wire into `check.py`**
   - Add `check_<name>` to the checkers list submitted to `ThreadPoolExecutor`

5. **Wire into `src/scheduler.py`**
   - Add `check_<name>` to the checkers list inside `_default_scan_executor()`

6. **Update `tests/test_integration_scan_pipeline.py`**
   - Add the new check to the `checkers` list in `_run_all_checks()`
   - Add a matching DNS response branch to `_all_pass_resolve()` or the
     test will silently score < 100 on the all-pass scenario (T2, T4)

7. **Write unit tests**
   - Add a test class to `tests/test_check_spf_dmarc_ptr_blacklists.py`
     (or create a new file for larger checks)
   - Mock `dns.resolver.resolve` via `patch("dns.resolver.resolve", ...)`
   - If the check calls `get_sending_ips`, patch it at the module level:
     `patch("src.checks.<name>.get_sending_ips", ...)` — NOT at the source
     (`src.checks._dns_cache.get_sending_ips`) since the name is already bound

Run `python -m pytest tests/ -v` and verify the count increases by at least 3.

## Scoring

Overall score weights (defined in `src/scorer.py`, must sum to 100):

| Check | Weight | Rationale |
|---|---|---|
| DMARC | 25 | Strongest policy signal; almost universally absent in Korean companies |
| SPF | 20 | Baseline authentication; widely supported |
| KISA RBL | 15 | Korea-specific; silent blocking with no bounce notification |
| DKIM | 15 | Required for DMARC alignment |
| PTR | 10 | Naver Mail sender signal; often misconfigured |
| 국제 블랙리스트 | 10 | Global reputation; affects non-Korean mailboxes |
| KISA 화이트도메인 | 5 | Beneficial but not blocking; most Korean domains are unregistered |

Naver compatibility score uses separate weights (see `src/scorer.py:NAVER_WEIGHTS`).
The Naver score is displayed as a secondary indicator and is NOT added to the overall score
to avoid double-counting.
