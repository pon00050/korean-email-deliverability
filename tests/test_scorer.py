"""Tests for src/scorer.py — grade boundaries, weight invariants, and score invariants.

T1 — Grade boundary correctness (parametrized against CLAUDE.md spec)
T2 — WEIGHTS and NAVER_WEIGHTS each sum to 100
T3 — All 7 checks pass with score=100 → overall_score == 100
T4 — 5 pass + 화이트도메인 error → overall_score == 100
T5 — 5 pass + both KISA checks error → overall_score == 100
"""
import pytest

from src.models import CheckResult
from src.scorer import (
    NAVER_WEIGHTS,
    WEIGHTS,
    grade,
    naver_score,
    overall_score,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pass(name: str) -> CheckResult:
    return CheckResult(name=name, status="pass", score=100, message_ko="OK")


def _error(name: str) -> CheckResult:
    return CheckResult(name=name, status="error", score=0, message_ko="오류")


# ---------------------------------------------------------------------------
# T1 — Grade boundary correctness
#
# Spec (from CLAUDE.md):
#   A  ≥ 90
#   B  75–89
#   C  60–74
#   D  40–59
#   F  < 40
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "score,expected_grade",
    [
        (100, "A"),
        (90,  "A"),
        (89,  "B"),
        (75,  "B"),
        (74,  "C"),
        (60,  "C"),
        (59,  "D"),
        (40,  "D"),
        (39,  "F"),
        (0,   "F"),
    ],
)
def test_grade_boundaries(score, expected_grade):
    assert grade(score) == expected_grade


# ---------------------------------------------------------------------------
# T2 — Weight sums
# ---------------------------------------------------------------------------

def test_weights_sum_to_100():
    # KISA 화이트도메인 is included in WEIGHTS for completeness but its
    # contribution is excluded from scoring when status="error".
    # The sum must still be 100 so the error-exclusion scaling works correctly.
    assert sum(WEIGHTS.values()) == 100


def test_naver_weights_sum_to_100():
    assert sum(NAVER_WEIGHTS.values()) == 100


# ---------------------------------------------------------------------------
# T3 — All 7 checks pass → overall_score == 100
# ---------------------------------------------------------------------------

def test_all_checks_pass_gives_100():
    results = [_pass(name) for name in WEIGHTS]
    assert overall_score(results) == 100


# ---------------------------------------------------------------------------
# T4 — 화이트도메인 error + all others pass → overall_score == 100
#
# This tests the error-exclusion invariant introduced in commit f95dd51:
# when a check returns status="error" its weight is excluded from the
# denominator, so a perfect score is still achievable.
# ---------------------------------------------------------------------------

def test_whitedomain_error_with_all_others_passing_gives_100():
    results = [
        _pass("SPF"),
        _pass("DKIM"),
        _pass("DMARC"),
        _pass("PTR"),
        _pass("KISA RBL"),
        _error("KISA 화이트도메인"),
        _pass("국제 블랙리스트"),
    ]
    assert overall_score(results) == 100


# ---------------------------------------------------------------------------
# T5 — Both KISA checks error (both services terminated) + 5 pass → overall_score == 100
#
# KISA RBL terminated January 31, 2024.
# KISA 화이트도메인 terminated June 28, 2024.
# Both return status="error" in production. Combined weight excluded = 20.
# Remaining denominator = 80; 80/80 = 100.
# ---------------------------------------------------------------------------

def test_both_kisa_checks_error_with_others_passing_gives_100():
    results = [
        _pass("SPF"),
        _pass("DKIM"),
        _pass("DMARC"),
        _pass("PTR"),
        _error("KISA RBL"),
        _error("KISA 화이트도메인"),
        _pass("국제 블랙리스트"),
    ]
    assert overall_score(results) == 100
