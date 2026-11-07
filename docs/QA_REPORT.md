# Quality assurance report — Marketplace-only v0.4.0b2 candidate

**Reviewed:** 7 November 2026. **Status: code/automated verification passed; public release acceptance NOT YET complete.** Proposed source is [draft PR #16](https://github.com/JonasHedberg/recall-watch/pull/16), not the older published `v0.4.0b1`.

## Recent full CI evidence

The expanded regression suite and native Home Assistant tests passed in [Actions run 42363403658](https://github.com/JonasHedberg/recall-watch/actions/runs/42363403658). Before release, recheck all required jobs at the **final exact candidate commit**.

| Check | Result | What the result proves |
|---|---|---|
| Offline tests on Python 3.13 | **102 passed** | Isolated parsers, packaging, metadata and mocked contracts |
| Offline tests on Python 3.14 | **102 passed** | The same regression suite on the HA runtime Python |
| Home Assistant **2026.11.0** native tests | **6 passed** | Real Home Assistant APIs with synthetic authority responses |
| Marketplace repository validation | **Passed** | Metadata, branding, source structure, relative links and HA version contract |
| Home Assistant hassfest | **Passed** | Static integration metadata checks |
| Live publisher probes | **6 of 6 parsed** | Actual bounded HTTP reads and parsable data; not exhaustive coverage |

### Live source sample (7 November 2026)

| Source | Notices parsed |
|---|---:|
| European Commission Safety Gate | 130 |
| Swedish Food Agency | 1 |
| Canada food | 3 |
| Canada consumer | 3 |
| UK OPSS | 50 |
| US CPSC | 192 |

The earlier 7 November probe failed when Safety Gate returned HTTP 500. A subsequent run on the **same source code** succeeded. The intermittent upstream failure is not proof of a parser defect and is not silently converted into zero recalls. Coverage may change between polls and data sources may be unavailable; an empty result never establishes safety.

## Improvements in this candidate

- Required minimum Home Assistant **2026.11.0**; uses the built-in Marketplace distribution and the first-party Home Assistant test harness.
- Kept the mandatory Marketplace metadata filename `hacs.json` (the platform requires it); removed obsolete installation paths, validation actions and publication guides.
- Explicit risk parsing for Canadian **flammability** and **fall/entrapment**, with English and Swedish enum labels.
- Existing corrections to complete bounded HTTP reads, redirect restrictions, EU action source selection and pagination, US CPSC update sorting, options and source separation remain tested.
- Added strict evidence-version consistency for `v0.4.0b2` and explicitly replaced the legacy installation acceptance gate with Marketplace install/update/rollback/uninstall requirements.
- Populated RSS, Atom and CPSC responses with no usable records now fail closed rather than presenting misleading zero results; invalid publisher URLs are rejected without crashing valid feeds.
- Removed the obsolete no-op CI workflow and made hassfest dependent on successful offline and Marketplace validation checks.

## Remaining release acceptance

- [ ] A maintainer performs an actual **Marketplace install, upgrade, rollback and uninstall** on Home Assistant 2026.11+, and visually checks the English and Swedish interface.
- [ ] Complete representative original-notice comparisons for all six sources, including corrected/withdrawn notices and EU full alert details (ten earlier independent spot checks are a start, not representative acceptance).
- [ ] Human review of publisher-specific reuse terms, attribution and request frequency, with dated linked evidence.
- [ ] `docs/release-evidence.json` is populated with genuine evidence and passes `python scripts/verify_release_evidence.py`.
- [ ] The repository owner replaces the obsolete required branch status check with **Marketplace repository validation** in the protected `main` rule. The GitHub app connection used for this work has no administration permission to change it.
- [ ] Correct the previously published `v0.4.0b1` beta release classification in the GitHub Releases interface.
- [ ] Reverify CI at the exact accepted final commit, merge, create **v0.4.0b2** as a prerelease and test installation of that published artifact.

This is a third-party Marketplace integration, **not** an official Home Assistant Core integration or an official publisher safety service.
