"""
Tests for KISA RBL check.

The service was terminated January 31, 2024. The check must:
- Return immediately without making any DNS request
- Report status="error" (service gone, not actionable — excluded from scoring)
- Message must reference the 2024 termination
- Remediation must point to Naver/Kakao individual paths, NOT the defunct KISA RBL URL
- Must NOT reference rbl.kisa.or.kr in remediation
"""

from unittest.mock import patch

from src.checks.kisa_rbl import check_kisa_rbl


def test_returns_error_without_dns_call():
    """Check must not make any DNS request — service is terminated."""
    with patch("dns.resolver.resolve") as mock_resolve:
        result = check_kisa_rbl("example.co.kr")
        mock_resolve.assert_not_called()
    assert result.status == "error"


def test_message_references_termination():
    """User-facing message must communicate the service ended."""
    result = check_kisa_rbl("example.co.kr")
    combined = (result.message_ko or "") + (result.detail_ko or "")
    assert any(
        keyword in combined
        for keyword in ["종료", "2024", "서비스 종료"]
    ), f"Message should mention termination, got: {combined}"


def test_remediation_does_not_reference_defunct_zone():
    """Remediation must not direct users to the defunct KISA RBL DNS zone."""
    result = check_kisa_rbl("example.co.kr")
    remediation = result.remediation_ko or ""
    assert "rbl.kisa.or.kr" not in remediation
    assert "kisarbl.or.kr" not in remediation


def test_remediation_mentions_naver_or_kakao():
    """Remediation should direct users to the replacement path."""
    result = check_kisa_rbl("example.co.kr")
    remediation = result.remediation_ko or ""
    assert any(
        keyword in remediation
        for keyword in ["네이버", "카카오", "Naver", "naver"]
    ), f"Remediation should mention Naver/Kakao path, got: {remediation}"


def test_score_is_zero():
    """Score is 0 — check is non-functional since service is gone."""
    result = check_kisa_rbl("example.co.kr")
    assert result.score == 0


def test_name_unchanged():
    """Check name must remain stable for scorer compatibility."""
    result = check_kisa_rbl("example.co.kr")
    assert result.name == "KISA RBL"
