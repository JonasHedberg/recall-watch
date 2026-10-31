# Developer guide and architecture

All code, documentation, service descriptions and canonical JSON keys are English. Swedish frontend text is supplied in `translations/sv.json`, including translated risk-type enum states. A custom integration does not use Home Assistant Core `strings.json` / Lokalise directly.

## Modules

```text
custom_components/recall_watch/
  __init__.py         Config entry lifecycle and response-only get_notices action
  config_flow.py      Per-source config flow and editable keyword options
  const.py            Constants and six-hour refresh interval
  coordinator.py      DataUpdateCoordinator, typed failures, shared cached feed
  entity.py           Unique IDs and common coordinator-backed entity behavior
  sensor.py           Count sensor, five latest-field sensors, max-five preview
  services.yaml       Action descriptions and selector forms
  manifest.json       HACS-compatible package metadata; version 0.4.0b1
  translations/       English and Swedish setup, options and entity strings
  brand/              Integration-provided artwork
  _client/
    client.py         Caller-owned Home Assistant aiohttp session, bounded GET
    parsing.py        Defused RSS/Atom XML parsing, sanitization, deduplication
    enrichment.py     Pure deterministic, conservative entity extraction
    models.py         Frozen notice / detail models
    serialization.py  Bounded JSON-safe preview and response pagination
    matching.py       Normalized, literal keyword filtering
    exceptions.py     Typed network and parsing error classes
```

## Update and storage behavior

The coordinator retrieves a single HTTPS feed every six hours. A failed refresh does not replace the last successful data with an empty snapshot. Entities become unavailable according to Home Assistant's coordinator behavior. Sensors read the coordinator's immutable tuple of notices, not the network. The `get_notices` action uses exactly the same cached snapshot. All matching is local; keywords never leave Home Assistant.

State fields stay within Home Assistant's 255-character limit. The count sensor keeps up to five condensed preview items as JSON-serializable attributes, while the action returns at most 100 items per request, with a page index and `has_more`. Neither attribute snapshots nor the action represent a persistent historical recall archive.

## Offline validation

```sh
python -m pip install pytest pytest-asyncio aiohttp defusedxml coverage
python -m pytest -q  # includes mocked HA lifecycle tests, not live runtime
python -m coverage run --source=custom_components/recall_watch/_client -m pytest -q
python -m coverage report -m
python -m compileall -q custom_components/recall_watch
python scripts/pre_release_check.py  # expected to block until maintainer metadata exists
```

The bundled pure-Python client has no Home Assistant imports; the custom integration requires a Home Assistant-supported Python environment and includes the Home Assistant-built-in `voluptuous` dependency. No additional PyPI package is required for the bundled client except `defusedxml` from `manifest.json`.

## Required Home Assistant end-to-end checks

In a **real supported Home Assistant runtime**, install `custom_components/recall_watch`, and test:

1. Clean setup, language switching (English/Swedish), invalid keywords, duplicate entry prevention, options edit and reload.
2. Count plus five latest-field sensors, `unknown` when fields absent, translated enum labels, stable unique IDs and no state longer than 255 characters.
3. Both successful and failed coordinator refresh, restart, network timeout, XML parse failures, sensor availability and recovery.
4. `recall_watch.get_notices` return schema, filtering, paging, `has_more`, offset/limit validation, and removal on unload.
5. Real responses from the Swedish Food Agency RSS endpoint, validated manually against the original notice for extraction correctness and missing values.
6. HACS/Marketplace install/upgrade/uninstall and checks by `hacs/action` and `hassfest` in GitHub Actions.
7. Recorder retention / attribute-size behavior with a busy 250-item feed and a changing latest notice.

The isolated tests in this repository **do not replace** these checks. The code must remain a beta candidate until the actual runtime checks have passed.

## Relationship to Home Assistant Core

This package is a **community custom integration**. To propose official Core inclusion, move the client into a separately published and maintained library, adapt Home Assistant manifest conventions, add native HA integration tests and review the [Home Assistant integration quality scale](https://developers.home-assistant.io/docs/core/integration-quality-scale/). The decision belongs to Home Assistant maintainers.


## International source adapters

Supported endpoints are stored in `custom_components/recall_watch/_client/sources.py`. The `RecallClient` chooses the appropriate RSS/Atom or CPSC JSON parser, and `ConfigFlow` creates one entry per source ID. The global `async_setup` registers a single response-only action, routing to the explicitly configured source. CPSC queries use a rolling 90-day `LastPublishDateStart` date to avoid loading the entire historic API.

Every new source requires recorded official provenance, fixed endpoint, country and category metadata, fixture-based parsing tests, failure isolation and live verification. See [DATA_SOURCES.md](DATA_SOURCES.md).
