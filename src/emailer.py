"""Email delivery via Resend SDK.

Renders an email-safe (no JS, inline CSS) HTML scan report and dispatches
it through the Resend API.

Environment variables required at runtime:
    RESEND_API_KEY  — Resend API key (re_...)
    FROM_EMAIL      — Verified sender address
"""

import os
from pathlib import Path
from typing import Any

import resend
from jinja2 import Environment, FileSystemLoader

from src.models import CheckResult

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

_GRADE_COLORS = {
    "A": "#16a34a",
    "B": "#65a30d",
    "C": "#d97706",
    "D": "#ea580c",
    "F": "#dc2626",
}


def render_email_report(
    domain: str,
    results: list[CheckResult],
    scores: dict[str, Any],
    *,
    unsubscribe_url: str = "",
) -> str:
    """Render the email_report.html.j2 template and return the HTML string."""
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)
    template = env.get_template("email_report.html.j2")
    grade_color = _GRADE_COLORS.get(scores.get("grade", "F"), "#6b7280")
    return template.render(
        domain=domain,
        results=results,
        scores=scores,
        grade_color=grade_color,
        unsubscribe_url=unsubscribe_url,
    )


def send_scan_report(
    *,
    to_email: str,
    domain: str,
    results: list[CheckResult],
    scores: dict[str, Any],
    unsubscribe_url: str,
) -> None:
    """Send the HTML scan report to the subscriber via Resend."""
    resend.api_key = os.environ["RESEND_API_KEY"]
    from_email = os.environ["FROM_EMAIL"]

    html = render_email_report(domain, results, scores, unsubscribe_url=unsubscribe_url)
    grade = scores.get("grade", "?")
    overall = scores.get("overall", 0)
    subject = f"[이메일 건강도] {domain} — {overall}/100 ({grade}등급)"

    resend.Emails.send({
        "from": from_email,
        "to": [to_email],
        "subject": subject,
        "html": html,
    })
