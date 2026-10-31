# Recall Watch data sources

**Status:** candidate adapter implementation only. URLs and publishing formats were checked against published documentation on 24 October 2026, but actual payloads from the six sources have **not** been validated live inside Home Assistant. Source adapters are not certified or endorsed by the publishers.

| ID | Country | Intended coverage | Exact official endpoint |
|---|---|---|---|
| `eu_safety_gate` | European Commission / EU and EEA (EU) | Dangerous **non-food** product alerts, last two weekly reports | `https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/list/xml/en` + fixed report detail URLs |
| `se_food` | Sweden (SE) | Food recalls by Livsmedelsverket | `https://www.livsmedelsverket.se/rss/rss-aterkallanden` |
| `ca_food` | Canada (CA) | CFIA-related food recalls | `https://recalls-rappels.canada.ca/en/feed/cfia-alerts-recalls` |
| `ca_consumer` | Canada (CA) | Consumer products | `https://recalls-rappels.canada.ca/en/feed/consumer-products-alerts-recalls` |
| `uk_consumer` | United Kingdom (GB) | GOV.UK OPSS product recall filter | `https://www.gov.uk/product-safety-alerts-reports-recalls.atom?product_alert_type%5B%5D=product-recall` |
| `us_consumer` | United States (US) | CPSC consumer product recalls, last 90 days of updates | `https://www.saferproducts.gov/restwebservices/Recall?format=json` with `LastPublishDateStart=YYYY-MM-DD` query parameter |

Official XML index: https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/list/xml/en

The adapter fetches the two newest weekly reports using validated numeric IDs and a fixed Commission endpoint; it does not follow arbitrary URLs. Each report's structured metadata is normalized to Home Assistant product, brand, hazard and batch fields where available. Missing data remains unknown.

**Safety limitations:** Safety Gate publishes alerts about dangerous non-food products, which are **not necessarily product recalls**. Not every product was sold in every EU country. The two-week window is not an exhaustive history, and it is not real-time alerting.

Attribution: Alerts from the Rapid Alert System for dangerous non-food products, published free of charge on the Safety Gate website (https://ec.europa.eu/safety-gate-alerts) © European Union, 2005 – 2026.

The integration is independent of the European Commission. Live XML response schemas, Home Assistant compatibility, HACS/hassfest and source terms must be verified **before publishing a release**.

### EU Safety Gate details and limitations

The EU's [Safety Gate data catalogue](https://data.europa.eu/data/datasets/rapex-rapid-alert-system-non-food?locale=en) describes an official XML distribution of weekly reports for dangerous non-food products. The integration reads the report index and fetches **only the two latest weekly reports** through fixed official HTTPS endpoints. It never follows report URLs from arbitrary hosts. Report dates are publication dates, not dates that a household bought a product. The publisher covers EU/EEA alerts; the code's `EU` source ID does **not** mean every listed item was sold in every EU country. Alerts include bans, withdrawals and other enforcement actions, not just consumer recalls. Older weeks, corrections, withdrawn notices and food-safety notifications may be missing from the current snapshot.

Re-use attribution: **Alerts from the Rapid Alert System for dangerous non-food products, published free of charge on the Safety Gate website (https://ec.europa.eu/safety-gate-alerts) © European Union, 2005 – 2026.** This is a third-party derivative presentation, not endorsed by the European Commission. Check the official [Safety Gate portal](https://ec.europa.eu/safety-gate-alerts/) and its legal notice for up-to-date details.

**Release gate:** Actual XML responses and live HA runtime remain unverified in this environment, which cannot reach the European Commission endpoint directly. Published XML formats could change. EU support is implemented as an **unreleased beta candidate**; no public release should be tagged until live tests are documented.

### Why not include US FDA food reports?

The authority's jurisdiction is not a statement of every affected sales market. No recall feed is exhaustive.