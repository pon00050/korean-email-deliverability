#!/usr/bin/env python3
"""
kr-email-health — Korean email domain health checker

Usage:
    senderfit example.co.kr
    senderfit example.co.kr --dkim-selector default
    senderfit example.co.kr --output reports/example.html
    uv run check.py example.co.kr  (no-install alternative)
"""

import sys
import io
import typer
from typing import Optional
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
from src.utils import normalize_domain

app = typer.Typer(help="한국 이메일 도메인 상태 검사기")


@app.command()
def scan(
    domain: str = typer.Argument(..., help="검사할 도메인 (예: example.co.kr)"),
    dkim_selector: Optional[str] = typer.Option(None, "--dkim-selector", help="DKIM 셀렉터 (미입력 시 자동 탐지)"),
    output: Optional[Path] = typer.Option(None, "--output", help="HTML 리포트 저장 경로"),
) -> None:
    domain = normalize_domain(domain)

    print(f"\n🔍 {domain} 도메인 검사 중...\n")

    checks = [
        ("SPF",              lambda: check_spf(domain)),
        ("DKIM",             lambda: check_dkim(domain, dkim_selector)),
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
    output_path = output if output else (
        Path("reports") / f"{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )
    generate_report(domain, results, output_path)
    print(f"\n  📄 리포트 저장됨: {output_path}\n")


if __name__ == "__main__":
    app()
