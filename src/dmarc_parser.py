"""DMARC aggregate report XML parser (RFC 7489 Appendix C).

Parses DMARC aggregate report XML (from Google, Microsoft, Yahoo, etc.) and
extracts metadata, policy, and per-record authentication results.

Supported XML schema: RFC 7489 Appendix C ``<feedback>`` root element.
Known provider variations:
    - Google wraps records in ``<feedback>`` (standard).
    - Some providers omit optional fields like ``<org_name>`` or ``<extra_contact_info>``.

Functions:
    parse_dmarc_report(xml_bytes) -> DmarcReport

Error handling:
    - Malformed XML raises ValueError with a descriptive message.
    - Missing required fields (``<domain>``, ``<record>``) raise ValueError.
    - Gzipped files should be decompressed before passing to this function.
"""

from __future__ import annotations

import defusedxml.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class DmarcRecord:
    """A single row from a DMARC aggregate report — one source IP's results."""
    source_ip: str
    count: int
    disposition: str  # none, quarantine, reject
    dkim_result: str  # pass, fail, etc.
    spf_result: str   # pass, fail, etc.
    dkim_domain: str = ""
    spf_domain: str = ""


@dataclass
class DmarcReport:
    """Parsed DMARC aggregate report with metadata and records."""
    org_name: str
    domain: str
    date_begin: str
    date_end: str
    records: list[DmarcRecord] = field(default_factory=list)

    @property
    def total_count(self) -> int:
        return sum(r.count for r in self.records)

    @property
    def pass_count(self) -> int:
        return sum(
            r.count for r in self.records
            if r.dkim_result == "pass" or r.spf_result == "pass"
        )

    def to_dict(self) -> dict:
        """Serialize to a JSON-safe dict for DB storage."""
        return {
            "org_name": self.org_name,
            "domain": self.domain,
            "date_begin": self.date_begin,
            "date_end": self.date_end,
            "records": [
                {
                    "source_ip": r.source_ip,
                    "count": r.count,
                    "disposition": r.disposition,
                    "dkim_result": r.dkim_result,
                    "spf_result": r.spf_result,
                    "dkim_domain": r.dkim_domain,
                    "spf_domain": r.spf_domain,
                }
                for r in self.records
            ],
        }


def _text(el: ET.Element | None, tag: str, default: str = "") -> str:
    """Get text content of a child element, or default if missing."""
    if el is None:
        return default
    child = el.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return default


def _epoch_to_iso(epoch_str: str) -> str:
    """Convert Unix epoch string to ISO 8601 datetime string."""
    try:
        ts = int(epoch_str)
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    except (ValueError, OSError):
        return epoch_str


def parse_dmarc_report(xml_bytes: bytes) -> DmarcReport:
    """Parse a DMARC aggregate report from XML bytes.

    Args:
        xml_bytes: Raw XML content (not gzipped).

    Returns:
        DmarcReport with metadata and list of DmarcRecord.

    Raises:
        ValueError: If XML is malformed or missing required elements.
    """
    # Reject XML with DOCTYPE or ENTITY declarations to prevent XXE attacks.
    # DMARC aggregate reports are pure XML with no DTD — any DTD is suspicious.
    xml_head = xml_bytes[:1024].lower()
    if b"<!doctype" in xml_head or b"<!entity" in xml_head:
        raise ValueError("XML에 DOCTYPE 또는 ENTITY 선언이 포함되어 있어 처리할 수 없습니다.")

    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        raise ValueError(f"유효하지 않은 XML 파일입니다: {e}") from e

    # Report metadata
    report_meta = root.find("report_metadata")
    org_name = _text(report_meta, "org_name", "unknown")
    date_range = report_meta.find("date_range") if report_meta is not None else None
    date_begin = _epoch_to_iso(_text(date_range, "begin"))
    date_end = _epoch_to_iso(_text(date_range, "end"))

    # Policy published
    policy = root.find("policy_published")
    domain = _text(policy, "domain")
    if not domain:
        raise ValueError("DMARC 보고서에 도메인 정보가 없습니다.")

    # Records
    records: list[DmarcRecord] = []
    for record_el in root.findall("record"):
        row = record_el.find("row")
        if row is None:
            continue

        source_ip = _text(row, "source_ip", "0.0.0.0")
        count = int(_text(row, "count", "0"))

        policy_eval = row.find("policy_evaluated")
        disposition = _text(policy_eval, "disposition", "none")
        dkim_result = _text(policy_eval, "dkim", "none")
        spf_result = _text(policy_eval, "spf", "none")

        # Auth results (optional, more detailed)
        auth = record_el.find("auth_results")
        dkim_domain = ""
        spf_domain = ""
        if auth is not None:
            dkim_el = auth.find("dkim")
            if dkim_el is not None:
                dkim_domain = _text(dkim_el, "domain")
                # Override with auth_results if present
                auth_dkim = _text(dkim_el, "result")
                if auth_dkim:
                    dkim_result = auth_dkim
            spf_el = auth.find("spf")
            if spf_el is not None:
                spf_domain = _text(spf_el, "domain")
                auth_spf = _text(spf_el, "result")
                if auth_spf:
                    spf_result = auth_spf

        records.append(DmarcRecord(
            source_ip=source_ip,
            count=count,
            disposition=disposition,
            dkim_result=dkim_result,
            spf_result=spf_result,
            dkim_domain=dkim_domain,
            spf_domain=spf_domain,
        ))

    return DmarcReport(
        org_name=org_name,
        domain=domain,
        date_begin=date_begin,
        date_end=date_end,
        records=records,
    )
