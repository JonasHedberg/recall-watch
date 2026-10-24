"""Verify repository publishing tools without contacting GitHub."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from scripts.configure_repository import configure
from scripts.validate_repository import validate

ROOT = Path(__file__).resolve().parents[2]


def repo_copy(tmp_path: Path) -> Path:
    """Construct a separate test repo without copying virtual environments."""
    for name in ("README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "GOVERNANCE.md", "SECURITY.md", "SUPPORT.md", "hacs.json"):
        shutil.copy2(ROOT / name, tmp_path / name)
    for name in (".github", "custom_components", "docs"):
        shutil.copytree(ROOT / name, tmp_path / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return tmp_path


def test_repository_structure_and_configured_owner(tmp_path: Path) -> None:
    root = repo_copy(tmp_path)
    assert validate(root=root) == []
    assert validate(require_owner=True, root=root) == []


def test_configure_owner_and_validate_release_metadata(tmp_path: Path) -> None:
    root = repo_copy(tmp_path)
    configure("Example-Owner", root=root)
    manifest = json.loads((root / "custom_components/recall_watch/manifest.json").read_text())
    assert manifest["codeowners"] == ["@Example-Owner"]
    assert manifest["issue_tracker"] == "https://github.com/Example-Owner/recall-watch/issues"
    assert "* @Example-Owner" in (root / ".github/CODEOWNERS").read_text()
    assert "Example-Owner/recall-watch" in (root / "README.md").read_text()
    assert validate(require_owner=True, root=root) == []


@pytest.mark.parametrize("invalid", ["x--y", "not valid", "../unsafe", "-start", "end-", ""])
def test_reject_invalid_owner(tmp_path: Path, invalid: str) -> None:
    root = repo_copy(tmp_path)
    original = (root / "custom_components/recall_watch/manifest.json").read_bytes()
    with pytest.raises(ValueError):
        configure(invalid, root=root)
    assert (root / "custom_components/recall_watch/manifest.json").read_bytes() == original
