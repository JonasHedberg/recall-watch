"""Recall Watch: multiple independent country-specific official recall sources."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from ._client import DEFAULT_SOURCE, SOURCES, RecallClient, matching_notices, page_notices, parse_keywords
from .const import CONF_KEYWORDS, CONF_SOURCE, DOMAIN
from .coordinator import RecallCoordinator

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS: list[Platform] = [Platform.SENSOR]
SERVICE_GET_NOTICES = "get_notices"
_GET_NOTICES_SCHEMA = vol.Schema({
    vol.Optional("source"): vol.In(list(SOURCES)),
    vol.Optional("matching_only", default=True): bool,
    vol.Optional("offset", default=0): vol.All(vol.Coerce(int), vol.Range(min=0, max=250)),
    vol.Optional("limit", default=20): vol.All(vol.Coerce(int), vol.Range(min=1, max=100)),
})


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register exactly one response-only action for all source entries."""
    hass.data.setdefault(DOMAIN, {})

    async def async_get_notices(call: ServiceCall) -> dict:
        entries: dict[str, tuple[RecallCoordinator, ConfigEntry]] = hass.data[DOMAIN]
        source_id = call.data.get("source")
        if source_id is None:
            if len(entries) != 1:
                raise HomeAssistantError(
                    "Provide a source when zero or multiple recall sources are configured"
                )
            source_id = next(iter(entries))
        if source_id not in entries:
            raise HomeAssistantError("The requested recall source is not configured")
        coordinator, entry = entries[source_id]
        notices = coordinator.data
        if call.data.get("matching_only", True):
            notices = matching_notices(notices, parse_keywords(entry.options.get(CONF_KEYWORDS, "")))
        result = page_notices(
            notices, offset=call.data.get("offset", 0), limit=call.data.get("limit", 20)
        )
        return {"source": source_id, **result}

    hass.services.async_register(
        DOMAIN, SERVICE_GET_NOTICES, async_get_notices,
        schema=_GET_NOTICES_SCHEMA, supports_response=SupportsResponse.ONLY,
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Fetch first, then add entities and associate a coordinator per source."""
    source_id = entry.data.get(CONF_SOURCE, DEFAULT_SOURCE)
    if source_id not in SOURCES:
        raise HomeAssistantError("This entry has an unsupported recall source")
    coordinator = RecallCoordinator(hass, RecallClient(async_get_clientsession(hass), source_id))
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    hass.data.setdefault(DOMAIN, {})[source_id] = (coordinator, entry)
    try:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    except Exception:
        hass.data[DOMAIN].pop(source_id, None)
        raise
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload a source after its keyword filters change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Remove only the unloaded source; leave other services/entries alone."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.data.get(CONF_SOURCE, DEFAULT_SOURCE), None)
    return unloaded


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Upgrade the single-source Swedish v0.2 entry without losing sensor IDs."""
    if entry.version == 1:
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, CONF_SOURCE: DEFAULT_SOURCE},
            unique_id=DEFAULT_SOURCE,
            version=2,
        )
        return True
    return entry.version == 2
