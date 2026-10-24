"""Common Recall Watch entity behavior."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import RecallCoordinator


class RecallEntity(CoordinatorEntity[RecallCoordinator]):
    """Coordinator-backed entity with a stable, configurable unique ID."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: RecallCoordinator, entry_id: str, key: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_{key}"
