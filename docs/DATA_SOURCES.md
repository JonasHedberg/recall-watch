# Data sources and geographical coverage

**Status:** candidate adapter implementation only. URLs and publishing formats were checked against published documentation on 24 October 2026, but actual payloads from the five sources have **not** been validated live inside Home Assistant. Source adapters are not certified or endorsed by the publishers.

| ID | Country | Intended coverage | Exact official endpoint |
|---|---|---|---|
| `se_food` | Sweden (SE) | Food recalls by Livsmedelsverket | `https://www.livsmedelsverket.se/rss/rss-aterkallanden` |
| `ca_food` | Canada (CA) | CFIA-related food recalls | `https://recalls-rappels.canada.ca/en/feed/cfia-alerts-recalls` |
| `ca_consumer` | Canada (CA) | Consumer products | `https://recalls-rappels.canada.ca/en/feed/consumer-products-alerts-recalls` |
| `uk_consumer` | United Kingdom (GB) | GOV.UK OPSS product recall filter | `https://www.gov.uk/product-safety-alerts-reports-recalls.atom?product_alert_type%5B%5D=product-recall` |
| `us_consumer` | United States (US) | CPSC consumer product recalls, last 90 days of updates | `https://www.saferproducts.gov/restwebservices/Recall?format=json` with `LastPublishDateStart=YYYY-MM-DD` query parameter |

### Source evidence

- Sweden: [Swedish Food Agency RSS subscription page](https://www.livsmedelsverket.se/om-oss/press/rss/).
- Canada: [Canadian recall RSS index](https://recalls-rappels.canada.ca/en/rss-feeds), listing separate food and consumer product feeds.
- UK: [GOV.UK OPSS product safety recalls](https://www.gov.uk/product-safety-alerts-reports-recalls?product_alert_type%5B%5D=product-recall), including a filtered Atom subscription.
- US: [CPSC API reference](https://www.cpsc.gov/Recalls/CPSC-Recalls-Application-Program-Interface-API-Information), supporting JSON recall records, and [CPSC date filtering](https://learn.microsoft.com/en-us/connectors/cpscrecallsretrievalip/).

### Data semantics

The country code represents the authority's jurisdiction. It is **not** a comprehensive affected-markets list; do not claim that a recall in one market applies to another without reading the original notice. Data completeness, update frequency and recall definitions are set by each source, not by Recall Watch.

CPSC explicitly supports a `LastPublishDateStart` date parameter. The client requests 90 days of last-published records to avoid downloading the API's full historic result set. There is no archive search, no stable database and no completeness claim. When the provider edits or removes a record, the current sensor values can change accordingly.

### Why not include EU-wide Safety Gate or US FDA food reports?

The EU [Safety Gate alerts portal](https://ec.europa.eu/safety-gate-alerts/) provides consumer-facing alerts, but its supported, stable public machine-access interface has not been sufficiently validated for this version. An adapter will require reproducible official examples, license/rate-limit review, and fixtures. **EU coverage is not implemented.**

The [openFDA food enforcement API](https://open.fda.gov/apis/food/enforcement/) explicitly cautions against using its enforcement dataset to issue public alerts or track recall lifecycles. It is intentionally **not used** as a recall-alert source in this release.

### Adding new countries

New endpoints must come from verifiable public authority documentation. Require an explicit and fixed HTTPS URL, a clearly stated jurisdiction, bounded parser, limits and safe fallback, provider attribution, privacy/terms review, positive and negative fixtures, owner-reviewed QA and a translated selector label. Do not scrape a site or advertise a country until its source contract is confirmed and tests run.
