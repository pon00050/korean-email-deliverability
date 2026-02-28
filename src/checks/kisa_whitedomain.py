"""
KISA 화이트도메인 (whitedomain) registration check.

The 화이트도메인 program is operated by KISA at:
  https://화이트도메인.한국  (IDN: https://xn--hq1bm8jm9l.xn--3e0b707e)
  Mirror: https://whitedomains.kisa.or.kr

Registration signals Korean ISPs (Naver, Kakao) that the domain is a
legitimate sender. Stibee's sending IPs are registered; individual
company sending domains typically are not.

Verified 2026-02-28: No public API or queryable URL exists. KISA's site
(spam.kisa.or.kr/white/sub2.do) rejects direct GET requests with params.
The _unavailable() fallback is intentional — direct users to check manually.
"""

import requests
from src.models import CheckResult

_LOOKUP_URL = "https://spam.kisa.or.kr/white/sub2.do"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; korean-email-deliverability/0.1; "
        "+https://github.com/pon00050/korean-email-deliverability)"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
}
_TIMEOUT = 5


def check_kisa_whitedomain(domain: str) -> CheckResult:
    try:
        resp = requests.get(
            _LOOKUP_URL,
            params={"searchDomain": domain},
            headers=_HEADERS,
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        if "잘못된 접근" in resp.text:
            return _unavailable("자동 조회 불가 — KISA 사이트 직접 확인 필요")
    except requests.exceptions.Timeout:
        return _unavailable("요청 시간 초과")
    except requests.exceptions.RequestException:
        return _unavailable("사이트 연결 실패 — 수동 확인 필요")

    registered = _parse_response(resp.text, domain)

    if registered is None:
        return _unavailable("응답 파싱 실패 — 사이트 구조가 변경되었을 수 있습니다")

    if registered:
        return CheckResult(
            name="KISA 화이트도메인",
            status="pass",
            score=100,
            message_ko="KISA 화이트도메인에 등록되어 있습니다",
            detail_ko="화이트도메인 등록은 네이버, 카카오 등 한국 ISP에 정상 발신자임을 알립니다.",
        )

    return CheckResult(
        name="KISA 화이트도메인",
        status="warn",
        score=0,
        message_ko="KISA 화이트도메인에 등록되지 않았습니다",
        detail_ko=(
            "화이트도메인 등록은 한국 ISP(네이버 메일, 카카오 메일)에서의 "
            "수신율 향상에 도움이 됩니다. 필수는 아니지만 권장합니다."
        ),
        remediation_ko=(
            "등록 신청: https://화이트도메인.한국\n"
            "신청 시 발신 도메인, 발신 IP, 담당자 정보가 필요합니다.\n"
            "심사 기간: 약 5~10 영업일"
        ),
    )


def _parse_response(html: str, domain: str) -> bool | None:
    """
    Returns True if domain is registered, False if not, None if unparseable.
    Update this function if the KISA whitedomain site structure changes.
    """
    html_lower = html.lower()
    domain_lower = domain.lower()

    # Heuristic: if the domain appears in the response body, it's likely registered.
    # A more robust implementation would parse the table rows.
    if "등록되지 않" in html or "no result" in html_lower or "검색 결과가 없" in html:
        return False
    if domain_lower in html_lower and ("등록" in html or "registered" in html_lower):
        return True

    # If the page loaded but we can't determine status, return None
    return None


def _unavailable(reason: str) -> CheckResult:
    return CheckResult(
        name="KISA 화이트도메인",
        status="error",
        score=0,
        message_ko=f"KISA 화이트도메인 확인 불가 ({reason})",
        detail_ko="현재 자동 확인 불가 — KISA 사이트에서 직접 확인하세요: https://spam.kisa.or.kr/white/sub2.do",
    )
