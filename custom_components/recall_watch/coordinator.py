"""Coordinated and conservative polling for public recall data."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ._client import RecallClient, RecallError, RecallNotice

from .const import SCAN_INTERVAL


class RecallCoordinator(DataUpdateCoordinator[tuple[RecallNotice, ...]]):
    """Retrieve a single shared feed instead of polling per entity."""

    def __init__(self, hass: HomeAssistant, client: RecallClient) -> None:
        super().__init__(hass, name=f"Recall Watch: {client.source.name}", update_interval=SCAN_INTERVAL)
        self.source = client.source
        self._client = client

    async def _async_update_data(self) -> tuple[RecallNotice, ...]:
        try:
            return await self._client.async_get_notices()
        except RecallError as err:
            raise UpdateFailed("Unable to update the recall feed") from err
