"""Library parsing and input safety tests."""

from datetime import datetime, timezone

import pytest

from _client import RecallParseError, parse_recall_feed
from _client.parsing import MAX_FEED_BYTES


RSS = b'''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel><title>Recall notices</title>
<item><guid>id-1</guid><title>Brand A recalls cinnamon</title>
<link>https://example.org/recall/1</link><pubDate>Fri, 23 Oct 2026 13:00:00 GMT</pubDate>
<description>Possible contamination &amp; advice</description></item>
<item><guid>id-1</guid><title>Duplicate notice</title></item>
<item><title>Brand B recalls cheese</title><link>javascript:alert(1)</link></item>
</channel></rss>'''


def test_rss_parsing_deduplicates_and_sanitizes() -> None:
    notices = parse_recall_feed(RSS)
    assert len(notices) == 2
    assert notices[0].identifier == "id-1"
    assert notices[0].summary == "Possible contamination & advice"
    assert notices[0].published == datetime(2026, 10, 23, 13, tzinfo=timezone.utc)
    assert notices[1].url is None


def test_atom_parsing() -> None:
    atom = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>abc</id>
    <title>Product warning</title><link href="https://example.org/warning" />
    <updated>2026-10-23T10:00:00Z</updated></entry></feed>'''
    result = parse_recall_feed(atom)
    assert result[0].title == "Product warning"
    assert result[0].url == "https://example.org/warning"
    assert result[0].published is not None


@pytest.mark.parametrize("payload", [
    b"", b"<html></html>", b"<rss></rss>", b"<rss><channel>",
    b'<!DOCTYPE rss [<!ENTITY x SYSTEM "file:///etc/passwd">]><rss><channel><item><title>&x;</title></item></channel></rss>',
])
def test_unsafe_or_invalid_xml_rejected(payload: bytes) -> None:
    with pytest.raises(RecallParseError):
        parse_recall_feed(payload)


def test_oversized_feed_rejected() -> None:
    with pytest.raises(RecallParseError, match="size limit"):
        parse_recall_feed(b"a" * (MAX_FEED_BYTES + 1))


def test_empty_feed_is_allowed() -> None:
    assert parse_recall_feed(b"<rss><channel/></rss>") == ()


def test_malformed_dates_do_not_break_feed() -> None:
    feed = b"<rss><channel><item><title>Recall</title><pubDate>nonsense</pubDate></item></channel></rss>"
    assert parse_recall_feed(feed)[0].published is None


def test_bounded_attributes() -> None:
    long_title = "x" * 8000
    result = parse_recall_feed(f"<rss><channel><item><title>{long_title}</title></item></channel></rss>".encode())
    assert len(result[0].title) == 2048


def test_items_without_titles_are_ignored() -> None:
    result = parse_recall_feed(b"<rss><channel><item><link>https://example.org</link></item></channel></rss>")
    assert result == ()


def test_newest_dated_notices_first_and_undated_last() -> None:
    rss = b"""<rss><channel>
        <item><title>Old</title><pubDate>Fri, 23 Oct 2026 10:00:00 GMT</pubDate></item>
        <item><title>Undated</title></item>
        <item><title>New</title><pubDate>2026-10-24T10:00:00</pubDate></item>
        </channel></rss>"""
    result = parse_recall_feed(rss)
    assert [notice.title for notice in result] == ["New", "Old", "Undated"]
