# 배치 API 문서 (Batch API Documentation)

Senderfit 배치 API를 사용하면 여러 도메인의 이메일 발송 환경을 한 번에 검사할 수 있습니다.

---

## 인증 (Authentication)

`X-API-Key` 헤더에 API 키를 포함하세요.

```
X-API-Key: sf_live_aBcDeFgHiJkLmNoPqRsTuVwXyZ012345
```

API 키는 관리자에게 요청하세요. 키는 발급 시 한 번만 표시됩니다.
키를 분실한 경우 기존 키를 폐기하고 새 키를 발급받아야 합니다.

> **참고:** 서버에 `BATCH_API_KEY` 환경 변수가 설정되어 있지 않고 per-customer 키도
> 설정되어 있지 않은 경우, 인증 없이도 접근 가능합니다 (개발/테스트 환경).

---

## 엔드포인트 (Endpoint)

```
POST /batch
Content-Type: application/json
```

### 요청 (Request)

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `domains` | `string[]` | 예 | 검사할 도메인 목록 (최대 50개) |
| `format` | `"json"` \| `"csv"` | 아니오 | 응답 형식 (기본값: `"json"`) |

#### 예시 요청

```bash
curl -s -X POST https://senderfit.kr/batch \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sf_live_YOUR_KEY_HERE" \
  -d '{"domains": ["example.co.kr"], "format": "json"}' \
  | python -m json.tool --no-ensure-ascii
```

> **팁:** `--no-ensure-ascii` 옵션을 사용하면 한국어 문자가 `\uXXXX` 대신 정상 출력됩니다.

---

### 응답 — JSON (Response — JSON)

```json
{
  "results": [
    {
      "domain": "example.co.kr",
      "overall": 63,
      "grade": "C",
      "naver": 44,
      "naver_label": "보통 — 일부 이메일이 스팸함에 분류될 수 있음",
      "checks": [
        {
          "name": "SPF",
          "status": "pass",
          "score": 100,
          "message_ko": "SPF 레코드가 올바르게 설정되어 있습니다.",
          "detail_ko": "v=spf1 include:_spf.google.com ~all",
          "remediation_ko": "",
          "raw": "v=spf1 include:_spf.google.com ~all"
        },
        {
          "name": "DKIM",
          "status": "fail",
          "score": 0,
          "message_ko": "DKIM 레코드를 찾을 수 없습니다.",
          "detail_ko": "",
          "remediation_ko": "DKIM을 설정하세요.",
          "raw": ""
        }
      ]
    }
  ]
}
```

### 응답 — CSV (Response — CSV)

`"format": "csv"` 를 지정하면 `text/csv` 형식으로 응답합니다.

```
domain,overall,grade,naver,SPF,DKIM,DMARC,PTR,KISA RBL,KISA 화이트도메인,국제 블랙리스트
example.co.kr,63,C,44,100,0,50,0,0,0,100
```

---

## 검사 항목 (Check Fields)

각 검사 결과에 포함되는 필드:

| 필드 | 타입 | 설명 |
|------|------|------|
| `name` | `string` | 검사 항목 이름 (SPF, DKIM, DMARC, PTR, KISA RBL, KISA 화이트도메인, 국제 블랙리스트) |
| `status` | `string` | `"pass"`, `"warn"`, `"fail"`, `"error"` 중 하나 |
| `score` | `integer` | 0–100 |
| `message_ko` | `string` | 한국어 요약 메시지 |
| `detail_ko` | `string` | 상세 설명 (해당 시) |
| `remediation_ko` | `string` | 조치 방법 (실패/주의 시) |
| `raw` | `string` | 원시 DNS 레코드 (해당 시) |

### Status 값 의미

| Status | 의미 |
|--------|------|
| `pass` | 정상 |
| `warn` | 설정은 있으나 개선 필요 |
| `fail` | 미설정 또는 심각한 문제 |
| `error` | 검사 불가 (서비스 종료 등) |

---

## 제한 사항 (Rate Limits)

| 항목 | 제한 |
|------|------|
| 요청당 최대 도메인 수 | 50개 |
| 도메인당 검사 시간 | 약 5초 |

50개를 초과하면 `400 Bad Request`가 반환됩니다.

---

## 오류 코드 (Error Codes)

| HTTP 코드 | 의미 | 설명 |
|-----------|------|------|
| `200` | 성공 | 검사 완료 |
| `400` | 잘못된 요청 | 도메인 수 초과 (>50), 잘못된 도메인 형식, 빈 목록 |
| `401` | 인증 실패 | API 키가 없거나 유효하지 않음 |
| `422` | 유효성 검사 실패 | 요청 본문 형식 오류 |

---

## 키 관리 (Key Management)

API 키는 관리자 CLI로 관리됩니다:

```bash
# 키 발급
python admin.py create-key --email customer@example.com --label "프로덕션 키"

# 키 폐기
python admin.py revoke-key sf_live_aBcD

# 키 목록 조회
python admin.py list-keys --customer-email customer@example.com
```

키 형식: `sf_live_` + 43자 랜덤 문자열. 데이터베이스에는 SHA-256 해시만 저장됩니다.
