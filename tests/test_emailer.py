"""Tests for src/emailer.py — HTML email generation and Resend dispatch.

Resend API calls are mocked so tests run without network access or a real API key.
"""
from unittest.mock import patch, MagicMock

import pytest

from src.models import CheckResult
from src.emailer import (
    render_email_report,
    send_scan_report,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_RESULTS = [
    CheckResult(
        name="SPF",
        status="pass",
        score=100,
        message_ko="SPF 레코드가 올바르게 설정되어 있습니다.",
        detail_ko="v=spf1 include:example.com ~all",
        remediation_ko="",
        raw="v=spf1 include:example.com ~all",
    ),
    CheckResult(
        name="DMARC",
        status="fail",
        score=0,
        message_ko="DMARC 레코드가 없습니다.",
        detail_ko="",
        remediation_ko="_dmarc 레코드를 추가하세요.",
        raw="",
    ),
]

SAMPLE_SCORES = {"overall": 52, "grade": "D", "naver": 44, "naver_label": "주의"}


# ---------------------------------------------------------------------------
# render_email_report
# ---------------------------------------------------------------------------

def test_render_email_report_returns_html_string():
    html = render_email_report("example.co.kr", SAMPLE_RESULTS, SAMPLE_SCORES)
    assert isinstance(html, str)
    assert len(html) > 100


def test_render_email_report_contains_domain():
    html = render_email_report("example.co.kr", SAMPLE_RESULTS, SAMPLE_SCORES)
    assert "example.co.kr" in html


def test_render_email_report_contains_score():
    html = render_email_report("example.co.kr", SAMPLE_RESULTS, SAMPLE_SCORES)
    assert "52" in html


def test_render_email_report_contains_check_names():
    html = render_email_report("example.co.kr", SAMPLE_RESULTS, SAMPLE_SCORES)
    assert "SPF" in html
    assert "DMARC" in html


def test_render_email_report_no_javascript():
    """Email clients strip JS — ensure the template has none."""
    html = render_email_report("example.co.kr", SAMPLE_RESULTS, SAMPLE_SCORES)
    assert "<script" not in html.lower()


def test_render_email_report_has_unsubscribe_link():
    html = render_email_report(
        "example.co.kr", SAMPLE_RESULTS, SAMPLE_SCORES, unsubscribe_url="https://example.com/unsubscribe?token=abc"
    )
    assert "unsubscribe" in html.lower()
    assert "abc" in html


# ---------------------------------------------------------------------------
# send_scan_report
# ---------------------------------------------------------------------------

def test_send_scan_report_calls_resend(monkeypatch):
    mock_send = MagicMock(return_value=MagicMock(id="email-id-123"))
    monkeypatch.setattr("src.emailer.resend.Emails.send", mock_send)
    monkeypatch.setenv("RESEND_API_KEY", "re_test_key")
    monkeypatch.setenv("FROM_EMAIL", "noreply@example.com")

    send_scan_report(
        to_email="user@example.co.kr",
        domain="example.co.kr",
        results=SAMPLE_RESULTS,
        scores=SAMPLE_SCORES,
        unsubscribe_url="https://app.example.com/unsubscribe?token=abc",
    )

    mock_send.assert_called_once()
    call_kwargs = mock_send.call_args[0][0]
    assert call_kwargs["to"] == ["user@example.co.kr"]
    assert "example.co.kr" in call_kwargs["subject"]
    assert "<html" in call_kwargs["html"].lower()


def test_send_scan_report_subject_contains_grade(monkeypatch):
    mock_send = MagicMock(return_value=MagicMock(id="x"))
    monkeypatch.setattr("src.emailer.resend.Emails.send", mock_send)
    monkeypatch.setenv("RESEND_API_KEY", "re_test_key")
    monkeypatch.setenv("FROM_EMAIL", "noreply@example.com")

    send_scan_report(
        to_email="user@example.co.kr",
        domain="example.co.kr",
        results=SAMPLE_RESULTS,
        scores=SAMPLE_SCORES,
        unsubscribe_url="https://app.example.com/unsubscribe?token=abc",
    )

    subject = mock_send.call_args[0][0]["subject"]
    assert "D" in subject  # grade letter
