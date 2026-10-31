"""Offline repository release structure tests (no HA installation required)."""
from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
COMPONENT = ROOT / "custom_components" / "recall_watch"


def test_manifest_and_hacs_layout() -> None:
    manifest = json.loads((COMPONENT / "manifest.json").read_text())
    hacs = json.loads((ROOT / "hacs.json").read_text())
    assert manifest["domain"] == COMPONENT.name == "recall_watch"
    assert manifest["config_flow"] is True
    assert manifest["version"] == "0.4.0b1"
    assert manifest["requirements"] == ["defusedxml>=0.7.1"]
    assert (COMPONENT / "_client" / "client.py").exists()
    assert (COMPONENT / "strings.json").exists()
    assert hacs["name"] == "Recall Watch"


def test_localizations_share_all_keys() -> None:
    def keys(value, path="") -> set[str]:
        if isinstance(value, dict):
            return {key for k, v in value.items() for key in keys(v, path + "." + k)}
        return {path}

    en = json.loads((COMPONENT / "translations/en.json").read_text())
    sv = json.loads((COMPONENT / "translations/sv.json").read_text())
    assert keys(en) == keys(sv)
    assert en["entity"]["sensor"]["matching_notices"]["name"]
    assert sv["entity"]["sensor"]["matching_notices"]["name"]
    assert en["entity"]["sensor"]["latest_risk_type"]["state"]["multiple"]
    assert sv["entity"]["sensor"]["latest_batch_number"]["name"]


def test_release_files_and_dependencies() -> None:
    for filename in ("__init__.py", "sensor.py", "config_flow.py", "coordinator.py", "manifest.json"):
        assert (COMPONENT / filename).is_file()
    for filename in ("README.md", "hacs.json", "LICENSE"):
        assert (ROOT / filename).is_file()
    assert (COMPONENT / "services.yaml").is_file()
    assert (COMPONENT / "_client" / "enrichment.py").is_file()
    assert not any("recall_watch_client" in x.read_text() for x in COMPONENT.glob("*.py"))


def test_resources_present() -> None:
    assert (COMPONENT / "brand/icon.png").stat().st_size > 100
    assert (COMPONENT / "brand/logo.png").stat().st_size > 100

def test_action_source_selector_is_in_sync_with_registry() -> None:
    import sys
    import yaml

    sys.path.insert(0, str(COMPONENT))
    from _client.sources import SOURCES
    from _client.serialization import MAX_OFFSET
    fields = yaml.safe_load((COMPONENT / "services.yaml").read_text())["get_notices"]["fields"]
    ids = {entry["value"] for entry in fields["source"]["selector"]["select"]["options"]}
    assert ids == set(SOURCES)
    assert fields["offset"]["selector"]["number"]["max"] == MAX_OFFSET
