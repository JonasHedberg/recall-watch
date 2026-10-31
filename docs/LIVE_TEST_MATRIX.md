# Live acceptance matrix — 2026-10-31

**Release BLOCKED:** automated live reads and one native Home Assistant test suite are passing, but substantive manual acceptance remains incomplete.

| Source | Live HTTP + bounded parser (CI) | Human original-notice comparison | Outage/recovery in real HA | Approved |
|---|---|---|---|---|
| EU Safety Gate (2 weekly reports) | ✓ 157 notices | ☐ | ☐ | ☐ |
| Sweden, Livsmedelsverket RSS | ✓ 2 notices | ☐ | ☐ | ☐ |
| Canada food RSS | ✓ 3 notices | ☐ | ☐ | ☐ |
| Canada consumer RSS | ✓ 3 notices | ☐ | ☐ | ☐ |
| UK OPSS Atom | ✓ 50 notices | ☐ | ☐ | ☐ |
| US CPSC JSON, rolling 90 days | ✓ 191 notices | ☐ | ☐ | ☐ |

Counts from [GitHub Actions run 41184630659](https://github.com/JonasHedberg/recall-watch/actions/runs/41184630659), sampled on 2026-10-31. These numbers indicate parser acceptance of available records, **not** correctness or coverage of every recall. Failed parsers must not quietly substitute an empty "safe" feed. Safety Gate items are dangerous-product alerts and are not necessarily consumer recalls.

## Mandatory manual checks

1. Install the candidate in a supported Home Assistant instance; configure all six sources and compare the UI against the original authority sites.
2. Verify refresh, retry, recovery after timeout or malformed response, entity availability, options edit/reload, restart, uninstall, and migration from Swedish v0.2.
3. Check translated English/Swedish setup and sensor states in the real frontend.
4. Compare notice title, type, product, date, case ID, brand, risk and batch against authority articles. Unknown remains unknown where an RSS/Atom summary is insufficient.
5. Verify attribution, source terms and six-hour polling.
6. Run [the acceptance gate](RELEASE_ACCEPTANCE.md), sign human evidence, and retest the exact accepted release candidate.

All approvals and source owners must be recorded in the dated human acceptance evidence, not inferred from a successful unit-test or network response.
