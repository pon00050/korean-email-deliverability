"""Batch domain scanner for Phase 3 B2B Enrichment API.

Runs up to _MAX_BATCH_DOMAINS scans in parallel and returns structured results.
"""

from __future__ import annotations

import csv
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any

from src.models import CheckResult
from src.scanner import run_scan
from src.scorer import WEIGHTS

_MAX_BATCH_DOMAINS = 50
_MAX_BATCH_WORKERS = 10

# Derived from WEIGHTS so new checks appear in output automatically
_BATCH_CHECK_ORDER: list[str] = list(WEIGHTS.keys())

# Safe CSV column prefixes for each check name
_CHECK_COL_PREFIX: dict[str, str] = {
    "SPF": "spf",
    "DKIM": "dkim",
    "DMARC": "dmarc",
    "PTR": "ptr",
    "KISA RBL": "kisa_rbl",
    "KISA 화이트도메인": "kisa_white",
    "국제 블랙리스트": "intl_bl",
}


def run_batch_scan(domains: list[str]) -> dict[str, Any]:
    """Scan multiple domains in parallel; return structured result dict."""
    results_map: dict[str, dict] = {}

    with ThreadPoolExecutor(max_workers=min(len(domains), _MAX_BATCH_WORKERS)) as pool:
        futures = {pool.submit(run_scan, d): d for d in domains}
        for fut in as_completed(futures):
            domain = futures[fut]
            try:
                check_results, scores = fut.result()
                results_map[domain] = _format_domain_result(domain, check_results, scores)
            except Exception as exc:
                results_map[domain] = {"domain": domain, "error": str(exc)}

    # Preserve input order
    ordered = [results_map[d] for d in domains]
    return {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "count": len(ordered),
        "results": ordered,
    }


def batch_result_to_csv(data: dict[str, Any]) -> str:
    """Format a run_batch_scan result dict as a CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)

    header = ["domain", "overall", "grade", "naver"]
    for check in _BATCH_CHECK_ORDER:
        prefix = _CHECK_COL_PREFIX[check]
        header += [f"{prefix}_status", f"{prefix}_score"]
    writer.writerow(header)

    for row in data["results"]:
        if "error" in row:
            writer.writerow(
                [row["domain"], "error", "", ""] + [""] * (len(_BATCH_CHECK_ORDER) * 2)
            )
            continue
        line: list = [row["domain"], row["overall"], row["grade"], row["naver"]]
        for check in _BATCH_CHECK_ORDER:
            c = row["checks"].get(check, {})
            line += [c.get("status", ""), c.get("score", "")]
        writer.writerow(line)

    return output.getvalue()


def _format_domain_result(
    domain: str, check_results: list[CheckResult], scores: dict[str, Any]
) -> dict[str, Any]:
    checks = {
        r.name: {"status": r.status, "score": r.score, "message_ko": r.message_ko}
        for r in check_results
    }
    return {
        "domain": domain,
        "overall": scores["overall"],
        "grade": scores["grade"],
        "naver": scores["naver"],
        "naver_label": scores["naver_label"],
        "checks": checks,
    }
