# Quality assurance report — International beta 0.4.0b1

**Assessment date:** 24 October 2026
**Classification:** Source package candidate — **NOT RELEASE-APPROVED**.

## Verified locally

| Check | Result | Scope |
|---|---|---|
| Offline automated tests | **77 passed** | RSS/Atom, CPSC JSON, normalized model, text enrichment, network error handling, country/source isolation, service stub contracts, migration, package metadata |
| Client statement coverage | **475 / 486 = 97.7% (reported as 98%)** | `custom_components/recall_watch/_client/` **only**, includes Safety Gate; not Home Assistant runtime integration |
| Syntax compilation | Passed | Custom component Python code |
| Local repository validation | Passed | JSON, YAML, translation key parity, Markdown links and directory layout |
| HACS multi-country metadata | Verified offline | No `country` restriction in `hacs.json` |
| Release guard | **Expected failure** | Live-provider, Home Assistant runtime and independent release gates remain unverified |

Tests were run using Python 3.13.5. Mocked Home Assistant modules are **not** a substitute for genuine Core runtime tests. No GitHub release was published. GitHub source upload does not imply runtime validation.

## Not tested or verified

| Mandatory step | Status |
|---|---|
| Live EU Safety Gate index and report XML | **Blocked / not verified** |
| Live Swedish Food Agency RSS | **Blocked / not verified** |
| Live Canadian food/consumer RSS | **Blocked / not verified** |
| Live GOV.UK OPSS Atom feed | **Blocked / not verified** |
| Live US CPSC JSON API with 90-day filter | **Blocked / not verified** |
| Stable source terms, rate limits and attribution permissions | **Needs maintainer review** |
| Genuine Home Assistant 2026.10+/Python runtime config/options/sensors/service/migration/reload/unload | **Not run** |
| Real-language UI review in English and Swedish | **Not run** |
| GitHub Actions HACS Action and hassfest | **Not run** |
| HACS/Marketplace manual install, upgrade, restore and uninstall | **Not run** |
| Human-labeled extraction accuracy, completeness and false positives | **Not performed** |
| Real GitHub owner and codeowners | **Configured:** `JonasHedberg` |
| Published release URL | **Not created** |
| EU Safety Gate machine interface | **Not implemented** |

## Fail-closed behaviors

- Unsupported source IDs are rejected; Home Assistant configuration cannot supply arbitrary URLs.
- Invalid, oversized or excessive-entry RSS/JSON responses fail rather than silently reporting a safe state.
- CPSC requests are restricted to a recent 90-day update window to limit payload size, not to claim full historical coverage.
- Nonexistent brand/batch fields remain unknown; company names are not treated as brands.
- Multiple source entries remain independent, including when a source is removed.
- A response-only action without a source is rejected if multiple sources are installed.

## Commands for maintainers

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
coverage run --source=custom_components/recall_watch/_client -m pytest -q
coverage report -m
python scripts/validate_repository.py
python scripts/pre_release_check.py
```

The last command may deliberately fail until live-provider and runtime release gates are documented. Repository ownership is configured, but this does not prove runtime or provider compatibility. Do not issue a stable or public beta release without reviewing [the release checklist](RELEASE_CHECKLIST.md) and [live-test matrix](LIVE_TEST_MATRIX.md).
