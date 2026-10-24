# Changelog

All notable user-visible changes are documented here. Version numbers in this repository describe **unreleased candidate code**, not published GitHub releases.

## 0.3.0b1 — Unreleased international beta candidate (2026-10-24)

- Added fixed-source adapters for Canada (food and consumer products), GOV.UK/OPSS product recalls (Atom), and US CPSC consumer products (JSON API), retaining the Swedish Food Agency source.
- Added independent configuration entries, coordinator state, keyword filters and six sensors per source.
- Added `source` field and strict source separation for the `recall_watch.get_notices` action; omit source only if exactly one source is configured.
- Preserved existing Swedish config entries with explicit v1→v2 migration; preserved entry-based entity unique IDs.
- Added source/country/category metadata to serializations and increased the hazard vocabulary for international products.
- Restricted CPSC data retrieval to a rolling 90-day update window; no full historic data load.
- Removed the HACS country-specific metadata, since the integration now supports multiple jurisdictions.
- Updated English documentation, maintained Swedish UI translations and added international source tests.
- **Still blocked:** real runtime testing, live feed/API data contracts, HACS/hassfest, owner configuration and release approval.

## 0.2.0b1 — Earlier Swedish beta candidate

- Added conservative product, brand, risk, batch and best-before extraction, new sensors, bounded previews and paginated action responses.

## 0.1.0b1 — Initial Swedish beta candidate

- Added basic Swedish RSS client, config/option flows, count sensor and localizations.
