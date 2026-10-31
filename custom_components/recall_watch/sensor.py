"""Recall notice count and small translated summary sensors."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from ._client import MAX_PREVIEW, RecallNotice, matching_notices, parse_keywords, serialize_notice
from .const import CONF_KEYWORDS
from .coordinator import RecallCoordinator
from .entity import RecallEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    """Set up count and overview sensors, all sharing one coordinator."""
    async_add_entities(
        [RecallNoticesSensor(entry.runtime_data, entry)]
        + [RecallLatestFieldSensor(entry.runtime_data, entry, key) for key in (
            "product", "brand", "risk_type", "batch_number", "best_before_date"
        )]
    )


class _FilteredRecallSensor(RecallEntity, SensorEntity):
    """Shared keyword filtering, restricted to coordinator state."""

    def __init__(self, coordinator: RecallCoordinator, entry: ConfigEntry, key: str) -> None:
        super().__init__(coordinator, entry.entry_id, key)
        self._keywords = parse_keywords(entry.options.get(CONF_KEYWORDS, ""))

    @property
    def _matches(self) -> tuple[RecallNotice, ...]:
        return matching_notices(self.coordinator.data, self._keywords)


class RecallNoticesSensor(_FilteredRecallSensor):
    """Count currently published notices and provide a small preview list."""

    _attr_translation_key = "matching_notices"
    _attr_icon = "mdi:alert-circle-outline"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: RecallCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry, "matching_notices")

    @property
    def native_value(self) -> int:
        """Match count in the current feed, not the historic count."""
        return len(self._matches)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Keep recorder writes small; full results use the get_notices action."""
        matches = self._matches
        result: dict[str, Any] = {
            "source": getattr(getattr(self.coordinator, "source", None), "name", "Swedish Food Agency"),
            "preview_count": min(len(matches), MAX_PREVIEW),
            "notices": [serialize_notice(item) for item in matches[:MAX_PREVIEW]],
        }
        if matches:
            latest = matches[0]
            result["latest_title"] = latest.title[:255]
            if latest.url is not None:
                result["latest_url"] = latest.url
            if latest.published is not None:
                result["latest_published"] = latest.published.isoformat()
            if latest.updated is not None:
                result["latest_updated"] = latest.updated.isoformat()
        return result


class RecallLatestFieldSensor(_FilteredRecallSensor):
    """A translated latest-notice field; unknown stays unknown."""

    _attr_icon = "mdi:food-alert"

    def __init__(self, coordinator: RecallCoordinator, entry: ConfigEntry, key: str) -> None:
        super().__init__(coordinator, entry, f"latest_{key}")
        self._field = key
        self._attr_translation_key = f"latest_{key}"
        if key == "risk_type":
            self._attr_device_class = SensorDeviceClass.ENUM
            self._attr_options = [
                "allergen", "chemical", "foreign_object", "microbiological",
                "labelling", "packaging", "fire", "burn", "electric_shock", "choking", "multiple",
            ]

    @property
    def native_value(self) -> str | None:
        """Return None for unknown; never infer an affected brand/batch."""
        matches = self._matches
        if not matches:
            return None
        details = matches[0].details
        if self._field == "batch_number":
            return details.batch_numbers[0] if details.batch_numbers else None
        if self._field == "best_before_date":
            return details.best_before_dates[0] if details.best_before_dates else None
        return getattr(details, self._field)
