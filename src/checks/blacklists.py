"""
International blacklist checks via DNS.

Checked lists:
  - Spamhaus ZEN (zen.spamhaus.org) — most widely used; covers SBL, XBL, PBL
  - Barracuda BRBL (b.barracudacentral.org) — common in enterprise mail gateways
  - SURBL (multi.surbl.org) — domain-based (not IP-based)

All three offer free DNS-based lookups with no API key required.
Rate limiting: add per-query delay if running bulk scans.
"""

import dns.resolver
from concurrent.futures import ThreadPoolExecutor
from src.models import CheckResult
from src.checks._dns_cache import get_sending_ips, DNS_TIMEOUT

_IP_BLACKLISTS = {
    "Spamhaus ZEN": "zen.spamhaus.org",
    "Barracuda BRBL": "b.barracudacentral.org",
}

_DOMAIN_BLACKLISTS = {
    "SURBL": "multi.surbl.org",
}

BLACKLISTS_SCORE_PASS = 100
BLACKLISTS_SCORE_FAIL = 0


def check_blacklists(domain: str) -> CheckResult:
    ips = list(get_sending_ips(domain))

    # Build a flat list of (query_string, label, ip_or_none) tuples
    queries: list[tuple[str, str, str | None]] = []
    for ip in ips:
        rev = ".".join(reversed(ip.split(".")))
        for name, zone in _IP_BLACKLISTS.items():
            queries.append((f"{rev}.{zone}", name, ip))
    for name, zone in _DOMAIN_BLACKLISTS.items():
        queries.append((f"{domain}.{zone}", name, None))

    findings: list[str] = []
    if queries:
        with ThreadPoolExecutor(max_workers=len(queries)) as ex:
            futures = {ex.submit(_dns_listed, q): (label, ip) for q, label, ip in queries}
            for fut, (label, ip) in futures.items():
                if fut.result():
                    if ip:
                        findings.append(f"{label} (IP: {ip})")
                    else:
                        findings.append(f"{label} (도메인)")

    if findings:
        listed_str = ", ".join(findings)
        return CheckResult(
            name="국제 블랙리스트",
            status="fail",
            score=BLACKLISTS_SCORE_FAIL,
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
        score=BLACKLISTS_SCORE_PASS,
        message_ko=f"주요 국제 블랙리스트에 등록되지 않았습니다",
        raw=f"Checked: {checked} | IPs: {', '.join(ips) if ips else 'none'}",
    )


def _dns_listed(query: str) -> bool:
    try:
        dns.resolver.resolve(query, "A", lifetime=DNS_TIMEOUT)
        return True  # resolved → listed
    except dns.resolver.NXDOMAIN:
        return False
    except Exception:
        return False
