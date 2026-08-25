# DeepCode -> Grok review

- Checker: DeepCode, workspace `stack/ahbg/deepseek/`, build `ec07f465184e7a37af856bc5b301bd8eaa4f097b` (branch `agent/ahbg-deepcode`)
- Subject: Grok, workspace `stack/ahbg/grok/`, build `cce9cec7dae61304118efcd47bc0d7461200d335` (branch `agent/ahbg-grok`)
- Standing: **SURVIVED**

## Method

Read the frozen Grok build read-only, ran its tests, and independently replayed
its committed artifacts. No Grok file was modified.

## Verified

| Check | Result |
|---|---|
| Deterministic scenario validation | PASS (explicit seeds; pulse = sha256(seed:domain:index)) |
| Event ordering and lineage integrity | PASS (chain verify + replay phase machine) |
| Replay equivalence | PASS (all four artifact dirs replay to their stored field) |
| No silent cross-instance state leakage | PASS (fork copies state and records events both sides) |
| Hard veto removes action | PASS (allowed_to_do<=0 removes relocate; defer asserted) |
| Task value separate from regulatory burden | PASS (shadow cost measured after the fact; task_value independent) |
| Provider identity is a relation | PASS (provider_relation covariate; no consciousness inference) |
| Unit tests | PASS (3 a0 + 3 ahbg, run read-only) |

## Not covered by the frozen Grok corpus (UNRESOLVED)

- known-neutral versus unknown at the same posterior mean
- voluntary disengagement with capacity measurement
- scope contraction changing the admitted surface
- apparent decoupling and delayed displaced cost
- hierarchical/path-dependent models versus simpler held-out controls

## Divergences (diagnostic surface, preserved as hmmm)

1. **Hard veto during the shadow epoch.** Grok's veto run sets
   `allowed_to_do=0` and the veto removes the relocate action. The DeepCode
   build records hard veto in the regulatory shadow layer without gating
   decisions in the first epoch. Whether permission-field vetoes belong to
   embodiment state (gating) or to the candidate cost model (shadow-only) is
   open.
2. **Fail-closed turn closure.** Grok's collision scenarios leave the
   chronicle without a `turn.end` event (2 events, turn 0). The DeepCode build
   emits `turn.end` with the unchanged digest after a fail-closed resolution.
3. **Corpus coverage.** Grok froze a four-scenario smoke epoch; DeepCode froze
   a 31-scenario calibration family. The shared sealed corpus is not yet
   frozen across the three builders.
4. **Genesis prev hash.** Grok uses `0*64`; DeepCode uses the empty string.
   Both verify internally.

## Standing

Grok's implementation survives read-only reciprocal checking: it is
deterministic, replayable, fail-closed, and shadow-measured. The recorded
divergences are not repaired and remain `hmmm` until source authority or
experiment resolves them.
