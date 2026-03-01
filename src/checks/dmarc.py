import dns.resolver
import re
from src.models import CheckResult
from src.checks._dns_cache import DNS_TIMEOUT

DMARC_SCORE_REJECT = 100
DMARC_SCORE_QUARANTINE = 75
DMARC_SCORE_NONE = 20


def check_dmarc(domain: str) -> CheckResult:
    query = f"_dmarc.{domain}"
    try:
        answers = dns.resolver.resolve(query, "TXT", lifetime=DNS_TIMEOUT)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return _missing()
    except Exception as e:
        return CheckResult(name="DMARC", status="error", score=0, message_ko=f"조회 오류: {e}")

    record = None
    for rdata in answers:
        txt = b"".join(rdata.strings).decode("utf-8", errors="ignore")
        if txt.startswith("v=DMARC1"):
            record = txt
            break

    if not record:
        return _missing()

    policy = _tag(record, "p") or "none"
    pct = _tag(record, "pct") or "100"
    rua = _tag(record, "rua")

    if policy == "reject":
        score = DMARC_SCORE_REJECT
        status = "pass"
        message = "DMARC 정책이 reject로 설정되어 있습니다 — 최고 수준의 보호"
    elif policy == "quarantine":
        score = DMARC_SCORE_QUARANTINE
        status = "warn"
        message = "DMARC 정책이 quarantine입니다 — reject로 강화를 권장합니다"
    else:  # none
        score = DMARC_SCORE_NONE
        status = "warn"
        message = "DMARC가 있지만 p=none (모니터링 전용) — 실제 차단 효과 없음"

    detail = f"정책: p={policy}, 적용률: pct={pct}"
    if not rua:
        detail += "\n⚠ rua 태그 없음 — DMARC 리포트를 수신하지 못합니다"
        score = max(0, score - 10)

    remediation = ""
    if policy == "none":
        remediation = (
            "단계적 강화를 권장합니다:\n"
            "1단계: p=none, rua=mailto:dmarc@yourdomain.com (현재)\n"
            "2단계: p=quarantine; pct=10 → pct=100\n"
            "3단계: p=reject (최종 목표)"
        )
    elif policy == "quarantine":
        remediation = "충분한 모니터링 후 p=reject로 변경하세요."

    return CheckResult(
        name="DMARC",
        status=status,
        score=score,
        message_ko=message,
        detail_ko=detail,
        remediation_ko=remediation,
        raw=record,
    )


def _missing() -> CheckResult:
    return CheckResult(
        name="DMARC",
        status="fail",
        score=0,
        message_ko="DMARC 레코드가 없습니다",
        detail_ko="한국 기업의 약 98%가 이 상태입니다. DMARC가 없으면 도메인 위조(스푸핑)를 방지할 수 없습니다.",
        remediation_ko=(
            "_dmarc.yourdomain.com에 TXT 레코드를 추가하세요.\n"
            "시작 예시: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com\n"
            "충분한 데이터 수집 후 p=quarantine → p=reject로 단계적 강화하세요."
        ),
    )


def _tag(record: str, tag: str) -> str | None:
    match = re.search(rf"{tag}=([^;]+)", record)
    return match.group(1).strip() if match else None
