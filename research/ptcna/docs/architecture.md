# PTCNA architecture and historical scaffold

## 2026-08-17 authority correction

**PTCNA** — *Prime Tensor Circled Neural Architecture* — is intended to be an
architecture **derived from UCNS audit evidence obtained from a functioning
conventional neural network**.

```text
functioning conventional neural network
        ↓
UCNS audit
        ↓
source-bound relational evidence
        ↓
PTCNA construction derived from that evidence
```

The intended PTCNA has therefore **not yet been built**. Construction is BLOCKED
until the upstream UCNS audit exists. Missing architectural detail remains
`hmmm`; it is not permission to complete the pattern from imagery, prior code,
or an executable scaffold.

The four-layer implementation currently in this repository predates restoration
of that prerequisite. It remains valuable as a **historical pre-audit
experimental scaffold**, but it is not the authority for the eventual
architecture. See `docs/INTENDED_CONSTRUCTION_GATE.md`.

## Intended language-input boundary

For the intended PTCNA language path, the primitive input object is a **UCNS
Unicode-character gonol**.

There is no conventional tokenizer layer between source text and that primitive.
Tokenizer ids, subword ids, whole-string cryptographic fingerprints, and opaque
external embedding vectors may not be silently substituted.

The exact way the future audit-derived architecture composes or routes Unicode-
character gonols is unresolved until the audit supplies the structural evidence.

## Historical scaffold: four implemented layers

The material below records the executable scaffold. Where it conflicts with the
authority correction above, the correction governs.

| Module | Scaffold layer | Divides… → … | Tensor kind | Backprop? |
|---|---|---|---|---|
| `neural/` | neural (**pcna**) | (base) neural tensors | **neural** | **yes — the only differentiable scaffold layer** |
| `circle/` | circle | neural tensors → circles | auditing / timing | no |
| `seed/` | seed | circles → seeds | auditing / timing | no |
| `core/` | core | seeds → cores | auditing / timing | no |

In the scaffold:

- every circle, seed, and core is itself a tensor;
- reverse-mode differentiation is owned by the neural layer;
- circle/seed/core tensors are auditing/timing hosts;
- fiqs gate internal core propagation through the existing Fick-inspired timing
  rule; and
- PCEA remains a separate orthogonal repository rather than a PTCNA layer.

These statements describe implemented historical behavior. They are not claims
that the neural audit will recover exactly four layers, the same ring sizes, the
same weights, the same prime constants, or the same propagation laws.

## Historical provenance

PTCNA consolidated the former `pcna`, `pcta`, and `pcsa` repositories. `pcea`
remained separate.

| Destination | Historical source | Notes |
|---|---|---|
| `ptcna/neural/` | `pcna` | prior backprop/ring engine |
| `ptcna/circle/` | `pcna` circle-audit logic + `pcta` material | scaffold circle audit/timing |
| `ptcna/seed/` | `pcta` + `pcna` seed-audit logic | scaffold seed audit/timing |
| `ptcna/core/` | `pcsa` | scaffold core timing + fiqs |

The consolidation solved repository/naming problems and produced an executable
research object. It did not provide the missing upstream neural-network audit.

## Historical construction and evaluation record

The scaffold was deliberately made executable and falsifiable. It includes:

- `PTCNAEngine` and `PTCNARuntime`;
- a separately identified `HashedLinearFallback`;
- an exact UCNS candidate-state receipt for `157×7×7×53`;
- explicit target/fallback routing receipts; and
- immutable digest-bearing `EvaluationPlan` / terminal result infrastructure.

The UCNS receipt pinned at
`b7b6f35cce69c273860923489a1c8b5372d14eb0` established compatibility with the
preselected scaffold state. It did **not** establish that the state had been
derived from UCNS observation of a conventional neural network.

The scaffold's neural input path also projects each complete input string through
a SHA-derived fixed-width feature representation. That path is historical and is
not the intended Unicode-character-gonol input contract.

### Frozen role-acquisition result

