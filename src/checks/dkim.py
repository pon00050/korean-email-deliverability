import logging
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.models import CheckResult
from src.checks._dns_cache import DNS_TIMEOUT

logger = logging.getLogger(__name__)

MIN_DKIM_KEY_BITS = 2048
DKIM_SCORE_WEAK_KEY = 70

COMMON_SELECTORS = [
    "default", "google", "selector1", "selector2",
    "k1", "dkim", "mail", "smtp", "stibee", "nhn",
    "s1", "s2", "key1", "key2", "mimecast",
]


def check_dkim(domain: str, selector: str | None = None) -> CheckResult:
    selectors = [selector] if selector else COMMON_SELECTORS

    # Parallel lookup — return on first hit
    with ThreadPoolExecutor(max_workers=len(selectors)) as ex:
        futures = {ex.submit(_lookup, domain, sel): sel for sel in selectors}
        for fut in as_completed(futures):
            sel = futures[fut]
            result = fut.result()
            if result is not None:
                # Cancel remaining (best-effort; threads complete naturally)
                for f in futures:
                    f.cancel()
                key_bits = _estimate_key_bits(result)
                if key_bits and key_bits < MIN_DKIM_KEY_BITS:
                    return CheckResult(
                        name="DKIM",
                        status="warn",
                        score=DKIM_SCORE_WEAK_KEY,
                        message_ko=f"DKIM 서명이 있지만 키 길이가 짧습니다 ({key_bits}비트, 셀렉터: {sel})",
                        detail_ko="1024비트 이하 키는 취약합니다. 2048비트 이상을 권장합니다.",
                        remediation_ko="이메일 발송 서비스(ESP) 설정에서 DKIM 키를 2048비트로 재생성하세요.",
                        raw=result,
                    )
                return CheckResult(
                    name="DKIM",
                    status="pass",
                    score=100,
                    message_ko=f"DKIM 서명이 설정되어 있습니다 (셀렉터: {sel})",
                    raw=result,
                )

    hint = f" (셀렉터 '{selector}'를 찾을 수 없습니다)" if selector else " (자동 탐지 실패)"
    return CheckResult(
        name="DKIM",
        status="fail",
        score=0,
        message_ko=f"DKIM 레코드를 찾을 수 없습니다{hint}",
        detail_ko="DKIM이 없으면 수신 서버가 이메일의 진위를 검증할 수 없습니다.",
        remediation_ko=(
            "ESP에서 DKIM을 활성화하고 제공된 DNS 레코드를 추가하세요.\n"
            "셀렉터를 알고 있다면 --dkim-selector 옵션으로 지정할 수 있습니다."
        ),
    )


def _lookup(domain: str, selector: str) -> str | None:
    query = f"{selector}._domainkey.{domain}"
    try:
        answers = dns.resolver.resolve(query, "TXT", lifetime=DNS_TIMEOUT)
        for rdata in answers:
            txt = b"".join(rdata.strings).decode("utf-8", errors="ignore")
            if "v=DKIM1" in txt or "p=" in txt:
                return txt
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        pass
    except Exception:
        logger.debug("DKIM lookup failed for %s._domainkey.%s", selector, domain, exc_info=True)
    return None


def _estimate_key_bits(record: str) -> int | None:
    """Return the RSA modulus bit length by parsing the DER-encoded SubjectPublicKeyInfo.

    Walks the ASN.1 DER structure to reach the RSA modulus INTEGER and reads
    its length directly, rather than using the total DER byte count which
    overestimates by ~34–38 bytes of wrapper overhead.
    """
    import re
    import base64

    match = re.search(r"p=([A-Za-z0-9+/=]+)", record)
    if not match:
        return None
    try:
        der = base64.b64decode(match.group(1) + "==")
        pos = 0

        def read_len(pos: int) -> tuple[int, int]:
            b = der[pos]
            if b & 0x80 == 0:
                return b, pos + 1
            n = b & 0x7F
            return int.from_bytes(der[pos + 1: pos + 1 + n], "big"), pos + 1 + n

        # Outer SEQUENCE
        if der[pos] != 0x30:
            return None
        pos += 1
        _, pos = read_len(pos)

        # AlgorithmIdentifier SEQUENCE — skip entirely
        if der[pos] != 0x30:
            return None
        pos += 1
        alg_len, pos = read_len(pos)
        pos += alg_len

        # BIT STRING
        if der[pos] != 0x03:
            return None
        pos += 1
        _, pos = read_len(pos)
        pos += 1  # skip "unused bits" byte (always 0x00 for RSA)

        # RSAPublicKey SEQUENCE
        if der[pos] != 0x30:
            return None
        pos += 1
        _, pos = read_len(pos)

        # Modulus INTEGER
        if der[pos] != 0x02:
            return None
        pos += 1
        mod_len, pos = read_len(pos)

        # Strip leading 0x00 padding byte (positive integer with high bit set)
        if der[pos] == 0x00:
            mod_len -= 1

        return mod_len * 8
    except Exception:
        return None
