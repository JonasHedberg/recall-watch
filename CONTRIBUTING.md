# Contributing to Recall Watch

Thank you for considering a contribution. Recall Watch is a **community** Home Assistant integration. It is not affiliated with Home Assistant or the Swedish Food Agency. Contributions must preserve source attribution and avoid conveying false product-safety assurance.

## Before starting

1. Check existing issues and the [roadmap](docs/ROADMAP.md). For larger changes, open a feature proposal first.
2. Read the [data extraction policy](docs/DATA_EXTRACTION.md) and [security policy](SECURITY.md).
3. Do not submit copies of private Home Assistant logs, credentials, addresses, shopping lists or other personal data.
4. Prefer small, reviewable pull requests with tests. A maintainer must review and approve every change.

## Development environment

Python 3.13 is sufficient for the isolated parser tests; Home Assistant runtime testing must use a Python version supported by the **target Home Assistant release**. Use a disposable test installation, not a production household.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m coverage run --source=custom_components/recall_watch/_client -m pytest -q
python -m coverage report -m
python scripts/validate_repository.py
python -m compileall -q custom_components/recall_watch
```

On Windows, activate with `.venv\Scripts\activate`. Runtime validation also requires the real Home Assistant integration test environment, HACS Action and hassfest in GitHub Actions.

## Project conventions

- Public code, documentation, commit messages and issue discussions: **English**. Translation files may use their target language; English is the reference locale and Swedish is supported.
- Use typed, deterministic parsing functions. Do not add language-model guesses, hidden network access, telemetry or direct calls to unverified endpoints.
- New extraction rules must have positive and negative fixture tests, including cases that must remain `unknown`.
- Do not store full recall feeds in recorder attributes or log unbounded feed text.
- Preserve existing entity unique IDs, structured response fields and conservative missing-value semantics whenever feasible.
- Follow the Home Assistant developer guidance and quality scale where applicable.

## Pull request process

1. Create a topic branch from `main`; do not commit to the release tag.
2. Add relevant tests and documentation, and update `CHANGELOG.md` under **Unreleased**.
3. Open a pull request using the provided template; explain externally observable changes and tests run.
4. Resolve automated checks and maintainer feedback. Do not self-merge unless explicitly authorized.
5. Maintainers decide whether a change warrants a beta or stable version. Contributors must not publish releases independently.

## AI-assisted contributions

AI-assisted code is welcome only when the submitter can explain it, test it, verify sources and licenses, and assume responsibility for the change. Include disclosure in the PR checklist when AI assistance materially affected code or documentation. Never present generated fixtures as actual agency data.

## License

By submitting a contribution, you agree that it may be distributed under the repository's [MIT license](LICENSE) and confirm you have the right to contribute the material.
