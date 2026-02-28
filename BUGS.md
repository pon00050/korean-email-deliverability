# BUGS.md

Bug reports with full investigation trail.
Format per entry: date · symptom · root cause · fix · test added.

---

## 2026-02-28 — KISA 화이트도메인: "응답 파싱 실패" 표시 오류

**Symptom:** Live scan of `barobill.co.kr` showed "응답 파싱 실패 — 사이트 구조가 변경되었을 수 있습니다"
in the KISA 화이트도메인 row instead of the intended "자동 조회 불가" message.

**Root cause:** KISA's `spam.kisa.or.kr/white/sub2.do` rejects direct GET requests (with query
params) by returning HTTP 200 with an error page body containing "잘못된 접근입니다".
`raise_for_status()` did not throw (it's a 200), so `_unavailable()` was never reached.
`_parse_response()` returned `None` (the error HTML matched no registered/unregistered patterns),
routing to the `None` branch which displayed the misleading parse-failure message.

**Fix:** Added an error-page guard in `check_kisa_whitedomain()` immediately after
`raise_for_status()`:
```python
if "잘못된 접근" in resp.text:
    return _unavailable("자동 조회 불가 — KISA 사이트 직접 확인 필요")
```
Short-circuits before `_parse_response()` is called.

**File changed:** `src/checks/kisa_whitedomain.py`

**Tests added:** `tests/test_checks.py::TestKisaWhitedomain`
- `test_error_page_returns_unavailable` — mocks 200 + error HTML; asserts `status == "error"` and `spam.kisa.or.kr` in `detail_ko`
- `test_connection_error_returns_unavailable` — mocks `ConnectionError`; asserts `status == "error"`

---

## 2026-02-28 — CI: pyproject.toml TOML structure caused cascading build failures

**Symptom:** GitHub Actions CI failed across 5 consecutive runs with different errors:
run #1 pytest not found, run #2 requests not found, runs #3–#5 hatchling build errors.

**Root cause (three compounding issues discovered in sequence):**

1. `pytest` declared under `[project.optional-dependencies]` but `uv sync` (without `--extra dev`)
   does not install optional groups — pytest was never installed.

2. `dependencies = [...]` was placed in the file *after* `[project.urls]`. In TOML, all key-value
   pairs after a section header belong to that section until the next header. So `dependencies`
   was being parsed as `project.urls.dependencies`, not `project.dependencies`. Hatchling threw:
   `TypeError: URL 'dependencies' of field 'project.urls' must be a string`.

3. No `[build-system]` table existed — uv treated the project as a virtual project and skipped
   the editable install, so main dependencies were never installed in earlier runs.

4. After adding `[build-system]` with hatchling, hatchling could not find the package because
   no `[tool.hatch.build.targets.wheel]` was defined and the project name `kr-email-health`
   does not match any directory name. Hatchling threw: `ValueError: Unable to determine which
   files to ship inside the wheel`.

**Fix:** Restructured `pyproject.toml` so all `[project]` fields are declared before any
subsection headers, added `[build-system]` with hatchling, and added:
```toml
[tool.hatch.build.targets.wheel]
packages = ["src"]
```
CI workflow uses `uv sync --extra dev` (mirrors `kr-forensic-finance` which was already working).

**File changed:** `pyproject.toml`, `.github/workflows/tests.yml`

**Tests added:** None — existing 17 tests now pass in CI.

---

## 2026-02-28 — 전체 실행 시간 ~79초: 순차 DNS 조회 구조

**Symptom:** Live runs of `check.py barobill.co.kr` consistently took ~79 seconds.

**Root cause (4 compounding issues):**

1. All 7 checks run sequentially in a for-loop (`check.py:62–71`)
2. DKIM tries 15 selectors sequentially (`dkim.py:16–18`); each NXDOMAIN waits for the default
   dnspython timeout (~10s)
3. `dns.resolver.resolve()` called with no `lifetime=` — dnspython default is ~10s per query
4. `blacklists.py` and `kisa_rbl.py` both resolve MX records independently with no caching

**Fix:**
- `ThreadPoolExecutor` at two levels: top-level checks run in parallel (`check.py`), and
  intra-check DNS queries run in parallel (`dkim.py`, `blacklists.py`, `kisa_rbl.py`)
- `DNS_TIMEOUT = 5` defined once in `src/checks/_dns_cache.py` and imported as `lifetime=`
  argument in every `dns.resolver.resolve()` call across all check modules
- New `src/checks/_dns_cache.py` with `@functools.lru_cache` on `get_sending_ips()` eliminates
  duplicate MX resolution between `blacklists.py` and `kisa_rbl.py`
- KISA 화이트도메인 HTTP timeout reduced 10 → 5s

**Files changed:** `check.py`, `src/checks/dkim.py`, `src/checks/blacklists.py`,
`src/checks/kisa_rbl.py`, `src/checks/ptr.py`, `src/checks/spf.py`, `src/checks/dmarc.py`,
`src/checks/kisa_whitedomain.py`, `src/checks/_dns_cache.py` (new)

**Tests added:** None new — existing 17 tests use mocks and are unaffected by I/O changes.
Performance verified by timing two consecutive live runs post-fix.
