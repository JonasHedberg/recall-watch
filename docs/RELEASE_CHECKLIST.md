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

EU Safety Gate contains **dangerous non-food product alerts**, not exclusively recalled goods. The latest two weekly reports are not comprehensive historical coverage.