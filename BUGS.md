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
