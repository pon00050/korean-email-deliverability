# kr-email-health

> 한국 이메일 도메인 상태 검사기 — Korean email domain health checker.
> SPF · DKIM · DMARC · KISA RBL · 화이트도메인 · Naver 호환성 점수

![Tests](https://github.com/pon00050/korean-email-deliverability/actions/workflows/tests.yml/badge.svg)

---

## 누구를 위한 도구인가 (Who it's for)

**세금계산서·법정 이메일을 발송하는 SaaS 및 플랫폼 운영사.**
바로빌, 이카운트, 더존비즈온처럼 이메일 미발송이 건당 0.3~0.5% 가산세 등
법적 불이익으로 이어지는 환경에서, 발송 실패 원인을 사전에 진단합니다.

그 외 이 도구가 유용한 대상:
- 뉴스레터·마케팅 이메일을 네이버/카카오 메일로 발송하는 마케터
- 고객사 이메일 발송 환경을 점검하는 이메일 컨설턴트 및 에이전시

## 무엇을 하는 도구인가 (What it does)

도메인을 입력하면 15초 안에 이메일 발송 상태를 진단합니다.
한국 기업 대상 7가지 검사 + 네이버 메일 호환성 점수.

```
$ uv run check.py barobill.co.kr

kr-email-health  barobill.co.kr
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SPF              ✓ PASS   v=spf1 레코드 확인됨
  DKIM             ✓ PASS   selector 탐지됨
  DMARC            ✓ PASS   p=reject 정책 적용
  PTR              ✓ PASS   역방향 DNS 일치
  KISA RBL         ✓ PASS   차단 목록에 없음
  KISA 화이트도메인  ~ WARN   등록되지 않음 (권장)
  국제 블랙리스트    ✓ PASS   Spamhaus/Barracuda/SURBL 이상 없음
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  네이버 호환성 점수  85 / 100

보고서: reports/barobill.co.kr_20260228_120000.html
```

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

## 빠른 시작 (Quickstart)

### uv (권장)
```bash
git clone https://github.com/pon00050/korean-email-deliverability
cd korean-email-deliverability
uv sync
uv run check.py barobill.co.kr
```

### pip
```bash
git clone https://github.com/pon00050/korean-email-deliverability
cd korean-email-deliverability
pip install -e .
python check.py barobill.co.kr
```

Output: `reports/barobill.co.kr_YYYYMMDD_HHMMSS.html`

## 옵션 (Options)

```
python check.py <domain> [--dkim-selector <selector>] [--output <path>]
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

- [ ] 정기 재검사 + 상태 변경 알림
- [ ] 도메인 일괄 검사 (CSV 입력)
- [ ] 카카오/다음 메일 호환성 점수
- [ ] DMARC 집계 리포트 업로드 + 시각화

## 주의사항 (Disclaimer)

본인이 소유하거나 검사 권한을 부여받은 도메인에만 사용하세요.
네이버 메일 호환성 점수는 공개된 기술 신호 기반 추정값이며, 네이버의 공식 측정값이 아닙니다.
이 도구의 결과는 참고용이며 전문 컨설팅을 대체하지 않습니다.

## 라이선스 (License)

MIT
