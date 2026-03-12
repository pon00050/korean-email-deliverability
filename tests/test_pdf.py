"""Tests for PDF generation — gated on WeasyPrint availability.

WeasyPrint requires system-level dependencies (Pango, Cairo) that may not
be present in CI. Tests are skipped if weasyprint is not importable.
"""

import pytest

weasyprint = pytest.importorskip("weasyprint")


SAMPLE_SCAN = {
    "domain": "example.co.kr",
    "overall": 63,
    "grade": "C",
    "naver": 44,
    "naver_label": "보통 — 일부 이메일이 스팸함에 분류될 수 있음",
    "scanned_at": "2026-03-13T12:00:00",
    "public_token": "abc123test",
    "checks": [
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
            "detail_ko": "",
            "remediation_ko": "DKIM을 설정하세요.",
            "raw": "",
        },
    ],
}


def test_generate_pdf_returns_valid_bytes():
    from src.pdf import generate_pdf

    pdf_bytes = generate_pdf(SAMPLE_SCAN, base_url="https://senderfit.kr")
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes[:5] == b"%PDF-"
    assert len(pdf_bytes) > 1000  # sanity: a real PDF is at least a few KB
