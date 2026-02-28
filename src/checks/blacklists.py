"""
International blacklist checks via DNS.

Checked lists:
  - Spamhaus ZEN (zen.spamhaus.org) — most widely used; covers SBL, XBL, PBL
  - Barracuda BRBL (b.barracudacentral.org) — common in enterprise mail gateways
  - SURBL (multi.surbl.org) — domain-based (not IP-based)

All three offer free DNS-based lookups with no API key required.
Rate limiting: add per-query delay if running bulk scans.
"""

import socket
import dns.resolver
from src.models import CheckResult

_IP_BLACKLISTS = {
    "Spamhaus ZEN": "zen.spamhaus.org",
    "Barracuda BRBL": "b.barracudacentral.org",
}

_DOMAIN_BLACKLISTS = {
    "SURBL": "multi.surbl.org",
}

MAX_IPS_TO_CHECK = 3


def check_blacklists(domain: str) -> CheckResult:
    ips = _get_ips(domain)
    findings: list[str] = []

    # IP-based checks
    for ip in ips:
        reversed_ip = ".".join(reversed(ip.split(".")))
        for name, zone in _IP_BLACKLISTS.items():
            if _dns_listed(f"{reversed_ip}.{zone}"):
                findings.append(f"{name} (IP: {ip})")

    # Domain-based checks
    for name, zone in _DOMAIN_BLACKLISTS.items():
        if _dns_listed(f"{domain}.{zone}"):
            findings.append(f"{name} (도메인)")

    if findings:
        listed_str = ", ".join(findings)
        return CheckResult(
            name="국제 블랙리스트",
            status="fail",
            score=0,
            message_ko=f"블랙리스트에 등록되어 있습니다: {listed_str}",
            detail_ko=(
                "국제 블랙리스트에 등록되면 Gmail, Outlook 등 글로벌 메일 서비스로의 "
                "발송도 차단됩니다."
            ),
            remediation_ko=(
                "Spamhaus: https://www.spamhaus.org/lookup/\n"
                "Barracuda: https://www.barracudacentral.org/lookups\n"
                "차단 해제 신청 전 스팸 발송 원인을 반드시 제거하세요."
            ),
            raw=f"Listed on: {listed_str}",
        )

    checked = ", ".join(list(_IP_BLACKLISTS) + list(_DOMAIN_BLACKLISTS))
    return CheckResult(
        name="국제 블랙리스트",
        status="pass",
        score=100,
        message_ko=f"주요 국제 블랙리스트에 등록되지 않았습니다",
        raw=f"Checked: {checked} | IPs: {', '.join(ips) if ips else 'none'}",
    )


def _get_ips(domain: str) -> list[str]:
    ips = []
    try:
        mx_answers = dns.resolver.resolve(domain, "MX")
        for rdata in sorted(mx_answers, key=lambda r: r.preference):
            mx_host = str(rdata.exchange).rstrip(".")
            try:
                ip = socket.gethostbyname(mx_host)
                if ip not in ips:
                    ips.append(ip)
            except Exception:
                continue
    except Exception:
        pass
    return ips[:MAX_IPS_TO_CHECK]


def _dns_listed(query: str) -> bool:
    try:
        dns.resolver.resolve(query, "A")
        return True  # resolved → listed
    except dns.resolver.NXDOMAIN:
        return False
    except Exception:
        return False
