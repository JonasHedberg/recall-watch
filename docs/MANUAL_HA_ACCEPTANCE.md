# Real Home Assistant Marketplace acceptance (English + Swedish)

**Status: requires human execution in a genuine Home Assistant environment.** Automated Home Assistant 2026.11 tests exercise the runtime with synthetic notices; they do not verify actual frontend display or Marketplace installation.

## Requirements

- Dedicated test Home Assistant **2026.11.0 or later** with Marketplace available under *Settings → Marketplace*.
- GitHub connection for adding a custom repository from a link, real Internet access to every supported authority, and access to application logs.
- A backup of the test configuration and any existing Recall Watch installation.
- The exact reviewed candidate commit and a **published pre-release** to test installation and update paths. Never claim a prior published tag contains unreleased code.

## Marketplace installation and setup

1. Once the candidate is reviewed and published as a **GitHub pre-release**, open **Settings → Marketplace**, accept its security warning, choose **Add from link** and enter `https://github.com/JonasHedberg/recall-watch`. Connect GitHub if prompted.
2. Under **Settings → Devices & services → Marketplace**, enable the repository's disabled-by-default **Pre-release** entity and turn on its switch. Select the exact candidate version `v0.4.0b2` in Marketplace. Record the displayed version and any repair/restart request.
3. Install and select Recall Watch under **Settings → Devices & services**.
4. Add **all six** independently configured source entries. Confirm six sensor entities per entry, stable entity IDs, correct source names and original authority links.
5. Observe fresh data after setup; verify that EU Safety Gate alerts are not described as guaranteed recalls. The publisher may return HTTP 500; this should produce unavailable entities/clear diagnostics, never a misleading empty safe state.

## English and Swedish language acceptance

Repeat using a user with language **English** and **Svenska**:

- Check configuration titles, source dropdown, keyword validation errors, options flow, translated sensor names, unknown values and readable mobile screens.
- Verify risk translations for `allergen`, `chemical`, `foreign_object`, `fire`, `burn`, `fall`, `entrapment`, `flammability` and `multiple`.
- Confirm that an English-language source does not receive invented Swedish translations of publisher notice content.

## Data, reliability and migration

- Run `recall_watch.get_notices` for every source, compare source IDs, order, pagination and links. Without `source`, the action must reject ambiguous multi-source requests.
- Update keywords and verify the count changes without affecting other source entries.
- Interrupt network access, trigger refresh, verify sensors become unavailable and preserve cached last-successful results without incorrectly reporting zero notices; restore network and verify recovery.
- Restart and verify all sources and entity registry IDs.
- Upgrade an existing beta in an isolated copy of Home Assistant; restore a backup of the legacy Swedish v0.2 config and verify migration, history and source selection.
- Test **Marketplace uninstall, reinstall, version rollback and update** in the test system.

## Evidence and release decision

Capture Home Assistant version, git commit and release tag, English/Swedish screenshots, redacted logs, version selection, update/uninstall results and sample publisher article comparisons. Provide HTTPS links to immutable, sanitized evidence in `docs/release-evidence.json`; do not upload personal Home Assistant configuration.

The human maintainer must also review actual publisher terms, rate limits and original-notice accuracy across every source. Finally run:

```sh
python scripts/verify_release_evidence.py
```

A successful test in Python alone does not constitute a signed user-installation review.
