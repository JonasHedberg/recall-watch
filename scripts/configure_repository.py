"""Safely set owner-specific metadata before creating the public repository.

This does not publish to GitHub and must be run by the future human maintainer.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GITHUB_OWNER_PATTERN = re.compile(r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?")


def configure(owner: str, repository: str = "recall-watch", root: Path = ROOT) -> None:
    """Update manifest and community ownership for a real GitHub account."""
    if not GITHUB_OWNER_PATTERN.fullmatch(owner) or "--" in owner:
        raise ValueError("Invalid GitHub owner name; use the exact GitHub login or organization")
    if not GITHUB_OWNER_PATTERN.fullmatch(repository) or "--" in repository:
        raise ValueError("Invalid GitHub repository name")

    manifest_file = root / "custom_components/recall_watch/manifest.json"
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    manifest["documentation"] = f"https://github.com/{owner}/{repository}#readme"
    manifest["issue_tracker"] = f"https://github.com/{owner}/{repository}/issues"
    manifest["codeowners"] = [f"@{owner}"]
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (root / ".github/CODEOWNERS").write_text(
        f"# Responsible repository maintainer.\n* @{owner}\n", encoding="utf-8"
    )
    readme_file = root / "README.md"
    readme = readme_file.read_text(encoding="utf-8")
    readme = readme.replace("OWNER/recall-watch", f"{owner}/{repository}")
    readme_file.write_text(readme, encoding="utf-8")
    print(f"Configured owner for https://github.com/{owner}/{repository}")
    print("Review repository URLs and check that this account is real before publishing.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", required=True, help="Real GitHub username or organization")
    parser.add_argument("--repository", default="recall-watch", help="GitHub repo name")
    args = parser.parse_args()
    configure(args.owner, args.repository)


if __name__ == "__main__":
    main()
