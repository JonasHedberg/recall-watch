# Live acceptance matrix — v0.4.0b1

**Release blocked:** real-world data and Home Assistant runtime have not been checked.

| Data source | Endpoint accessible | Correct RSS/Atom/JSON/XML | Correct language/date/URL | Size < 2 MiB and ≤ 250 records | Outage/recovery | Approved |
|---|---|---|---|---|---|---|
| EU Safety Gate XML (index + two reports) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Swedish Food Agency RSS | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Canada food RSS | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Canada consumer RSS | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| GOV.UK OPSS Atom | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| US CPSC JSON (90 days) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

## Additional release gates

1. Run integration in a real, supported Home Assistant instance and test setup, reload, unload and six sensors for each source.
2. Verify the Safety Gate weekly index and detail XML schema from the official live feed with reproducible fixtures. Ensure CDATA, date, URL and risk fields are correct.
3. Check attribution, publisher terms and per-source data limitations.
4. Run repository CI, hassfest and HACS validation with passing results.
5. Confirm that no notice count or missing metadata is presented as proof that a product is safe.

Do not create a GitHub release until these conditions are met.