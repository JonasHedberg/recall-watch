# Installation through HACS or Home Assistant Marketplace

## Supported repository layout

```text
recall-watch/
├── hacs.json
├── README.md
└── custom_components/
    └── recall_watch/
        ├── manifest.json
        ├── __init__.py
        ├── config_flow.py
        ├── sensor.py
        ├── translations/
        └── _client/
```

Only one custom integration resides under `custom_components/`. Runtime files stay inside `custom_components/recall_watch/`. `hacs.json` remains in the repository root. Repository must be public.

## User installation after the repository exists

For Home Assistant **2026.10 and earlier**, use HACS and add `<OWNER>/recall-watch` as a custom repository of type **Integration**. For Home Assistant **2026.11 and later**, use the built-in **Marketplace**; installation routes may vary as the UI evolves. The repository is not automatically in the default catalog.

After installing, restart Home Assistant as requested, navigate to **Settings → Devices & services → Add integration**, search for **Recall Watch** and select an official source, then configure keywords (optional). Add another Recall Watch instance to select another country or category. `get_notices` is a response-only action and must be invoked from a suitable automation or Developer Tools interface that supports response data.

For manual installation, copy `custom_components/recall_watch/` to `<HA_CONFIG>/custom_components/recall_watch/` and restart. A repository ZIP is **not** a one-click installation bundle.

## Releases

A GitHub prerelease is not the same as a stable release. When releases exist, version selection and update detection follow HACS/Marketplace behavior. See [Marketplace internals](https://contributors.home-assistant.io/marketplace/how-it-works/) and [hacs.json reference](https://contributors.home-assistant.io/marketplace/reference/hacs-json/).

## Known constraints

No currently supplied integration version has been validated in a real HA runtime or with live recall feed requests in this delivery. Configure and test in a disposable installation first. If the public RSS feed is blocked or changes format, the integration cannot provide reliable results. Recall Watch is **not** a safety assurance service.


## International country metadata

Since the package supports multiple country jurisdictions, root `hacs.json` intentionally omits a single-country `country` field. The integration does not promise comprehensive worldwide or EU-wide coverage. See [DATA_SOURCES.md](DATA_SOURCES.md).
