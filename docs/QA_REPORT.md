# Quality assurance report — Release-readiness candidate (2026-10-31)

**Candidate source:** `release-readiness-2026-10-31` / [draft PR #12](https://github.com/JonasHedberg/recall-watch/pull/12). **NOT RELEASE-APPROVED.** Existing published `v0.4.0b1` is an earlier unapproved beta; this PR does not change that tag.

## Verified in GitHub Actions

| Verification | Recorded result | Limits |
|---|---|---|
| Offline automated tests on Python 3.13 | **92 passed** | Synthetic fixtures and mocked component lifecycle, not a full HA installation |
| Offline automated tests on Python 3.14 | **92 passed** | Same scope as above |
| Real Home Assistant 2026.10.4 test API smoke | **2 passed** | Real integration framework; synthetic authority data; setup/unload, sensors/action and config flow checks |
| HACS validator | Passed | Packaging and HACS consistency, not install/upgrade acceptance |
| Home Assistant hassfest | Passed | Static metadata and schema validation |
| Six live authority probes | **6/6 sources parsed** | Successful bounded HTTP reads and parsing, not accuracy/completeness certification |
| Strict response-size bounds | 2 MiB per network response | Hard limit, not a completeness guarantee |
| Release acceptance evidence | **BLOCKED** | A dated human acceptance record has not been supplied |

Reference: [GitHub Actions run 41184630659](https://github.com/JonasHedberg/recall-watch/actions/runs/41184630659), 31 October 2026; updated document review does not replace re-running the checks on the final exact commit.

## Live source sample (2026-10-31)

| Source | Parsed notices | Example metadata checked by parser |
|---|---:|---|
| EU Safety Gate | 157 | Report/alert ID, alert URL, product, risk and report date |
| Swedish Food Agency | 2 | Recall headline, source link, product and risk |
| Canadian food | 3 | Food/allergen headline, product and publisher ID |
| Canadian consumer | 3 | Consumer product headline and hazard terms |
| United Kingdom | 50 | GOV.UK Atom publication date, title and product |
| US CPSC | 191 | Recall/update dates, structured product and original link |

All source counts reflect a *limited current response*, never all active notices or all markets. Sources can be incomplete; an empty result is never proof of a product's safety. Live probes retain two bounded example records per source in the CI artifact for manual comparison.

## Changes reviewed

- Corrected `aiohttp` stream reading to EOF with 2 MiB cap and tests for split reads.
- EU selector source registry parity and pagination up to 500.
- US CPSC last-update ordering with original recall date retained.
- Conservative Swedish/English headlines and allergen/hazard recognition; unknown brands remain unknown.
- English and Swedish JSON locale keys present and parity-checked.
- Fail-closed evidence checker and source licence/attribution research.

## NOT verified / mandatory before public release

- [ ] Real Home Assistant installed on user hardware/VM: six sources, options/reload, timeouts/outages/recovery, migration, recorder behavior and restart.
- [ ] Manual English and Swedish actual frontend UI review, plus HACS/Marketplace install, upgrade, backup and uninstall.
- [ ] Representative human-labeled notices from **all six sources** compared to original authority product/brand, date, batch, hazard, case ID and jurisdiction, including withdrawn/corrected notices.
- [ ] Publisher-specific reuse, attribution and rate-limit review signed by a human maintainer.
- [ ] Human review of accepted version and release notes, including correct prerelease classification of `v0.4.0b1`.
- [ ] `docs/release-evidence.json` with dated evidence links and all gates completed, passing `python scripts/verify_release_evidence.py`.
- [ ] Review final exact revision CI after PR changes and verify published release via clean installation.

No client-wide statement coverage was measured for this exact PR; earlier coverage figures from `2026-10-24` must not be cited for the new code.

See [Release acceptance](RELEASE_ACCEPTANCE.md), [live acceptance matrix](LIVE_TEST_MATRIX.md), [source reuse research](SOURCE_REUSE_REVIEW.md), and [issue #1](https://github.com/JonasHedberg/recall-watch/issues/1).
