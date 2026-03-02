# BUGS.md

Bug reports with full investigation trail.
Format per entry: date · symptom · root cause · fix · test added.

---

## 2026-03-02 — Railway Phase 2 첫 배포: 6단계 연속 오류

**Symptom:** Phase 2 FastAPI app failed to deploy on Railway across 6 consecutive
attempts over ~90 minutes. Each fix uncovered the next hidden problem.

**Root causes (in order of discovery):**

### 1. No start command found
Railpack could not detect a start command. Root cause: `railway.toml` contained
`[build] builder = "nixpacks"` which conflicted with Railpack (the current default
builder). Railpack ignored the `startCommand` in the file as a result.

**Fix:** Removed `[build]` section entirely from `railway.toml`. Set start command
to `uvicorn app:app --host 0.0.0.0 --port $PORT` directly in the Railway dashboard
as an immediate workaround.

---

### 2. `uvicorn: command not found`
Railpack installs packages into `.venv` but the dashboard start command ran `uvicorn`
as a global binary, which is not on the container PATH.

**Fix:** Changed start command to `python -m uvicorn app:app --host 0.0.0.0 --port $PORT`.

---

### 3. `/app/.venv/bin/python: No module named uvicorn`
`python -m uvicorn` found the venv Python but uvicorn was not installed in it, because
`uv.lock` had never been updated after Phase 2 dependencies were added to `pyproject.toml`.
Railway runs `uv sync --locked` (strict — will not update the lockfile), so it installed
only what was in the stale lockfile from Phase 1.

**Fix:** Changed start command to `uv run uvicorn ...` (uv is on PATH via mise and
activates the venv automatically). Running `uv sync --extra dev` locally regenerated
`uv.lock` with all Phase 2 packages and committed it.

---

### 4. `ModuleNotFoundError: No module named 'src.db'`
All Phase 2 source files (`src/db.py`, `src/emailer.py`, `src/scheduler.py`),
templates, and tests had been created and tested locally but were never committed
to git. Railway's container only has what is in the repository.

**Fix:** Committed all 10 missing files in one batch commit.

---

### 5. Healthcheck timeout (30s) too short
`railway.toml` had `healthcheckTimeout = 30`. The container needed more time on cold
start to connect to Postgres and start APScheduler. Railway marked the deploy failed
before the app was ready.

**Fix:** Increased `healthcheckTimeout` to `300`.

---

### 6. `RuntimeError: Form data requires "python-multipart" to be installed`
FastAPI's `Form()` requires `python-multipart` as a separate package. It is not
installed by bare `fastapi`. The dependency was not declared in `pyproject.toml`.
This caused uvicorn to crash at startup while registering the `/subscribe` route
(FastAPI validates form dependencies at route-decoration time, not request time).

**Fix:** Replaced `"fastapi>=0.115"` with `"fastapi[standard]>=0.115"` in
`pyproject.toml`. The `[standard]` extra is the officially recommended install and
bundles `python-multipart`, `jinja2`, `uvicorn[standard]`, `email-validator`, and
`pydantic-settings` — eliminating the entire class of missing-sub-dependency errors.
Ran `uv sync --extra dev` to update `uv.lock` and committed both files.

**Final state:** Both Railway services (Postgres + app) show green "Online" status.
`GET /health` returns HTTP 200. Database connection established. Scheduler started.

**Lessons:**
- Always run `uv sync --extra dev` and commit `uv.lock` immediately after editing
  `pyproject.toml` — a stale lockfile is invisible locally (pip fills the gap) but
  fatal on Railway where `uv sync --locked` is strict.
- Always commit all new files before pushing deploy-triggering changes. `git status`
  before every push.
- Use `fastapi[standard]` not bare `fastapi` to avoid piecemeal sub-dependency failures.
- Remove `[build] builder = "nixpacks"` from `railway.toml` — Railpack is the current
  default and the nixpacks builder key causes silent config conflicts.
- Set `healthcheckTimeout = 300` (5 minutes) for any app with a DB connection in the
  startup path.

**Files changed:** `pyproject.toml`, `uv.lock`, `railway.toml`, `Procfile`, `app.py`

**Tests added:** None — these were infrastructure/deployment failures, not logic bugs.

