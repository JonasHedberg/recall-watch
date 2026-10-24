"""Offline structure checks for a public HACS/Marketplace source repository.

Does NOT prove that HACS/hassfest accept the repo or that HA runtime works.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "recall_watch"
REQUIRED = [
    "README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md", "hacs.json",
    ".github/CODEOWNERS", ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/ci.yml", ".github/dependabot.yml",
    "custom_components/recall_watch/__init__.py",
    "custom_components/recall_watch/sensor.py",
    "custom_components/recall_watch/manifest.json",
    "custom_components/recall_watch/translations/en.json",
    "custom_components/recall_watch/translations/sv.json",
    "docs/GITHUB_SETUP.md", "docs/RELEASE_PROCESS.md",
    "docs/RELEASE_CHECKLIST.md", "docs/QA_REPORT.md",
]
LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)]+)\)")


def leaf_keys(value: object, prefix: str = "") -> set[str]:
    if isinstance(value, dict):
        return {k for key, val in value.items() for k in leaf_keys(val, f"{prefix}/{key}")}
    return {prefix}


def validate(require_owner: bool = False, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for file in REQUIRED:
        if not (root / file).is_file():
            errors.append(f"Missing required file: {file}")
    if errors:
        return errors

    manifest = json.loads((root / "custom_components/recall_watch/manifest.json").read_text())
    hacs = json.loads((root / "hacs.json").read_text())
    if manifest.get("domain") != "recall_watch":
        errors.append("Invalid integration domain")
    for key in ("domain", "documentation", "issue_tracker", "codeowners", "name", "version"):
        if not manifest.get(key):
            errors.append(f"Manifest missing {key} (codeowners can be empty until configured)")
    if manifest.get("codeowners") == [] and not require_owner:
        errors = [x for x in errors if not x.startswith("Manifest missing codeowners")]
    if hacs.get("name") != "Recall Watch":
        errors.append("Invalid HACS name")
    components = root / "custom_components"
    if len([p for p in components.iterdir() if p.is_dir()]) != 1:
        errors.append("Expected exactly one custom integration")
    en = json.loads((components / "recall_watch/translations/en.json").read_text())
    sv = json.loads((components / "recall_watch/translations/sv.json").read_text())
    if leaf_keys(en) != leaf_keys(sv):
        errors.append("English and Swedish locale keys differ")

    for path in root.rglob("*.yml"):
        if any(part in {"__pycache__", ".venv"} for part in path.parts):
            continue
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"Invalid YAML {path.relative_to(root)}: {exc}")

    for md in root.rglob("*.md"):
        if any(part in {"__pycache__", ".venv"} for part in md.parts):
            continue
        content = md.read_text(encoding="utf-8")
        for match in LINK.findall(content):
            dest = unquote(match.split("#", 1)[0].strip())
            if not dest or dest.startswith(("https://", "http://", "mailto:", "#")):
                continue
            if not (md.parent / dest).exists():
                errors.append(f"Broken relative link in {md.relative_to(root)}: {match}")

    if require_owner:
        if "REPLACE_WITH_OWNER" in json.dumps(manifest):
            errors.append("Repository owner is not configured")
        if not manifest.get("codeowners"):
            errors.append("Set actual codeowners before release")
        if "REPLACE_WITH_OWNER" in (root / ".github/CODEOWNERS").read_text():
            errors.append("Set real CODEOWNERS before release")
        if "OWNER/recall-watch" in (root / "README.md").read_text():
            errors.append("Replace README custom-repository example with real owner")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", action="store_true", help="Require real owner metadata")
    args = parser.parse_args()
    failures = validate(require_owner=args.release)
    if failures:
        print("Repository validation failed:")
        for error in failures:
            print(f" - {error}")
        return 1
    print("Offline repository structure and documentation links validated.")
    print("Not a substitute for HACS Action, hassfest, feed tests or a real HA runtime.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
