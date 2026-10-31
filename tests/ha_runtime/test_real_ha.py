"""Exercise configuration, sensors, and the action with genuine Home Assistant fixtures.

Unlike the repository's mocked-contract tests, this suite loads real HA APIs.
Run separately with pytest-homeassistant-custom-component.
"""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.recall_watch._client import SOURCES, parse_recall_feed
from custom_components.recall_watch.const import DOMAIN


@pytest.fixture(autouse=True)
def enable_custom_components(enable_custom_integrations) -> None:
    """Use the real HA integration loader."""


@pytest.mark.asyncio
async def test_real_ha_config_entry_sensors_action_and_unload(hass) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN, unique_id="se_food",
        data={"source": "se_food"}, options={"keywords": ""},
    )
    entry.add_to_hass(hass)
    notices = parse_recall_feed(
        b"<rss><channel><item><title>Sample recall notice</title>"
        b"<link>https://www.livsmedelsverket.se/</link></item></channel></rss>"
    )

    with patch("custom_components.recall_watch.RecallClient", autospec=True) as client_cls:
        client = client_cls.return_value
        client.source = SOURCES["se_food"]
        client.async_get_notices = AsyncMock(return_value=notices)
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        from homeassistant.helpers import entity_registry as er
        registry = er.async_get(hass)
        entities = [item for item in registry.entities.values()
                    if item.platform == DOMAIN and item.config_entry_id == entry.entry_id]
        assert len(entities) == 6
        states = [hass.states.get(item.entity_id) for item in entities]
        assert all(state is not None for state in states)
        assert any(state.state == "1" for state in states)

        result = await hass.services.async_call(
            DOMAIN, "get_notices", {"source": "se_food", "matching_only": True},
            blocking=True, return_response=True,
        )
        assert result["total"] == 1
        assert result["notices"][0]["title"] == "Sample recall notice"
        assert await hass.config_entries.async_unload(entry.entry_id)


@pytest.mark.asyncio
async def test_real_ha_config_flow_validation_and_duplicate_prevention(hass) -> None:
    from homeassistant.data_entry_flow import FlowResultType

    with patch("custom_components.recall_watch.config_flow.RecallClient", autospec=True) as client_cls:
        client_cls.return_value.async_get_notices = AsyncMock(return_value=())
        initial = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
        assert initial["type"] == FlowResultType.FORM

        invalid = await hass.config_entries.flow.async_configure(
            initial["flow_id"], user_input={"source": "se_food", "keywords": "x," * 21}
        )
        assert invalid["type"] == FlowResultType.FORM
        assert invalid["errors"]["keywords"] == "invalid_keywords"

        configured = await hass.config_entries.flow.async_configure(
            initial["flow_id"], user_input={"source": "se_food", "keywords": "Coop"}
        )
        assert configured["type"] == FlowResultType.CREATE_ENTRY
        assert configured["data"]["source"] == "se_food"
        assert configured["options"]["keywords"] == "Coop"

        next_flow = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
        duplicate = await hass.config_entries.flow.async_configure(
            next_flow["flow_id"], user_input={"source": "se_food", "keywords": ""}
        )
        assert duplicate["type"] == FlowResultType.ABORT
        assert duplicate["reason"] == "already_configured"
