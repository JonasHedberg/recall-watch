# Release checklist — Marketplace-only v0.4.0b2

**Status: BLOCKED until remaining real-world/manual acceptance.** The published `v0.4.0b1` release contains older code and must not be retagged or presented as the current candidate.

## Completed (7 November 2026)

- [x] Home Assistant 2026.11.0 is the required minimum version in Marketplace metadata.
- [x] Mandatory Marketplace `hacs.json` metadata is present; only the official Marketplace distribution is documented.
- [x] **98 offline tests on Python 3.13 and 98 on 3.14** pass in [Actions run 42362105080](https://github.com/JonasHedberg/recall-watch/actions/runs/42362105080).
- [x] **6 native HA 2026.11 integration tests** pass with the official first-party test harness.
- [x] Marketplace structural validation and Home Assistant hassfest pass.
- [x] All six curated public-source HTTP feeds successfully fetched and parsed in the latest bounded live probe.
- [x] English/Swedish translation-key parity and risk labels checked automatically.
- [x] EU source selection and pagination, US update sorting, complete bounded stream reads, refusal of unapproved redirects and source isolation regression-tested.
- [x] Live-derived Canadian flammability and fall/entrapment hazard recognition added.
- [x] Independent spot-checks of ten publisher notices and provisional publisher reuse research recorded.

## Must be completed before public release

- [ ] Verify the true Marketplace GUI workflow on a real HA 2026.11+ installation: clean install, English/Swedish screens, multiple sources, update, rollback, restart, migration and uninstall.
- [ ] Independently compare a representative, reviewer-labelled corpus against original publisher notices across six sources, including EU detail records and corrected/withdrawn notices.
- [ ] Human maintainer approves publisher reuse/attribution, rate limits and safety disclaimer; keep evidence accessible.
- [ ] Add timestamped, genuine reviewer evidence in `docs/release-evidence.json`, pass `python scripts/verify_release_evidence.py` and independently review signoff.
- [ ] Replace any obsolete required status check with **Marketplace repository validation** under GitHub's protected-`main` rule. Keep offline tests and hassfest mandatory.
- [ ] Change the existing `v0.4.0b1` GitHub Release to **pre-release** (or withdraw it) without rewriting history.
- [ ] Review final CI on the exact merge candidate, publish a **new** `v0.4.0b2` GitHub **pre-release**, and test its published-version installation through Marketplace.

See [QA report](QA_REPORT.md), [release acceptance](RELEASE_ACCEPTANCE.md), [manual Marketplace acceptance](MANUAL_HA_ACCEPTANCE.md), [source reuse](SOURCE_REUSE_REVIEW.md), and [original notice spot-checks](AUTHORITY_SAMPLE_AUDIT.md).

An empty or failed upstream feed is **not proof that any product is safe**.
