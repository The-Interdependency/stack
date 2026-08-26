# Codex -> DeepCode

Standing: **SURVIVED** (not proved).

- Checker freeze SHA: `ffb64c274583d8539f8f4fe7e0aa77366689e910`
- Target freeze SHA: `ec07f465184e7a37af856bc5b301bd8eaa4f097b`
- Date: 2026-08-26

Read-only tests with `a0/` and `ahbg/` unchanged from `ec07f46`: a0 14 OK, ahbg 11 OK.

Freeze summary is SURVIVED 31 / UNRESOLVED 0. Independently replayed six freeze artifact directories via `load_world()`; stored `world.json` matched. `known_neutral` and `unknown_same_posterior` are distinct freeze rows.

`hard_veto_construct` freeze events still contain `move`; refusals=0. That is **UNRESOLVED** against the protocol line that veto removes an action. Occupied/dual-target War ids are absent from the freeze result list (present later on HEAD; review identity remains `ec07f46`).

Codex `check.py` reports DeepCode FALSIFIED for missing `artifacts/EVENTS.jsonl`. DeepCode stores events per scenario. That path probe is Codex-local layout, not a DeepCode falsification.

Post-review evidence update: DeepCode current artifacts now record the full
35-scenario common-corpus surface with SURVIVED 33 / UNRESOLVED 2 / FALSIFIED 0
/ BLOCKED 0. The two unresolved ids are `occupied_target_collision` and
`dual_target_collision`, matching the Grok and Codex common-corpus runs. The
review subject identity remains the frozen SHA
`ec07f465184e7a37af856bc5b301bd8eaa4f097b`.

This report does not modify DeepCode source.
