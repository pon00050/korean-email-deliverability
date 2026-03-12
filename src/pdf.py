"""PDF generation from persisted scan reports.

Uses WeasyPrint to render an HTML template to PDF. Requires system-level
dependencies (Pango, Cairo) and Korean fonts (fonts-noto-cjk) on the server.

Local dev setup:
    Windows:  choco install gtk-runtime
    macOS:    brew install pango
    Linux:    apt-get install libpango-1.0-0 libcairo2 fonts-noto-cjk

The print-optimized template (report_pdf.html.j2) differs from report_web:
    - No JavaScript, all detail sections expanded
    - @page CSS for margins and page breaks
    - Explicit font declarations for Hangul rendering
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


_jinja_env = None


def _get_jinja_env():
    global _jinja_env
    if _jinja_env is None:
        from jinja2 import Environment, FileSystemLoader
        _jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    return _jinja_env


def generate_pdf(scan: dict[str, Any], base_url: str = "") -> bytes:
    """Render a scan result dict as a PDF and return the raw bytes.

    Args:
        scan: A scan dict as returned by get_scan_by_token() (includes 'checks' list).
        base_url: Public URL for linking (used in template).

    Returns:
        PDF file contents as bytes.

    Raises:
        ImportError: If WeasyPrint is not installed.
    """
    import weasyprint

    template = _get_jinja_env().get_template("report_pdf.html.j2")

    html_string = template.render(
        scan=scan,
        report_url=f"{base_url}/report/{scan.get('public_token', '')}",
    )

    return weasyprint.HTML(string=html_string).write_pdf()
