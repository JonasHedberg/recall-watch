"""Release acceptance requires real evidence, not just mock-only tests."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

from _client.sources import SOURCES
from scripts.verify_release_evidence import REQUIRED_CHECKS, verify

ROOT = Path(__file__).resolve().parents[2]


def evidence() -> dict:
    return {
        "release_tag": "v0.4.0b2", "reviewed_by": "Release Maintainer",
        "reviewed_commit": "a" * 40,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "sources": {k: {"live_parser_passed": True, "manual_authority_comparison": True,
                        "evidence_url": f"https://github.com/JonasHedberg/recall-watch/actions/runs/42363668578#{k}"} for k in SOURCES},
        "checks": dict.fromkeys(REQUIRED_CHECKS, True),
    }


def test_complete_evidence_contract() -> None:
    assert verify(evidence()) == []


def test_missing_or_false_evidence_blocks() -> None:
    data = evidence()
    data["sources"].pop("eu_safety_gate")
    data["checks"]["real_home_assistant_setup_and_unload"] = False
    assert len(verify(data)) >= 2


def test_old_evidence_and_missing_reviewer_are_blocked() -> None:
    data = evidence()
    data["reviewed_by"] = ""
    data["reviewed_at"] = "2020-01-01T00:00:00+00:00"
    assert len(verify(data)) >= 2


def test_evidence_rejects_stale_or_mismatching_release_tag() -> None:
    data = evidence()
    data["release_tag"] = "v0.4.0b1"
    assert any("manifest version" in error for error in verify(data))

    data["release_tag"] = "v0.4.0b2"
    assert verify(data) == []


def test_evidence_is_bound_to_reviewed_revision_and_proof_is_not_placeholder() -> None:
    data = evidence()
    assert verify(data, expected_commit="a" * 40) == []
    assert any("release candidate" in msg for msg in verify(data, expected_commit="b" * 40))
    data["reviewed_commit"] = "not-a-sha"
    assert any("40-character" in msg for msg in verify(data))
    data = evidence()
    data["sources"]["ca_food"]["evidence_url"] = "https://example.com/example-proof"
    assert any("ca_food" in msg for msg in verify(data))


def test_template_is_deliberately_unapproved() -> None:
    template = json.loads((ROOT / "docs/release-evidence.example.json").read_text())
    assert verify(template)


def test_no_evidence_file_is_an_error() -> None:
    result = subprocess.run([sys.executable, str(ROOT / "scripts/verify_release_evidence.py"),
        "--evidence", str(ROOT / "docs/nonexistent-release-evidence.json")],
        text=True, capture_output=True, check=False)
    assert result.returncode != 0
    assert "BLOCKED" in result.stdout


def test_only_marketplace_installation_is_an_acceptance_requirement() -> None:
    assert "marketplace_install_upgrade_rollback_and_uninstall" in REQUIRED_CHECKS
    assert all(check.islower() for check in REQUIRED_CHECKS)
    data = evidence()
    data["checks"].pop("marketplace_install_upgrade_rollback_and_uninstall")
    data["checks"]["legacy_installation_acceptance"] = True
    assert any("marketplace_install_upgrade_rollback_and_uninstall" in issue for issue in verify(data))
