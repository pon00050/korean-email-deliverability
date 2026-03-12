# Security Hardening — 2026-03-13

Comprehensive code review and hardening pass for the Senderfit codebase.
16 findings (4 critical/high, 8 medium, 4 low) + 4 test coverage gaps addressed.

## Findings

| ID | Severity | Description | Status |
|---|---|---|---|
| 0A | High | SECRET_KEY fallback in production (no fail-closed) | **Fixed** — RuntimeError if missing without SENDERFIT_SKIP_DB |
| 0B | Medium | Rate limiter not thread-safe | **Fixed** — `threading.Lock` wraps `_check_rate_limit` |
| 0C | Low | Batch thread pool unbounded (up to 50 workers) | **Fixed** — capped at `_MAX_BATCH_WORKERS = 10` |
| 0D | Low | Admin CLI LIKE injection via `key_hash_prefix` | **Fixed** — `%` and `_` escaped before LIKE query |
| 1A | High | No CSRF protection on browser form POST routes | **Fixed** — `itsdangerous`-based tokens on all 6 form routes |
| 1B | Medium | Gzip bomb via DMARC upload (no decompressed size limit) | **Fixed** — `DMARC_MAX_DECOMPRESSED_SIZE = 50MB` check |
| 1C | Medium | Background thread error handling in `_run_scan_for_subscriber` | **Verified OK** — already wrapped in try/except with logging |
| 2A | High | stdlib XML parser vulnerable to XXE | **Fixed** — replaced with `defusedxml`; string-based check retained as defense-in-depth |
| 2B | Medium | Resend API call has no timeout | **Fixed** — 30s timeout via `ThreadPoolExecutor` |
| 2C | Medium | Multiple DMARC records not detected | **Fixed** — warns with score=15 per RFC 7489 |
| 3A | Medium | Session max_age 30 days (excessive) | **Fixed** — reduced to 7 days; hardcoded values replaced with `SESSION_MAX_AGE` constant |
| 3B | Medium | DB connection pooling (no pool) | **Deferred** — requires psycopg_pool integration; current per-request connect works at current scale |
| 3C | Low | Silent catch-all exceptions in check modules | **Fixed** — `logger.debug()` added to blacklists and DKIM catch-all handlers |
| 3D | Low | DKIM key bit estimation overestimates | **Documented** — conservative behavior; code comment added |
| T3 | Test gap | DB connection failure in routes | **Fixed** — `test_subscribe_raises_on_db_failure` |
| T4 | Test gap | PDF ImportError returns 501 | **Existing** — covered by `test_pdf.py` (skipped when WeasyPrint absent) |

## Test Coverage Added

| Test | File | Description |
|---|---|---|
| `test_missing_secret_key_raises_without_skip_db` | test_auth_session.py | SECRET_KEY fail-closed in production |
| `test_missing_secret_key_allowed_with_skip_db` | test_auth_session.py | Dev mode fallback still works |
| `test_rate_limiter_thread_safety` | test_routes.py | 10 concurrent calls yield exactly 3 allowed |
| `test_post_subscribe_without_csrf_returns_403` | test_routes.py | Missing CSRF token → 403 |
| `test_post_subscribe_with_valid_csrf_succeeds` | test_routes.py | Valid CSRF token → 200 |
| `test_batch_route_has_no_csrf_parameter` | test_routes.py | JSON API structurally skips CSRF |
| `test_subscribe_raises_on_db_failure` | test_routes.py | DB failure propagates correctly |
| `test_xxe_entity_payload_rejected` | test_dmarc_parser.py | XXE payloads blocked |
| `test_billion_laughs_rejected` | test_dmarc_parser.py | Entity expansion attacks blocked |
| `test_dmarc_multiple_records_warns` | test_check_spf_dmarc_ptr_blacklists.py | Duplicate DMARC records detected |
| `test_dmarc_upload_rejects_gzip_bomb` | test_dashboard.py | Decompression bomb protection |

## Accepted Risks

- **Session revocation:** No server-side session store — mitigated by 7-day max_age and signed cookies.
- **PTR multi-MX:** Only the primary MX is checked — feature enhancement, deferred.
- **DKIM key estimation margin:** Overestimates by ~16 bits due to ASN.1 — conservative, documented.
- **DB connection pooling:** Deferred — per-request connections work at current traffic level.

## New Conventions

- All browser-form POST routes must include a `csrf_token` hidden field and validate via `_check_csrf()`.
- `defusedxml` must be used instead of `xml.etree.ElementTree` for untrusted XML parsing.
- Session max_age is 7 days (constant `SESSION_MAX_AGE` in `src/auth.py`).
- `SECRET_KEY` is required in production; only falls back to dev default when `SENDERFIT_SKIP_DB=1`.
