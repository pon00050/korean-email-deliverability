"""Tests for scan persistence — src/scanner.py persist_scan() and route integration."""

from unittest.mock import patch, MagicMock

from src.db import save_scan, get_scan_by_token, create_customer
from src.models import CheckResult


# conn fixture is in tests/conftest.py


MOCK_RESULTS = [
    CheckResult(name="SPF", status="pass", score=100, message_ko="SPF 통과"),
    CheckResult(name="DKIM", status="fail", score=0, message_ko="DKIM 미발견"),
]

MOCK_SCORES = {
    "overall": 63,
    "grade": "C",
    "naver": 44,
    "naver_label": "보통",
}


class TestPersistScan:
    def test_persist_and_retrieve(self, conn):
        from src.scanner import persist_scan

        with patch("src.scanner.run_scan", return_value=(MOCK_RESULTS, MOCK_SCORES)):
            results, scores, token = persist_scan(conn, domain="example.co.kr")

        assert len(token) > 0
        assert scores["overall"] == 63

        scan = get_scan_by_token(conn, token)
        assert scan is not None
        assert scan["domain"] == "example.co.kr"
        assert scan["overall"] == 63
        assert len(scan["checks"]) == 2

    def test_persist_with_provided_results(self, conn):
        from src.scanner import persist_scan

        results, scores, token = persist_scan(
            conn,
            domain="example.co.kr",
            results=MOCK_RESULTS,
            scores=MOCK_SCORES,
        )
        assert scores["grade"] == "C"
        scan = get_scan_by_token(conn, token)
        assert scan["grade"] == "C"

    def test_persist_with_customer(self, conn):
        from src.scanner import persist_scan

        cid = create_customer(conn, email="owner@example.com")
        with patch("src.scanner.run_scan", return_value=(MOCK_RESULTS, MOCK_SCORES)):
            _, _, token = persist_scan(conn, domain="example.co.kr", customer_id=cid)

        scan = get_scan_by_token(conn, token)
        assert scan["customer_id"] == cid

    def test_tokens_unique_across_scans(self, conn):
        from src.scanner import persist_scan

        tokens = set()
        for _ in range(5):
            with patch("src.scanner.run_scan", return_value=(MOCK_RESULTS, MOCK_SCORES)):
                _, _, token = persist_scan(conn, domain="example.co.kr")
            tokens.add(token)
        assert len(tokens) == 5
