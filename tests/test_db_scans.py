"""Tests for scan persistence CRUD in src/db.py."""

from src.db import (
    create_customer,
    save_scan,
    get_scan_by_token,
    list_scans_by_domain,
    list_scans_for_customer,
    list_customer_domains,
)


# conn fixture is in tests/conftest.py

SAMPLE_CHECKS = [
    {
        "name": "SPF",
        "status": "pass",
        "score": 100,
        "message_ko": "SPF 레코드가 올바르게 설정되어 있습니다.",
        "detail_ko": "v=spf1 include:_spf.google.com ~all",
        "remediation_ko": "",
        "raw": "v=spf1 include:_spf.google.com ~all",
    },
    {
        "name": "DKIM",
        "status": "fail",
        "score": 0,
        "message_ko": "DKIM 레코드를 찾을 수 없습니다.",
    },
]


class TestSaveScan:
    def test_save_and_retrieve_by_token(self, conn):
        scan_id, token = save_scan(
            conn,
            domain="example.co.kr",
            overall=63,
            grade="C",
            naver=44,
            naver_label="보통",
            checks=SAMPLE_CHECKS,
        )
        assert scan_id > 0
        assert len(token) > 0

        scan = get_scan_by_token(conn, token)
        assert scan is not None
        assert scan["domain"] == "example.co.kr"
        assert scan["overall"] == 63
        assert scan["grade"] == "C"
        assert scan["naver"] == 44
        assert scan["naver_label"] == "보통"
        assert len(scan["checks"]) == 2
        assert scan["checks"][0]["name"] == "SPF"
        assert scan["checks"][0]["status"] == "pass"
        assert scan["checks"][1]["name"] == "DKIM"
        assert scan["checks"][1]["score"] == 0

    def test_token_not_found(self, conn):
        assert get_scan_by_token(conn, "nonexistent") is None

    def test_tokens_are_unique(self, conn):
        _, t1 = save_scan(
            conn, domain="a.co.kr", overall=50, grade="D",
            naver=40, naver_label="x", checks=[],
        )
        _, t2 = save_scan(
            conn, domain="b.co.kr", overall=60, grade="C",
            naver=50, naver_label="y", checks=[],
        )
        assert t1 != t2

    def test_save_with_customer_id(self, conn):
        cid = create_customer(conn, email="owner@example.com")
        scan_id, token = save_scan(
            conn,
            domain="example.co.kr",
            overall=80,
            grade="B",
            naver=70,
            naver_label="양호",
            checks=SAMPLE_CHECKS,
            customer_id=cid,
        )
        scan = get_scan_by_token(conn, token)
        assert scan["customer_id"] == cid

    def test_check_detail_fields_stored(self, conn):
        _, token = save_scan(
            conn, domain="example.co.kr", overall=100, grade="A",
            naver=100, naver_label="양호", checks=SAMPLE_CHECKS,
        )
        scan = get_scan_by_token(conn, token)
        spf = scan["checks"][0]
        assert spf["detail_ko"] == "v=spf1 include:_spf.google.com ~all"
        assert spf["raw"] == "v=spf1 include:_spf.google.com ~all"


class TestListScans:
    def test_list_by_domain(self, conn):
        save_scan(conn, domain="example.co.kr", overall=50, grade="D",
                  naver=40, naver_label="x", checks=[])
        save_scan(conn, domain="example.co.kr", overall=60, grade="C",
                  naver=50, naver_label="y", checks=[])
        save_scan(conn, domain="other.co.kr", overall=70, grade="B",
                  naver=60, naver_label="z", checks=[])

        rows = list_scans_by_domain(conn, "example.co.kr")
        assert len(rows) == 2
        # Newest first
        assert rows[0]["overall"] == 60

    def test_list_for_customer(self, conn):
        cid = create_customer(conn, email="c@example.com")
        save_scan(conn, domain="a.co.kr", overall=50, grade="D",
                  naver=40, naver_label="x", checks=[], customer_id=cid)
        save_scan(conn, domain="b.co.kr", overall=60, grade="C",
                  naver=50, naver_label="y", checks=[], customer_id=cid)
        # Different customer
        cid2 = create_customer(conn, email="other@example.com")
        save_scan(conn, domain="c.co.kr", overall=70, grade="B",
                  naver=60, naver_label="z", checks=[], customer_id=cid2)

        rows = list_scans_for_customer(conn, cid)
        assert len(rows) == 2

    def test_list_customer_domains(self, conn):
        cid = create_customer(conn, email="c@example.com")
        save_scan(conn, domain="a.co.kr", overall=50, grade="D",
                  naver=40, naver_label="x", checks=[], customer_id=cid)
        save_scan(conn, domain="a.co.kr", overall=70, grade="B",
                  naver=60, naver_label="y", checks=[], customer_id=cid)
        save_scan(conn, domain="b.co.kr", overall=80, grade="B",
                  naver=70, naver_label="z", checks=[], customer_id=cid)

        domains = list_customer_domains(conn, cid)
        assert len(domains) == 2
        by_domain = {d["domain"]: d for d in domains}
        # Should show latest scan for a.co.kr
        assert by_domain["a.co.kr"]["overall"] == 70
        assert by_domain["b.co.kr"]["overall"] == 80
