"""Bounded, defensive parsing of RSS 2.0 and Atom recall feeds."""

from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlsplit
from xml.etree.ElementTree import ParseError

from defusedxml.ElementTree import fromstring
from defusedxml.common import DefusedXmlException

from .exceptions import RecallParseError
from .enrichment import extract_recall_details
from .models import RecallNotice

MAX_FEED_BYTES = 2 * 1024 * 1024
MAX_NOTICES = 250
MAX_FIELD_CHARS = 2048
_TAG_RE = re.compile(r"<[^>]*>")
_ATOM = "{http://www.w3.org/2005/Atom}"


def _clean_text(value: str | None) -> str:
    """Normalize text while preventing excessively large HA state attributes."""
    if not value:
        return ""
    plain = html.unescape(_TAG_RE.sub(" ", value))
    return " ".join(plain.split())[:MAX_FIELD_CHARS]


def _url(value: str | None) -> str | None:
    """Return only absolute HTTP(S) hyperlinks; never publish unsafe schemes."""
    if not value:
        return None
    url = value.strip()
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return None
    return url[:MAX_FIELD_CHARS]


def _date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError, OverflowError):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (TypeError, ValueError, OverflowError):
            return None


def parse_recall_feed(data: bytes, *, source_id: str = "se_food") -> tuple[RecallNotice, ...]:
    """Parse bounded XML, de-duplicate entries and reject unexpected formats."""
    if len(data) > MAX_FEED_BYTES:
        raise RecallParseError("Feed exceeds size limit")
    try:
        root = fromstring(data)
    except (ParseError, DefusedXmlException, ValueError) as err:
        raise RecallParseError("Malformed or unsafe XML") from err

    if root.tag == "rss":
        channel = root.find("channel")
        if channel is None:
            raise RecallParseError("RSS feed lacks a channel")
        elements = channel.findall("item")
        atom = False
    elif root.tag == f"{_ATOM}feed":
        elements = root.findall(f"{_ATOM}entry")
        atom = True
    else:
        raise RecallParseError("Unsupported feed format")

    if len(elements) > MAX_NOTICES:
        raise RecallParseError("Recall feed contains more entries than the safe limit")

    notices: list[RecallNotice] = []
    seen: set[str] = set()
    for element in elements[:MAX_NOTICES]:
        if atom:
            title = _clean_text(element.findtext(f"{_ATOM}title"))
            link_element = element.find(f"{_ATOM}link[@rel='alternate']")
            if link_element is None:
                link_element = element.find(f"{_ATOM}link")
            link = _url(link_element.get("href") if link_element is not None else None)
            identifier = _clean_text(element.findtext(f"{_ATOM}id"))
            published = _date(element.findtext(f"{_ATOM}published") or element.findtext(f"{_ATOM}updated"))
            summary = _clean_text(element.findtext(f"{_ATOM}summary"))
        else:
            title = _clean_text(element.findtext("title"))
            link = _url(element.findtext("link"))
            identifier = _clean_text(element.findtext("guid"))
            published = _date(element.findtext("pubDate"))
            summary = _clean_text(element.findtext("description"))

        if not title:
            continue
        key = identifier or link or title
        if key in seen:
            continue
        seen.add(key)
        notices.append(
            RecallNotice(
                identifier=key,
                title=title,
                url=link,
                published=published,
                summary=summary,
                details=extract_recall_details(title, summary),
                source_id=source_id,
            )
        )
    # RSS feeds are not guaranteed to place the newest entry first. Treat naive
    # source timestamps as UTC for sorting, but preserve original timestamp data.
    def published_timestamp(notice: RecallNotice) -> float:
        if notice.published is None:
            return float("-inf")
        date = notice.published
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        return date.timestamp()

    notices.sort(key=published_timestamp, reverse=True)
    return tuple(notices)
