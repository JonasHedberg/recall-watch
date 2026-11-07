# Changelog

All notable changes to Recall Watch are recorded here. Version numbers in the manifest describe the source version; a GitHub release is published separately after formal acceptance.

## [0.4.0b2] — Release candidate, not published (2026-11-07)

### Fixed
- Fully consume bounded HTTP responses rather than parsing incomplete chunks.
- Reject redirects to unexpected hosts; preserve endpoint/size limits.
- Restore EU Safety Gate as a selectable source in `recall_watch.get_notices`.
- Support complete bounded two-week EU Safety Gate pagination (offset up to 500).
- Order CPSC recall notices by their last publication/update date while preserving the original recall date.
- Improve conservative product and hazard recognition from Swedish, Canadian, UK and US notices, including explicit fall, entrapment and flammability risks with English and Swedish translations.
- Reject populated RSS, Atom and CPSC feeds that yield no usable notices, instead of reporting a misleading empty feed.
- Reject malformed publisher links, including invalid URL authorities, credential-bearing links and invalid ports, without interrupting valid records.
- Replace legacy installation acceptance requirements with explicit Marketplace installation, upgrade, rollback and removal checks.
- Avoid duplicate PR/push CI runs and require offline tests for the overall hassfest gate.

### Validation
- Test cases for client, translations and six Home Assistant runtime fixtures.
- Test live public-source parsers for EU, Sweden, Canada, UK and US in CI.
- Run Python 3.13/3.14 offline coverage and native Home Assistant 2026.11.0 tests; require Marketplace repository validation.
- Implement a fail-closed release-evidence checklist; retain unresolved real installation and publisher-accuracy checks.

**Release caveat:** This is a proposed beta, not a verified safety service. A keyword match is not a confirmed product/batch match; lack of an alert does not establish safety. No public release is authorized until the acceptance checklist is signed.

## [0.4.0b1] — Published on GitHub (2026-10-24)

- Initial EU Safety Gate two-weekly-report dangerous non-food alert support.
- Multi-region sources introduced as a beta (EU, SE, Canada, UK and US).
- This beta was published as a regular GitHub release by mistake; its metadata must be changed to pre-release or explicitly withdrawn. Never rewrite its published tag.

## [0.3.0b1] — Historical development candidate

- Canadian food/consumer sources, GOV.UK Atom feed and US CPSC API.
- Multi-source config entries, six per-source sensors, keyword filters and action source selection.
- Version 1 to version 2 Swedish configuration migration.

## [0.2.0b1] — Historical development candidate

- Conservative product, brand, risk, batch and best-before extraction, plus preview sensors and response-only notices.

## [0.1.0b1] — Historical development candidate

- Swedish Food Agency RSS client, configuration flow and count sensor with English and Swedish localization.
