# Source reuse and attribution review — 2026-10-31

**Status: preliminary legal/documentation research, NOT final publisher or legal approval.** Recall Watch reads already-public notices from public authorities. The source's jurisdiction is not equivalent to a list of affected consumer markets. No alert is a confirmed match for a user's product or batch.

## Publisher evidence

| Source | Official source and reuse documentation | Attribution / caveat |
|---|---|---|
| EU Safety Gate | https://ec.europa.eu/safety-gate-alerts/ ; https://data.europa.eu/en/copyright-notice | Safety Gate notices may include withdrawals, bans and other safety alerts, not exclusively consumer recalls. Existing data source documentation contains EU attribution; check the **specific Safety Gate portal's legal notice** and downstream rights, not only data.europa.eu's general editorial-content notice. |
| Sweden, Livsmedelsverket | https://www.livsmedelsverket.se/om-oss/press/rss/ | Livsmedelsverket publishes official RSS subscription feeds; confirm the precise reuse terms for redistribution of notice text. Link directly to each original notice. |
| Canada, food and consumer | https://recalls-rappels.canada.ca/en/rss-feeds ; https://open.canada.ca/data/en/dataset/d38de914-c94c-429b-8ab1-8776c31643e3 | Canada's open recalls and safety alerts **dataset** is licensed under Open Government Licence – Canada. Confirm applicability to the RSS feed content and satisfy required source attribution. |
| GOV.UK, OPSS | https://www.gov.uk/help/reuse-govuk-content | GOV.UK content normally requires compliance with the Open Government Licence. Use original GOV.UK notice links; confirm third-party materials or exceptions. |
| USA, CPSC recalls API | https://www.cpsc.gov/Recalls/CPSC-Recalls-Application-Program-Interface-API-Information ; https://catalog.data.gov/dataset/recalls-api | The CPSC recalls API is public; data.gov lists a US public-domain designation. US federal public-domain content and trademarks/third-party items may have different restrictions; preserve original CPSC links. |

## Suggested user-facing source acknowledgement

> Recall Watch displays data derived from government-issued recall notices. Source agencies include Livsmedelsverket (Sweden), the European Commission's Safety Gate (EU), Government of Canada, GOV.UK / Office for Product Safety and Standards (UK), and the US Consumer Product Safety Commission. Recall Watch is independent of and not endorsed by these authorities. Always consult the original authority notice for complete product, model, batch and location details.

For EU Safety Gate, retain the attribution from [DATA_SOURCES.md](DATA_SOURCES.md) when presenting derived alert data. No live-data sample may be presented as proof that no dangerous products remain in a market.

## Outstanding maintainer actions

- [ ] Verify the specific publisher licences and attribution terms on each original authority site.
- [ ] Review request frequency (currently once per configured source every six hours), caching and any rate-limit requirements.
- [ ] Confirm redistribution of text excerpts, dates, model names, metadata, icons, trademarks and photos does not violate third-party rights. Do **not** reproduce photos without confirmed rights.
- [ ] Record a dated, named human review in the release evidence file.
- [ ] Confirm service UI, readme, release notes and user documentation contain an accessible disclaimer and links to authoritative notices.

This document is a review aid; it is not legal advice or a release sign-off.
