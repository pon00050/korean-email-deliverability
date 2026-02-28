"""
KISA RBL (한국인터넷진흥원 실시간 차단 목록) check.

DNS zone: {reversed-ip}.rbl.kisa.or.kr
If the query resolves → IP is listed (blocked).
If NXDOMAIN → IP is clean.

Verified 2026-02-28: Zone responds correctly (NXDOMAIN for clean IPs).
"""

import socket
import dns.resolver
import dns.reversename
from src.models import CheckResult

KISA_RBL_ZONE = "rbl.kisa.or.kr"
MAX_IPS_TO_CHECK = 3


def check_kisa_rbl(domain: str) -> CheckResult:
    ips = _get_sending_ips(domain)
    if not ips:
        return CheckResult(
            name="KISA RBL",
            status="error",
            score=50,
            message_ko="발신 IP를 확인할 수 없어 KISA RBL 검사를 건너뜁니다",
        )

    listed = []
    for ip in ips:
        if _is_listed(ip):
            listed.append(ip)

    if listed:
        return CheckResult(
            name="KISA RBL",
            status="fail",
            score=0,
            message_ko=f"KISA RBL에 등록되어 있습니다 (IP: {', '.join(listed)})",
            detail_ko=(
                "KISA(한국인터넷진흥원) 차단 목록에 등록된 IP는 "
                "네이버, 카카오, KT 등 한국 ISP로의 이메일 발송이 차단됩니다. "
                "차단은 자동 알림 없이 이루어집니다."
            ),
            remediation_ko=(
                "KISA 차단 해제 신청: https://www.kisa.or.kr/\n"
                "해제 전 스팸 발송 원인(취약한 계정, 악성코드 등)을 반드시 제거하세요."
            ),
            raw=f"Listed IPs: {', '.join(listed)}",
        )

    return CheckResult(
        name="KISA RBL",
        status="pass",
        score=100,
        message_ko="KISA RBL(한국인터넷진흥원 차단 목록)에 등록되지 않았습니다",
        raw=f"Checked IPs: {', '.join(ips)}",
    )


def _get_sending_ips(domain: str) -> list[str]:
    ips = []
    try:
        mx_answers = dns.resolver.resolve(domain, "MX")
        for rdata in sorted(mx_answers, key=lambda r: r.preference):
            mx_host = str(rdata.exchange).rstrip(".")
            try:
                ip = socket.gethostbyname(mx_host)
                ips.append(ip)
            except Exception:
                continue
    except Exception:
        pass

    if not ips:
        # fallback: try resolving the domain's A record directly
        try:
            a_answers = dns.resolver.resolve(domain, "A")
            for rdata in a_answers:
                ips.append(str(rdata))
        except Exception:
            pass

    return ips[:MAX_IPS_TO_CHECK]


def _is_listed(ip: str) -> bool:
    try:
        reversed_ip = ".".join(reversed(ip.split(".")))
        query = f"{reversed_ip}.{KISA_RBL_ZONE}"
        dns.resolver.resolve(query, "A")
        return True  # resolved → listed
    except dns.resolver.NXDOMAIN:
        return False  # not listed
    except Exception:
        return False  # treat lookup errors as clean
