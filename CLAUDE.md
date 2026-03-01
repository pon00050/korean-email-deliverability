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

## Privacy — No Real Company Data in Public Files

**Never use real company names, domains, or scan results in any public-facing file.**
This includes: `README.md`, `sample/`, `content/` articles, code comments, test fixtures,
and any file tracked by git (unless it is explicitly gitignored).

- Use `example.co.kr` as the canonical dummy domain in all examples and sample output.
- When a comparison table or multi-domain example is needed, use anonymised labels:
  "세금계산서 SaaS A", "이커머스 B2B SaaS B", etc. — never real brand names.
- Prospect intelligence files (`content/outreach_emails.md`, `content/target_list.md`)
  are gitignored and must never be committed.
- If real scan data is needed for research or drafting, keep it in a local-only file
  that is covered by `.gitignore` before writing anything.

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
