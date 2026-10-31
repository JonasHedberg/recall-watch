"""Fail-closed checks for human-reviewed release acceptance evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "custom_components" / "recall_watch"))
from _client.sources import SOURCES

REQUIRED_CHECKS = (
    "real_home_assistant_setup_and_unload",
    "real_home_assistant_options_reload",
    "english_and_swedish_ui",
    "migration_from_prior_release",
    "failure_recovery_and_stale_data",
    "hacs_install_upgrade_and_uninstall",
    "publisher_terms_and_attribution_reviewed",
    "recall_accuracy_manually_compared_with_authority",
    "github_ci_and_security_review",
)


def verify(evidence: dict, *, now: datetime | None = None) -> list[str]:
    errors: list[str] = []
    now = now or datetime.now(timezone.utc)
    if not isinstance(evidence, dict):
        return ["Evidence must be a JSON object"]
    if evidence.get("release_tag") in (None, "", "REPLACE_ME"):
        errors.append("Release tag is not specified")
    reviewer = evidence.get("reviewed_by")
    if not isinstance(reviewer, str) or len(reviewer.strip()) < 3:
        errors.append("Human reviewer identity is required")
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
            if not isinstance(details, dict) or not isinstance(details.get("evidence_url"), str) or not details["evidence_url"].startswith("https://"):
                errors.append(f"{source_id}: valid HTTPS evidence URL missing")
    checks = evidence.get("checks")
    for key in REQUIRED_CHECKS:
        if not isinstance(checks, dict) or checks.get(key) is not True:
            errors.append(f"Manual acceptance gate not completed: {key}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=Path("docs/release-evidence.json"))
    path = parser.parse_args().evidence
    if not path.is_file():
        print(f"BLOCKED: Missing {path}; see docs/RELEASE_ACCEPTANCE.md")
        return 1
    try:
        evidence = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        print(f"BLOCKED: Cannot read evidence: {exc}")
        return 1
    issues = verify(evidence)
    if issues:
        for issue in issues:
            print(f"BLOCKED: {issue}")
        return 1
    print("Recorded acceptance evidence complete; still requires independent human review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
