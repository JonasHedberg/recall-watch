"""Produce installable pre-release candidate ZIP archives without build caches."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent
VERSION = json.loads((ROOT / "custom_components/recall_watch/manifest.json").read_text())["version"]
ARTIFACTS = (
    (OUT / f"recall-watch-hacs-{VERSION}-repository.zip", False),
    (OUT / f"recall-watch-hacs-{VERSION}-manual-install.zip", True),
)
FORBIDDEN = {"__pycache__", ".pytest_cache", ".coverage", ".DS_Store", ".git", ".venv"}


def include(path: Path) -> bool:
    return not any(part in FORBIDDEN or part.endswith(".pyc") for part in path.parts)


def build() -> None:
    component = ROOT / "custom_components/recall_watch"
    for destination, manual in ARTIFACTS:
        base = component if manual else ROOT
        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(base.rglob("*")):
                if path.is_file() and include(path.relative_to(ROOT)):
                    archive.write(path, path.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(destination) as check:
            assert check.testzip() is None
            files = set(check.namelist())
            assert "custom_components/recall_watch/manifest.json" in files
            assert "custom_components/recall_watch/services.yaml" in files
            assert "custom_components/recall_watch/_client/enrichment.py" in files
            assert "custom_components/recall_watch/translations/sv.json" in files
            assert not any("__pycache__" in f or f.endswith(".pyc") for f in files)
            if manual:
                assert all(path.startswith("custom_components/recall_watch/") for path in files)
            else:
                assert "README.md" in files and "hacs.json" in files and "docs/DATA_EXTRACTION.md" in files
        print(f"{destination}: {destination.stat().st_size} bytes, {len(files)} files")


if __name__ == "__main__":
    build()
