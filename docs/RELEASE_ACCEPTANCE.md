# Public release acceptance — Recall Watch

**Status: BLOCKED (2026-10-31).** Passing unit tests, HACS validation and hassfest do not prove real Home Assistant operation or accuracy of live public-authority recalls.

## Mandatory acceptance procedure

1. Test the current candidate in a real supported Home Assistant installation with **all six** configured sources. Verify setup, six sensors per source, the `get_notices` response-only action and proper EU selection.
2. Verify clean install, restart, source deduplication, options update/reload, source unload, migration from Swedish v0.2, loss of network, stale cached data and recovery. Check the real Swedish and English interface.
3. Run `python scripts/live_source_probe.py --output /tmp/recall-watch-live-results.json` on a networked host. The workflow's optional **Live publisher probes** job runs the same parser on actual public data. Both are probes, not evidence of accurate product classification.
4. For every source, compare actual product, brand, hazard, batch, identifier, original URL and dates with real authority notices. Explicitly distinguish Safety Gate *alerts* from actual recalls and verify both weekly index and report payloads.
5. Review source reuse terms, attribution, availability, polling frequency, and regional limitations. Verify HACS/Marketplace installation, upgrade and uninstall in actual Home Assistant.
6. Ensure all required GitHub checks pass and separately review security and all live-probe results. Fill `docs/release-evidence.json` from the template, with human review identity, current time and HTTPS links to retained proof. Run `python scripts/verify_release_evidence.py`.
7. Publish a **new** beta tag matching the exact accepted source revision, mark its GitHub Release as **pre-release**, and smoke-test installation from that release. Never claim that a successful mocked unit test is live verification.

## Existing incorrectly classified beta release

The existing `v0.4.0b1` release was published on 2026-10-24 with `prerelease=false` despite being a beta and despite incomplete runtime and live-source gates. A maintainer with GitHub Releases management rights must mark it as **pre-release**, describe the missing verification, or withdraw it. **Do not retag published history.** This cannot be edited using the connected GitHub API permissions available here.

## Evidence and limitations

A successful live read proves that the endpoint responded with something the parser accepted. It does *not* prove that alert coverage is complete, a product has been positively identified, a batch is affected, or a real Home Assistant runtime works. An empty or missing result must never be represented as proof of safety.

The official Home Assistant Core contribution process is **separate**: this repository remains a third-party custom integration. Home Assistant Core additionally requires an established user base, a maintained PyPI client, native integration tests and documented Bronze-tier compliance.
