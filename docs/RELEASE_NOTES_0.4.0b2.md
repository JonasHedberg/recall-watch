# Recall Watch v0.4.0b2 — release notes (DRAFT)

> **Not yet approved or published.** Intended as a GitHub **pre-release** for opt-in beta testers only. Not an official Home Assistant Core integration.

## Highlights

This beta updates the international recall monitoring integration for Home Assistant. It fixes truncated public-authority HTTP payloads, restores the EU Safety Gate action selection, improves paginated results and correctly sorts recently updated US CPSC notices.

## Fixes and enhancements

- Official feed requests now consume complete responses under a strict limit and reject unapproved HTTP redirects.
- Populated feeds whose entries are all unusable now fail safely rather than showing zero notices; malformed publisher links are discarded without crashing an otherwise valid feed.
- The `recall_watch.get_notices` action supports all six configured sources and offsets through 500 within its cached bounded feed.
- CPSC exposes separate original recall and last-update timestamps; recently updated older recalls are no longer buried by original date.
- More careful English/Swedish/Canadian product name extraction, explicit allergen and fire/burn signals, plus English/Swedish fall hazard state.
- Source-aware configuration, keyword matching, six sensors per source and migration from older Swedish settings remain supported.
- Release acceptance explicitly requires the Marketplace install/update/rollback/uninstall workflow; no separate community-store dependency is needed.

## Compatibility and installation

- Minimum Home Assistant version: **2026.11.0**.
- Automated CI target: **Home Assistant 2026.11.0**, Python 3.14.
- Home Assistant 2026.11+: **Settings → Marketplace → Add from link**, using `https://github.com/JonasHedberg/recall-watch`. Enable the repository's **Pre-release** entity under **Settings → Devices & services → Marketplace** when deliberately testing this beta.
- An existing `v0.4.0b1` installation should be backed up prior to opting into this new beta. Test migration and rollback in a test Home Assistant instance first.

## Coverage and safety limitations

- Only six curated authority feeds are supported: Safety Gate (EU dangerous non-food alerts), Swedish food, Canadian food/consumer, UK OPSS and US CPSC.
- This does not include every recall, every EU or worldwide authority, old source archives or every affected batch.
- Source notices may be edited, withdrawn, incomplete or inaccessible; keyword matches are **possible notices**, not proof of a match to a product or batch in your home.
- A source returning zero results **does not prove your products are safe**. Always use original official notices before deciding how to act.
- The project is community-maintained; authorities and Home Assistant have not endorsed it.

## Tests and approvals

Automated parser, HA-API and upstream live-probe checks must pass at the precise release revision. Independent original-notice comparison, installed English/Swedish UI acceptance, Marketplace install/update, security and source reuse review must also be completed by the maintainer before changing this document from draft.

See [QA report](QA_REPORT.md), [release acceptance](RELEASE_ACCEPTANCE.md), [manual HA test plan](MANUAL_HA_ACCEPTANCE.md) and [release evidence template](release-evidence.example.json).

## Rollback

Make a full Home Assistant configuration backup. Revert to an earlier installed integration version in Marketplace or restore the backup, restart and verify six sensors per source plus the `get_notices` action.
