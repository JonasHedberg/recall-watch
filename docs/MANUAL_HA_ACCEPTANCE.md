# Real Home Assistant acceptance runbook (English + Swedish)

**Status: not executed against the maintainer's real Home Assistant environment.**
This guide is intended for a human reviewer with an actual supported Home Assistant instance. GitHub Actions already executes native Home Assistant tests with synthetic source responses; those do not test HACS/Marketplace installation or real frontend rendering.

## Prerequisites

- Dedicated Home Assistant test VM / installation (not an unbacked-up production household).
- Supported Home Assistant 2026.10.x or newer, network access to the six publisher endpoints and access to logs.
- A fresh backup of the test configuration and a copy of the currently installed Recall Watch state, if upgrading.
- The **exact** reviewed PR commit SHA. Do not test an older public tag and label it as this candidate.

## Install candidate from source

1. Record the full PR commit SHA from [PR #12](https://github.com/JonasHedberg/recall-watch/pull/12).
2. Check out that SHA in a clean local repository.
3. Copy `custom_components/recall_watch` to `<HA_CONFIG>/custom_components/recall_watch` (not the repository root ZIP). Restart Home Assistant.
4. Inspect Home Assistant logs. Loading as a custom integration generates a normal custom-integrations warning, but should have no Recall Watch setup exceptions.
5. For later HACS/Marketplace testing, install the same code through the actual supported repository UI, once a *correctly flagged* testing prerelease exists.

## UI / localization verification

Repeat the following in **English** and **Swedish**:

- Open *Settings → Devices & services → Add integration → Recall Watch*.
- Confirm configuration title, source selector, keyword field, descriptions and validation errors are readable; no untranslated keys or malformed characters.
- Select each source separately, and check all six sensors created for the source. Expected keys include matching count, product, brand, risk type, batch, best-before date.
- Confirm risk type translation for `allergen`, `chemical`, `foreign_object`, `microbiological`, `fire`, `burn`, `choking`, `fall`, `multiple`; unknown must display as *unknown*, not `safe`.
- Confirm unknown values, source attribution, original publisher links and mobile views are readable.
- Add a keyword such as `Coop`, verify the count is filtered, then change options and check reload/updated count. Repeat with an invalid keyword list and verify it is rejected.

## Multi-source and lifecycle verification

- Configure all six sources. Check that all 36 expected entities are registered with stable unique IDs and data never leaks between sources.
- Run `recall_watch.get_notices` for each source with `matching_only` true and false, and compare resulting source IDs, pagination limits (0–500) and original links.
- With multiple sources configured, omit `source` from the action and verify it fails with a clear message.
- Record each source's count and sample notices, and manually compare to the publisher URLs. Include an EU Safety Gate alert and distinguish alerts from recalls.
- Disconnect networking or block outbound requests. Trigger a coordinator refresh and verify sensors become *unavailable*, old data is not falsely replaced with zero and recovery is automatic when networking returns.
- Restart Home Assistant. Inspect that configured options, unique IDs, entity names and correct sources survive.
- Restore a backup containing the previous Swedish v0.2 integration; verify migration to `se_food` while maintaining existing entity registry IDs and recordings.
- Unload and delete one entry, confirm the other configured sources and `get_notices` action still work; then uninstall custom integration and check no unexpected persistent registrations.

## HACS/Marketplace installation, update and rollback

HACS validation alone is not a substitute for actual installation:

1. When a reviewed prerelease is ready, add the custom repository `JonasHedberg/recall-watch` as an Integration in HACS/Marketplace.
2. Install from that exact prerelease, restart, verify configuration. Record displayed version and status.
3. Upgrade from the old beta on a backup/sandbox; verify source migration, options and entities.
4. Roll back to the backed-up version, repeat setup/unload, and document whether recovery restores all entity IDs.
5. Uninstall and reinstall cleanly. Verify the six source adapters again.

## Acceptance evidence

Record HA version, Python version, tested commit, English and Swedish screenshots, service response and logs (after removing private data), plus direct links to publisher notices. Store the evidence outside the repository if it contains sensitive information; provide only sanitized URLs in the acceptance file.

The human maintainer must independently verify publisher reuse requirements, the notice matching accuracy, and all required checks, then update `docs/release-evidence.json` and run:

```sh
python scripts/verify_release_evidence.py
```

Do not publish from a GitHub green check alone.
