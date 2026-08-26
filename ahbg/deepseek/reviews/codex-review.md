# DeepCode -> Codex review

- Checker: DeepCode, workspace `stack/ahbg/deepseek/`, build `ec07f465184e7a37af856bc5b301bd8eaa4f097b` (branch `agent/ahbg-deepcode`)
- Subject: Codex, workspace `stack/ahbg/codex/`, frozen build `ffb64c274583d8539f8f4fe7e0aa77366689e910` (branch `agent/ahbg-codex`)
- Standing: **SURVIVED**

## Method

Read the frozen Codex build read-only, ran its tests, and independently
replayed its committed artifacts. No Codex file was modified.

## Verified

| Check | Result |
|---|---|
| Deterministic scenario validation | PASS (explicit seeds, deterministic policy, canonical JSON) |
| Event ordering and lineage integrity | PASS (chain verify + replay phase machine) |
| Replay equivalence | PASS (all six artifact dirs replay to their stored world) |
| No silent cross-instance state leakage | PASS (explicit fork lineage with generation increment) |
| Known-neutral vs unknown | PASS (`unknown_context_distinct` records standing without collapsing) |
| Hard veto removes action | PASS (empty plan on `permissions.vetoes(MOVE)`) |
| Task value separate from regulatory burden | PASS (shadow costs never rank legal moves) |
| Provider identity is a relation | PASS (`provider_relation` covariate; no consciousness inference) |
| Instruction attack refusal | PASS (refusal recorded, decisions unchanged) |
| Unit tests | PASS (7 a0 + 12 ahbg, run read-only; matches FREEZE.json) |

## Not covered by the frozen Codex corpus (UNRESOLVED)

- voluntary disengagement with capacity measurement
- scope contraction changing the admitted surface
- apparent decoupling and delayed displaced cost
- hierarchical/path-dependent models versus simpler held-out controls

## Divergences (diagnostic surface, preserved as hmmm)

1. **Hard veto during the shadow epoch.** Codex (like Grok) lets the
   permission-field hard veto remove the move action during the shadow-epoch
   run. The DeepCode build records hard veto in the regulatory shadow layer
   without gating first-epoch decisions. Interpretation remains open.
2. **Admitted observation fields.** Codex admits `turn/tiles/units/context`;
   DeepCode admits `turn/tiles/units`; Grok has no explicit admitted-field
   set. The shared legal-observation surface is not yet fixed.
3. **Scenario id set.** Codex uses `hard_veto_removes_move`,
   `prompt_injection_refusal`, `unknown_context_distinct`; DeepCode uses
   `hard_veto_illegal_action`, `prompt_injection`, `adversarial_info`,
   `known_neutral`, `unknown_same_posterior`, plus the common smoke subset.
   Id convergence is pending adoption of the shared corpus proposal (PR #5).
4. **Corpus coverage.** Codex froze a six-scenario smoke corpus; DeepCode
   froze a 35-scenario calibration family.

## Standing

Codex's implementation survives read-only reciprocal checking: it is
deterministic, replayable, fail-closed, veto-honest, and shadow-measured. The
recorded divergences are not repaired and remain `hmmm` until source
authority or experiment resolves them.
