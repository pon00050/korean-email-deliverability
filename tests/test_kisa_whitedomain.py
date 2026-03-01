"""
Tests for KISA 화이트도메인 check.

The service was terminated June 28, 2024. The check must:
- Return immediately without making any network request
- Report status="warn" (service gone, not actionable)
- Message must reference the 2024 termination
- Remediation must point to Naver/Kakao individual paths, NOT the defunct KISA URL
- Must NOT reference spam.kisa.or.kr/white or 화이트도메인.한국 in remediation
"""

from unittest.mock import patch, MagicMock
import pytest

from src.checks.kisa_whitedomain import check_kisa_whitedomain


def test_returns_warn_without_network_call():
    """Check must not make any HTTP request — service is terminated."""
    with patch("requests.get") as mock_get:
        result = check_kisa_whitedomain("example.co.kr")
        mock_get.assert_not_called()
    assert result.status == "warn"


def test_message_references_termination():
    """User-facing message must communicate the service ended."""
    result = check_kisa_whitedomain("example.co.kr")
    combined = (result.message_ko or "") + (result.detail_ko or "")
    assert any(
        keyword in combined
        for keyword in ["종료", "폐지", "2024", "서비스 종료"]
    ), f"Message should mention termination, got: {combined}"


def test_remediation_points_to_naver_not_kisa_whitedomain():
    """Remediation must not direct users to the defunct KISA whitedomain service."""
    result = check_kisa_whitedomain("example.co.kr")
    remediation = result.remediation_ko or ""
    assert "화이트도메인.한국" not in remediation
    assert "spam.kisa.or.kr/white" not in remediation


def test_remediation_mentions_naver_or_kakao():
    """Remediation should direct users to the replacement path."""
    result = check_kisa_whitedomain("example.co.kr")
    remediation = result.remediation_ko or ""
    assert any(
        keyword in remediation
        for keyword in ["네이버", "카카오", "Naver", "naver"]
    ), f"Remediation should mention Naver/Kakao path, got: {remediation}"


def test_score_is_zero():
    """Score is 0 — nobody can register since service is gone."""
    result = check_kisa_whitedomain("example.co.kr")
    assert result.score == 0


def test_name_unchanged():
    """Check name must remain stable for scorer compatibility."""
    result = check_kisa_whitedomain("example.co.kr")
    assert result.name == "KISA 화이트도메인"
