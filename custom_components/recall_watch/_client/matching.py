"""Transparent, conservative title/summary keyword matching."""

from __future__ import annotations

import unicodedata

from .models import RecallNotice

MAX_KEYWORDS = 20
MAX_KEYWORD_LENGTH = 64


def parse_keywords(text: str) -> tuple[str, ...]:
    """Parse case-insensitive literal keywords; empty means all notices."""
    parts = [part.strip() for part in text.split(",")]
    if len(parts) > MAX_KEYWORDS:
        raise ValueError("Too many keywords")
    keywords: list[str] = []
    for part in parts:
        if not part:
            continue
        if len(part) > MAX_KEYWORD_LENGTH or any(ord(char) < 32 for char in part):
            raise ValueError("Invalid keyword")
        normalized = unicodedata.normalize("NFKC", part).casefold()
        if normalized not in keywords:
            keywords.append(normalized)
    return tuple(keywords)


def matching_notices(
    notices: tuple[RecallNotice, ...], keywords: tuple[str, ...]
) -> tuple[RecallNotice, ...]:
    """Match literal substrings; a match does not establish a product/batch match."""
    if not keywords:
        return notices
    return tuple(
        notice
        for notice in notices
        if any(
            keyword in unicodedata.normalize("NFKC", f"{notice.title} {notice.summary} {notice.details.product or ''} {notice.details.brand or ''}").casefold()
            for keyword in keywords
        )
    )
