"""Bounded HTTP retrieval for curated official recall RSS/Atom and CPSC JSON."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from aiohttp import ClientError, ClientResponseError, ClientSession

from .cpsc import parse_cpsc_recalls
from .safety_gate import (MAX_RECENT_REPORTS, parse_safety_gate_index, parse_safety_gate_report, safety_gate_detail_url)
from .exceptions import RecallConnectionError, RecallHTTPError, RecallParseError
from .models import RecallNotice
from .parsing import MAX_FEED_BYTES, parse_recall_feed
from .sources import DEFAULT_SOURCE, SOURCES

SWEDISH_FOOD_RECALLS_URL = SOURCES[DEFAULT_SOURCE].url  # Legacy import compatibility.


async def _read_bounded(content) -> bytes:
    """Read all available stream chunks up to the hard response size limit.

    aiohttp StreamReader.read(n) may return fewer than n bytes before EOF.
    Never pass truncated XML/JSON on to a parser.
    """
    chunks: list[bytes] = []
    remaining = MAX_FEED_BYTES + 1
    while remaining:
        chunk = await content.read(remaining)
        if not chunk:
            break
        if len(chunk) > remaining:
            raise RecallParseError("Recall source exceeds the size limit")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


class RecallClient:
    """Stateless per-source polling client using a caller-owned session."""

    def __init__(self, session: ClientSession, source_id: str = DEFAULT_SOURCE) -> None:
        if source_id not in SOURCES:
            raise ValueError("Unknown source ID")
        self._session = session
        self.source = SOURCES[source_id]

    async def async_get_notices(self) -> tuple[RecallNotice, ...]:
        """Retrieve and parse notices, raising a typed error on failure."""
        accept = (
            "application/json"
            if self.source.feed_format == "cpsc_json"
            else "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9"
        )
        # The unfiltered CPSC API is >20 MB. Ask for recently updated
        # records to bound network, memory and API load; older events can be
        # missed, so this is deliberately a recent-notices monitor only.
        query = {}
        if self.source.feed_format == "cpsc_json":
            query["LastPublishDateStart"] = (
                datetime.now(timezone.utc) - timedelta(days=90)
            ).date().isoformat()
        try:
            async with self._session.get(
                self.source.url,
                headers={"Accept": accept},
                **({"params": query} if query else {}),
                timeout=20,
                allow_redirects=self.source.feed_format != "safety_gate_xml",
                max_redirects=3,
            ) as response:
                response.raise_for_status()
                content = await _read_bounded(response.content)
        except ClientResponseError as err:
            raise RecallHTTPError(f"Recall source returned HTTP {err.status}") from err
        except (ClientError, asyncio.TimeoutError) as err:
            raise RecallConnectionError("Could not connect to recall source") from err
        if not content:
            raise RecallParseError("Empty recall response")
        if self.source.feed_format == "safety_gate_xml":
            reports = parse_safety_gate_index(content)[:MAX_RECENT_REPORTS]
            notices: list[RecallNotice] = []
            seen: set[str] = set()
            # Restrict all additional requests to the fixed official endpoint.
            for report_id, published in reports:
                try:
                    async with self._session.get(
                        safety_gate_detail_url(report_id),
                        headers={"Accept": "application/xml, text/xml"},
                        timeout=20, allow_redirects=False,
                    ) as detail:
                        detail.raise_for_status()
                        document = await _read_bounded(detail.content)
                except ClientResponseError as err:
                    raise RecallHTTPError(f"Safety Gate returned HTTP {err.status}") from err
                except (ClientError, asyncio.TimeoutError) as err:
                    raise RecallConnectionError("Could not download Safety Gate report") from err
                for item in parse_safety_gate_report(document, report_date=published):
                    if item.identifier not in seen:
                        seen.add(item.identifier)
                        notices.append(item)
            return tuple(notices)
        if self.source.feed_format == "cpsc_json":
            return parse_cpsc_recalls(content, source_id=self.source.source_id)
        return parse_recall_feed(content, source_id=self.source.source_id)
