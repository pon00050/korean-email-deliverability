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

## Conventions
- Korean is the primary language for all user-facing strings (`message_ko`, `detail_ko`, `remediation_ko`).
- `status` values: `"pass"`, `"warn"`, `"fail"`, `"error"` — no others.
- Score range: 0–100 integers.
- All new checks must return a `CheckResult` (see `src/models.py`).
- Use `uv` for all package management — not pip directly.
- **Named constants over magic numbers:** Prefer dynamic, named constants (e.g. `MIN_DKIM_KEY_BITS`, `MAX_IPS_TO_CHECK`, `GRADE_THRESHOLDS`) over inline literals. Protocol-spec strings (`v=spf1`, `_dmarc.`, etc.) are exempt — they are fixed by the standard.

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
