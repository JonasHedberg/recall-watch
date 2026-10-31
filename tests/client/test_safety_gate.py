"""Fixed official Safety Gate XML contract fixtures, including failure modes."""
from datetime import datetime, timezone

import pytest
from _client import RecallClient, RecallParseError
from _client.safety_gate import (
    parse_safety_gate_index, parse_safety_gate_report, safety_gate_detail_url,
)

INDEX = b'''<?xml version="1.0"?><Safety-Gate>
<weeklyReport><reference>Report-2026-42</reference><publicationDate>23/10/2026</publicationDate>
<URL>https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/detail/xml/4042?language=en</URL></weeklyReport>
<weeklyReport><reference>Report-2026-41</reference><publicationDate>16/10/2026</publicationDate>
<URL>https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/detail/xml/4041?language=en</URL></weeklyReport>
<weeklyReport><reference>Report-2026-40</reference><publicationDate>09/10/2026</publicationDate>
<URL>https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/detail/xml/4040?language=en</URL></weeklyReport>
</Safety-Gate>'''
DETAIL = b'''<Safety-Gate><report_date>23/10/2026</report_date>
<notifications><caseNumber>SR/123/26</caseNumber>
<name><![CDATA[Example LED night light]]></name><product>Electrical appliance</product>
<brand>TestBrand</brand><riskType>Electric shock</riskType>
<danger>Exposed live connectors.</danger><batchNumber>A12</batchNumber>
<reference>https://ec.europa.eu/safety-gate-alerts/screen/webReport/alertDetail/888</reference>
</notifications></Safety-Gate>'''


def test_index_parsing_and_fixed_detail_url():
    reports = parse_safety_gate_index(INDEX)
    assert [rid for rid, _ in reports] == ['4042', '4041', '4040']
    assert reports[0][1] == datetime(2026, 10, 23, tzinfo=timezone.utc)
    assert safety_gate_detail_url('4042').startswith('https://ec.europa.eu/safety-gate-alerts/')
    for invalid in ('../admin', 'https://example.com', '12?x=1', '１２', ''):
        with pytest.raises(ValueError):
            safety_gate_detail_url(invalid)


def test_metadata_in_report_is_explicit():
    result = parse_safety_gate_report(DETAIL, report_date=datetime(2026, 10, 23, tzinfo=timezone.utc))
    assert len(result) == 1
    alert = result[0]
    assert alert.source_id == 'eu_safety_gate'
    assert alert.identifier == 'SR/123/26'
    assert alert.details.brand == 'TestBrand'
    assert alert.details.product == 'Example LED night light'
    assert alert.details.risk_type == 'electric_shock'
    assert alert.details.batch_numbers == ('A12',)
    assert alert.details.best_before_dates == ()


def test_index_refuses_bad_data_and_nonmatching_id():
    for bad in [b'', b'<html>error</html>', b'<!DOCTYPE x [<!ENTITY x "bad">]><Safety-Gate>&x;</Safety-Gate>', b'<Safety-Gate/>']:
        with pytest.raises(RecallParseError):
            parse_safety_gate_index(bad)
    injected = INDEX.replace(b'/4042?', b'/x4042?')
    assert parse_safety_gate_index(injected)[0][0] == '4041'


def test_report_refuses_fabricated_or_unverifiable_links():
    for raw in [DETAIL.replace(b'https://ec.europa.eu/safety-gate-alerts/', b'https://malicious.invalid/'),
                DETAIL.replace(b'<caseNumber>SR/123/26</caseNumber>', b'<caseNumber/>'),
                b'<Safety-Gate><notifications/></Safety-Gate>']:
        with pytest.raises(RecallParseError):
            parse_safety_gate_report(raw, report_date=datetime(2026, 10, 23, tzinfo=timezone.utc))


@pytest.mark.asyncio
async def test_client_uses_bounded_fixed_endpoint_and_deduplicates():
    class Response:
        def __init__(self, payload):
            self.content, self.payload = self, payload
            self.offset = 0
        async def read(self, max_bytes):
            chunk = self.payload[self.offset:self.offset+max_bytes]
            self.offset += len(chunk)
            return chunk
        def raise_for_status(self):
            pass
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            return False
    class Session:
        def __init__(self):
            self.requests = []
        def get(self, url, **kwargs):
            self.requests.append((url, kwargs))
            return Response(INDEX if len(self.requests) == 1 else DETAIL)
    session = Session()
    result = await RecallClient(session, 'eu_safety_gate').async_get_notices()
    assert len(result) == 1
    assert len(session.requests) == 3
    assert all('ec.europa.eu' in url for url, _ in session.requests)
    assert all(options['allow_redirects'] is False for _, options in session.requests)
