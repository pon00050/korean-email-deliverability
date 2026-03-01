# kr-email-health

> 한국 이메일 도메인 상태 검사기 — Korean email domain health checker.
> SPF · DKIM · DMARC · KISA RBL · 화이트도메인 · Naver 호환성 점수

![Tests](https://github.com/pon00050/korean-email-deliverability/actions/workflows/tests.yml/badge.svg)

---

## 누구를 위한 도구인가 (Who it's for)

**세금계산서·법정 이메일을 발송하는 SaaS 및 플랫폼 운영사.**
세금계산서·법정고지서를 발송하는 SaaS 플랫폼처럼 이메일 미발송이 건당 0.3~0.5% 가산세 등
법적 불이익으로 이어지는 환경에서, 발송 실패 원인을 사전에 진단합니다.

그 외 이 도구가 유용한 대상:
- 뉴스레터·마케팅 이메일을 네이버/카카오 메일로 발송하는 마케터
- 고객사 이메일 발송 환경을 점검하는 이메일 컨설턴트 및 에이전시

## 무엇을 하는 도구인가 (What it does)

도메인을 입력하면 15초 안에 이메일 발송 상태를 진단합니다.
한국 기업 대상 7가지 검사 + 네이버 메일 호환성 점수.

```
$ uv run check.py example.co.kr

🔍 example.co.kr 도메인 검사 중...

  ✅   SPF                  SPF 레코드가 올바르게 설정되어 있습니다
  ❌   DKIM                 DKIM 레코드를 찾을 수 없습니다 (자동 탐지 실패)
  ⚠️   DMARC                DMARC가 있지만 p=none (모니터링 전용) — 실제 차단 효과 없음
  ⚠️   PTR                  PTR 레코드 없음 — 역방향 DNS 미설정
  ✅   KISA RBL             KISA RBL(한국인터넷진흥원 차단 목록)에 등록되지 않았습니다
  ⚠️   KISA 화이트도메인     KISA 화이트도메인 서비스 종료 (2024년 6월 28일)
  ✅   국제 블랙리스트        주요 국제 블랙리스트에 등록되지 않았습니다

───────────────────────────────────────────────────────
  네이버 메일 호환성: 🔴 44/100  위험 — 네이버 메일 수신율이 크게 저하될 가능성 있음
  전체 점수:         52/100  (D등급)
───────────────────────────────────────────────────────

  📄 리포트 저장됨: reports/example.co.kr_YYYYMMDD_HHMMSS.html
```

## 샘플 리포트 (Sample Report)

코드 없이 결과물을 바로 확인하려면: [example.co.kr 샘플 리포트 보기](https://raw.githack.com/pon00050/korean-email-deliverability/main/sample/example.co.kr.html)

## 검사 항목 (Checks)

| 항목 | 설명 |
|---|---|
| SPF | 발신 도메인 인증 레코드 |
| DKIM | 이메일 서명 키 탐지 (15개 셀렉터 자동 시도) |
| DMARC | 정책 수준 및 리포트 설정 |
| PTR | 역방향 DNS 일치 여부 |
| KISA RBL | 한국인터넷진흥원 차단 목록 |
| KISA 화이트도메인 | 화이트도메인 등록 여부 |
| 국제 블랙리스트 | Spamhaus ZEN, Barracuda, SURBL |

## 호스팅 버전 (Hosted)

설치 없이 바로 사용하려면 아래 주소에서 도메인을 입력하세요.
정기 스캔과 이메일 리포트를 자동으로 받을 수 있습니다.

👉 https://korean-email-deliverability-production.up.railway.app

## 빠른 시작 (Quickstart)

### uv (권장)
```bash
git clone https://github.com/pon00050/korean-email-deliverability
cd korean-email-deliverability
uv sync
uv run check.py example.co.kr
```

### pip
```bash
git clone https://github.com/pon00050/korean-email-deliverability
cd korean-email-deliverability
pip install -e .
python check.py example.co.kr
```

Output: `reports/example.co.kr_YYYYMMDD_HHMMSS.html`

## 옵션 (Options)

```
uv run check.py <domain> [--dkim-selector <selector>] [--output <path>]
```

## 배경 (Background)

한국은 DMARC 도입률 1.8% (APAC 최하위). KISA RBL은 알림 없이 차단.
네이버/카카오 메일은 필터링 기준 비공개. 이 도구는 그 공백을 채웁니다.

**왜 법정 이메일 발송사에게 중요한가:**
세금계산서 이메일이 수신자에게 도달하지 않으면 발송 실패로 간주되어
건당 공급가액의 0.3~0.5% 가산세가 부과될 수 있습니다. KISA RBL 차단은
반송 메일 없이 조용히 발생하기 때문에 운영팀이 문제를 인지하지 못하는
경우가 대부분입니다.

## 한계 (Limitations)

- 네이버 메일 호환성 점수는 공개 신호 기반 추정값입니다 (공식 API 없음)
- DKIM은 셀렉터가 알려진 경우에만 탐지됩니다 (`--dkim-selector` 옵션 사용)
- KISA 화이트도메인 조회는 자동화 API가 없어 수동 확인을 안내합니다

## 로드맵 (Roadmap)

- [x] 정기 재검사 + 상태 변경 알림 (호스팅 버전에서 제공)
- [ ] 도메인 일괄 검사 (CSV 입력)
- [ ] 카카오/다음 메일 호환성 점수
- [ ] DMARC 집계 리포트 업로드 + 시각화

## 주의사항 (Disclaimer)

본인이 소유하거나 검사 권한을 부여받은 도메인에만 사용하세요.
네이버 메일 호환성 점수는 공개된 기술 신호 기반 추정값이며, 네이버의 공식 측정값이 아닙니다.
이 도구의 결과는 참고용이며 전문 컨설팅을 대체하지 않습니다.

## 라이선스 (License)

MIT
