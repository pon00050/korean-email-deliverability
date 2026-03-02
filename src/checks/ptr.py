import socket
import dns.resolver
import dns.reversename
from src.models import CheckResult
from src.checks._dns_cache import DNS_TIMEOUT

PTR_SCORE_PASS = 100
PTR_SCORE_FCRDN_MISMATCH = 50
PTR_SCORE_FORWARD_FAIL = 60
PTR_SCORE_NO_PTR = 20
PTR_SCORE_NO_IP = 30


def check_ptr(domain: str) -> CheckResult:
    # Step 1: get MX records
    try:
        mx_answers = dns.resolver.resolve(domain, "MX", lifetime=DNS_TIMEOUT)
        mx_hosts = sorted(
            [(r.preference, str(r.exchange).rstrip(".")) for r in mx_answers]
        )
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return CheckResult(
            name="PTR",
            status="fail",
            score=0,
            message_ko="MX 레코드가 없습니다 — 이메일 수신 설정이 되어 있지 않습니다",
        )
    except Exception as e:
        return CheckResult(name="PTR", status="error", score=0, message_ko=f"MX 조회 오류: {e}")

    # Check the primary (lowest preference) MX host
    _, mx_host = mx_hosts[0]

    # Step 2: resolve MX host to IP
    try:
        ip = socket.gethostbyname(mx_host)
    except Exception:
        return CheckResult(
            name="PTR",
            status="warn",
            score=PTR_SCORE_NO_IP,
            message_ko=f"MX 호스트({mx_host})의 IP를 확인할 수 없습니다",
        )

    # Step 3: reverse DNS lookup
    try:
        rev_name = dns.reversename.from_address(ip)
        ptr_answers = dns.resolver.resolve(rev_name, "PTR", lifetime=DNS_TIMEOUT)
        ptr_hostname = str(ptr_answers[0]).rstrip(".")
    except Exception:
        return CheckResult(
            name="PTR",
            status="fail",
            score=PTR_SCORE_NO_PTR,
            message_ko=f"PTR(역방향 DNS) 레코드가 없습니다 (IP: {ip})",
            detail_ko="PTR 레코드가 없으면 네이버 메일 등 한국 ISP의 필터링에 영향을 줄 수 있습니다.",
            remediation_ko="호스팅 또는 서버 제공업체에 PTR 레코드 설정을 요청하세요.",
        )

    # Step 4: check forward-confirmed PTR (FCrDNS)
    try:
        forward_ip = socket.gethostbyname(ptr_hostname)
        if forward_ip == ip:
            return CheckResult(
                name="PTR",
                status="pass",
                score=PTR_SCORE_PASS,
                message_ko=f"PTR 레코드가 올바르게 설정되어 있습니다 ({ip} → {ptr_hostname})",
                raw=f"{ip} → {ptr_hostname} → {forward_ip}",
            )
        else:
            return CheckResult(
                name="PTR",
                status="warn",
                score=PTR_SCORE_FCRDN_MISMATCH,
                message_ko=f"PTR 레코드가 있지만 정방향 확인이 일치하지 않습니다",
                detail_ko=f"PTR: {ptr_hostname}, 정방향 조회 IP: {forward_ip} (예상: {ip})",
                remediation_ko="PTR 레코드와 A 레코드가 서로 일치하도록 수정하세요.",
                raw=f"{ip} → {ptr_hostname} → {forward_ip}",
            )
    except Exception:
        return CheckResult(
            name="PTR",
            status="warn",
            score=PTR_SCORE_FORWARD_FAIL,
            message_ko=f"PTR 레코드가 있지만 정방향 확인 불가 ({ptr_hostname})",
            raw=f"{ip} → {ptr_hostname}",
        )
