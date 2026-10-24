"""International source catalog, structured CPSC, country-aware serialization."""
from __future__ import annotations

import json
from datetime import datetime

import pytest

from _client import RecallClient, RecallParseError, parse_cpsc_recalls, parse_recall_feed, serialize_notice
from _client.sources import SOURCES, DEFAULT_SOURCE


CPSC_SAMPLE = [{
    "RecallID": 99991,
    "RecallNumber": "26001",
    "RecallDate": "2026-10-20T00:00:00",
    "Title": "Example electric kettles recalled due to fire hazard",
    "Products": [{"Name": "Demo kettle", "Type": "Appliances"}],
    "Description": "Model X may overheat.",
    "Hazards": [{"Name": "Fire hazard"}],
    "Manufacturers": [{"Name": "Unrelated distributor"}],
    "URL": "https://www.cpsc.gov/Recalls/2026/example",
}]


def test_source_registry_is_fixed_and_jurisdiction_aware():
    assert DEFAULT_SOURCE == "se_food"
    assert set(SOURCES) == {"se_food", "ca_food", "ca_consumer", "uk_consumer", "us_consumer"}
    assert {source.country for source in SOURCES.values()} == {"SE", "CA", "GB", "US"}
    assert all(source.url.startswith("https://") for source in SOURCES.values())


def test_cpsc_structured_fields_are_explicit_and_safe():
    notices = parse_cpsc_recalls(json.dumps(CPSC_SAMPLE).encode())
    assert len(notices) == 1
    notice = notices[0]
    assert notice.identifier == "99991"
    assert notice.details.product == "Demo kettle"
    assert notice.details.brand is None  # manufacturer is not automatically a brand
    assert notice.details.risk_type == "fire"
    assert notice.published == datetime(2026, 10, 20)
    assert serialize_notice(notice)["country"] == "US"
    assert serialize_notice(notice)["source"] == "us_consumer"


def test_cpsc_mixed_records_deduplicated_and_malformed_rejected():
    duplicate = dict(CPSC_SAMPLE[0])
    entries = parse_cpsc_recalls(json.dumps([CPSC_SAMPLE[0], duplicate, {}, 5, None]).encode())
    assert len(entries) == 1
    for payload in [b"", b"{}", b"null", b"no json", b"\xff"]:
        with pytest.raises(RecallParseError):
            parse_cpsc_recalls(payload)
    with pytest.raises(RecallParseError):
        parse_cpsc_recalls(b"[]" * 2_000_000)


def test_cpsc_date_format_and_url_safety():
    record = dict(CPSC_SAMPLE[0], RecallID=None, RecallNumber="DUP-2",
                  RecallDate="/Date(1609459200000)/", URL="javascript:alert(1)", Products=[])
    notices = parse_cpsc_recalls(json.dumps([record]).encode())
    assert notices[0].published is not None
    assert notices[0].published.year == 2021
    assert notices[0].url is None


def test_country_tagging_for_atom_and_rss():
    atom = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>uk-1</id>
      <title>Product recall UK</title><link href="https://www.gov.uk/example"/>
      <updated>2026-10-20T10:00:00Z</updated></entry></feed>'''
    ca_rss = b"<rss><channel><item><title>Canada alert</title></item></channel></rss>"
    assert serialize_notice(parse_recall_feed(atom, source_id="uk_consumer")[0])["country"] == "GB"
    assert serialize_notice(parse_recall_feed(ca_rss, source_id="ca_food")[0])["country"] == "CA"


@pytest.mark.asyncio
async def test_client_source_transport_selection():
    class Response:
        def __init__(self, payload):
            self.content = self
            self.payload = payload
        async def read(self, n):
            return self.payload[:n]
        def raise_for_status(self):
            pass
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            return False
    class Session:
        def __init__(self, payload):
            self.payload = payload
            self.url = None
            self.kwargs = {}
        def get(self, url, **kwargs):
            self.url = url
            self.kwargs = kwargs
            return Response(self.payload)
    ca = Session(b"<rss><channel><item><title>Canada recall</title></item></channel></rss>")
    assert (await RecallClient(ca, "ca_food").async_get_notices())[0].source_id == "ca_food"
    assert ca.url == SOURCES["ca_food"].url
    assert "params" not in ca.kwargs
    usa = Session(json.dumps(CPSC_SAMPLE).encode())
    assert (await RecallClient(usa, "us_consumer").async_get_notices())[0].source_id == "us_consumer"
    assert usa.kwargs["params"]["LastPublishDateStart"]
    assert usa.kwargs["headers"]["Accept"] == "application/json"
    with pytest.raises(ValueError):
        RecallClient(usa, "https://localhost/private")


def test_safe_failure_on_unbounded_cpsc_record_set():
    big_payload = json.dumps([CPSC_SAMPLE[0]] * 251).encode()
    with pytest.raises(RecallParseError, match="safe limit"):
        parse_cpsc_recalls(big_payload)


def test_safe_failure_on_unbounded_rss_entries():
    large = b"<rss><channel>" + b"<item><title>x</title></item>" * 251 + b"</channel></rss>"
    with pytest.raises(RecallParseError, match="safe limit"):
        parse_recall_feed(large)


def test_cpsc_optional_values_are_safely_ignored():
    record = dict(CPSC_SAMPLE[0], RecallID="not-int", RecallNumber=22,
                  RecallDate=None, URL=42, Products=None, Hazards=None,
                  Description=42)
    result = parse_cpsc_recalls(json.dumps([record]).encode())[0]
    assert result.details.product is None
    assert result.published is None
    assert result.url is None
    assert result.identifier == record["Title"]


def test_cpsc_rejects_impossible_timestamp_without_crash():
    record = dict(CPSC_SAMPLE[0], RecallDate="/Date(999999999999999999999999999)/")
    result = parse_cpsc_recalls(json.dumps([record]).encode())[0]
    assert result.published is None
