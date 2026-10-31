# Roadmap

## Release-readiness candidate — international sources

Six curated government feed adapters: European Union Safety Gate dangerous non-food alerts; Sweden food; Canada food and consumer; UK consumer; US CPSC consumer. The sources are not an exhaustive catalog of recall notices worldwide.

Implemented: per-source setup and keyword filters, six sensors per source, bounded preview and paginated `get_notices` action, localized English/Swedish UI strings, coordinator polling, network/parse errors, conservative extraction, migration logic for Swedish v0.2.

As of 2026-10-31, [PR #12](https://github.com/JonasHedberg/recall-watch/pull/12) contains offline regressions, live read/parse probes (all six sources) and six native Home Assistant smoke/contract tests. **It remains a draft, not a public-release approval.**

## Release milestones

1. Resolve [release blocker #1](https://github.com/JonasHedberg/recall-watch/issues/1): real UI, install/upgrade, migration and failure-recovery acceptance.
2. Manually compare representative data against original authority notice details; assess extraction errors and limits.
3. Finish publisher rights/attribution/rate-limit review and evidence-signoff.
4. Publish only after documented acceptance per [Release acceptance](RELEASE_ACCEPTANCE.md).
5. Explore richer historical and model/batch-specific matching without implying confirmed household safety.
6. Evaluate suitability for official Home Assistant Core separately: maintained PyPI client, native Core test conventions, quality-scale compliance and developer review.

No arbitrary user-entered feed URLs, guaranteed safety ratings, or unchecked global recall coverage are planned.
