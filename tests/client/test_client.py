"""Client behavior with isolated, deterministic HTTP fakes."""

from __future__ import annotations

import asyncio

from aiohttp import ClientConnectionError, ClientResponseError
import pytest

from _client import RecallClient, RecallConnectionError, RecallHTTPError, RecallParseError
from _client.parsing import MAX_FEED_BYTES


class FakeContent:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload
        self.read_size: int | None = None
        self.offset = 0

    async def read(self, size: int) -> bytes:
        if self.read_size is None:
            self.read_size = size
        chunk = self.payload[self.offset:self.offset + size]
        self.offset += len(chunk)
        return chunk


class FakeResponse:
    def __init__(self, payload: bytes, error: Exception | None = None) -> None:
        self.content = FakeContent(payload)
        self.error = error

    async def __aenter__(self) -> "FakeResponse":
        return self

    async def __aexit__(self, *_args: object) -> None:
        pass

    def raise_for_status(self) -> None:
        if self.error:
            raise self.error


class FakeSession:
    def __init__(self, response: FakeResponse | Exception) -> None:
        self.response = response
        self.request_url: str | None = None
        self.options: dict[str, object] = {}

    def get(self, url: str, **kwargs: object) -> FakeResponse:
        self.request_url = url
        self.options = kwargs
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


@pytest.mark.asyncio
async def test_get_recalls() -> None:
    response = FakeResponse(b"<rss><channel><item><title>Recall</title></item></channel></rss>")
    session = FakeSession(response)
    notices = await RecallClient(session).async_get_notices()  # type: ignore[arg-type]
    assert notices[0].title == "Recall"
    assert session.request_url == "https://www.livsmedelsverket.se/rss/rss-aterkallanden"
    assert response.content.read_size == MAX_FEED_BYTES + 1
    assert session.options["timeout"] == 20


@pytest.mark.asyncio
async def test_invalid_xml_is_error() -> None:
    with pytest.raises(RecallParseError):
        await RecallClient(FakeSession(FakeResponse(b"no xml"))).async_get_notices()  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_empty_response_is_error() -> None:
    with pytest.raises(RecallParseError):
        await RecallClient(FakeSession(FakeResponse(b""))).async_get_notices()  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_timeout_converted() -> None:
    with pytest.raises(RecallConnectionError):
        await RecallClient(FakeSession(asyncio.TimeoutError())).async_get_notices()  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_connection_error_converted() -> None:
    with pytest.raises(RecallConnectionError):
        await RecallClient(FakeSession(ClientConnectionError("offline"))).async_get_notices()  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_http_error_converted() -> None:
    response = FakeResponse(b"", ClientResponseError(request_info=None, history=(), status=503))  # type: ignore[arg-type]
    with pytest.raises(RecallHTTPError, match="503"):
        await RecallClient(FakeSession(response)).async_get_notices()  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_oversized_content_rejected() -> None:
    response = FakeResponse(b"x" * (MAX_FEED_BYTES + 1))
    with pytest.raises(RecallParseError, match="size limit"):
        await RecallClient(FakeSession(response)).async_get_notices()  # type: ignore[arg-type]

@pytest.mark.asyncio
async def test_http_body_in_multiple_chunks() -> None:
    """Aiohttp read(n) may return less than requested, even without EOF."""
    class FragmentedContent(FakeContent):
        async def read(self, size: int) -> bytes:
            return await super().read(min(size, 9))

    response = FakeResponse(b"<rss><channel><item><title>Complete record</title></item></channel></rss>")
    response.content = FragmentedContent(response.content.payload)
    notices = await RecallClient(FakeSession(response)).async_get_notices()  # type: ignore[arg-type]
    assert len(notices) == 1
    assert notices[0].title == "Complete record"


@pytest.mark.asyncio
async def test_unexpected_redirect_is_refused_without_following_it() -> None:
    """Official endpoints must not redirect requests to arbitrary hosts."""
    response = FakeResponse(b"<html>Moved</html>")
    response.status = 302
    session = FakeSession(response)
    with pytest.raises(RecallHTTPError, match="redirected"):
        await RecallClient(session).async_get_notices()  # type: ignore[arg-type]
    assert session.options["allow_redirects"] is False


@pytest.mark.asyncio
async def test_each_country_uses_non_redirecting_requests() -> None:
    """No country adapter may silently follow an attacker-controlled 3xx target."""
    for source in ("se_food", "ca_food", "ca_consumer", "uk_consumer"):
        content = (b"<feed xmlns='http://www.w3.org/2005/Atom'><entry><title>Sample</title></entry></feed>"
                   if source == "uk_consumer" else
                   b"<rss><channel><item><title>Sample</title></item></channel></rss>")
        session = FakeSession(FakeResponse(content))
        await RecallClient(session, source).async_get_notices()  # type: ignore[arg-type]
        assert session.options["allow_redirects"] is False
