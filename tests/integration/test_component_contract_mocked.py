"""Offline contract smoke-tests with HA substitutes.

These do NOT establish compatibility with a real Home Assistant installation.
They exercise our service logic and sensor API shape without a supported HA runtime.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

COMPONENT = Path(__file__).resolve().parents[2] / "custom_components/recall_watch"


@pytest.fixture
def mocked_ha(monkeypatch):
    """Inject only the minimal objects needed by our component modules."""

    def register_module(name: str, **attrs: object) -> None:
        module = ModuleType(name)
        for attr, value in attrs.items():
            setattr(module, attr, value)
        monkeypatch.setitem(sys.modules, name, module)

    class CoordinatorEntity:
        def __class_getitem__(cls, item):
            return cls

        def __init__(self, coordinator):
            self.coordinator = coordinator

    class DataUpdateCoordinator:
        def __class_getitem__(cls, item):
            return cls

        def __init__(self, hass, *, name, update_interval):
            self.hass = hass

    class UpdateFailed(Exception):
        pass

    class Platform:
        SENSOR = "sensor"

    class SensorDeviceClass:
        ENUM = "enum"

    class SensorStateClass:
        MEASUREMENT = "measurement"

    class SupportsResponse:
        ONLY = "only"

    class FakeVol:
        @staticmethod
        def Schema(value):
            return value

        @staticmethod
        def Optional(name, default=None):
            return name

        @staticmethod
        def All(*values):
            return values

        @staticmethod
        def Coerce(value):
            return value

        @staticmethod
        def In(value):
            return value

        @staticmethod
        def Range(*, min, max):
            return min, max

    register_module("voluptuous", **{key: getattr(FakeVol, key) for key in dir(FakeVol) if not key.startswith("_")})
    register_module("homeassistant")
    register_module("homeassistant.components")
    register_module("homeassistant.components.sensor", SensorEntity=type("SensorEntity", (), {}),
                    SensorDeviceClass=SensorDeviceClass, SensorStateClass=SensorStateClass)
    register_module("homeassistant.config_entries", ConfigEntry=type("ConfigEntry", (), {}))
    register_module("homeassistant.const", Platform=Platform)
    register_module("homeassistant.exceptions", HomeAssistantError=type("HomeAssistantError", (Exception,), {}))
    register_module("homeassistant.core", HomeAssistant=type("HomeAssistant", (), {}),
                    ServiceCall=type("ServiceCall", (), {}), SupportsResponse=SupportsResponse)
    register_module("homeassistant.helpers")
    register_module("homeassistant.helpers.aiohttp_client", async_get_clientsession=lambda hass: object())
    register_module("homeassistant.helpers.entity_platform", AddConfigEntryEntitiesCallback=object)
    register_module("homeassistant.helpers.update_coordinator",
                    DataUpdateCoordinator=DataUpdateCoordinator, UpdateFailed=UpdateFailed)
    # Make fake CoordinatorEntity visible at the actual coordinator import location.
    sys.modules["homeassistant.helpers.update_coordinator"].CoordinatorEntity = CoordinatorEntity

    pkg_name = "recall_watch_component_mock"
    package = ModuleType(pkg_name)
    package.__path__ = [str(COMPONENT)]
    monkeypatch.setitem(sys.modules, pkg_name, package)
    yield pkg_name
    for name in list(sys.modules):
        if name.startswith(pkg_name + "."):
            sys.modules.pop(name, None)


def _notices(pkg):
    parser = importlib.import_module(f"{pkg}._client").parse_recall_feed
    return parser(b"""<rss><channel>
       <item><title>Butiken \xc3\xa5terkallar kex p\xc3\xa5 grund av glasbitar</title>
       <description>Varum\xc3\xa4rke: Exempel. Batchnummer: AB123. B\xc3\xa4st f\xc3\xb6re 2027-06-15</description></item>
       <item><title>Important general notice</title></item>
       </channel></rss>""")


@pytest.mark.asyncio
async def test_sensor_contract_latest_fields_and_unknown(mocked_ha) -> None:
    pkg = mocked_ha
    sensor = importlib.import_module(f"{pkg}.sensor")
    entries = SimpleNamespace(options={"keywords": ""}, entry_id="test")
    coordinator = SimpleNamespace(data=_notices(pkg))
    entities = []
    await sensor.async_setup_entry(None, SimpleNamespace(runtime_data=coordinator, **entries.__dict__), entities.extend)
    assert len(entities) == 6
    count = entities[0]
    assert count.native_value == 2
    preview = count.extra_state_attributes["notices"]
    assert preview[0]["product"] == "kex"
    assert preview[0]["brand"] == "Exempel"
    assert preview[0]["risk_type"] == "foreign_object"
    assert preview[0]["batch_numbers"] == ["AB123"]
    assert preview[0]["best_before_dates"] == ["2027-06-15"]
    assert preview[1]["brand"] is None
    assert [entity.native_value for entity in entities[1:]] == [
        "kex", "Exempel", "foreign_object", "AB123", "2027-06-15"
    ]
    first_only = SimpleNamespace(options={"keywords": "general"}, entry_id="test")
    blank = sensor.RecallLatestFieldSensor(coordinator, first_only, "brand")
    assert blank.native_value is None


@pytest.mark.asyncio
async def test_multiple_source_service_registration_and_unload(mocked_ha, monkeypatch) -> None:
    pkg = mocked_ha
    module = importlib.import_module(pkg + ".__init__")
    parser = importlib.import_module(f"{pkg}._client").parse_recall_feed
    se_data = _notices(pkg)
    ca_data = parser(b"<rss><channel><item><title>Canada recall</title></item></channel></rss>", source_id="ca_food")

    class FakeCoordinator:
        def __init__(self, hass, client):
            self.data = se_data if client.source_id == "se_food" else ca_data
            self.async_config_entry_first_refresh = AsyncMock()

    monkeypatch.setattr(module, "RecallClient", lambda session, source_id="se_food": SimpleNamespace(source_id=source_id))
    monkeypatch.setattr(module, "RecallCoordinator", FakeCoordinator)
    registered = {}
    services = SimpleNamespace(async_register=lambda domain, action, handler, **kw: registered.update(
        {"domain": domain, "action": action, "handler": handler, "kwargs": kw}
    ), async_remove=MagicMock())
    config_entries = SimpleNamespace(
        async_forward_entry_setups=AsyncMock(), async_unload_platforms=AsyncMock(return_value=True),
        async_reload=AsyncMock(), async_update_entry=MagicMock(),
    )
    hass = SimpleNamespace(services=services, config_entries=config_entries, data={})
    await module.async_setup(hass, {})
    assert registered["action"] == "get_notices"
    assert registered["kwargs"]["supports_response"] == "only"
    se_entry = SimpleNamespace(data={"source": "se_food"}, options={"keywords": "kex"},
        entry_id="abc", async_on_unload=MagicMock(), add_update_listener=lambda cb: lambda: None)
    ca_entry = SimpleNamespace(data={"source": "ca_food"}, options={"keywords": ""},
        entry_id="def", async_on_unload=MagicMock(), add_update_listener=lambda cb: lambda: None)
    assert await module.async_setup_entry(hass, se_entry)
    assert await module.async_setup_entry(hass, ca_entry)
    result = await registered["handler"](SimpleNamespace(data={"source": "ca_food", "matching_only": True, "offset": 0, "limit": 10}))
    assert result["source"] == "ca_food"
    assert result["total"] == 1
    result = await registered["handler"](SimpleNamespace(data={"source": "se_food", "matching_only": True, "offset": 0, "limit": 10}))
    assert result["total"] == 1
    with pytest.raises(Exception, match="Provide a source"):
        await registered["handler"](SimpleNamespace(data={"offset": 0, "limit": 10}))
    await module.async_update_options(hass, se_entry)
    config_entries.async_reload.assert_awaited_once_with("abc")
    assert await module.async_unload_entry(hass, se_entry)
    assert "ca_food" in hass.data["recall_watch"]
    assert "se_food" not in hass.data["recall_watch"]
    services.async_remove.assert_not_called()
    result = await registered["handler"](SimpleNamespace(data={"offset": 0, "limit": 10}))
    assert result["source"] == "ca_food"
    assert await module.async_unload_entry(hass, ca_entry)


@pytest.mark.asyncio
async def test_legacy_v1_migration(mocked_ha):
    module = importlib.import_module(mocked_ha + ".__init__")
    entries = SimpleNamespace(async_update_entry=MagicMock())
    hass = SimpleNamespace(config_entries=entries)
    entry = SimpleNamespace(version=1, data={}, unique_id="swedish_food_agency")
    assert await module.async_migrate_entry(hass, entry)
    assert entries.async_update_entry.call_args.kwargs["data"] == {"source": "se_food"}
    assert entries.async_update_entry.call_args.kwargs["version"] == 2


@pytest.mark.asyncio
async def test_sensor_preview_bounded_and_missing_product_unknown(mocked_ha) -> None:
    pkg = mocked_ha
    sensor = importlib.import_module(f"{pkg}.sensor")
    parser = importlib.import_module(f"{pkg}._client").parse_recall_feed
    xml = "<rss><channel>" + "".join(f"<item><title>General notice {x}</title></item>" for x in range(16)) + "</channel></rss>"
    coordinator = SimpleNamespace(data=parser(xml.encode()))
    entry = SimpleNamespace(options={"keywords": ""}, entry_id="test")
    count = sensor.RecallNoticesSensor(coordinator, entry)
    assert count.native_value == 16
    assert count.extra_state_attributes["preview_count"] == 5
    assert len(count.extra_state_attributes["notices"]) == 5
    product = sensor.RecallLatestFieldSensor(coordinator, entry, "product")
    assert product.native_value is None