---

## 2026-03-02 — Scheduler 중복 실행: `max_instances=1` 누락 및 라우트 테스트 부재

**Symptom (잠재적):** 5분 주기 스케줄러 잡이 이전 실행이 아직 끝나지 않은 상태에서
다시 실행될 수 있었다. 구독자 수가 늘거나 DNS 조회가 느려지면 동일 구독자에 대해
이메일이 중복 발송되고 `next_scan_at`이 두 번 갱신될 위험이 있었다.

**Root cause:** `scheduler.add_job()` 호출에 `max_instances` 인자가 없었다.
APScheduler 기본값은 `max_instances=1`이 아닌 `max_instances=3`으로,
중복 실행을 허용한다.

**Fix:**
- `app.py`: `scheduler.add_job(..., max_instances=1)` 추가 — 이전 잡이 실행 중이면
  다음 트리거는 건너뜀.
- `src/scheduler.py`: `_default_scan_executor` 반환 타입 힌트를 `tuple[list, dict]`
  → `tuple[list[CheckResult], dict[str, Any]]`로 정밀화 (동일 커밋).
- `tests/test_routes.py` (신규): FastAPI 라우트 전체를 in-memory SQLite로 커버하는
  테스트 파일 추가. psycopg는 CI 환경에 libpq 없음을 고려해 import 시점에 stub 처리.
  `_NoCloseConn` 래퍼로 테스트가 공유하는 SQLite 커넥션이 라우트 핸들러에 의해
  닫히지 않도록 보호.
- `tests/test_scheduler.py`: 스캔 중 예외 발생 시에도 `next_scan_at`이 갱신되는지
  확인하는 테스트 추가.

**Files changed:** `app.py`, `src/scheduler.py`, `tests/test_routes.py` (new),
`tests/test_scheduler.py`

**Tests added:** `test_routes.py` — 14개 (health, signup, subscribe strips URL prefix,
subscribe success HTML, subscribe invalid input ×6, unsubscribe valid/missing/unknown token);
`test_scheduler.py` — `test_run_due_scans_advances_next_scan_at_even_on_exception`. 총 38 → 45개.

---

## 2026-03-02 — GRADE_THRESHOLDS: C/D 등급 경계 오류 (ship-blocking)

**Symptom:** 점수 45점 도메인이 스펙상 D등급이어야 하는데 C등급으로 표시됨.
점수 39점 도메인이 스펙상 F등급이어야 하는데 D등급으로 표시됨.

**Root cause:** `src/scorer.py`의 `GRADE_THRESHOLDS`가 잘못된 임계값을 사용했다.

| 등급 | 스펙 (CLAUDE.md) | 코드 (버그) |
|------|------------------|-------------|
| C    | ≥ 60             | ≥ 50        |
| D    | ≥ 40             | ≥ 25        |

```python
# 버그
GRADE_THRESHOLDS = [(90, "A"), (75, "B"), (50, "C"), (25, "D")]
# 수정
GRADE_THRESHOLDS = [(90, "A"), (75, "B"), (60, "C"), (40, "D")]
```

**Discovery:** Pre-Phase3 위험 평가 작업 중 `tests/test_scorer.py` T1 작성 시 발견.
기존 테스트 없이 코드가 무검증으로 배포되었다.

**Fix:** `GRADE_THRESHOLDS`의 C 임계값 50 → 60, D 임계값 25 → 40으로 수정.

**Files changed:** `src/scorer.py`

**Tests added:** `tests/test_scorer.py::test_grade_boundaries` — 10개 parametrize 케이스
로 모든 경계값(A/B/C/D/F 각 상하한) 전수 검증.

---

## 2026-03-02 — Pre-Phase3 일관성 감사: 7가지 코드베이스 불일치

Phase 3 착수 전 수동 감사에서 발견된 7개 항목. 각각 독립적이나 묶어서 수정하였다.

---

### 1. KISA 화이트도메인: `status="warn"` → `"error"` — 100점 달성 불가 버그

**Symptom:** 모든 다른 검사를 통과해도 전체 점수가 최대 95/100으로 고정되었다.
KISA 화이트도메인의 weight 5점이 항상 차감되었다.

