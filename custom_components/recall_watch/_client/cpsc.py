"""Bounded, conservative parsing of official CPSC recall JSON records."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from .enrichment import RecallDetails, extract_recall_details
from .exceptions import RecallParseError
from .models import RecallNotice
from .parsing import MAX_FEED_BYTES, MAX_NOTICES, _clean_text, _date, _url


def _as_text(value: Any) -> str:
    return _clean_text(value) if isinstance(value, str) else ""


def _first_named(items: Any) -> str:
    if not isinstance(items, list):
        return ""
    for item in items[:10]:
        if isinstance(item, dict):
            name = _as_text(item.get("Name"))
            if name:
                return name
    return ""


def _recall_date(raw: Any) -> datetime | None:
    """CPSC returns ISO dates; some historical interfaces use .NET ticks."""
    if not isinstance(raw, str):
        return None
    parsed = _date(raw)
    if parsed is not None:
        return parsed
    if raw.startswith("/Date(") and raw.endswith(")/"):
        ticks = raw[6:-2]
        if ticks.lstrip("-").isdigit():
            try:
                return datetime.fromtimestamp(int(ticks) / 1000, tz=timezone.utc)
            except (OverflowError, OSError, ValueError):
                pass
    return None


def parse_cpsc_recalls(data: bytes, *, source_id: str = "us_consumer") -> tuple[RecallNotice, ...]:
    """Accept only a CPSC list of objects; unknown metadata remains unknown."""
    if not data or len(data) > MAX_FEED_BYTES:
        raise RecallParseError("Empty or oversized CPSC response")
    try:
        records = json.loads(data)
    except (UnicodeDecodeError, ValueError) as err:
        raise RecallParseError("Invalid CPSC JSON") from err
    if not isinstance(records, list):
        raise RecallParseError("CPSC response is not a list")
    if len(records) > MAX_NOTICES:
        raise RecallParseError("CPSC response has more notices than the safe limit")
    output: list[RecallNotice] = []
    seen: set[str] = set()
    for record in records[:MAX_NOTICES]:
        if not isinstance(record, dict):
            continue
        title = _as_text(record.get("Title"))
        if not title:
            continue
        recall_id = record.get("RecallID")
        recall_number = _as_text(record.get("RecallNumber"))
        record_id = str(recall_id) if isinstance(recall_id, int) and not isinstance(recall_id, bool) else recall_number
        url = _url(record.get("URL") if isinstance(record.get("URL"), str) else None)
        identifier = record_id or url or title
        if identifier in seen:
            continue
        seen.add(identifier)
        product = _first_named(record.get("Products")) or None
        hazard = _first_named(record.get("Hazards"))
        summary = _as_text(record.get("Description")) or hazard
        extracted = extract_recall_details(title, summary)
        details = RecallDetails(
            product=product or extracted.product,
            brand=extracted.brand,  # Firm/manufacturer is NOT proof of a brand.
            risk_type=extract_recall_details(title, f"{summary} {hazard}").risk_type,
            batch_numbers=extracted.batch_numbers,
            best_before_dates=extracted.best_before_dates,
        )
        output.append(RecallNotice(
            identifier=identifier,
            title=title,
            url=url,
            published=_recall_date(record.get("RecallDate")),
            updated=_recall_date(record.get("LastPublishDate")),
            summary=summary,
            details=details,
            source_id=source_id,
        ))
    def chronological_key(notice: RecallNotice) -> tuple[datetime, datetime, str]:
        """Order amended recalls by last publication date, not original issue date."""
        def utc(date: datetime | None) -> datetime:
            if date is None:
                return datetime.min.replace(tzinfo=timezone.utc)
            return date.replace(tzinfo=timezone.utc) if date.tzinfo is None else date.astimezone(timezone.utc)

        return (utc(notice.updated or notice.published), utc(notice.published), notice.identifier)

    return tuple(sorted(output, key=chronological_key, reverse=True))
