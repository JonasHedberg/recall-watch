"""Small, JSON-safe views of upstream notices for Home Assistant."""

from __future__ import annotations

from typing import Any

from .models import RecallNotice
from .sources import SOURCES

MAX_PREVIEW = 5
MAX_PAGE_SIZE = 100
# Up to two EU reports, each limited to 250 alerts.
MAX_OFFSET = 500


def serialize_notice(notice: RecallNotice, *, include_summary: bool = False) -> dict[str, Any]:
    """Return bounded details; None signifies unknown, never 'safe'."""
    details = notice.details
    data: dict[str, Any] = {
        "identifier": notice.identifier[:255],
        "source": notice.source_id,
        "country": SOURCES[notice.source_id].country if notice.source_id in SOURCES else None,
        "category": SOURCES[notice.source_id].category if notice.source_id in SOURCES else None,
        "title": notice.title[:255],
        "url": notice.url,
        "published": notice.published.isoformat() if notice.published else None,
        "updated": notice.updated.isoformat() if notice.updated else None,
        "product": details.product,
        "brand": details.brand,
        "risk_type": details.risk_type,
        "batch_numbers": list(details.batch_numbers),
        "best_before_dates": list(details.best_before_dates),
    }
    if include_summary:
        data["summary"] = notice.summary[:1024]
    return data


def page_notices(
    notices: tuple[RecallNotice, ...], *, offset: int = 0, limit: int = 20
) -> dict[str, Any]:
    """Paginate the cached feed; never make per-page network requests."""
    if not 0 <= offset <= MAX_OFFSET or not 1 <= limit <= MAX_PAGE_SIZE:
        raise ValueError("Invalid pagination")
    return {
        "total": len(notices),
        "offset": offset,
        "limit": limit,
        "has_more": offset + limit < len(notices),
        "notices": [serialize_notice(item, include_summary=True) for item in notices[offset:offset + limit]],
    }
