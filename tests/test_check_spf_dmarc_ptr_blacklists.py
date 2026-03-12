"""
Unit tests for SPF, DMARC, PTR, and Blacklists check modules.
These tests do NOT make live DNS/HTTP calls — they use mocked responses.
Run: uv run pytest tests/test_check_spf_dmarc_ptr_blacklists.py
"""

import pytest
from unittest.mock import patch, MagicMock
import dns.resolver


# ─── SPF ──────────────────────────────────────────────────────────────────────

class TestSPF:
    def _mock_txt(self, record: str):
        rdata = MagicMock()
        rdata.strings = [record.encode()]
        return [rdata]

    def test_pass_with_dash_all(self):
        from src.checks.spf import check_spf
        with patch("dns.resolver.resolve", return_value=self._mock_txt("v=spf1 include:stibee.com -all")):
            r = check_spf("example.co.kr")
        assert r.status == "pass"
        assert r.score == 100

    def test_warn_with_plus_all(self):
        from src.checks.spf import check_spf
        with patch("dns.resolver.resolve", return_value=self._mock_txt("v=spf1 include:stibee.com +all")):
            r = check_spf("example.co.kr")
        assert r.status == "warn"
        assert r.score < 100

    @pytest.mark.parametrize("exc,expected_msg_fragment", [
        (dns.resolver.NoAnswer,  "SPF 레코드가 없습니다"),
        (dns.resolver.NXDOMAIN, "도메인을 찾을 수 없습니다"),
    ])
    def test_spf_fail_when_no_record(self, exc, expected_msg_fragment):
        from src.checks.spf import check_spf
        with patch("dns.resolver.resolve", side_effect=exc):
            r = check_spf("example.co.kr")
        assert r.status == "fail"
        assert r.score == 0
        assert expected_msg_fragment in r.message_ko


# ─── DMARC ────────────────────────────────────────────────────────────────────

class TestDMARC:
    def _mock_txt(self, record: str):
        rdata = MagicMock()
        rdata.strings = [record.encode()]
        return [rdata]

    @pytest.mark.parametrize("record,exp_status,exp_score", [
        ("v=DMARC1; p=reject; rua=mailto:dmarc@example.co.kr",     "pass", 100),
        ("v=DMARC1; p=quarantine; rua=mailto:dmarc@example.co.kr", "warn",  75),
        ("v=DMARC1; p=none; rua=mailto:dmarc@example.co.kr",       "warn",  20),
    ])
    def test_dmarc_policy_outcomes(self, record, exp_status, exp_score):
        from src.checks.dmarc import check_dmarc
        with patch("dns.resolver.resolve", return_value=self._mock_txt(record)):
            r = check_dmarc("example.co.kr")
        assert r.status == exp_status
        assert r.score == exp_score

    def test_dmarc_no_rua_reduces_score(self):
        from src.checks.dmarc import check_dmarc
        with patch("dns.resolver.resolve", return_value=self._mock_txt("v=DMARC1; p=none")):
            r = check_dmarc("example.co.kr")
        assert r.status == "warn"
        assert r.score == 10  # DMARC_SCORE_NONE(20) - DMARC_PENALTY_NO_RUA(10)

    def test_fail_missing(self):
        from src.checks.dmarc import check_dmarc
        with patch("dns.resolver.resolve", side_effect=dns.resolver.NXDOMAIN):
            r = check_dmarc("example.co.kr")
        assert r.status == "fail"
        assert r.score == 0

    def test_dmarc_multiple_records_warns(self):
        """Multiple v=DMARC1 records should return warn per RFC 7489."""
        from src.checks.dmarc import check_dmarc, DMARC_SCORE_MULTIPLE
        rdata1 = MagicMock()
        rdata1.strings = [b"v=DMARC1; p=reject"]
        rdata2 = MagicMock()
        rdata2.strings = [b"v=DMARC1; p=none"]
        with patch("dns.resolver.resolve", return_value=[rdata1, rdata2]):
            r = check_dmarc("example.co.kr")
        assert r.status == "warn"
        assert r.score == DMARC_SCORE_MULTIPLE
        assert "2개 이상" in r.message_ko


# ─── Scorer (Naver only — overall/grade tests are in test_scorer.py) ──────────

class TestScorer:
    def _results(self, scores: dict[str, int]):
        from src.models import CheckResult
        return [
            CheckResult(name=name, status="pass" if s == 100 else "fail",
                        score=s, message_ko="")
            for name, s in scores.items()
        ]

    def test_naver_score_all_pass(self):
        from src.scorer import naver_score
        results = self._results({
            "SPF": 100, "DKIM": 100, "DMARC": 100,
            "PTR": 100, "KISA 화이트도메인": 100,
        })
        assert naver_score(results) == 100


# ─── PTR ──────────────────────────────────────────────────────────────────────

class TestPTR:
    def test_no_mx_returns_fail(self):
        """Missing MX records should return status='fail', not 'warn'."""
        from src.checks.ptr import check_ptr
        with patch("dns.resolver.resolve", side_effect=dns.resolver.NXDOMAIN):
            r = check_ptr("example.co.kr")
        assert r.status == "fail"
        assert r.score == 0


# ─── Blacklists ───────────────────────────────────────────────────────────────

class TestBlacklists:
    @pytest.mark.parametrize("listed,exp_status,exp_score", [
        (False, "pass", 100),
        (True,  "fail",   0),
    ])
    def test_blacklists_outcome(self, listed, exp_status, exp_score):
        from src.checks.blacklists import check_blacklists
        with patch("src.checks.blacklists.get_sending_ips", return_value=("1.2.3.4",)), \
             patch("src.checks.blacklists._dns_listed", return_value=listed):
            r = check_blacklists("example.co.kr")
        assert r.status == exp_status
        assert r.score == exp_score
