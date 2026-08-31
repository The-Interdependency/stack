# AHBG burden and coupling aggregate

Generated: `2026-08-31T08:28:09Z`

## Provenance

- schema: `interdependency.ahbg.burden-coupling/1.2.0`
- runner: `stack/ahbg/burden_coupling.py`
- corpus source: `stack/ahbg/deepseek/corpus-proposal/corpus.json`
- common corpus: `calibration-family-1.0.1-proposal-1`
- Grok: `stack/ahbg/grok/corpus-run/calibration-family-1.0.1-proposal-1/CALIBRATION_RESULT.json`
- Codex: `stack-codex/ahbg/codex/corpus-run/calibration-family-1.0.1-proposal-1/CALIBRATION_RESULT.json`
- DeepCode: `stack-deepcode/ahbg/deepseek/artifacts/CALIBRATION_RESULT.json`

## Evidence standings

| claim | standing |
|---|---|
| `common_corpus_survival` | `SURVIVED` |
| `org_burden_inventory` | `SURVIVED` |
| `common_runtime_burden_observables` | `SURVIVED` |
| `common_runtime_burden_mapping` | `UNRESOLVED` |
| `hierarchical_fixture_comparator` | `UNRESOLVED` |
| `hierarchical_runtime_vectors_shared` | `BLOCKED` |
| `hierarchical_coupling_vs_simpler_controls` | `UNRESOLVED` |
| `deepcode_live_burden_extension` | `SURVIVED` |

## Common corpus scalars

| builder | scenarios | SURVIVED | events | telemetry rows | refusals | invalid | replay equal |
|---|---:|---:|---:|---:|---:|---:|---:|
| Grok | 35 | 35 | 316 | 183 | 30 | 0 | 35 |
| Codex | 35 | 35 | 342 | 557 | 3 | 0 | 35 |
| DeepCode | 35 | 35 | 342 | 522 | 3 | 0 | 35 |

## Runtime term coverage

| builder | tokens | latency_ms | retries | tool_calls | memory |
|---|---:|---:|---:|---:|---:|
| Grok | 35/35 numeric; 35 hmmm | 35/35 numeric; 35 hmmm | 35/35 numeric; 35 hmmm | 35/35 numeric; 35 hmmm | reads 35; writes 35 |
| Codex | 35/35 numeric; 0 hmmm | 35/35 numeric; 0 hmmm | 35/35 numeric; 0 hmmm | 35/35 numeric; 0 hmmm | reads 35; writes 35 |
| DeepCode | 35/35 numeric; 0 hmmm | 35/35 numeric; 0 hmmm | 35/35 numeric; 0 hmmm | 35/35 numeric; 0 hmmm | reads 35; writes 35 |

## Hierarchy Fixture Comparator

- standing: `UNRESOLVED`
- sample count: 2
- minimum claim sample: 6
- impedance lift vs best constant control: 0.5

| scenario | impedance | actual transition | impedance-sign | constant contract | constant expand | constant none |
|---|---:|---|---|---|---|---|
| `scope_avoidance` | 0.2 | `contract` | `contract` | `contract` | `expand` | `none` |
| `true_decoupling` | 0.0 | `expand` | `expand` | `contract` | `expand` | `none` |

| model | correct | total | accuracy |
|---|---:|---:|---:|
| `impedance_sign` | 2 | 2 | 1.0 |
| `constant_contract` | 1 | 2 | 0.5 |
| `constant_expand` | 1 | 2 | 0.5 |
| `constant_none` | 0 | 2 | 0.0 |

## Regulatory Vector Coverage

| builder | permission vectors | shadow records | non-empty coupling | non-empty impedance | non-empty scope log |
|---|---:|---:|---:|---:|---:|
| Grok | 35 | 35 | 0 | 0 | 0 |
| Codex | 35 | 0 | 0 | 0 | 0 |
| DeepCode | 35 | 35 | 0 | 2 | 5 |

## DeepCode Live Extensions

| extension | tokens | latency_ms | calls | failures | scope |
|---|---:|---:|---:|---:|---|
| `epoch3_live_provider` | 7921 | 32332.5 | 34 | 0 | 13 |
| `whole_system_game` | 111897 | 77150.6 | 90 | 0 | 90 |

## Scenario Vector Summary

- Standing mismatches: 0
- World-digest mismatches: 35
- Full per-scenario vectors are in `BURDEN_COUPLING.json`.

## Oddities

- Some per-decision burden rows still preserve hmmm placeholders; scenario-level resource rows are the common surface.
- No common telemetry contains non-empty coupling_weights.
- DeepCode records non-empty impedance telemetry; Grok and Codex do not yet emit matching runtime vectors.
- The admitted hierarchy fixture is too small for a general coupling claim.
- World digest vectors disagree on 35 scenarios.
- DeepCode has live-provider burden evidence, but it is not replicated by Grok and Codex.

## Recommendations

- Keep burden fitting on scenario-level resource rows until per-decision burden fields are normalized.
- Promote impedance telemetry into Grok and Codex before claiming shared runtime hierarchy evidence.
- Expand the two-row hierarchy fixture before treating impedance lift as a validated law.
- Add non-empty coupling_weights only with a declared update rule and a simpler-control comparator.
- Run live-provider burden extensions only as bounded, explicit spend decisions.

## hmmm

- Cross-provider burden fitting remains unresolved.
- The hierarchy comparator exists, but the sample is too small and not implemented across all builders.
- Remote branch merge and release authority remain outside this local aggregate.
- Tiny samples make loud graphs; keep the volume down.
