"""Fail-closed checks for human-reviewed release acceptance evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = json.loads(
    (ROOT / "custom_components/recall_watch/manifest.json").read_text(encoding="utf-8")
)["version"]
EXPECTED_RELEASE_TAG = f"v{MANIFEST_VERSION}"

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "custom_components" / "recall_watch"))
from _client.sources import SOURCES

REQUIRED_CHECKS = (
    "real_home_assistant_setup_and_unload",
    "real_home_assistant_options_reload",
    "english_and_swedish_ui",
    "migration_from_prior_release",
    "failure_recovery_and_stale_data",
    "marketplace_install_upgrade_rollback_and_uninstall",
    "publisher_terms_and_attribution_reviewed",
    "recall_accuracy_manually_compared_with_authority",
    "github_ci_and_security_review",
)


def verify(
    evidence: dict, *, now: datetime | None = None, expected_commit: str | None = None
) -> list[str]:
    errors: list[str] = []
    now = now or datetime.now(timezone.utc)
    if not isinstance(evidence, dict):
        return ["Evidence must be a JSON object"]
    if evidence.get("release_tag") != EXPECTED_RELEASE_TAG:
        errors.append(
            f"Release tag must match the manifest version: {EXPECTED_RELEASE_TAG}"
        )
    reviewer = evidence.get("reviewed_by")
    if (not isinstance(reviewer, str) or len(reviewer.strip()) < 3
            or reviewer.strip().casefold() in {"example reviewer", "placeholder", "unknown"}):
        errors.append("A real human reviewer identity is required")
    revision = evidence.get("reviewed_commit")
    if not isinstance(revision, str) or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        errors.append("Evidence must identify the exact reviewed 40-character Git commit")
    if expected_commit is not None and revision != expected_commit:
        errors.append("Reviewed commit does not match the release candidate revision")
    try:
        timestamp = datetime.fromisoformat(evidence["reviewed_at"])
        if timestamp.tzinfo is None or not (now - timedelta(days=7) <= timestamp.astimezone(timezone.utc) <= now):
            errors.append("Evidence review must be timezone-aware and at most seven days old")
    except (TypeError, ValueError, KeyError):
        errors.append("Invalid evidence review date")
    sources = evidence.get("sources")
    if not isinstance(sources, dict) or set(sources) != set(SOURCES):
        errors.append("Every published source needs evidence")
    else:
        for source_id, details in sources.items():
            if not isinstance(details, dict) or details.get("live_parser_passed") is not True or details.get("manual_authority_comparison") is not True:
                errors.append(f"{source_id}: live and manual comparison evidence missing")
            url = details.get("evidence_url") if isinstance(details, dict) else None
            try:
                parsed = urlsplit(url) if isinstance(url, str) else None
                valid_link = bool(
                    parsed and parsed.scheme == "https" and parsed.hostname
                    and parsed.username is None and parsed.password is None
                    and parsed.hostname.casefold() not in {"example.com", "example.org", "example.net"}
                    and not parsed.hostname.casefold().endswith(".invalid")
                )
                if valid_link:
                    _ = parsed.port
            except ValueError:
                valid_link = False
            if not valid_link:
                errors.append(f"{source_id}: real HTTPS evidence URL missing")
    checks = evidence.get("checks")
    for key in REQUIRED_CHECKS:
        if not isinstance(checks, dict) or checks.get(key) is not True:
            errors.append(f"Manual acceptance gate not completed: {key}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=Path("docs/release-evidence.json"))
    parser.add_argument("--expected-commit", help="Exact 40-character commit SHA for this release candidate")
    args = parser.parse_args()
    path = args.evidence
    if not path.is_file():
        print(f"BLOCKED: Missing {path}; see docs/RELEASE_ACCEPTANCE.md")
        return 1
    try:
        evidence = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        print(f"BLOCKED: Cannot read evidence: {exc}")
        return 1
    issues = verify(evidence, expected_commit=args.expected_commit)
    if issues:
        for issue in issues:
            print(f"BLOCKED: {issue}")
        return 1
    print("Recorded acceptance evidence complete; still requires independent human review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
