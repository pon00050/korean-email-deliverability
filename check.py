#!/usr/bin/env python3
"""
kr-email-health — Korean email domain health checker

Usage:
    uv run check.py <domain>
    uv run check.py ＜실제도메인＞.co.kr
    uv run check.py ＜실제도메인＞.co.kr --dkim-selector default
    uv run check.py ＜실제도메인＞.co.kr --output reports/barobill.html
"""

import argparse
import sys
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Ensure UTF-8 output on Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from pathlib import Path

from src.checks import (
    check_spf,
    check_dkim,
    check_dmarc,
    check_ptr,
    check_kisa_rbl,
    check_kisa_whitedomain,
    check_blacklists,
)
from src.scorer import overall_score, naver_score, grade, naver_label, status_emoji
from src.report import generate_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="한국 이메일 도메인 상태 검사기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="예시: uv run check.py ＜실제도메인＞.co.kr",
    )
    parser.add_argument("domain", help="검사할 도메인 (예: ＜실제도메인＞.co.kr)")
    parser.add_argument("--dkim-selector", help="DKIM 셀렉터 (미입력 시 자동 탐지)", default=None)
    parser.add_argument("--output", help="HTML 리포트 저장 경로", default=None)
    args = parser.parse_args()

    domain = args.domain.strip().lower().removeprefix("https://").removeprefix("http://").rstrip("/")

    print(f"\n🔍 {domain} 도메인 검사 중...\n")

    checks = [
        ("SPF",              lambda: check_spf(domain)),
        ("DKIM",             lambda: check_dkim(domain, args.dkim_selector)),
        ("DMARC",            lambda: check_dmarc(domain)),
        ("PTR",              lambda: check_ptr(domain)),
        ("KISA RBL",         lambda: check_kisa_rbl(domain)),
        ("KISA 화이트도메인",  lambda: check_kisa_whitedomain(domain)),
        ("국제 블랙리스트",    lambda: check_blacklists(domain)),
    ]

    from src.models import CheckResult

    print(f"  검사 중...", end="\r")
    results_map: dict[str, CheckResult] = {}
    with ThreadPoolExecutor(max_workers=len(checks)) as ex:
        futures = {ex.submit(fn): label for label, fn in checks}
        for fut in as_completed(futures):
            label = futures[fut]
            try:
                results_map[label] = fut.result()
            except Exception as e:
                results_map[label] = CheckResult(
                    name=label, status="error", score=0,
                    message_ko=f"예기치 않은 오류: {e}"
                )

    # Print in original display order
    results = []
    for label, _ in checks:
        result = results_map[label]
        results.append(result)
        emoji = status_emoji(result.status)
        print(f"  {emoji:<3} {result.name:<20} {result.message_ko}")

    # Scores
    score = overall_score(results)
    n_score = naver_score(results)
    n_emoji, n_label = naver_label(n_score)
    g = grade(score)

    print(f"\n{'─'*55}")
    print(f"  네이버 메일 호환성: {n_emoji} {n_score}/100  {n_label}")
    print(f"  전체 점수:         {score}/100  ({g}등급)")
    print(f"{'─'*55}")

    # HTML report
    output_path = Path(args.output) if args.output else (
        Path("reports") / f"{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )
    generate_report(domain, results, output_path)
    print(f"\n  📄 리포트 저장됨: {output_path}\n")


if __name__ == "__main__":
    main()
