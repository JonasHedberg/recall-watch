# Migration guide: Swedish 0.2 → international 0.3 beta

The integration domain remains `recall_watch`, and existing entry-based entity unique IDs are retained. No end-user dashboard changes should be necessary when Home Assistant accepts the migration, but this expectation **requires live regression testing** before production release.

## Data model changes

- Legacy entries created by v0.2 use the unique ID `swedish_food_agency` and no explicit source ID.
- v0.3 migrates their data to `{"source": "se_food"}` with config-entry version 2 and unique ID `se_food`.
- The keyword option is preserved. Existing source coordinator and six sensors are still derived from the original entry ID.
- Other regions can be added independently as extra configuration entries; duplicate source entries are rejected.
- `recall_watch.get_notices` now optionally accepts a `source` ID. It remains backward-compatible if exactly one source exists. **When multiple sources exist, the action must specify a source.**

## Maintainer acceptance test

1. Back up an HA installation with a populated v0.2 Swedish entry and note its six entity unique IDs and keyword setting.
2. Upgrade the test instance to v0.3; ensure the config entry upgrades to v2 with `source=se_food` and preserved keywords.
3. Confirm existing entities have the same unique IDs and sensible data values.
4. Add Canadian and/or UK/US entry without affecting the Swedish entry.
5. Call `recall_watch.get_notices` without `source`: expect an explicit error when two or more entries exist.
6. Call it with `source=se_food`, then a second source; verify the returned records never mix.
7. Unload/remove the second source; check that the Swedish sensors and action continue functioning.
8. Reboot, test locale names in English/Swedish, remove the new entries and verify rollback.

This has **only** been checked by mocked tests. Do not perform an unbacked-up migration on a production controller.
