# Structured notice extraction policy

## Scope

`_client.enrichment.extract_recall_details(title, summary)` processes the public RSS title and description **only**. No linked articles are fetched; no OCR, external language model, web search, or private household data is used. This is a **heuristic presentation aid**, not a safety determination or product-matching engine.

## Field semantics

| Field | Extraction | Missing value | False-positive controls |
| --- | --- | --- | --- |
| `product` | Product phrase following explicit Swedish/English recall wording | JSON `null` / sensor `unknown` | Do not infer from general product mentions; cap length at 120 characters |
| `brand` | Explicit `varumärke`, `märket`, `brand` label | JSON `null` / sensor `unknown` | Never treat the recalling business name as an automatic brand |
| `risk_type` | Listed known hazard terms; combined types become `multiple` | JSON `null` / sensor `unknown` | Suppress adjacent explicit negations; do not generate severity scores |
| `batch_numbers` | Tokens immediately after `batch`, `parti`, `lot` labels | Empty list / sensor `unknown` | Validate bounded simple tokens; cap to five; never infer from dates or product names |
| `best_before_dates` | Numeric or Swedish-language dates after best-before/use-by labels | Empty list / sensor `unknown` | Validate actual calendar dates; normalize to `YYYY-MM-DD`; cap to five |

Recognized risk codes: `allergen`, `foreign_object`, `microbiological`, `chemical`, `labelling`, `packaging`, `multiple`. The sensor’s translated display values come from `translations/en.json` and `translations/sv.json`. The response-only action returns stable, untranslated machine-readable codes.

## Interpretability

All structured values are **unverified candidates**. The presence of a batch number or an expiry date in an RSS description does **not** establish that an item in the user's possession is recalled, and the absence of those fields does **not** mean that no batches are affected.

We do not store extraction confidence as a pseudo-precise percentage. At this development stage we disclose source and method and require reference to the original notice. For public release, maintainers should test against real Swedish Food Agency feed snapshots and manually label the extraction correctness of each supported field. If precision is insufficient, narrow the heuristics rather than guessing.

## Data lifecycle and resource controls

- HTTP content limit: 2 MiB; max processed feed items: 250.
- Title, description and identifiers are bounded before enrichment.
- A maximum of five preview notices is stored in count sensor attributes.
- A maximum of 100 cached notices is returned per response-only action call. Request subsequent pages with `offset`.
- No continual record of previously seen notices is persisted.
- Feed retrieval errors are surfaced as coordinator update failures, not empty results.
- No dynamic regular expressions are assembled from user input; configured keywords are literal NFKC-casefolded substrings.

## Examples

`Arla återkallar proteinpudding` with `Risk för glasbitar` -> product `proteinpudding`, risk `foreign_object`, **brand unknown**.

`Återkallar kex` with `Varumärke: Exempel. Batchnummer: AB123. Bäst före 2027-01-15` -> product `kex`, brand `Exempel`, batch `AB123`, best-before `2027-01-15`.

`Viktig produktinformation` without explicit recall phrase or labels -> product/brand/risk unknown, batch/dates empty.

These are **fabricated fixtures**, not real official notices.

## Limitations and review requirements

Natural-language extraction can misinterpret sentence boundaries, negation, product names and mixed date formats. The feed may contain nonstandard XML, HTML, multiple recalled product variants, omitted batches and incomplete product information. None of these limitations can be eliminated by unit-test coverage alone. Keep warnings visible and maintain a manual review dataset before a stable public release.


## International fields

CPSC `Products[].Name` is a structured authority-supplied product name, not heuristic brand matching. Canada and UK notices remain unstructured feed entries unless an adapter can establish a reliably supported field. New English hazards include fire, burn, electric shock and choking. Unknowns remain `null` and the mere presence of a product name never proves a product or batch in a household is affected. Exact endpoint provenance is described in [DATA_SOURCES.md](DATA_SOURCES.md).
