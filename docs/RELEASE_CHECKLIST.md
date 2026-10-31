# Release checklist — next public beta candidate

**NOT RELEASE APPROVED.** Do not reuse/overwrite the existing public `v0.4.0b1` tag. Run `python scripts/verify_release_evidence.py` only after attaching genuine, recent evidence and completing [Release acceptance](RELEASE_ACCEPTANCE.md).

## Implemented and tested in PR #12

- [x] EU Safety Gate index/report support with fixed government endpoints, bounded `defusedxml` parsing and country-specific source isolation.
- [x] EU action selector and full possible weekly-report pagination; regression tests.
- [x] Complete bounded HTTP stream reads, including chunked responses; regression tests.
- [x] CPSC update-aware ordering, preserving original recall date; regression tests.
- [x] Conservative product/risk extraction improvements based on inspected live examples; regression tests.
- [x] 92 offline tests on each of Python 3.13 and 3.14 (2026-10-31).
- [x] 2 genuine Home Assistant 2026.10.4 framework tests for setup/config/action/unload (2026-10-31).
- [x] Passing HACS and Home Assistant hassfest validators (2026-10-31).
- [x] Six publisher endpoints successfully fetched and parsed by a bounded live CI probe (2026-10-31).
- [x] English and Swedish locale key parity; translated actual frontend remains unchecked.
- [x] Preliminary publisher reuse research recorded in [Source reuse review](SOURCE_REUSE_REVIEW.md).

## Must be completed before releasing

- [ ] Complete original-notice accuracy comparison for each country, including risks and incomplete summary cases.
- [ ] Test all six sources in an actual Home Assistant installation, user-facing English and Swedish UI, migration, restart, reconfiguration, outage and stale-state recovery.
- [ ] Confirm HACS/Marketplace install/upgrade/uninstall from the proposed release.
- [ ] Confirm the publisher's specific reuse terms, logo/trademark rights, licence/attribution and responsible polling with a human maintainer.
- [ ] Reclassify or withdraw prior published `v0.4.0b1` as an unapproved beta; do not modify an existing tag's history.
- [ ] Human review and timestamped release evidence linked to GitHub artifacts/source comparisons.
- [ ] Run `python scripts/verify_release_evidence.py` successfully and manually review the evidence; check CI at the final exact commit.
- [ ] Mark the next beta GitHub Release as prerelease and smoke-test its fresh installation.

See [Live test matrix](LIVE_TEST_MATRIX.md) and [QA report](QA_REPORT.md). A recall-monitoring tool must never claim that absent notifications establish product safety.