The preregistered 18-case, five-repetition role-acquisition experiment produced:

```text
target ptcna.experimental.v1: 0.3333333333
hashed-linear fallback:       0.9444444444
absolute usefulness:          FALSIFIED
superiority vs fallback:      FALSIFIED
```

That result remains sealed. It is valid evidence about the exact historical
scaffold and exact workload. It must not be weakened, erased, or silently
redefined after outcome inspection.

It also must not be generalized to the intended PTCNA, because the intended
PTCNA was not constructed under the required audit-before-architecture process.

## Correct construction contract

The old rule that construction could proceed independently of upstream evidence
is superseded for the **intended PTCNA**.

The corrected contract is:

1. UCNS selects and instruments a functioning conventional neural-network
   specimen under explicit provenance.
2. The observation protocol freezes model/task identity, what is observed,
   resource/stopping/failure behavior, and raw-evidence custody before structural
   outcomes are inspected.
3. UCNS records the network's relational behavior without a preselected PTCNA
   topology.
4. Raw observations remain separate from interpretations and derived structure.
5. Only after the audit is complete may PTCNA derive a new architecture
   candidate from the evidence.
6. The derived candidate receives a new identity and does not overwrite the
   historical scaffold.
7. The new candidate uses UCNS Unicode-character gonols as primitive language
   input objects; the audit-derived routing/composition law must be explicit.
8. Evaluation of that new candidate receives its own frozen workload,
   comparator, metrics, thresholds, limits, stopping rules, and failure
   propagation. Historical results remain historical.

## What PTCNA may do while blocked

Until the UCNS audit contract exists, PTCNA-side work may:

- preserve the scaffold, its receipts, and its sealed falsification;
- preserve the fallback as a separately attributed historical control;
- document the future UCNS consumer interface;
- remove misleading claims that the scaffold is the intended architecture; and
- prepare non-semantic plumbing that does not choose future topology.

PTCNA-side work may not repair or elaborate the intended architecture by
assuming what the missing audit would have found.

## Status log

- **2026-08-17 — intended-construction prerequisite restored.** The intended
  PTCNA is downstream of UCNS auditing a functioning conventional neural
  network. The current four-layer system is reclassified as historical
  pre-audit experimental scaffolding. Intended language input is fixed at UCNS
  Unicode-character gonols; the current whole-string hash path is historical.

- **2026-08-17 — critical role-acquisition evaluation FALSIFIED.** The frozen
  18-case, five-repetition program produced target accuracy `0.3333333333`
  against fallback accuracy `0.9444444444`. The target failed its absolute
  `0.75` usefulness threshold and its `0.05` superiority-margin threshold. The
  result remains valid for the exact pre-audit scaffold.

- **2026-08-17 — executable scaffold/evaluation boundary.** Added the
  four-layer target receipt, independently test-backed hashed-linear fallback,
  explicit attributed failover, and frozen evaluation/verdict API.

- **2026-07-05 — circle/seed audit extraction.** Aggregation moved out of the
  neural engine into separate scaffold circle and seed modules.

- **2026-07-05 — ring-core rename.** `PTCACore` in the neural layer became
  `RingCore`; stale bare `ptca`/`pcta` audit prefixes were removed.

- **2026-07-16 — seed/core identity sweep.** Standalone package identities were
  reconciled into the four-layer repository, and interdependent-lib rewiring
  landed.

- **2026-07-28 — source repos archived.** `pcna`, `pcta`, and `pcsa` were
  archived after provenance-preserving migration of unique material.

- **2026-07-29 — four-layer runtime reconciliation (`0.1.1`).** One
  `CircleTensor`, neural-only reverse-mode scalar ownership, typed UCNS
  suspension/receipt handling, and external EDCM injection were reconciled into
  the scaffold runtime.

## hmmm

The minimum sufficient UCNS neural-audit observables, the architecture that will
be recovered from them, and the lawful path by which Unicode-character gonols
flow through that architecture remain unresolved. No unresolved gap authorizes
an architectural assumption.
