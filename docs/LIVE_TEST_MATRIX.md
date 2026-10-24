# Pre-release live acceptance matrix

This is a **manual checklist**, not evidence of execution. Log date, HA version, Python version, publisher response status and redacted test notes when completed. A human reviewer must sign off on every relevant item.

| Data source | Endpoint accessible | Correct RSS/Atom/JSON | Correct language/date/URL | Size < 2 MiB and ≤ 250 records | Outage/recovery | Approved |
|---|---|---|---|---|---|---|
| Swedish Food Agency RSS | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Canada food RSS | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Canada consumer RSS | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| GOV.UK OPSS Atom | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| US CPSC JSON (90 days) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

Also verify the original URLs point to appropriate authority records and that source attribution, data licensing and poll frequency comply with publisher terms.

## Home Assistant integration matrix

- [ ] Install on supported HA Core with the version-recommended Python runtime and required dependencies.
- [ ] Add one entry for each source and prevent duplicate entries for the same source.
- [ ] Run a manual six-hour update, verify shared polling and API load.
- [ ] Test five latest-field sensors and one count sensor for each configured source.
- [ ] Check unrecognized brands, batch details and risk categories show unknown rather than invented values.
- [ ] Confirm `get_notices` includes country, source and category; verify pagination and local keyword matching.
- [ ] Ensure multi-source calls require a specified source ID; verify no cross-source data leakage.
- [ ] Simulate HTTP 403/404/429/500, timeout, oversized feed, malformed XML, invalid JSON and empty responses.
- [ ] Verify original-language notice content remains unmodified; switch UI language English ↔ Swedish.
- [ ] Migrate a real v0.2 Swedish config entry; verify unique IDs and options after update and rollback.
- [ ] Test source unload and reload while another source remains configured.
- [ ] Run `hassfest` and HACS Action in the public repository with zero errors.
- [ ] Validate HACS/Marketplace install, upgrade, reinstall and uninstall; ensure no unattended release is made.

## Extraction accuracy acceptance

Collect a representative, redacted and legally reusable fixture set per jurisdiction. For each real notice, label explicitly stated product, brand, hazard, lot/batch and best-before date against the primary source. Review false-positive and false-negative cases. Record the reviewed cases and acceptance criteria before enabling notification automations. A missing classification must not be interpreted as safe.
