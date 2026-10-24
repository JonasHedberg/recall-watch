"""Source selection and optional notice keyword filtering for Recall Watch."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from ._client import (
    DEFAULT_SOURCE, SOURCES, RecallClient, RecallConnectionError,
    RecallHTTPError, RecallParseError, parse_keywords,
)
from .const import CONF_KEYWORDS, CONF_SOURCE, DOMAIN

_LOGGER = logging.getLogger(__name__)


def _entry_schema() -> vol.Schema:
    """Allow only explicitly supported official endpoints."""
    return vol.Schema({
        vol.Required(CONF_SOURCE, default=DEFAULT_SOURCE): vol.In(
            {source_id: item.name for source_id, item in SOURCES.items()}
        ),
        vol.Optional(CONF_KEYWORDS, default=""): str,
    })


def _options_schema(default: str) -> vol.Schema:
    return vol.Schema({vol.Optional(CONF_KEYWORDS, default=default): str})


class RecallWatchConfigFlow(ConfigFlow, domain=DOMAIN):
    """One independently monitored public source per configuration entry."""

    VERSION = 2

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Check keywords, de-duplicate by source and verify accessibility."""
        errors: dict[str, str] = {}
        if user_input is not None:
            source_id = user_input.get(CONF_SOURCE, DEFAULT_SOURCE)
            if source_id not in SOURCES:
                errors[CONF_SOURCE] = "invalid_source"
            else:
                keywords = user_input.get(CONF_KEYWORDS, "")
                try:
                    parse_keywords(keywords)
                except ValueError:
                    errors[CONF_KEYWORDS] = "invalid_keywords"
                else:
                    await self.async_set_unique_id(source_id)
                    self._abort_if_unique_id_configured()
                    client = RecallClient(async_get_clientsession(self.hass), source_id)
                    try:
                        await client.async_get_notices()
                    except (RecallConnectionError, RecallHTTPError):
                        errors["base"] = "cannot_connect"
                    except RecallParseError:
                        errors["base"] = "invalid_response"
                    except Exception:
                        _LOGGER.exception("Unexpected error validating recall source")
                        errors["base"] = "unknown"
                    else:
                        return self.async_create_entry(
                            title=SOURCES[source_id].name,
                            data={CONF_SOURCE: source_id},
                            options={CONF_KEYWORDS: keywords.strip()},
                        )
        return self.async_show_form(step_id="user", data_schema=_entry_schema(), errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> RecallWatchOptionsFlow:
        """Allow editing search filters, not changing the underlying source."""
        return RecallWatchOptionsFlow()


class RecallWatchOptionsFlow(OptionsFlow):
    """Editable, locally validated keyword filtering."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            keywords = user_input.get(CONF_KEYWORDS, "")
            try:
                parse_keywords(keywords)
            except ValueError:
                errors[CONF_KEYWORDS] = "invalid_keywords"
            else:
                return self.async_create_entry(title="", data={CONF_KEYWORDS: keywords.strip()})
        return self.async_show_form(
            step_id="init",
            data_schema=_options_schema(self.config_entry.options.get(CONF_KEYWORDS, "")),
            errors=errors,
        )
