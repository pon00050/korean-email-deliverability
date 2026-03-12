"""
Scoring logic.

Overall score weights (sum = 100):
  SPF            20
  DKIM           15
  DMARC          25
  PTR            10
  KISA RBL       15
  KISA 화이트도메인  5
  Blacklists     10

Naver compatibility score is a separate composite — not added to the overall
score to avoid double-counting. It's displayed as a secondary indicator.
"""

from src.models import CheckResult

# Grade thresholds: (minimum_score, grade_letter), checked in order
GRADE_THRESHOLDS: list[tuple[int, str]] = [
    (90, "A"),
    (75, "B"),
    (60, "C"),
    (40, "D"),
]

# Naver compatibility label thresholds
NAVER_SCORE_GOOD = 80
NAVER_SCORE_OK = 50

WEIGHTS: dict[str, int] = {
    "SPF": 20,
    "DKIM": 15,
    "DMARC": 25,
    "PTR": 10,
    # KISA RBL service was terminated January 31, 2024. The check returns
    # status="error", which causes overall_score() to exclude this weight from
    # the denominator — so 100/100 is still achievable. The entry is kept here
    # so the weights sum to 100 and the error-exclusion scaling works correctly.
    "KISA RBL": 15,
    # KISA 화이트도메인 service was terminated June 28, 2024. Same treatment.
    "KISA 화이트도메인": 5,
    "국제 블랙리스트": 10,
}

# Naver score weights (independent composite, sums to 100 internally)
# KISA RBL and 국제 블랙리스트 excluded — Naver filtering is independent of these zones
NAVER_WEIGHTS: dict[str, int] = {
    "SPF": 25,
    "DKIM": 20,
    "DMARC": 25,
    "PTR": 15,
    "KISA 화이트도메인": 15,
}


def overall_score(results: list[CheckResult]) -> int:
    by_name = {r.name: r for r in results}
    total = 0
    weight_used = 0
    for name, weight in WEIGHTS.items():
        result = by_name.get(name)
        if result and result.status != "error":
            total += (result.score / 100) * weight
            weight_used += weight
    if weight_used == 0:
        return 0
    # Scale to 100 if some checks were skipped due to errors
    return round(total * 100 / weight_used)


def naver_score(results: list[CheckResult]) -> int:
    by_name = {r.name: r for r in results}
    total = 0
    weight_used = 0
    for name, weight in NAVER_WEIGHTS.items():
        result = by_name.get(name)
        if result and result.status != "error":
            total += (result.score / 100) * weight
            weight_used += weight
    if weight_used == 0:
        return 0
    return round(total * 100 / weight_used)


def grade(score: int) -> str:
    for threshold, letter in GRADE_THRESHOLDS:
        if score >= threshold:
            return letter
    return "F"


def naver_label(score: int) -> tuple[str, str]:
    """Returns (emoji, Korean label) for Naver compatibility score."""
    if score >= NAVER_SCORE_GOOD:
        return "🟢", "양호 — 네이버 메일 수신 가능성 높음"
    if score >= NAVER_SCORE_OK:
        return "🟡", "보통 — 일부 이메일이 스팸함에 분류될 수 있음"
    return "🔴", "위험 — 네이버 메일 수신율이 크게 저하될 가능성 있음"


def status_emoji(status: str) -> str:
    return {"pass": "✅", "warn": "⚠️", "fail": "❌", "error": "⚠️"}.get(status, "")
