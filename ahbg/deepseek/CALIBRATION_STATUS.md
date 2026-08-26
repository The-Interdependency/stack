# DeepCode AHBG calibration status

Builder: DeepCode — workspace `stack/ahbg/deepseek/`, branch `agent/ahbg-deepcode`.
Frozen build SHA: `ec07f465184e7a37af856bc5b301bd8eaa4f097b`.

## Sealed corpus

- Corpus: `calibration-family`, version `1.0.0-proposal-1`.
- Canonical scenarios digest: `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`.
- Adopted by all three builders; merged to `main` as `3a92c7b0` via PR #5.
- Reproduction is partial (Grok 4, Codex 6, DeepCode 35 scenarios); differences are recorded as `hmmm`, not corpus edits.

## Frozen build SHAs

| Builder | Branch | Frozen build |
|---|---|---|
| Grok | `agent/ahbg-grok` | `cce9cec7dae61304118efcd47bc0d7461200d335` |
| Codex | `agent/ahbg-codex` | `ffb64c274583d8539f8f4fe7e0aa77366689e910` |
| DeepCode | `agent/ahbg-deepcode` | `ec07f465184e7a37af856bc5b301bd8eaa4f097b` |

## Six directional checks — COMPLETE

| Direction | Standing | Checker artifact |
|---|---|---|
| Grok → Codex | SURVIVED | `ahbg/grok/reviews/codex-review.json` (subject `ffb64c2`) |
| Grok → DeepCode | SURVIVED | `ahbg/grok/reviews/deepcode-review.json` (subject `ec07f46`) |
| Codex → Grok | SURVIVED | `ahbg/codex/reviews/grok-review.json` (subject `cce9cec`) |
| Codex → DeepCode | SURVIVED | `ahbg/codex/reviews/deepcode-review.json` (subject `ec07f46`) |
| DeepCode → Grok | SURVIVED | `ahbg/deepseek/reviews/grok-review.json` (subject `cce9cec`) |
| DeepCode → Codex | SURVIVED | `ahbg/deepseek/reviews/codex-review.json` (subject `ffb64c2`) |

All six directional checks are complete. No builder was falsified; agreement is
replication evidence, not proof.

## DeepCode workspace extensions beyond the sealed corpus

- **build_v2 mechanic**: construct one unbuilt circle adjacent to a built
  circle, validated against the pre-turn built set, recorded as `build`
  events, replayed with digest verification. Sibling builds do not yet
  implement build; the shared corpus does not yet include it (`hmmm`).
- **Energy layer**: `a0(deepseek)` default (key from `.env`), pluggable
  providers, strict legal validation with deterministic fallback.
- **Epoch 2**: shadow-veto interpretation experiment — the interpretation is
  load-bearing (8/35 scenarios differ between shadow-only and veto-gating).
  Proposed resolution: hard veto = permission denial (gates); cost channels
  remain shadow-only in epoch 1. Adopted in the DeepCode workspace.
- **Epoch 3**: bounded live run (13 scenarios, 34 energy calls, 7,921 tokens,
  replay_all_equal=true).
- **Whole-system bounded test**: 30-layer board, 5 layers built (90 builds),
  20% hidden threat circles (589), `a0(deepseek)` live energy. Result:
  win=true, 18 threat encounters with zero instruction compliance,
  replay_equal=true. Compact frontier observation: 111,897 tokens vs
  5,909,444 full-board tokens, identical final world digest.

## Divergence register (visible, not averaged)

1. **Hard veto during the shadow epoch.** Grok and Codex gate the
   permission-field hard veto during shadow-epoch runs; DeepCode recorded it
   shadow-only in epoch 1, then proposed the permission-denial reading in
   epoch 2 and adopted it. Awaiting source-authority or builder confirmation.
2. **Admitted observation fields.** Codex admits `turn/tiles/units/context`;
   DeepCode admits `turn/tiles/units` (plus a `summary` block in compact game
   observations); Grok has no explicit admitted-field set. `hmmm`.
3. **Scenario id set.** Codex: `hard_veto_removes_move`,
   `prompt_injection_refusal`, `unknown_context_distinct`. DeepCode:
   `hard_veto_illegal_action`, `prompt_injection`, `adversarial_info`,
   `known_neutral`, `unknown_same_posterior`, plus the common smoke subset.
   `hmmm`.
4. **Fail-closed turn closure.** Grok leaves collision turns without a
   `turn.end` event; DeepCode and Codex emit `turn.end` with the unchanged
   digest. `hmmm`.
5. **Genesis prev hash.** Grok uses `0*64`; DeepCode uses the empty string;
   Codex its own convention. All verify internally. `hmmm`.
6. **Build mechanic.** Only the DeepCode workspace implements build_v2;
   siblings fail closed on build. `hmmm` until the shared corpus adds it.
7. **Threat layout.** DeepCode assigns 20% hidden threats deterministically;
   no canonical threat layout exists yet. `hmmm`.

## Remaining to close the program

- Source-authority or builder confirmation of the shadow-veto disambiguation.
- A shared corpus revision that adds build_v2 and a canonical threat layout.
- The final cross-build comparison publishing which regulatory components
  SURVIVED / FALSIFIED / UNRESOLVED / BLOCKED, with this register kept
  visible.
