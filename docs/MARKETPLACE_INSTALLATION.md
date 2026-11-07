# Install Recall Watch through Home Assistant Marketplace

Recall Watch targets **Home Assistant 2026.11.0 and later** and is currently being prepared as a community-maintained Marketplace integration. It is **not** an official Home Assistant Core integration and is not automatically listed in the community catalog.

## Marketplace installation

1. Open **Settings → Marketplace** and accept the Marketplace safety notice if this is your first use.
2. Select **Add from link**, sign in to GitHub if requested, and add `https://github.com/JonasHedberg/recall-watch`.
3. Open Recall Watch and install a published, accepted version. For an explicitly offered beta, enable the **Pre-release** entity/switch under **Settings → Devices & services → Marketplace** first. A candidate branch is not itself a published release.
4. Add Recall Watch under **Settings → Devices & services** and choose one of its official sources. Repeat setup for each additional source.
5. The Marketplace can load integrations with configuration flows directly; follow any restart or repair instructions shown after an update.

Only public GitHub repositories can be used. Adding an unlisted custom repository requires a GitHub connection; listing in the Marketplace catalog requires a separate publisher review.

## Repository layout

```text
recall-watch/
├── README.md
├── hacs.json
└── custom_components/
    └── recall_watch/
        ├── __init__.py
        ├── manifest.json
        ├── config_flow.py
        ├── sensor.py
        ├── brand/
        │   ├── icon.png
        │   └── logo.png
        ├── translations/
        └── _client/
```

**The filename `hacs.json` is mandatory for the Home Assistant Marketplace**, even though its name is historical. It must not be deleted or renamed. This project retains it only because the Marketplace contract requires it.

The metadata sets minimum Home Assistant version `2026.11.0`. No separate community-store integration is required. The Marketplace validates that the integration version and its manifest are loadable.

## Known limitations

Recall Watch polls only six curated official feeds and stores bounded data. EU Safety Gate provides dangerous-product alerts, not exclusively recalls. Missing notices, incomplete product/batch fields or a failed data source do not establish that a product is safe. Always check the publisher's original alert.

See [Release acceptance](RELEASE_ACCEPTANCE.md), [manual installation acceptance](MANUAL_HA_ACCEPTANCE.md) and the [official Marketplace publishing instructions](https://contributors.home-assistant.io/marketplace/).
