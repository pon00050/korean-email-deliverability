"""Tests for src/utils.py."""
import pytest

from src.utils import normalize_domain


@pytest.mark.parametrize("raw,expected", [
    ("  Example.CO.KR  ", "example.co.kr"),
    ("https://example.co.kr/", "example.co.kr"),
    ("http://example.co.kr", "example.co.kr"),
    ("example.co.kr", "example.co.kr"),
])
def test_normalize_domain(raw, expected):
    assert normalize_domain(raw) == expected
