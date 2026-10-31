# HACS default-catalog submission

Recall Watch is a public custom integration. **No default-catalog submission or GitHub release has been published yet.**

## Verified on 24 October 2026

- Main contains the custom integration, translations, `strings.json`, and HACS/hassfest workflows.
- The Home Assistant user has confirmed a successful live setup after the coordinator logger fix.
- Offline Python tests and hassfest passed on a prior main commit.
- **BLOCKED:** repository has no GitHub Topics, and HACS validation fails.
- **BLOCKED:** no published GitHub release matches `manifest.json`.
- Live checks for all government sources including Safety Gate remain unverified.

## Owner publishing steps

Requires authenticated GitHub CLI (`gh auth login`) and a local checkout.

1. Review [HACS publishing](https://hacs.xyz/docs/publish/start) and [inclusion requirements](https://hacs.xyz/docs/publish/include).
2. Run `python scripts/hacs_submission.py --metadata` to set GitHub Topics and description and rerun Actions. Alternatively set Topics under GitHub About.
3. Verify green **HACS validator**, **hassfest**, and offline tests for the current `main` commit via [Actions](https://github.com/JonasHedberg/recall-watch/actions).
4. Check live official source responses and perform a real Home Assistant smoke test for each supported source.
5. After approval of those checks, publish a stable GitHub release with a tag matching the integration manifest version, after the successful Actions.
6. Run `python scripts/hacs_submission.py` for a read-only preflight; fix any `BLOCKED` findings.
7. Run `python scripts/hacs_submission.py --submit --confirm-reviewed-guidelines` to fork `hacs/default` and open the catalog PR. Ensure its body matches the latest HACS PR template.

An accepted HACS catalog entry does not mean official Home Assistant Core approval. Safety Gate includes dangerous non-food product alerts, not just recalls; an empty result does not prove safety.
