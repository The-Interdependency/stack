# Frozen-source startup repair

Reviewed head: `f435c65152cc23f65abc5edc403adca3cb191e64`.
Integrated main: `3032238fc8549b58721c9baf2753c53844eb8d96`.

The reviewed adapters compare historical SOURCE.json identities against current
checkout files. Startup fails before any command with `ValueError: source identity
mismatch: research/weave/README.md`. Editing the historical lock would relabel the
experiment. This repair keeps it unchanged and supplies its exact source closure
as a separately validated bundle.

| Surface | Result |
| --- | --- |
| Historical inputs | 61 locked files from Stack `9de81c67b271df09c1d9ba5422660c96fe8af7ac` and UCNS `905e66964a495d7596a577bb64e4158db9465864`, plus their two original licenses. |
| Reproducibility | Deterministic stored ZIP rebuilds byte for byte from those Git objects; every source member retains its original Git blob identity. |
| Import boundary | Validate the complete bundle before extraction/import; compile verified buffers, ignore stale bytecode, reject conflicting cached modules. Current checkout bytes are not historical inputs. |
| Adapter compatibility | Nine synthetic vectors sealed with the original adapters reproduce exact forward bytes and inverse recovery, including the native cycle and typed transport. |
| Standalone use | Nine level-six exports recover exact synthetic inputs in fresh `-I -B` processes without Git or separate native checkouts; private grading passes. Requests contain only receiver inputs. |
| Failure witnesses | Altered, missing, duplicate, extra, escaped and symlinked ZIP members, duplicate JSON identities, conflicting imports and poisoned bytecode are exercised. |
| Existing behavior | 16 containment/checkpoint regressions pass; the current 196-test Weave suite passes with zero skips and unchanged-source identity. |

The active checkout remains the privacy boundary. Exports copy frozen source bytes
and required adapter/bundle files; they do not copy the active checkout or operator
answers. Main's current native public-recovery experiment and its expected failing
distinction gate remain intact in CI.

The original blind archive, all 1,841 wires, v1 subtree, SOURCE.json, coverage,
predictions and prior RESULTS/CHECKS/REVIEW_REPAIR records are unchanged. This repair
used synthetic receiver material; it did not access the original operator archive,
rerun the original 11-test full-corpus harness, or conduct attacker trials. The
historical 176-test observation remains historical; 196 is the current suite.

See [README.md](README.md) for run and rebuild commands and
[SOURCE_REPAIR_20261116.json](SOURCE_REPAIR_20261116.json) for exact digests and
preservation checks. `SHA256SUMS` covers current files; its prior bytes remain in
`SHA256SUMS.f435c65`. Roll back the adapters and bundle together, retaining the
historical lock and challenge evidence.

hmmm: content identity is not a signature or OS sandbox. These results establish
replay compatibility and failure refusal; they supply no cryptographic strength,
private reconstruction law, authentication or replay-state mechanism. Full-Weave
coverage remains incomplete.

GPT generated; context, prompt Erin Spencer.
