"""
Unit tests for individual check modules.
These tests do NOT make live DNS/HTTP calls — they use mocked responses.
Run: uv run pytest tests/test_checks.py
"""

import pytest
import requests
from unittest.mock import patch, MagicMock, Mock
import dns.resolver


# ─── KISA 화이트도메인 ─────────────────────────────────────────────────────────
# Service terminated June 28, 2024. Full tests in test_kisa_whitedomain.py.


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

    def test_fail_no_record(self):
        from src.checks.spf import check_spf
        with patch("dns.resolver.resolve", side_effect=dns.resolver.NoAnswer):
            r = check_spf("example.co.kr")
        assert r.status == "fail"
        assert r.score == 0

    def test_fail_nxdomain(self):
        from src.checks.spf import check_spf
        with patch("dns.resolver.resolve", side_effect=dns.resolver.NXDOMAIN):
            r = check_spf("nonexistent.co.kr")
        assert r.status == "fail"


# ─── DMARC ────────────────────────────────────────────────────────────────────

class TestDMARC:
    def _mock_txt(self, record: str):
        rdata = MagicMock()
        rdata.strings = [record.encode()]
        return [rdata]

    def test_pass_reject(self):
        from src.checks.dmarc import check_dmarc
        with patch("dns.resolver.resolve", return_value=self._mock_txt(
            "v=DMARC1; p=reject; rua=mailto:dmarc@example.co.kr"
        )):
            r = check_dmarc("example.co.kr")
        assert r.status == "pass"
        assert r.score == 100

    def test_warn_quarantine(self):
        from src.checks.dmarc import check_dmarc
        with patch("dns.resolver.resolve", return_value=self._mock_txt(
            "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.co.kr"
        )):
            r = check_dmarc("example.co.kr")
        assert r.status == "warn"
        assert 0 < r.score < 100

    def test_warn_none_policy(self):
        from src.checks.dmarc import check_dmarc
        with patch("dns.resolver.resolve", return_value=self._mock_txt(
            "v=DMARC1; p=none"
        )):
            r = check_dmarc("example.co.kr")
        assert r.status == "warn"

    def test_fail_missing(self):
        from src.checks.dmarc import check_dmarc
        with patch("dns.resolver.resolve", side_effect=dns.resolver.NXDOMAIN):
            r = check_dmarc("example.co.kr")
        assert r.status == "fail"
        assert r.score == 0


# ─── Scorer ───────────────────────────────────────────────────────────────────

class TestScorer:
    def _results(self, scores: dict[str, int]):
        from src.models import CheckResult
        return [
            CheckResult(name=name, status="pass" if s == 100 else "fail",
                        score=s, message_ko="")
            for name, s in scores.items()
        ]

    def test_perfect_score(self):
        from src.scorer import overall_score
        results = self._results({
            "SPF": 100, "DKIM": 100, "DMARC": 100,
            "PTR": 100, "KISA RBL": 100, "KISA 화이트도메인": 100,
            "국제 블랙리스트": 100,
        })
        assert overall_score(results) == 100

    def test_zero_score(self):
        from src.scorer import overall_score
        results = self._results({
            "SPF": 0, "DKIM": 0, "DMARC": 0,
            "PTR": 0, "KISA RBL": 0, "KISA 화이트도메인": 0,
            "국제 블랙리스트": 0,
        })
        assert overall_score(results) == 0

    def test_grade_a(self):
        from src.scorer import grade
        assert grade(95) == "A"
        assert grade(90) == "A"

    def test_grade_f(self):
        from src.scorer import grade
        assert grade(10) == "F"
        assert grade(0) == "F"

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
    def test_clean_domain(self):
        from src.checks.blacklists import check_blacklists
        with patch("src.checks.blacklists.get_sending_ips", return_value=("1.2.3.4",)), \
             patch("src.checks.blacklists._dns_listed", return_value=False):
            r = check_blacklists("clean.co.kr")
        assert r.status == "pass"
        assert r.score == 100

    def test_listed_domain(self):
        from src.checks.blacklists import check_blacklists
        with patch("src.checks.blacklists.get_sending_ips", return_value=("1.2.3.4",)), \
             patch("src.checks.blacklists._dns_listed", return_value=True):
            r = check_blacklists("spam.co.kr")
        assert r.status == "fail"
        assert r.score == 0
