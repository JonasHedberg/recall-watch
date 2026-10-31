# Source reuse and attribution research — 2026-10-31

**Status:** publisher terms independently checked, subject to final maintainer compliance review. Not legal advice, not a signed release approval. Recall Watch only reads public publisher payloads through fixed endpoints and links to the original notices. Agency-issued alerts are not confirmed household product/batch matches.

| Source | Publisher's reuse statement | Application-specific compliance |
|---|---|---|
| Sweden: Livsmedelsverket | https://www.livsmedelsverket.se/om-oss/om-webbplatsen/far-man-anvanda-text-bild/ | Material can be reused with conditions: do not distort or mislead; copied passages must be unchanged; attribute Livsmedelsverket; update downstream information. Display original source links and do not claim complete recall coverage. Do not reuse publisher photos/logos without rights verification. |
| EU: Safety Gate | https://webgate.ec.europa.eu/safety/consumers/consumers_safety_gate/menu/documents/New_disclaimer_EN.pdf | EU-specific Safety Gate disclaimer explicitly authorizes reuse provided original meaning is not distorted, proper source acknowledgement is used and machine-translation is disclosed if added. Check the **current** required copyright year and attribution on the live portal at release time. Exclude rights to third-party marks, logos and photos. |
| Canada: Health Canada / CFIA | https://open.canada.ca/data/en/dataset/d38de914-c94c-429b-8ab1-8776c31643e3 ; https://open.canada.ca/open-government-licence-canada | Official *open dataset* is under Open Government Licence – Canada and is explicitly for third-party apps. Include required source statement: **Contains information licensed under the Open Government Licence – Canada.** Confirm the feed's exact reuse applicability with the publisher. Do not imply government endorsement. |
| United Kingdom: GOV.UK OPSS | https://www.gov.uk/help/reuse-govuk-content | Reuse of GOV.UK content follows the Open Government Licence, subject to exceptions for third-party materials and branding. Include acknowledgement and a link to the licence: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/ |
| United States: CPSC | https://catalog.data.gov/dataset/recalls-api ; https://www.cpsc.gov/Recalls/CPSC-Recalls-Application-Program-Interface-API-Information | CPSC's government recalls API is a publicly accessible source and its Data.gov dataset is labelled U.S. Public Domain. Neither the CPSC name/logo nor third-party product photographs are licensed by the data designation; keep source links. |

## Required acknowledgement in user-facing documentation

> Recall Watch uses public authority information, including the European Commission's Safety Gate alerts, Livsmedelsverket, Health Canada / CFIA, GOV.UK / Office for Product Safety and Standards, and the U.S. Consumer Product Safety Commission. It is an independent third-party project and is not endorsed by these agencies. For important product, model, batch, purchase-market, and risk details, always consult the original publisher notice.
>
> Canada: Contains information licensed under the Open Government Licence – Canada.
>
> EU Safety Gate: Alerts from the Rapid Alert System for dangerous non-food products, published free of charge on the Safety Gate website (https://ec.europa.eu/safety-gate-alerts) © European Union. The copyright year and exact wording must be reviewed against the current portal's notice before release.
>
> UK: Contains public sector information licensed under the Open Government Licence v3.0.

## Outstanding maintainer checks

- [x] Locate and record official source-specific reuse terms for all jurisdictions (links above).
- [ ] Confirm the *exact* feed terms where source pages and an open dataset differ, including any aggregation/redistribution exceptions.
- [ ] Review request frequency (currently every six hours), caching and publisher rate limits.
- [ ] Confirm no third-party photos, logos, protected design elements or text are included without rights.
- [ ] Confirm user-facing attribution and legal notice on release assets/UI; user-provided translations must not misrepresent the official notice.
- [ ] Obtain dated, human sign-off in the release evidence file. A green CI job is **not** sign-off.

See [Independent authority sample audit](AUTHORITY_SAMPLE_AUDIT.md), [Release acceptance](RELEASE_ACCEPTANCE.md), and [Data sources](DATA_SOURCES.md).
