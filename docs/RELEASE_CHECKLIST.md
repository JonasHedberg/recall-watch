# Release checklist — all gates are mandatory

- [x] Implement best-effort structured extraction with unknown values and explicit no-safety-guarantee documentation.
- [x] Unit test empty, positive, negated, multi-risk, malformed-date and overly long/batched input cases.
- [x] Test bounded JSON serialization and paginated results offline.
- [x] Preserve the matching count sensor's unique identifier and the existing options flow.
- [ ] Assign a real human maintainer; run `python scripts/configure_repository.py --owner YOUR_GITHUB_OWNER` and verify repository metadata.
- [ ] Create a **public** GitHub repository with the required description, topics and Issues; enable secure vulnerability reporting.
- [ ] Review [GitHub setup](GITHUB_SETUP.md), [release process](RELEASE_PROCESS.md) and [repository metadata](REPOSITORY_METADATA.md).
- [ ] Verify the real feed returns correct RSS/Atom in a Home Assistant instance, including malformed/blocked responses and rate limits.
- [ ] Perform a manually labeled extraction accuracy evaluation on real feed samples; document false positives and false negatives and adjust the patterns.
- [ ] Run full integration tests (config, options, sensors, translation, service action, failure/recovery, reload/unload) under a supported Home Assistant + Python runtime.
- [ ] Verify Home Assistant's sensor names, risk enum translations, correct `unknown` state and state/attribute size limits in the UI.
- [ ] Pass `hassfest`, the HACS Marketplace validator, `python scripts/validate_repository.py` and configured GitHub CI with zero errors.
- [ ] Complete any required Home Assistant brand registration/review in `home-assistant/brands`.
- [ ] Review source data licensing, robot/fetch policy, request rate, security and dependency provenance.
- [ ] Install, update and remove the package from the target HACS/Marketplace version, and test recovery from restart.
- [ ] Run `python scripts/pre_release_check.py` without release-blocking findings.
- [ ] Verify artifact contents exclude caches, `.coverage`, secrets and test-only artifacts; synchronize manifest version and Git tag.
- [ ] Publish release notes and mark beta/stable appropriately only after approval.

**Status: UNRELEASED.** Passing the offline client tests does not satisfy the HA runtime, feed, manual accuracy, or publishing requirements.

## Additional global beta release gates (0.4.0b1)

- [ ] Verify **each of all six** official source endpoints and real response shapes, error conditions, terms of service, attribution and update cadence.
- [ ] Test CPSC 90-day `LastPublishDateStart` filtering against a real upstream response; confirm payload size and no silent pagination/truncation.
- [ ] Verify UK and Canada feeds remain stable and meet the configured 2 MB response limit.
- [ ] Verify multiple sources installed together, individually configured, reloaded and removed without cross-source leakage.
- [ ] Confirm the v0.2 Swedish configuration migrates safely to `se_food`, including preserving entity unique IDs.
- [ ] Inspect Swedish/English translations, country labels, and original-language notice semantics in a real HA UI.
- [ ] Verify HACS multi-country listing behavior after removing `country: SE` from `hacs.json`.
- [ ] Publish only after signing off on [data-source status](DATA_SOURCES.md); do **not** claim exhaustive EU/worldwide coverage.

- [ ] Complete the manual [live-test matrix](LIVE_TEST_MATRIX.md) and [migration guide](MIGRATION.md).

- [ ] Live-test the European Commission weekly XML index and two detail reports; confirm IDs, dates, official hyperlinks, CDATA text, response sizes, schema, safety and attribution.
- [ ] Distinguish EU dangerous-product alerts from actual consumer recalls in the UI and documentation.
