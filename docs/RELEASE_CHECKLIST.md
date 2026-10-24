# Release readiness checklist

**Status: BLOCKED — no release should be published.**

## Required checks

- [x] GitHub owner and public repository verified: `JonasHedberg/recall-watch`.
- [x] English overview and safety disclaimer published.
- [x] Offline candidate completed with 72 passing tests in a separate environment.
- [ ] Entire source tree and test suite committed to GitHub, including `custom_components/recall_watch`.
- [ ] Actual feed data fetched and manually verified for Swedish, Canadian, UK and US sources.
- [ ] Home Assistant integration/runtime tested with supported Python and HA releases.
- [ ] Migration from pre-global Sweden-only configuration verified with a real HA backup.
- [ ] HACS validation and hassfest pass in GitHub Actions.
- [ ] Independent maintainer code/security review completed.
- [ ] Branding, translations and license provenance confirmed.
- [ ] Real GitHub beta release and install test completed.
- [ ] HACS inclusion criteria assessed separately (not synonymous with custom repository support).

**Safety:** Feed items are not guaranteed complete or current. Matching does not establish that a specific batch or product is affected.
