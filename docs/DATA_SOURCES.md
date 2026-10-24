# Recall Watch data sources

## EU Safety Gate — dangerous non-food products (beta)

ID: `eu_safety_gate`; jurisdiction: EU/EEA; category: consumer; official publisher: European Commission.

Official XML index: https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/list/xml/en

The adapter fetches the two newest weekly reports using validated numeric IDs and a fixed Commission endpoint; it does not follow arbitrary URLs. Each report's structured metadata is normalized to Home Assistant product, brand, hazard and batch fields where available. Missing data remains unknown.

**Safety limitations:** Safety Gate publishes alerts about dangerous non-food products, which are **not necessarily product recalls**. Not every product was sold in every EU country. The two-week window is not an exhaustive history, and it is not real-time alerting.

Attribution: Alerts from the Rapid Alert System for dangerous non-food products, published free of charge on the Safety Gate website (https://ec.europa.eu/safety-gate-alerts) © European Union, 2005 – 2026.

The integration is independent of the European Commission. Live XML response schemas, Home Assistant compatibility, HACS/hassfest and source terms must be verified **before publishing a release**.

## Other sources

- `se_food`: Livsmedelsverket RSS (Sweden).
- `ca_food`: Government of Canada / CFIA food RSS.
- `ca_consumer`: Government of Canada consumer products RSS.
- `uk_consumer`: GOV.UK OPSS Atom.
- `us_consumer`: CPSC JSON, 90-day last-published window.

The authority's jurisdiction is not a statement of every affected sales market. No recall feed is exhaustive.