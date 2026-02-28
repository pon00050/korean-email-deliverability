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
