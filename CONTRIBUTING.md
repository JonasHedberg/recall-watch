# Contributing to Recall Watch

Recall Watch welcomes focused improvements to its data-source adapters, Home Assistant integration, localization, automated tests and documentation.

## Development requirements

1. Open an issue before significant user-visible API or architecture changes.
2. Make changes on a feature branch and open a pull request to `main`.
3. Keep one authority/source adapter per clearly documented endpoint contract.
4. Run offline tests, repository validation, linting, Home Assistant tests and HACS/hassfest validation as appropriate.
5. Add regression tests using anonymized, deterministic fixtures for changed parsing logic.
6. Document updates to source availability, license/terms, polling constraints and country coverage.
7. Describe security and safety consequences of any change.

Do not add unverified production endpoints, unbounded scrapers, live-only tests without fixtures, or claims that absence of an alert means a product is safe.

## Localization

Use English for code, canonical configuration and documentation. Preserve Swedish user-interface translations and keep message keys synchronized. Source notices remain in their original language unless a later explicitly tested translation feature is developed.

## Pull request checklist

- [ ] Tests cover the changes.
- [ ] Existing configuration entries remain compatible or are migrated.
- [ ] Documentation and release notes are updated.
- [ ] Safety warnings remain visible.
- [ ] No personal information, credentials or API tokens are committed.
- [ ] A human maintainer has reviewed the change.
