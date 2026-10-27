"""Prepare HACS catalog submission from the repository owner's authenticated gh CLI.

Default mode is read-only. --metadata updates GitHub description/topics;
--submit opens the official HACS catalog PR only after verified prerequisites.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

OWNER = "JonasHedberg"
REPO = f"{OWNER}/recall-watch"
ROOT = Path(__file__).resolve().parents[1]
TOPICS = (
    "home-assistant", "hacs", "custom-integration",
    "product-recalls", "food-safety", "safety-gate",
)
DESCRIPTION = (
    "Monitor official food and consumer product safety recalls "
    "from multiple countries in Home Assistant."
)


def run(*args: str, cwd: Path | None = None) -> str:
    proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
    if proc.returncode:
        raise RuntimeError(f"{' '.join(args[:3])} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def api(path: str):
    return json.loads(run("gh", "api", path))


def insert_catalog_entry(items: list[str], name: str = REPO) -> list[str]:
    """Insert alphabetically without reordering unrelated catalog entries."""
    result = list(items)
    if name in result:
        return result
    position = next(
        (index for index, item in enumerate(result)
         if item.casefold() > name.casefold()),
        len(result),
    )
    result.insert(position, name)
    return result


def check() -> tuple[list[str], dict]:
    errors: list[str] = []
    repo = api(f"repos/{REPO}")
    if repo.get("private") or repo.get("archived"):
        errors.append("Repository must be public and unarchived")
    if not repo.get("description"):
        errors.append("Repository description is missing")
    if not repo.get("has_issues"):
        errors.append("GitHub Issues must be enabled")
    if not repo.get("topics"):
        errors.append("GitHub Topics missing: run --metadata")

    manifest = json.loads(
        (ROOT / "custom_components/recall_watch/manifest.json").read_text()
    )
    version = manifest["version"]
    head = api(f"repos/{REPO}/git/ref/heads/main")["object"]["sha"]
    runs = api(f"repos/{REPO}/actions/runs?branch=main&per_page=100")["workflow_runs"]
    good_run = None
    for candidate in runs:
        if candidate.get("head_sha") != head or candidate.get("conclusion") != "success":
            continue
        jobs = api(f"repos/{REPO}/actions/runs/{candidate['id']}/jobs?per_page=100")["jobs"]
        passing = {
            job["name"] for job in jobs if job.get("conclusion") == "success"
        }
        if {"HACS validator", "Home Assistant hassfest"}.issubset(passing) and any(
            name.startswith("Offline unit tests") for name in passing
        ):
            good_run = candidate
            break
    if good_run is None:
        errors.append("No passing HACS/hassfest and Python checks on current main")

    releases = api(f"repos/{REPO}/releases?per_page=30")
    release = next(
        (
            item for item in releases
            if item.get("tag_name", "").removeprefix("v") == version
            and not item.get("draft")
            and not item.get("prerelease")
        ),
        None,
    )
    if release is None:
        errors.append(f"No published stable GitHub release for version {version}")
    elif good_run and release["published_at"] <= good_run["updated_at"]:
        errors.append("Release must be published AFTER successful HACS/hassfest checks")
    return errors, {"version": version, "head": head, "run": good_run, "release": release}


def set_metadata() -> None:
    arguments = ["gh", "api", "-X", "PUT", f"repos/{REPO}/topics"]
    for topic in TOPICS:
        arguments.extend(["-f", f"names[]={topic}"])
    run(*arguments)
    run("gh", "repo", "edit", REPO, "--description", DESCRIPTION)
    run("gh", "workflow", "run", "validate.yml", "-R", REPO, "--ref", "main")
    print("Repository metadata updated. Check the GitHub Actions results before publishing.")


def submit(evidence: dict) -> None:
    """Open a correctly evidenced owner-fork PR to hacs/default."""
    fork = f"{OWNER}/default"
    try:
        api(f"repos/{fork}")
    except RuntimeError:
        run("gh", "repo", "fork", "hacs/default", "--clone=false")
    with tempfile.TemporaryDirectory(prefix="recall-watch-hacs-") as directory:
        workspace = Path(directory) / "default"
        run("git", "clone", f"https://github.com/{fork}.git", str(workspace))
        run("git", "remote", "add", "upstream", "https://github.com/hacs/default.git", cwd=workspace)
        run("git", "fetch", "upstream", "master", cwd=workspace)
        branch = "add-jonashedberg-recall-watch"
        run("git", "checkout", "-B", branch, "upstream/master", cwd=workspace)
        catalog = workspace / "integration"
        entries = json.loads(catalog.read_text())
        if REPO in entries:
            raise RuntimeError("The repository is already in the HACS catalog")
        catalog.write_text(
            json.dumps(insert_catalog_entry(entries), ensure_ascii=False, indent=2) + "\n"
        )
        run("git", "add", "integration", cwd=workspace)
        run("git", "commit", "-m", f"Adds new integration [{REPO}]", cwd=workspace)
        run("git", "push", "-u", "origin", branch, cwd=workspace)
        release_url = evidence["release"]["html_url"]
        action_url = evidence["run"]["html_url"]
        body = workspace / "hacs-pr.md"
        body.write_text(
            "## Checklist\n\n"
            "- [x] I've read the publishing documentation.\n"
            "- [x] I've added the HACS action.\n"
            "- [x] (Integrations only) I've added the hassfest action.\n"
            "- [x] The actions are passing without any disabled checks.\n"
            "- [x] I've added links to the successful action runs.\n"
            "- [x] I've created a new release after the actions passed.\n\n"
            "## Links\n\n"
            f"Link to current release: {release_url}\n\n"
            f"Link to successful HACS action (without ignore): {action_url}\n\n"
            f"Link to successful hassfest action: {action_url}\n"
        )
        print(run(
            "gh", "pr", "create", "-R", "hacs/default",
            "--head", f"{OWNER}:{branch}", "--base", "master",
            "--title", f"Adds new integration [{REPO}]",
            "--body-file", str(body),
        ))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--metadata", action="store_true", help="Set GitHub metadata and rerun CI")
    modes.add_argument("--submit", action="store_true", help="Submit verified catalog PR")
    parser.add_argument(
        "--confirm-reviewed-guidelines", action="store_true",
        help="Confirm the owner has reviewed current HACS submission rules",
    )
    args = parser.parse_args()
    run("gh", "auth", "status")
    if args.metadata:
        set_metadata()
        return
    errors, evidence = check()
    print(f"Main commit: {evidence['head']} | Version: {evidence['version']}")
    if errors:
        for error in errors:
            print(f"BLOCKED: {error}")
        if args.submit:
            raise SystemExit(1)
        return
    print("All automatically verifiable submission requirements passed.")
    if args.submit:
        if not args.confirm_reviewed_guidelines:
            raise SystemExit("Pass --confirm-reviewed-guidelines after reading HACS rules")
        submit(evidence)


if __name__ == "__main__":
    main()
