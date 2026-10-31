# Independent authority-notice sample review — 31 October 2026

This is a **small, independent research spot-check** against publisher pages; it is not a full dataset-quality validation and is not the maintainer's release sign-off. Compared with the bounded samples emitted by the live publisher probe of [CI run 41184562457](https://github.com/JonasHedberg/recall-watch/actions/runs/41184562457). The integration does not fetch these full pages: it only interprets RSS/Atom/API payloads.

| Source | Official authority notice | Observed sample | Outcome / limitation |
|---|---|---|---|
| Swedish Food Agency | [Coop frozen red chili](https://www.livsmedelsverket.se/om-oss/press/aterkallanden/coop-aterkallar-fryst-rod-chili---kan-innehalla-kadmium/) | Product `fryst röd chili`; hazard `chemical` | Source specifically says 50g red chili and cadmium. Category and product match, but feed-derived name omits package size. |
| Swedish Food Agency | [Arla protein pudding](https://www.livsmedelsverket.se/om-oss/press/aterkallanden/arla-aterkallar-proteinpudding-da-produkterna-kan-innehalla-sma-glasfragment/) | `proteinpudding`, `foreign_object` | Source confirms glass-fragment risk and affected product. Specific best-before dates are linked off-site and are *not* established by the integration. |
| Canada food | [Snow Crab Surimi Stick](https://recalls-rappels.canada.ca/en/alert-recall/snow-crab-flavoured-surimi-stick-recalled-due-undeclared-egg-and-soy) | Product name and `allergen` | Source confirms egg and soy undeclared; original has UPC and affected codes not present in the feed summary. Missing batch is **unknown**, not unaffected. |
| Canada food | [Sunchanggung Ssamjang](https://recalls-rappels.canada.ca/en/alert-recall/sunchanggung-990-ssamjang-seasoned-soybean-paste-recalled-due-undeclared-sesame) | Product name and `allergen` | Headline describes undeclared sesame; original page must be checked for exact affected item/UPC if used for inventory matching. |
| Canada consumer | [Harkla swings](https://recalls-rappels.canada.ca/en/alert-recall/harkla-children-s-compression-sensory-swings-recalled-due-fall-hazard) | Product name; risk previously unknown | Source explicitly says **fall hazard**; a missing `fall` enum was discovered and fixed in PR #12. Original has two affected SKU identifiers, absent from feed summary. |
| Canada consumer | [DREO heaters](https://recalls-rappels.canada.ca/en/alert-recall/dreo-space-heaters-recalled-due-fire-and-burn-hazards) | Product name; `multiple` risk types | Original confirms both fire and burn, and specifies model DR-HSH015; simplified risk label `multiple` does not enumerate exact affected models. |
| UK OPSS | [HAMAX Buddy Baby Seat](https://www.gov.uk/product-safety-alerts-reports-recalls/product-recall-hamax-buddy-baby-seat-2610-0181) | Product name; unknown `risk_type` | Original confirms **choking risk**. The Atom feed does not expose enough for classification in this extraction; unknown must remain unknown, not safe. |
| UK OPSS | [Axkid MiniKid Core](https://www.gov.uk/product-safety-alerts-reports-recalls/product-recall-axkid-minikid-core-car-seats-2609-0213) | Product name; unknown risk | Original explains a performance standard issue but no specific enum hazard. Leaving unknown is appropriate. |
| US CPSC | [HAIARA power banks](https://www.cpsc.gov/Recalls/2027/HAIARA-Power-Banks-Recalled-Due-to-Risk-of-Serious-Injury-or-Death-from-Fire-and-Burn-Hazards-Sold-on-Amazon-com-by-Mitrytech) | Structured product; `multiple`; brand unknown | Original confirms product, fire and burn. Original text identifies brand HAIARA, but automatic extraction is conservative and does not assert a brand from unrelated free text. |
| US CPSC | [Whatever Works microwave grill](https://www.cpsc.gov/Recalls/2027/Whatever-Works-Recalls-Microwave-Grills-Due-to-Risk-of-Serious-Injury-or-Death-from-Fire-Hazard) | Structured product; `fire` | Original confirms product name and fire hazard. Original gives a model identifier not exposed by the integration. |
| EU Safety Gate | [Example live alert](https://ec.europa.eu/safety-gate-alerts/screen/webReport/alertDetail/10099437) | French product title, ID `SR/03023/26`, `electric_shock` | XML was fetched and parsed in CI, but the interactive original alert portal did not expose legible content for independent comparison. **Not manually confirmed.** |

## Findings and release implication

- Ten original authority pages outside the interactive EU portal could be inspected and independently compared at headline/product/hazard level. This **is not** a representative sampling of all historical and updated notices, and does not demonstrate a numerical accuracy percentage.
- The Harkla missing fall category was an actionable omission; the UK information gap is unavoidable without fetching a richer authoritative structured source or deliberately leaving it `unknown`.
- If a product can be identified only in a linked page, the integration **must not** fabricate brand, batch, EAN, SKU, affected market or date.
- A user's keyword match is a *possible notice match*, not verification that a specific item is included. Absence in the feed is not a safety determination.
- EU data needs publisher-specific manual review of ID, original text, language/translation, batch, risk and affected markets before sign-off.

## Remaining acceptance

The maintainer must review a broad, labelled corpus spanning each provider, removed/corrected entries, hazards that conflict with headlines and records with missing data. Provide evidence links and a dated review for each source under `docs/release-evidence.json` before releasing; this research note does **not** satisfy the `manual_authority_comparison` gate on its own.
