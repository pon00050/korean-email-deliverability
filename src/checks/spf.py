import dns.resolver
from src.models import CheckResult
from src.checks._dns_cache import DNS_TIMEOUT

SPF_SCORE_PASS = 100
SPF_SCORE_WARN_NO_TERMINATOR = 60
SPF_SCORE_WARN_PERMISSIVE = 40


def check_spf(domain: str) -> CheckResult:
    try:
        answers = dns.resolver.resolve(domain, "TXT", lifetime=DNS_TIMEOUT)
    except dns.resolver.NXDOMAIN:
        return CheckResult(
            name="SPF",
            status="fail",
            score=0,
            message_ko="도메인을 찾을 수 없습니다",
        )
    except dns.resolver.NoAnswer:
        return _missing()
    except Exception as e:
        return CheckResult(name="SPF", status="error", score=0, message_ko=f"조회 오류: {e}")

    spf_records = []
    for rdata in answers:
        txt = b"".join(rdata.strings).decode("utf-8", errors="ignore")
        if txt.startswith("v=spf1"):
            spf_records.append(txt)

    if not spf_records:
        return _missing()

    record = spf_records[0]

    if "+all" in record or "?all" in record:
        return CheckResult(
            name="SPF",
            status="warn",
            score=SPF_SCORE_WARN_PERMISSIVE,
            message_ko="SPF 레코드가 있지만 효과가 없습니다 (+all 또는 ?all)",
            detail_ko="+all은 모든 서버의 발송을 허용합니다. 스팸 방지 효과가 없습니다.",
            remediation_ko="SPF 레코드 끝을 -all 또는 ~all로 변경하세요.\n예: v=spf1 include:stibee.com -all",
            raw=record,
        )

    if "-all" in record or "~all" in record:
        return CheckResult(
            name="SPF",
            status="pass",
            score=SPF_SCORE_PASS,
            message_ko="SPF 레코드가 올바르게 설정되어 있습니다",
            raw=record,
        )

    return CheckResult(
        name="SPF",
        status="warn",
        score=SPF_SCORE_WARN_NO_TERMINATOR,
        message_ko="SPF 레코드가 있지만 종료 정책(-all)이 없습니다",
        remediation_ko="SPF 레코드 끝에 -all 또는 ~all을 추가하세요.",
        raw=record,
    )


def _missing() -> CheckResult:
    return CheckResult(
        name="SPF",
        status="fail",
        score=0,
        message_ko="SPF 레코드가 없습니다",
        detail_ko="SPF가 없으면 다른 서버가 귀사 도메인을 발신자로 위조할 수 있습니다.",
        remediation_ko=(
            "DNS 관리 패널에서 TXT 레코드를 추가하세요.\n"
            "예: v=spf1 include:your-esp.com -all\n"
            "스티비 사용 시: v=spf1 include:stibee.com -all"
        ),
    )
