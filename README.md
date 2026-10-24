# Recall Watch — International product recall monitoring for Home Assistant

> **0.4.0b1 — UNRELEASED BETA CANDIDATE. Not validated in a real Home Assistant runtime or against current production feed payloads.** This is a third-party Home Assistant integration, not an official Home Assistant Core integration, an official government service, or a substitute for checking authoritative safety notices. Do **not** publish a release until [every release gate](docs/RELEASE_CHECKLIST.md) is cleared.

Recall Watch surfaces official recall notices as Home Assistant sensors and a response-only action. Choose one or more supported country-specific sources. Each configured source is independent, with its own keyword filter, coordinator and entity set. The integration never uploads keyword lists to a Recall Watch server; queries use only fixed government endpoints.

**A keyword match is not a confirmed product/batch match. An empty result does not establish that a product is safe.** Check the original authority notice, model, batch and purchase location before taking action.

## Available official sources (beta candidate)

| Selection | Country | Category | Publisher | Transport | Scope |
|---|---|---|---|---|---|
| `eu_safety_gate` | European Union / EEA | Dangerous non-food product alerts | European Commission / Safety Gate | Official weekly XML index + report XML | Most recent two weekly reports; includes alerts other than consumer recalls |
| `se_food` | Sweden | Food | Swedish Food Agency (Livsmedelsverket) | RSS | Published Swedish food recall notices |
| `ca_food` | Canada | Food | Government of Canada / CFIA | RSS | Canadian food recall alerts |
| `ca_consumer` | Canada | Consumer products | Government of Canada | RSS | Canadian consumer-product alerts |
| `uk_consumer` | United Kingdom | Consumer products | GOV.UK / OPSS | Atom | UK product recall notices |
| `us_consumer` | United States | Consumer products | US CPSC | JSON API | Recently published/updated US CPSC recalls (90-day update window) |

Official-source references and exact fixed URLs are documented in [DATA_SOURCES.md](docs/DATA_SOURCES.md). The country identifies **where the publishing authority operates**, not every market in which a recalled product was sold. Cross-border products, imports and multinational brands require checking more than one jurisdiction.

**Not yet supported:** RASFF, US FDA food enforcement, worldwide/country-agnostic coverage, barcode inventory checking and legal classification of affected products. Safety Gate uses the published weekly XML reports; its live feed schema has not yet passed acceptance tests in a Home Assistant installation. These are **dangerous-product alerts**, not necessarily product recalls. The report-based feed is not an exhaustive, real-time view of all alerts. Never interpret “international” as “all recalls worldwide”.

## Features

- UI-based configuration: add Recall Watch once for **each selected source**; different sources can monitor different keywords.
- Six-hour coordinator polling per source; all sensors under a source share the cached data.
- Matching notice count; latest product, brand, hazard category, batch and best-before date sensors.
- Bounded five-notice preview in sensor attributes; original notice hyperlinks and source/country/category metadata.
- `recall_watch.get_notices` response-only action for paginated results from the **last successful** source fetch, with optional source choice and matching filter.
- Best-effort, deterministic extraction from source text. Unknown details remain unknown. CPSC product names are read directly from structured JSON; manufacturers are **not** inferred to be brands.
- English default messages with Swedish (`sv`) translations, designed for future locales.
- Offline unit tests, mocked integration contract tests, CI and release safety checks.

## Installation

The project source is available at [JonasHedberg/recall-watch](https://github.com/JonasHedberg/recall-watch). This is an **unreleased beta candidate**; before installing as a custom repository, review the release limitations:

1. Make a backup of your Home Assistant configuration.
2. On Home Assistant 2026.10 or earlier, in HACS add `JonasHedberg/recall-watch` as a **Custom repository → Integration**, once a tested HACS release is available. On Home Assistant 2026.11+, use the built-in **Marketplace** with its custom repository option.
3. Download/install the integration and restart Home Assistant.
4. Select **Settings → Devices & services → Add integration → Recall Watch**. Select **one** official source and optionally supply up to 20 comma-separated search phrases (maximum 64 characters each).
5. Repeat step 4 to monitor additional countries or categories. There can be only one configuration entry per source, but multiple sources can be configured.

For a test installation without HACS, copy the folder `custom_components/recall_watch/` into your HA configuration's `custom_components/` folder and restart. The root repository ZIP is not a single-click installer.

Previously installed Swedish v0.2 entries are migrated to the `se_food` source; the sensor's entry-based unique IDs are retained. **Make a backup before upgrading and verify historical entities after restart.**

See [HACS and Marketplace installation](docs/HACS_MARKETPLACE.md) and [GitHub setup](docs/GITHUB_SETUP.md).

## Sensors and example data

Each configured source creates six sensors: a matching count sensor and five sensors for the newest matching notice: latest product, brand, risk type, batch number and best-before date. The count is **the number of matched notices in the feed's current limited response**, not all historic active recalls.

```json
{
  "source": "us_consumer",
  "country": "US",
  "category": "consumer",
  "identifier": "example-not-a-real-recall",
  "title": "Example product recalled due to fire hazard",
  "product": "Example kettle",
  "brand": null,
  "risk_type": "fire",
  "batch_numbers": [],
  "best_before_dates": [],
  "url": "https://www.cpsc.gov/"
}
```

This is **synthetic example data**, not a real recall, and not a promise that all shown fields exist upstream.

### Response-only action

```yaml
action: recall_watch.get_notices
data:
  source: ca_food
  matching_only: true
  offset: 0
  limit: 20
response_variable: recall_results
```

`source` may be omitted **only when exactly one source is configured**. Providing an unknown or unconfigured source raises a Home Assistant error; notice lists are not mixed between jurisdictions. Pagination is over cached records and does not query historical archives or new remote pages.

## Languages

All code, repository documents and canonical keys are English. UI messages are shipped in `translations/en.json` and `translations/sv.json`. Source notice content remains in the original language; no automatic machine translation is performed. Additional languages can be submitted using [TRANSLATIONS.md](docs/TRANSLATIONS.md).

## Privacy, safety and limitations

- Recall Watch makes outbound HTTPS requests to the fixed publisher websites; publishers may see the requesting host's IP address. No cloud account or API key is required in this release.
- RSS feeds can omit records or remove older entries, authorities may update notices after publication, and the CPSC source intentionally limits requests to the most recently updated 90 days. Polling every six hours is **not** a real-time alert guarantee.
- Brand, batch and risk information may be missing, misleading or falsely identified in unstructured text; a product in one country does not imply availability in another.
- The EU, UK, Canadian, Swedish and US source adapters have **offline fixtures only** here; live network and runtime acceptance remain blocked in [QA_REPORT.md](docs/QA_REPORT.md).
- Recall Watch is not endorsed by Home Assistant, any public agency or government.

Read [DATA_EXTRACTION.md](docs/DATA_EXTRACTION.md), [SECURITY_AND_PRIVACY.md](docs/SECURITY_AND_PRIVACY.md) and [DATA_SOURCES.md](docs/DATA_SOURCES.md) before relying on the integration.

## Contribute and maintain

- [Contributing](CONTRIBUTING.md) · [Security reporting](SECURITY.md) · [Support](SUPPORT.md) · [Changelog](CHANGELOG.md)
- [Development](docs/DEVELOPMENT.md) · [Quality verification](docs/QA_REPORT.md) · [Release gates](docs/RELEASE_CHECKLIST.md)
- [Repository publishing](docs/GITHUB_SETUP.md) · [Roadmap](docs/ROADMAP.md)

License: [MIT](LICENSE). Copyright (c) 2026 Recall Watch contributors.
