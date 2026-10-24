# Localization

English is the canonical language for code, documentation, comments, issue templates and translated-message keys. Swedish (`sv`) is the first additional interface language; new locales are welcome.

## Translation files

- `custom_components/recall_watch/translations/en.json` — English source UI messages.
- `custom_components/recall_watch/translations/sv.json` — Swedish UI messages.

All locale files should contain the same nested translation keys and enum identifiers. Keep machine-readable values such as `foreign_object`, `multiple` and API/action field names untranslated. The translation files affect labels, not the semantics of a fetched recall.

## Contributor checklist

1. Change English text first, then Swedish and any other supported locale.
2. Preserve placeholders, variable names and JSON key shape.
3. Avoid terms implying regulatory confirmation (such as *safe*, *certified* or *confirmed recall match*) where only heuristics exist.
4. Run `python -m pytest -q` and inspect the UI in a real Home Assistant installation using English and Swedish.
5. Record any locale that has not been checked in the real UI before release.

This is a custom HACS/Marketplace integration. If it later becomes an official Core integration, its internationalization flow will follow Home Assistant Core and Lokalise requirements instead.

Source notice content is **not** translated. Source menu labels are currently English for source identification; additional translated descriptions may be added with matching locale keys.
