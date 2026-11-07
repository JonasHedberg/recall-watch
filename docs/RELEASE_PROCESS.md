# Maintainer release process — Home Assistant Marketplace

Recall Watch is a **third-party Marketplace integration**, not a bundled Core integration. A GitHub repository, a published GitHub version and catalog inclusion are separate stages.

## Before publishing

1. Confirm Home Assistant **2026.11.0 or later** compatibility and Marketplace structure: `python scripts/validate_marketplace.py`. The file `hacs.json` must remain in the repository root because the Marketplace requires that specific filename.
2. Run offline tests, first-party Home Assistant 2026.11 native tests, hassfest and live authority probes in CI. Treat any failed source as a release blocker, not as zero notices or a safe-state signal.
3. Follow [Manual Marketplace acceptance](MANUAL_HA_ACCEPTANCE.md) in a real Home Assistant 2026.11 installation and capture actual English/Swedish screenshots and install/update/rollback/uninstall results.
4. Compare representative notices from all six publishers with original records, including dates, case IDs, alerts versus recalls, affected markets, models, batches and withdrawn/corrected notices.
5. Review publisher licence, attribution and request-rate obligations; record a named, dated maintainer approval.
6. Complete the [release acceptance](RELEASE_ACCEPTANCE.md) file `docs/release-evidence.json`; `python scripts/verify_release_evidence.py --expected-commit <SHA>` must pass with `reviewed_commit` equal to the exact accepted revision. The optional manual **Release preflight** GitHub Actions workflow also checks that SHA; do not fabricate acceptance.
7. Confirm all applicable GitHub branch status checks are green at the exact accepted commit and no critical open security findings remain.

## Release versioning

- The integration manifest has an unprefixed version such as `0.4.0b2`; publish it under the matching `v0.4.0b2` annotated Git tag.
- Do not rewrite or reuse the older `v0.4.0b1` tag. The owner should correct that release's **pre-release** classification.
- Prepare English release notes and changelog; for beta versions select **Set as a pre-release** in GitHub Releases.
- The Marketplace uses GitHub's release archive for installing repositories. There is no requirement to attach an additional custom ZIP; keep the standard `custom_components/recall_watch` layout.
- After publishing, verify **fresh Marketplace installation from the actual tag**, then use the Marketplace update, rollback and removal flows. A successful package check is not sufficient.

```sh
# Only after human acceptance
git tag -a v0.4.0b2 -m "Recall Watch v0.4.0b2"
git push origin v0.4.0b2
```

## Optional catalog listing

A custom repository can be used via **Settings → Marketplace → Add from link** without catalog acceptance. Inclusion in the shared catalog is a separate review and is not needed for a beta release. Do not claim official Home Assistant Core status.

## Rollback

Back up Home Assistant settings before updates. Use the Marketplace's version selector to install a known-good version or restore the full test backup. Verify config entries, sensors, entity IDs and the `get_notices` action after restart.