**Root cause:** 서비스 종료로 인해 검사 결과가 항상 `status="warn"`이었는데,
`src/scorer.py`는 `"error"` 상태만 weight 계산에서 제외한다. `"warn"`은 `score=0`인
채로 포함되어 5점이 감점되었다.

**Fix:** `check_kisa_whitedomain()` 반환값을 `status="error"`로 변경.
`"error"` 상태는 scorer에서 제외되어 weight 5점이 분모에서도 빠진다.
모듈 docstring에 설계 의도 명시. `tests/test_kisa_whitedomain.py` 어서션 일괄 수정.

**Files changed:** `src/checks/kisa_whitedomain.py`, `tests/test_kisa_whitedomain.py`

**Tests added:** 기존 테스트 어서션 `warn` → `error` 수정 (새 케이스 없음).

---

### 2. PTR: MX 없음 시 `status="warn"` → `"fail"` 및 도달 불가 코드 제거

**Symptom:** MX 레코드가 없는 도메인이 PTR 검사에서 `"warn"`을 반환했다.
SPF/DMARC 등 다른 검사들이 동일 조건에서 `"fail"`을 반환하는 것과 불일치.

**Root cause:** `NXDOMAIN`/`NoAnswer` 예외 처리 블록이 `status="warn"`을 반환했다.
또한 그 아래 `if not mx_hosts:` 분기가 존재했으나, 빈 MX 목록은 예외 전에
`NXDOMAIN`으로 처리되므로 실제로는 도달 불가능한 dead code였다.

**Fix:** `status="warn"` → `status="fail"`. `if not mx_hosts:` 블록 제거.

**Files changed:** `src/checks/ptr.py`

**Tests added:** `tests/test_checks.py::TestPTR::test_no_mx_returns_fail`.

---

### 3. KISA RBL: `KISA_RBL_SCORE_ERROR = 50` → `0`

**Symptom (잠재적):** `KISA_RBL_SCORE_ERROR = 50` 상수가 오해를 유발. scorer는
`"error"` 상태 검사를 계산에서 제외하므로 이 값은 실제로 점수에 반영되지 않는다.
미래 개발자가 이 상수를 실제 점수로 오해할 위험이 있었다.

**Fix:** `KISA_RBL_SCORE_ERROR = 0`으로 변경하고 "scorer에 의해 사용되지 않음"
주석 추가.

**Files changed:** `src/checks/kisa_rbl.py`

**Tests added:** 없음.

---

### 4. DKIM: 상수명 `DKIM_WEAK_KEY_SCORE` → `DKIM_SCORE_WEAK_KEY`

**Symptom:** DKIM 모듈의 상수명이 프로젝트 명명 규칙(`<CHECK>_SCORE_<CONDITION>`)을
따르지 않았다.

**Fix:** 상수 선언 및 사용처 일괄 rename.

**Files changed:** `src/checks/dkim.py`

**Tests added:** 없음.

---

### 5. Scheduler: `scan_executor` 타입 힌트 정밀화

**Symptom:** `run_due_scans`의 `scan_executor` 파라미터 타입이 `tuple[list, dict]`로
제네릭 없이 선언되어 있었다.

**Fix:** `tuple[list[CheckResult], dict[str, Any]]`로 정밀화. `CheckResult` import 추가.

**Files changed:** `src/scheduler.py`

**Tests added:** 없음.

---

### 6. Scorer: `NAVER_WEIGHTS` 설계 근거 주석 추가

**Symptom:** `NAVER_WEIGHTS`에서 KISA RBL과 국제 블랙리스트가 제외된 이유가
코드에 명시되지 않았다.

**Fix:** "Naver filtering is independent of these zones" 근거 주석 추가.

**Files changed:** `src/scorer.py`

**Tests added:** 없음.

---

**Overall test count after f95dd51:** 38 → 45개.

---

## 2026-03-02 — Phase 2 Post-Cleanup: 3가지 잠재 장애 선제 수정

세 항목은 기능 버그가 아닌 운영 위험(operational risk)으로 분류되어
실제 장애가 발생하기 전에 선제적으로 수정하였다.

---

### 1. Scheduler stale connection — Railway 재시작 시 스캐너 묵묵히 실패

