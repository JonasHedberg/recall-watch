"""Bounded parsing of the European Commission's Safety Gate weekly XML exports.

The official weekly reports contain *dangerous non-food product alerts*, not
necessarily consumer recalls. An alert is not proof a product is in your market.
"""

from __future__ import annotations

import re
from datetime import datetime, date, timezone
from xml.etree.ElementTree import ParseError
from defusedxml.ElementTree import fromstring
from defusedxml.common import DefusedXmlException

from .enrichment import RecallDetails, extract_recall_details
from .exceptions import RecallParseError
from .models import RecallNotice
from .parsing import MAX_FEED_BYTES, _clean_text, _url

# Official report index: only digit-only report IDs are extracted and used.
SAFETY_GATE_INDEX = "https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/list/xml/en"
SAFETY_GATE_DETAIL = "https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/detail/xml/"
MAX_INDEX_REPORTS = 1500
MAX_REPORT_ALERTS = 250
MAX_RECENT_REPORTS = 2
_ID = re.compile(r"/detail/xml/(\d+)(?:\?|$)")
_MISSING = {"", "none", "unknown", "n/a", "-"}


def _root(data: bytes):
    if not data or len(data) > MAX_FEED_BYTES:
        raise RecallParseError("Safety Gate response empty or too large")
    try:
        root = fromstring(data)
    except (ParseError, DefusedXmlException, ValueError) as exc:
        raise RecallParseError("Unsafe or malformed Safety Gate XML") from exc
    if root.tag != "Safety-Gate":
        raise RecallParseError("Unexpected Safety Gate document root")
    return root


def _field(element, key: str) -> str:
    node = element.find(key)
    if node is None:
        return ""
    value = _clean_text(" ".join(node.itertext()))
    return "" if value.casefold() in _MISSING else value


def _eu_date(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, "%d/%m/%Y").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def parse_safety_gate_index(data: bytes) -> tuple[tuple[str, datetime], ...]:
    """Read only well-formed report IDs and dates from the official XML index."""
    root = _root(data)
    rows = root.findall("weeklyReport")
    if not 1 <= len(rows) <= MAX_INDEX_REPORTS:
        raise RecallParseError("Safety Gate report index has an unexpected size")
    found: dict[str, datetime] = {}
    for row in rows:
        ref = _field(row, "reference")
        timestamp = _eu_date(_field(row, "publicationDate"))
        url = _field(row, "URL")
        match = _ID.search(url)
        if ref.startswith("Report-") and timestamp and match:
            found[match.group(1)] = timestamp
    if not found:
        raise RecallParseError("Safety Gate report index has no usable reports")
    # Future-dated reports should not be displayed as current.
    today = datetime.now(timezone.utc).date()
    current = [(rid, ts) for rid, ts in found.items() if ts.date() <= today]
    if not current:
        raise RecallParseError("No current Safety Gate weekly reports")
    return tuple(sorted(current, key=lambda item: (item[1], int(item[0])), reverse=True))


def safety_gate_detail_url(report_id: str) -> str:
    """Build a fixed-authority URL; never request arbitrary index-provided URLs."""
    if not report_id.isascii() or not report_id.isdecimal() or len(report_id) > 15:
        raise ValueError("Invalid Safety Gate report identifier")
    return (f"{SAFETY_GATE_DETAIL}{report_id}"
            f"?language=en&search=WEB_REPORT%7C:%7C{report_id},")


def parse_safety_gate_report(data: bytes, *, report_date: datetime) -> tuple[RecallNotice, ...]:
    """Use declared fields, preserving unknowns rather than guessing risk metadata."""
    root = _root(data)
    rows = root.findall("notifications")
    if not 1 <= len(rows) <= MAX_REPORT_ALERTS:
        raise RecallParseError("Safety Gate report has an unexpected number of alerts")
    seen: set[str] = set()
    notices: list[RecallNotice] = []
    for row in rows:
        case = _field(row, "caseNumber")
        raw_url = _field(row, "reference")
        url = _url(raw_url)
        # Reject missing/unverifiable identity or links, never count fabricated entries.
        if not case or not url or not url.startswith("https://ec.europa.eu/safety-gate-alerts/"):
            continue
        if case in seen:
            continue
        seen.add(case)
        product = _field(row, "name") or _field(row, "product")
        brand = _field(row, "brand")
        risk = _field(row, "riskType")
        danger = _field(row, "danger")
        batch = _field(row, "batchNumber")
        if not product:
            product = "Unspecified product"
        title = f"{brand} — {product}" if brand and brand.casefold() not in product.casefold() else product
        summary = " ".join(filter(None, [risk, danger]))[:2048]
        extracted = extract_recall_details(title, summary)
        # Safety Gate uses risk taxonomy different from HA's enum; map only clear names.
        category = risk.casefold()
        mapping = {
            "chemical": "chemical", "fire": "fire", "burns": "burn",
            "electric shock": "electric_shock", "choking": "choking",
            "microbiological": "microbiological",
        }
        risk_type = mapping.get(category) or extracted.risk_type
        batches = (batch[:120],) if batch else ()
        details = RecallDetails(
            product=product[:120] if product != "Unspecified product" else None,
            brand=brand[:120] or None,
            risk_type=risk_type,
            batch_numbers=batches,
        )
        notices.append(RecallNotice(
            identifier=case[:255], title=title[:2048], url=url,
            published=report_date, summary=summary,
            details=details, source_id="eu_safety_gate",
        ))
    if not notices:
        raise RecallParseError("Safety Gate report contained no usable alerts")
    return tuple(notices)
