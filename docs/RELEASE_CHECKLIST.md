**Release gate:** Run `python scripts/verify_release_evidence.py`; it fails until all live-source, real-HA and human acceptance evidence exists. See [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md).

# Release checklist — Recall Watch v0.4.0b1

Status: **not release approved**.

- [x] Add EU Safety Gate official weekly XML source to curated registry.
- [x] Parse weekly-report index and report details using defusedxml and bounded reads.
- [x] Offline safety tests and source-isolation regression tests (77/77 passing on development environment).
- [x] Update README and changelog for new EU source.
- [ ] Live-fetch the official EU XML index and report details.
- [ ] Verify real product, hazard, date, and original-link extraction against the Commission portal.
- [ ] Validate all other live sources.
- [ ] Run tests on supported Home Assistant runtime.
- [ ] Pass GitHub Actions CI, hassfest, HACS validation.
- [ ] Review European Commission Safety Gate reuse and attribution terms.
- [ ] Manual smoke tests for multilingual UI, setup, reload, error handling and migration.
- [ ] Approve release and create version tag only after all preceding gates pass.

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
