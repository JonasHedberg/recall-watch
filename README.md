# Recall Watch — international recall monitoring for Home Assistant

> **Status: pre-release development.** The international v0.3.0b1 source package has been prepared offline, but this repository is **not yet a complete installable integration**. Do not add it to HACS until the complete `custom_components/recall_watch` folder has been committed and tested.

Recall Watch is a community-developed Home Assistant integration intended to surface official product-recall notices as Home Assistant sensors. It is not an official Home Assistant Core integration, government service, or safety-critical alerting system.

## Planned supported data sources

| Region | Source | Type | Status |
| --- | --- | --- | --- |
| Sweden | Swedish Food Agency (Livsmedelsverket) | Food | Adapter implemented offline; live validation pending |
| Canada | Canadian Food Inspection Agency / Government of Canada | Food | Adapter implemented offline; live validation pending |
| Canada | Government of Canada | Consumer products | Adapter implemented offline; live validation pending |
| United Kingdom | GOV.UK / OPSS | Consumer products | Adapter implemented offline; live validation pending |
| United States | CPSC | Consumer products | Adapter implemented offline; live validation pending |

**This is not complete worldwide coverage.** EU Safety Gate, RASFF, FDA food recalls, and other jurisdictions are not integrated. A source's country does not establish which countries a recalled product may have been sold in.

## Intended functionality

- Each selected source has independent Home Assistant configuration and keyword filters.
- Read-only data fetching from curated fixed HTTPS government endpoints, without third-party Recall Watch accounts.
- Six-hour polling and per-source sensors for number of matched notices, latest product, brand, hazard, batch, and best-before date.
- Response-only `recall_watch.get_notices` action for paging through cached notices.
- English interface with Swedish translation, designed for additional languages.
- Conservative text extraction: missing details remain unknown.

## Critical safety limitations

**A keyword match is not a verified product match. A notice count of zero does not mean your products are safe.** Authorities may omit historical information, update notices, or publish incomplete descriptions; product, batch, or risk fields may be inaccurate when derived from natural language. Always consult the original issuing authority before taking action.

## Installation

**Not available yet through this repository.** Installation instructions will be enabled after the full implementation, tests, and `hacs.json` are committed and CI checks pass. Do not publish a GitHub release or request HACS directory listing while this banner remains.

## Development, contributions and license

The target integration domain is `recall_watch`; version under development: `0.3.0b1`.

Read the repository's future CONTRIBUTING, SECURITY, and technical documentation files before submitting a change. The repository currently uses the MIT license. Product-safety notices are third-party information; Recall Watch is not endorsed by Home Assistant or the issuing agencies.

Project owner: [@JonasHedberg](https://github.com/JonasHedberg).
