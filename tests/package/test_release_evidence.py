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
        "release_tag": "v0.4.1b1", "reviewed_by": "Example Reviewer",
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "sources": {k: {"live_parser_passed": True, "manual_authority_comparison": True,
                        "evidence_url": f"https://example.com/{k}"} for k in SOURCES},
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


def test_template_is_deliberately_unapproved() -> None:
    template = json.loads((ROOT / "docs/release-evidence.example.json").read_text())
    assert verify(template)


def test_no_evidence_file_is_an_error() -> None:
    result = subprocess.run([sys.executable, str(ROOT / "scripts/verify_release_evidence.py"),
        "--evidence", str(ROOT / "docs/nonexistent-release-evidence.json")],
        text=True, capture_output=True, check=False)
    assert result.returncode != 0
    assert "BLOCKED" in result.stdout
