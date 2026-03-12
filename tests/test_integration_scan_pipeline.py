"""
Integration tests for the full scan pipeline.

Exercises: parallel check functions (real) → scorer (real)
           → generate_report (real) → HTML file on disk.

All DNS / network calls are mocked at the dns.resolver.resolve boundary and via
get_sending_ips, so these tests run in CI without live DNS.

Run: python -m pytest tests/test_integration_scan_pipeline.py -v
"""

import dns.resolver
import pytest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock, patch

from src.checks.dkim import check_dkim
from src.checks.dmarc import check_dmarc
from src.checks.kisa_rbl import check_kisa_rbl
from src.checks.kisa_whitedomain import check_kisa_whitedomain
from src.checks.blacklists import check_blacklists
from src.checks.ptr import check_ptr
from src.checks.spf import check_spf
from src.report import generate_report
from src.scorer import grade, overall_score


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DOMAIN = "example.co.kr"
_FAKE_IP = "1.2.3.4"


def _mx(pref: int, host: str):
    r = MagicMock()
    r.preference = pref
    r.exchange = f"{host}."
    return r


def _txt(record: str):
    r = MagicMock()
    r.strings = [record.encode()]
    return r


def _all_pass_resolve(qname, rdtype, **kwargs):
    """
    Returns sensible 'pass' DNS answers for every record type needed by all 7 checks.
    """
    qname = str(qname)
    rdtype = str(rdtype)

    if rdtype == "MX":
        return [_mx(10, "mail.example.co.kr")]

    if rdtype == "TXT":
        if "_dmarc." in qname:
            return [_txt("v=DMARC1; p=reject; rua=mailto:r@example.co.kr")]
        if "_domainkey." in qname:
            # 400 base64 chars = 300 bytes = 2400 bits — passes MIN_DKIM_KEY_BITS (2048)
            key = "v=DKIM1; k=rsa; p=" + "A" * 400
            return [_txt(key)]
        # Generic TXT (SPF)
        return [_txt("v=spf1 include:example.com -all")]

    if rdtype == "A":
        # Blacklist DNSBL queries contain known zone suffixes — return NXDOMAIN (clean)
        for bl_zone in ("zen.spamhaus.org", "b.barracudacentral.org", "multi.surbl.org", "rbl.kisa.or.kr"):
            if bl_zone in qname:
                raise dns.resolver.NXDOMAIN
        return [MagicMock(address=_FAKE_IP)]

    if rdtype == "PTR":
        ans = MagicMock()
        ans.__getitem__ = lambda self, i: MagicMock(__str__=lambda s: "mail.example.co.kr.")
        ans.__iter__ = lambda self: iter([MagicMock(__str__=lambda s: "mail.example.co.kr.")])
        return ans

    raise dns.resolver.NXDOMAIN


def _all_fail_resolve(qname, rdtype, **kwargs):
    """Returns NXDOMAIN for every query — all checks should fail / score 0."""
    raise dns.resolver.NXDOMAIN


def _run_all_checks(mock_resolve_fn, mock_ips=None):
    """Run all 7 checks in a ThreadPoolExecutor, mirroring check.py parallelism."""
    if mock_ips is None:
        mock_ips = [_FAKE_IP]

    checkers = [
        check_spf,
        check_dkim,
        check_dmarc,
        check_ptr,
        check_kisa_rbl,
        check_kisa_whitedomain,
        check_blacklists,
    ]

    with (
        patch("dns.resolver.resolve", side_effect=mock_resolve_fn),
        patch("src.checks.blacklists.get_sending_ips", return_value=set(mock_ips)),
        patch("socket.gethostbyname", return_value=_FAKE_IP),
    ):
        with ThreadPoolExecutor(max_workers=len(checkers)) as ex:
            futures = [ex.submit(fn, _DOMAIN) for fn in checkers]
            results = [f.result() for f in futures]

    return results


@pytest.fixture(scope="module")
def all_pass_results():
    """All-pass check results, computed once per module for the 4 tests that share it."""
    return _run_all_checks(_all_pass_resolve)


# ---------------------------------------------------------------------------
# T1 — Full pipeline produces an HTML report file
# ---------------------------------------------------------------------------

class TestFullPipelineProducesHTMLReport:
    def test_html_file_is_created(self, all_pass_results, tmp_path):
        out = tmp_path / "report.html"
        generate_report(_DOMAIN, all_pass_results, out)

        assert out.exists()
        html = out.read_text(encoding="utf-8")
        assert "<html" in html.lower()
        assert _DOMAIN in html

    def test_score_appears_in_report(self, all_pass_results, tmp_path):
        score = overall_score(all_pass_results)
        out = tmp_path / "report.html"
        generate_report(_DOMAIN, all_pass_results, out)

        html = out.read_text(encoding="utf-8")
        assert str(score) in html


# ---------------------------------------------------------------------------
# T2 — All-pass: score=100, grade A appear in the report
# ---------------------------------------------------------------------------

class TestPipelineAllPassChecks:
    def test_grade_a_and_score_100_in_report(self, all_pass_results, tmp_path):
        score = overall_score(all_pass_results)
        g = grade(score)

        out = tmp_path / "report.html"
        generate_report(_DOMAIN, all_pass_results, out)
        html = out.read_text(encoding="utf-8")

        # Both KISA checks (RBL + 화이트도메인) return error (services terminated) — score should still be 100
        assert score == 100
        assert g == "A"
        assert "100" in html
        assert "A" in html


# ---------------------------------------------------------------------------
# T3 — All-failing checks: low score, D/F grade, remediation text in report
# ---------------------------------------------------------------------------

class TestPipelineAllFailingChecks:
    def test_low_score_and_remediation_present(self, tmp_path):
        results = _run_all_checks(_all_fail_resolve, mock_ips=[])
        score = overall_score(results)
        g = grade(score)

        out = tmp_path / "report.html"
        generate_report(_DOMAIN, results, out)
        html = out.read_text(encoding="utf-8")

        assert score < 50
        assert g in ("D", "F")

        # At least one check should have remediation text in the HTML
        remediation_texts = [r.remediation_ko for r in results if r.remediation_ko]
        assert len(remediation_texts) > 0
        assert any(rt[:20] in html for rt in remediation_texts)


# ---------------------------------------------------------------------------
# T4 — KISA 화이트도메인 error exclusion at the pipeline level
# ---------------------------------------------------------------------------

class TestWhitedomainErrorExclusionInPipeline:
    def test_whitedomain_error_does_not_reduce_score_below_100(self, all_pass_results):
        """
        6 checks all pass (score=100). KISA 화이트도메인 is always error (service
        terminated). The scorer must exclude its weight from the denominator, so
        overall_score should still be 100.
        """
        wd = next(r for r in all_pass_results if r.name == "KISA 화이트도메인")
        assert wd.status == "error"

        score = overall_score(all_pass_results)
        assert score == 100
