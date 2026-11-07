"""Validate the official Home Assistant Marketplace repository contract.

This checks files/metadata offline only. A real installation and publisher
contract acceptance must still be reviewed before a release.
"""
from __future__ import annotations

import json
from pathlib import Path

from validate_repository import validate

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "recall_watch"
EXPECTED_MINIMUM_HA = "2026.11.0"


def marketplace_errors(root: Path = ROOT) -> list[str]:
    """Return violations of the Marketplace custom-integration contract."""
    errors = validate(require_owner=True, root=root)
    metadata_file = root / "hacs.json"  # Mandatory Marketplace filename.
    if not metadata_file.is_file():
        return [*errors, "Missing mandatory Marketplace metadata file (hacs.json)"]
    meta = json.loads(metadata_file.read_text(encoding="utf-8"))
    manifest = json.loads(
        (root / "custom_components/recall_watch/manifest.json").read_text(encoding="utf-8")
    )
    if meta.get("homeassistant") != EXPECTED_MINIMUM_HA:
        errors.append(f"Marketplace minimum Home Assistant must be {EXPECTED_MINIMUM_HA}")
    if meta.get("name") != manifest.get("name"):
        errors.append("Marketplace metadata name must match the integration manifest")
    if manifest.get("domain") != "recall_watch":
        errors.append("The installed custom-integration domain must be recall_watch")
    if not manifest.get("version"):
        errors.append("A public custom integration requires a version")
    if not (root / "custom_components/recall_watch/brand/icon.png").is_file():
        errors.append("Marketplace branding icon is missing")
    if not (root / "custom_components/recall_watch/brand/logo.png").is_file():
        errors.append("Marketplace branding logo is missing")
    return errors


if __name__ == "__main__":
    problems = marketplace_errors()
    if problems:
        print("Marketplace validation BLOCKED:")
        for issue in problems:
            print(f" - {issue}")
        raise SystemExit(1)
    print("Marketplace repository structure and metadata validated.")
