# HACS default-catalog submission readiness

Last audited: 2026-10-24. Target: https://github.com/JonasHedberg/recall-watch

## Checks

- [x] Repository is public and exposes a HACS custom integration.
- [x] `hacs.json`, manifest, README, license, codeowners, issue templates, security policy and release checklist exist on the candidate branch.
- [x] `strings.json` is the English translation source, with English and Swedish JSON translations.
- [x] Python offline test jobs (3.13, 3.14) pass on GitHub Actions.
- [x] Home Assistant hassfest passes on GitHub Actions.
- [ ] HACS validator: fails because GitHub repository **Topics** are empty. **Repository owner must add topics using GitHub About → gear → Topics**. At least one valid topic is required, e.g. `home-assistant`, `hacs`, `custom-integration`, `product-recalls`, `food-safety`.
- [ ] EU Safety Gate and all other upstream sources must be checked against current live payloads.
- [ ] Real Home Assistant installation, configuration, reload, sensor updates, translation display, multi-source behavior, and recovery tests must pass.
- [ ] Merge reviewed candidate into `main`; GitHub Actions must pass on main.
- [ ] Publish a reviewed GitHub release with version matching `manifest.json`. No releases are currently published.
- [ ] Submit a default repository inclusion pull request to https://github.com/hacs/default after all HACS checklist items pass.

## Evidence

- Workflow (all Python tests and hassfest green; HACS topics failure): https://github.com/JonasHedberg/recall-watch/actions/runs/40124795949
- Draft PR for the EU source and quality fixes: https://github.com/JonasHedberg/recall-watch/pull/2

Do not treat any empty recall result as an indication that a product is safe. No code changes alone can validate upstream reliability. The release must remain blocked until the above requirements have been verified.
