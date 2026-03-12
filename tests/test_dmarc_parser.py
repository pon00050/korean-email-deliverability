"""Tests for DMARC aggregate report XML parser."""

from pathlib import Path

import pytest

from src.dmarc_parser import parse_dmarc_report

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_xml():
    return (FIXTURES / "sample_dmarc_report.xml").read_bytes()


class TestParseDmarcReport:
    def test_parses_metadata(self, sample_xml):
        report = parse_dmarc_report(sample_xml)
        assert report.org_name == "google.com"
        assert report.domain == "example.co.kr"
        assert "2024" in report.date_begin  # epoch 1709251200 -> 2024-03-01

    def test_parses_records(self, sample_xml):
        report = parse_dmarc_report(sample_xml)
        assert len(report.records) == 2

    def test_first_record_details(self, sample_xml):
        report = parse_dmarc_report(sample_xml)
        r = report.records[0]
        assert r.source_ip == "203.0.113.1"
        assert r.count == 150
        assert r.disposition == "none"
        assert r.dkim_result == "pass"
        assert r.spf_result == "pass"
        assert r.dkim_domain == "example.co.kr"

    def test_second_record_is_failure(self, sample_xml):
        report = parse_dmarc_report(sample_xml)
        r = report.records[1]
        assert r.source_ip == "198.51.100.5"
        assert r.count == 12
        assert r.disposition == "reject"
        assert r.dkim_result == "fail"
        assert r.spf_result == "fail"

    def test_total_and_pass_counts(self, sample_xml):
        report = parse_dmarc_report(sample_xml)
        assert report.total_count == 162
        assert report.pass_count == 150

    def test_to_dict_serialization(self, sample_xml):
        report = parse_dmarc_report(sample_xml)
        d = report.to_dict()
        assert d["domain"] == "example.co.kr"
        assert len(d["records"]) == 2
        assert d["records"][0]["source_ip"] == "203.0.113.1"

    def test_malformed_xml_raises(self):
        with pytest.raises(ValueError, match="XML"):
            parse_dmarc_report(b"<not valid xml")

    def test_missing_domain_raises(self):
        xml = b"""<?xml version="1.0"?>
        <feedback>
          <report_metadata><org_name>test</org_name></report_metadata>
          <policy_published></policy_published>
        </feedback>"""
        with pytest.raises(ValueError, match="도메인"):
            parse_dmarc_report(xml)

    def test_empty_records_ok(self):
        xml = b"""<?xml version="1.0"?>
        <feedback>
          <report_metadata><org_name>test</org_name></report_metadata>
          <policy_published><domain>example.co.kr</domain></policy_published>
        </feedback>"""
        report = parse_dmarc_report(xml)
        assert report.domain == "example.co.kr"
        assert len(report.records) == 0
        assert report.total_count == 0

    def test_xxe_entity_payload_rejected(self):
        """XML with external entity declarations must be rejected."""
        xxe_xml = b"""<?xml version="1.0"?>
        <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
        <feedback>
          <report_metadata><org_name>&xxe;</org_name></report_metadata>
          <policy_published><domain>example.co.kr</domain></policy_published>
        </feedback>"""
        with pytest.raises(ValueError):
            parse_dmarc_report(xxe_xml)

    def test_billion_laughs_rejected(self):
        """Nested entity expansion (billion laughs) must be rejected."""
        billion = b"""<?xml version="1.0"?>
        <!DOCTYPE lolz [
          <!ENTITY lol "lol">
          <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
          <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
        ]>
        <feedback>
          <report_metadata><org_name>&lol3;</org_name></report_metadata>
          <policy_published><domain>example.co.kr</domain></policy_published>
        </feedback>"""
        with pytest.raises(ValueError):
            parse_dmarc_report(billion)
