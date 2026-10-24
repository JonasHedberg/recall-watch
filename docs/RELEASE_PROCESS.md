# Maintainer release process

There are **three separate milestones**: a public source repository, a pre-release GitHub release, and optional HACS/Marketplace default-catalog inclusion. None is automatic.

## A. Before any public beta release

1. Assign a human maintainer, replace all owner placeholders, inspect third-party license obligations and confirm repository visibility is public.
2. Run `python -m pytest -q` and `python scripts/validate_repository.py` locally.
3. Run an actual supported Home Assistant instance with the component installed and exercise setup, options, sensors, `recall_watch.get_notices`, reload/unload and Swedish/English translations.
4. Confirm **every source** against live RSS, Atom or CPSC JSON, including actual extraction results reviewed against original agency records. Check source reuse requirements and responsible polling.
5. Ensure HACS Action and hassfest pass in GitHub Actions. Do not bypass warnings silently.
6. Confirm brand registration expectations with home-assistant/brands and test install, upgrade and removal from HACS/Marketplace.
7. Review [release checklist](RELEASE_CHECKLIST.md), [QA report](QA_REPORT.md), [security policy](../SECURITY.md) and [data extraction policy](DATA_EXTRACTION.md).
8. Run `python scripts/pre_release_check.py`. This only validates metadata and **never** proves production readiness.

## B. Tag and publish a release

- Use a compatible version string in `custom_components/recall_watch/manifest.json` and in the git tag (example: `0.3.0b1`).
- Update `CHANGELOG.md` and prepare release notes describing changes, incompatibilities, security implications and limitations.
- Commit and merge the reviewed code, confirm the passing CI run, then create a matching annotated tag and GitHub **Release** (not tag alone).
- Mark beta versions as **pre-release** on GitHub. HACS/Marketplace may require the user to opt in to pre-releases. A branch install is an alternative for testers.
- Do not generate or upload a custom ZIP release asset unless `hacs.json` is intentionally changed to support it; the default integration layout works with source archives.
- After publication, independently verify fresh installation and the resulting entity/action behavior.

Example commands **after review and acceptance**:

```sh
git tag -a 0.3.0b1 -m "Recall Watch 0.3.0b1"
git push origin 0.3.0b1
```

Then create the corresponding GitHub Release and mark it as a pre-release.

## C. Optional catalog inclusion

Follow [HACS include documentation](https://hacs.dev/docs/publish/include/). The owner or significant contributor submits a PR to `hacs/default` only after licensing, metadata, a release and validators pass. **A custom integration used solely to alpha/beta test a forthcoming Core integration is not eligible for HACS default catalog inclusion.** Being a custom repository is still supported. Separately, official Home Assistant Core inclusion has its own contributor review and is not conferred by HACS acceptance.

## Rollback

Before updating, back up Home Assistant configuration. If a release fails, use HACS/Marketplace version selection to return to a working build if supported, or restore the backup. Confirm any saved options and entity IDs before treating the rollback as complete.
