"""
KISA 화이트도메인 (whitedomain) registration check.

** SERVICE TERMINATED June 28, 2024 **

KISA formally ended the 화이트도메인 program:
  - New registrations closed: June 14, 2024
  - Service fully terminated: June 28, 2024
  - Reason: shift to managed ESPs (Naver Cloud, Kakao) reduced practical effectiveness

The replacement path is individual compliance with Naver and Kakao bulk sender
requirements (SPF + DKIM + DMARC + PTR), which Naver made mandatory July 19, 2024.

No network request is made. The check returns a static error result explaining
the termination and directing users to the current Naver/Kakao paths.
status="error" causes the scorer to exclude this check's weight, allowing
a perfect 100/100 score to be achievable for domains with all other checks passing.

Source: Thundermail 화이트도메인 서비스 종료 안내 (blog.thundermail.co.kr/366)
"""

from src.models import CheckResult

_NAME = "KISA 화이트도메인"


def check_kisa_whitedomain(domain: str) -> CheckResult:  # noqa: ARG001
    return CheckResult(
        name=_NAME,
        status="error",
        score=0,
        message_ko="KISA 화이트도메인 서비스 종료 (2024년 6월 28일)",
        detail_ko=(
            "KISA 화이트도메인 프로그램은 2024년 6월 28일 완전 종료됐습니다. "
            "등록 신청이나 조회가 더 이상 불가합니다. "
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