**Symptom (잠재적):** APScheduler가 앱 시작 시 생성된 단일 `psycopg` 커넥션을
앱 전체 수명 동안 보유한다. Railway가 Postgres를 재시작하거나 유휴 커넥션 타임아웃이
발생하면, 이후 5분 주기 스케줄러 실행이 모두 `OperationalError`로 실패하며
이메일은 전송되지 않는다. 로그에만 남고 사용자는 알 수 없다.

**Root cause:** `make_apscheduler_job(conn)`이 잡 생성 시점의 커넥션 객체를 클로저에
캡처한다. 해당 커넥션이 이후 끊어져도 교체 수단이 없다.

**Fix:**
- `make_apscheduler_job(conn)` → `make_apscheduler_job(conn_factory)` 로 시그니처 변경.
  `conn_factory`는 매 호출마다 새 커넥션을 반환하는 callable (= `get_db`).
- job 클로저 내부: 매 실행마다 `conn = conn_factory()` 후 `try/finally: conn.close()`.
  요청 핸들러가 이미 동일 패턴을 사용하고 있어 5분당 커넥션 1개 추가는 무시 가능한 수준.
- `app.py` lifespan: `_db_conn = get_db()` + `create_tables(_db_conn)` →
  `with get_db() as _init_conn: create_tables(_init_conn)` (종료 시 자동 close).
  `make_apscheduler_job(get_db)` 로 팩토리 전달. `_db_conn` 전역 변수 제거.
- `tests/test_routes.py`: `_NoCloseConn`에 `__enter__`/`__exit__` 추가 —
  lifespan의 `with get_db()` 패턴이 테스트 픽스처와도 작동하도록.

**Files changed:** `src/scheduler.py`, `app.py`, `tests/test_routes.py`

**Tests added:** 없음 — `test_scheduler.py`는 `run_due_scans`를 직접 테스트하며
커넥션 팩토리 레이어를 거치지 않음. 기존 67개 테스트 전부 통과.

---

### 2. `normalize_domain()` 중복 — 3번째 호출자 전에 추출

**Symptom (잠재적):** 동일한 `.strip().lower().removeprefix("https://")...` 체인이
`app.py:142`와 `check.py:48`에 각각 독립적으로 존재한다. 로직 변경 시 한 곳만
수정하면 두 진입점의 동작이 달라진다.

**Root cause:** Phase 1(`check.py`)에서 인라인으로 작성된 코드가 Phase 2(`app.py`)
개발 시 그대로 복사되었다. 공통 유틸리티 모듈이 없었다.

**Fix:**
- `src/utils.py` (신규): `normalize_domain(raw: str) -> str` 함수 한 곳에 정의.
- `app.py`, `check.py`: 인라인 체인을 `normalize_domain()` 호출로 교체.

**Files changed:** `src/utils.py` (new), `app.py`, `check.py`

**Tests added:** `tests/test_utils.py` (신규) — 4개 parametrize 케이스:
공백 포함, `https://` 접두사, `http://` 접두사, 순수 도메인.

---

### 3. `render_email_report` missing-key 폴백 미검증

**Symptom (잠재적):** `render_email_report`는 `scores` 딕트의 `"grade"` 키 부재 시
`"F"`로, `"overall"` 부재 시 `0`으로 폴백하도록 `.get()` 을 사용한다.
그러나 이 경로를 테스트하는 코드가 없어, `scores` 딕트가 잘못 구성된 버그가
발생해도 잘못된 내용의 이메일이 조용히 발송된다.

**Root cause:** `render_email_report` 작성 시 방어적 `.get()` 폴백을 추가했으나
대응하는 테스트가 누락되었다.

**Fix:** 두 폴백 경로를 각각 커버하는 테스트 추가:
- `test_render_email_report_missing_grade_defaults_to_F`: `scores`에 `"grade"` 없음 →
  렌더링 결과에 F등급 색상 `#dc2626` 포함 확인.
- `test_render_email_report_missing_overall_defaults_to_zero`: `scores`에 `"overall"` 없음 →
  렌더링 결과에 `"0"` 포함 확인.

**Files changed:** `tests/test_emailer.py`

**Tests added:** 위 2개 (총 테스트 수: 45 → 67).

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
