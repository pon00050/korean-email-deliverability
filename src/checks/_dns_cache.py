"""
Shared DNS resolution cache used by kisa_rbl and blacklists to avoid
resolving the same MX records twice per run.
"""

import functools
import socket
import dns.resolver

DNS_TIMEOUT = 5  # seconds — used as lifetime= on all dns.resolver.resolve() calls

_MAX_IPS = 3


@functools.lru_cache(maxsize=64)
def get_sending_ips(domain: str) -> tuple[str, ...]:
    """Resolve MX records → A records. Returns tuple (hashable) for lru_cache."""
    ips: list[str] = []
    try:
        mx_answers = dns.resolver.resolve(domain, "MX", lifetime=DNS_TIMEOUT)
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

    if not ips:
        # fallback: try the domain's A record
        try:
            a_answers = dns.resolver.resolve(domain, "A", lifetime=DNS_TIMEOUT)
            for rdata in a_answers:
                ips.append(str(rdata))
        except Exception:
            pass

    return tuple(ips[:_MAX_IPS])
