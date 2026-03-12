"""
KISA RBL (한국인터넷진흥원 실시간 차단 목록) check.

** SERVICE TERMINATED January 31, 2024 **

KISA formally ended the RBL DNS blacklist service:
  - Service fully terminated: January 31, 2024
  - DNS zone rbl.kisa.or.kr is no longer authoritative
  - Reason: shift to managed ESPs and carrier-level filtering reduced
    the practical effectiveness of a shared IP blacklist

The replacement path is individual compliance with Naver and Kakao bulk sender
requirements (SPF + DKIM + DMARC + PTR), which Naver made mandatory July 2024.

No network request is made. The check returns a static error result explaining
the termination.
status="error" causes the scorer to exclude this check's weight, allowing
a perfect 100/100 score to be achievable for domains with all other checks passing.

Source: 패스코리아넷 "KISA-RBL 서비스 종료 안내" (passkorea.net/notice/49644)
"""

from src.models import CheckResult

_NAME = "KISA RBL"


def check_kisa_rbl(domain: str) -> CheckResult:  # noqa: ARG001
    return CheckResult(
        name=_NAME,
        status="error",
        score=0,
        message_ko="KISA RBL 서비스 종료 (2024년 1월 31일)",
        detail_ko=(
            "KISA(한국인터넷진흥원) RBL DNS 차단 목록은 2024년 1월 31일 완전 종료됐습니다. "
            "rbl.kisa.or.kr 존은 더 이상 운영되지 않습니다. "
            "네이버·카카오는 자체 발신자 요건으로 전환했습니다."
        ),
        remediation_ko=(
            "현재 대체 경로:\n"
            "• 네이버 메일: SPF + DKIM + DMARC + PTR 4가지를 모두 설정하면 "
            "네이버 2024년 7월 요건을 충족합니다. 차단 시 "
            "help.naver.com → '스팸 차단 해제 요청' 폼 제출.\n"
            "• 카카오/Daum 메일: 별도 공개 신청 경로 없음. "
            "차단 발생 시 카카오 기업 고객센터 개별 문의."
        ),
    )
