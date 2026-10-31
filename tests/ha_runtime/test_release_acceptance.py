"""Extended native Home Assistant API tests for release acceptance.

No network requests: only Home Assistant runtime APIs are genuine. Publisher
accuracy and browser UI remain separate manual acceptance gates.
"""
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.recall_watch._client import (
    SOURCES, RecallConnectionError, parse_recall_feed,
)
from custom_components.recall_watch.const import DOMAIN


@pytest.fixture(autouse=True)
def enable_custom_components(enable_custom_integrations) -> None:
    """Allow custom components in the genuine HA test harness."""


def _source_records(source_id: str):
    """Generate records with distinct sources and filterable headings."""
    title = "Coop recalls sample chili" if source_id == "se_food" else "Canadian sample warning"
    xml = (f"<rss><channel><item><title>{title}</title>"
           f"<link>https://example.org/{source_id}</link></item></channel></rss>").encode()
    return parse_recall_feed(xml, source_id=source_id)


def _count_entity(hass, entry):
    registry = er.async_get(hass)
    entities = [
        record for record in registry.entities.values()
        if record.config_entry_id == entry.entry_id and
        record.unique_id.endswith("_matching_notices")
    ]
    assert len(entities) == 1
    return entities[0].entity_id


@pytest.mark.asyncio
async def test_real_ha_multiple_sources_options_reload_and_unload(hass) -> None:
    """Separate cached state, options reload and service routing per source."""
    entries = []
    clients = {}

    def make_client(session, source_id):
        client = SimpleNamespace(
            source=SOURCES[source_id],
            async_get_notices=AsyncMock(return_value=_source_records(source_id)),
        )
        clients[source_id] = client
        return client

    with patch("custom_components.recall_watch.RecallClient", side_effect=make_client):
        for source_id in ("se_food", "ca_food"):
            entry = MockConfigEntry(
                domain=DOMAIN,
                version=2,  # New entries come from ConfigFlow VERSION=2.
                unique_id=source_id,
                data={"source": source_id},
                options={"keywords": ""},
            )
            entry.add_to_hass(hass)
            entries.append(entry)
            assert await hass.config_entries.async_setup(entry.entry_id)
            await hass.async_block_till_done()

        assert hass.states.get(_count_entity(hass, entries[0])).state == "1"
        assert hass.states.get(_count_entity(hass, entries[1])).state == "1"

        # Home Assistant catches service-level HomeAssistantError and returns None
        # to callers in this runtime; ambiguous source must not leak notice data.
        ambiguous = await hass.services.async_call(
            DOMAIN, "get_notices", {}, blocking=True, return_response=True,
        )
        assert ambiguous is None

        for source_id in ("se_food", "ca_food"):
            results = await hass.services.async_call(
                DOMAIN, "get_notices", {"source": source_id},
                blocking=True, return_response=True,
            )
            assert results["source"] == source_id
            assert results["total"] == 1
            assert all(rec["source"] == source_id for rec in results["notices"])

        old_entity_ids = [_count_entity(hass, e) for e in entries]
        hass.config_entries.async_update_entry(entries[0], options={"keywords": "nomatch"})
        await hass.async_block_till_done()
        assert _count_entity(hass, entries[0]) == old_entity_ids[0]
        assert hass.states.get(old_entity_ids[0]).state == "0"
        assert hass.states.get(old_entity_ids[1]).state == "1"

        assert await hass.config_entries.async_unload(entries[0].entry_id)
        await hass.async_block_till_done()
        remaining = await hass.services.async_call(
            DOMAIN, "get_notices", {}, blocking=True, return_response=True,
        )
        assert remaining["source"] == "ca_food"
        assert await hass.config_entries.async_unload(entries[1].entry_id)


@pytest.mark.asyncio
async def test_real_ha_network_failure_and_recovery(hass) -> None:
    """Previously cached data is preserved while the coordinator becomes unavailable."""
    entry = MockConfigEntry(
        domain=DOMAIN, unique_id="se_food", version=2,
        data={"source": "se_food"}, options={"keywords": ""},
    )
    entry.add_to_hass(hass)
    client = SimpleNamespace(
        source=SOURCES["se_food"],
        async_get_notices=AsyncMock(return_value=_source_records("se_food")),
    )

    with patch("custom_components.recall_watch.RecallClient", return_value=client):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        entity_id = _count_entity(hass, entry)
        assert hass.states.get(entity_id).state == "1"
        client.async_get_notices.side_effect = RecallConnectionError("temporary outage")
        await entry.runtime_data.async_refresh()
        await hass.async_block_till_done()
        assert entry.runtime_data.last_update_success is False
        assert hass.states.get(entity_id).state == "unavailable"
        assert len(entry.runtime_data.data) == 1

        client.async_get_notices.side_effect = None
        await entry.runtime_data.async_refresh()
        await hass.async_block_till_done()
        assert entry.runtime_data.last_update_success is True
        assert hass.states.get(entity_id).state == "1"
        assert await hass.config_entries.async_unload(entry.entry_id)


@pytest.mark.asyncio
async def test_real_ha_legacy_migration_retains_entity_identity(hass) -> None:
    """Exercise v1 to v2 migration through Home Assistant's loader."""
    entry = MockConfigEntry(
        domain=DOMAIN, version=1,
        unique_id="swedish_food_agency", data={}, options={"keywords": ""},
    )
    entry.add_to_hass(hass)
    client = SimpleNamespace(
        source=SOURCES["se_food"],
        async_get_notices=AsyncMock(return_value=_source_records("se_food")),
    )
    with patch("custom_components.recall_watch.RecallClient", return_value=client):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        assert entry.version == 2
        assert entry.data["source"] == "se_food"
        assert entry.unique_id == "se_food"
        count_id = _count_entity(hass, entry)
        registry = er.async_get(hass)
        assert registry.async_get(count_id).unique_id == f"{entry.entry_id}_matching_notices"
        assert await hass.config_entries.async_unload(entry.entry_id)


@pytest.mark.asyncio
async def test_real_ha_swedish_and_english_translations_load(hass) -> None:
    """Check actual Home Assistant translation engine rather than just JSON keys."""
    from homeassistant.helpers.translation import async_get_translations
    for locale, expected in (
        ("en", "Monitor official product recalls"),
        ("sv", "Bevaka officiella produktåterkallelser"),
    ):
        result = await async_get_translations(hass, locale, "config", [DOMAIN])
        assert result[f"component.{DOMAIN}.config.step.user.title"] == expected
