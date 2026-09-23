# URPCS relational carrier v0 — read-only architecture audit

Classification: **RELATION_PRESENT_WITH_BLOCKED_CAPACITIES**.

The native multi-origin relation is present, but narrower than a global or peer-origin coordinate: canonical `LayerWire(G^r)` bytes become the exact input to layer `r+1`, where they are partitioned into successor origins and occurrence spans. Pairing and attachment remain local to one origin. URPCS v1 defines no origin phase, origin-to-origin phase transport, synchronization, traversal, or typed event-promotion law.

This analyzer is read-only. It changes no v1 serialization, state transition, vector, receipt, traversal, or UCNS law.

## Evidence identity

- Canonical receipt SHA-256: `08e9d8d951331d2298527298119f2a35280decb515eed6809b6697d39a07a700`
- Receipt payload SHA-256: `72bcd15c065f34c88a8b13b0b27d79cc599ebd3160583d270b884153407bcb05`
- Measurement SHA-256: `9ea9428ece73c4b1f9b190cf76d43e54db4c5de502e7828e9361f6fd38683cf4`
- Aggregate graph SHA-256: `4ccfdfff0a4ef82fa6cf5de64e43c2d85668e67d5a2cd905261747bb62601137`
- Corpus identity SHA-256: `8b0e356f23c462761ac4a036d37d36830879803faf72bb34d96f5bd9a44b8c62`
- Governing Stack commit/tree: `164f86ce2cb640242dbfb06390330142e90a406e` / `de450f1355bf2c9d7f178b0f3f770ed05460a3a7`
- UCNS commit/law: `4086ab82399c4d142b0eacfbc09e0a69ed151aa5` / `ucns.native-mobius-root-loop@1.0.0`
- skill-lib commit/tree: `22c2c5702d14fb4b0faeb717777ecab2665770a1` / `6e483e484d5682e638de5f0957224d37993643dd`
- METAPAT consultation commit/tree: `e4165b0cac9eca41daef9c2f941881028ca55d48` / `9918f1188f64a517745851514804deb5fcae9c96`

## Source-backed relation

First-task classification: **MULTI_ORIGIN_RELATION_PRESENT**.

LayerWire(G^r) is the exact byte input D^(r+1), then partitioned into successor region origins and occurrence bit intervals.

- Within a layer: pairing and attachment relate objects only inside one origin; no relation joins peer origins
- Across layers: serialization relates a whole source layer to successor input spans; it does not define semantic origin-to-origin phase transport
- Invertibility: byte-exact when the complete authenticated successor layer and witness are present
- Direct origin-to-origin edges observed: 0
- Canonical graph size: 3337 nodes and 7845 edges
- Directed cycles observed: 0

## Declared corpus

all eight committed URPCS vectors; every tracked research/urpcs artifact at PR #54 head; four deterministic probes only for native relations absent from committed positive traces.

the trace population is the complete declared corpus, not an exhaustive plaintext, key, or state domain.

| Trace | Source | Nodes | Edges | Local observations |
|---|---|---:|---:|---:|
| `empty_r0` | committed-positive-vector | 3 | 2 | 0 |
| `empty_r1` | committed-positive-vector | 343 | 804 | 279 |
| `odd_09_r0` | committed-positive-vector | 8 | 11 | 5 |
| `generated_odd_09_r1` | deterministic-generated-unrepresented-nonempty-recursion | 2966 | 7006 | 2445 |
| `generated_state_chain_0` | deterministic-generated-state-transition-chain | 3 | 2 | 0 |
| `generated_state_chain_1` | deterministic-generated-state-transition-chain | 8 | 11 | 5 |
| `generated_state_chain_2` | deterministic-generated-state-transition-chain | 6 | 7 | 3 |

The prior 514-case Möbius receipt is preserved and consumed only as a narrow fixed-harness baseline. Its absence of winding in one-byte inputs does not resolve the contribution of recursive relations.

## Ablation lattice

| Projection | Classes | Max multiplicity | Colliding pairs retained | Pairs separated at step |
|---|---:|---:|---:|---:|
| `phase` | 6 | 1158 | 1017117 | None |
| `phase_sheet` | 6 | 1158 | 1017117 | 0 |
| `origin_phase_sheet` | 1613 | 4 | 1409 | 1015708 |
| `origin_gonol_phase_sheet` | 1677 | 4 | 1237 | 172 |
| `origin_gonol_arity_phase_sheet_provenance` | 2737 | 1 | 0 | 1237 |
| `full_relational_transformation_history` | 2737 | 1 | 0 | 0 |

- Identities in shared visible-angle classes: 2737
- Identities in shared phase-and-sheet classes: 2737
- Identifiers and geometry remain separate dimensions; these multiplicities are not called complete-state collisions.
- Common phase rotation preserves every measured relative phase and sheet product; no privileged global zero was selected.

| Added component | Colliding pairs separated |
|---|---:|
| sheet/frame | 0 |
| origin | 1015708 |
| gonol identity | 172 |
| arity and shape | 1066 |
| provenance | 1237 |
| full transformation history after provenance | 0 |

The frame supplies no additional distinction in this declared corpus. Origin, gonol identity, arity/shape, and provenance do; transformation history adds no further split after case-scoped provenance is already included. These are representation contributions, not utility or security claims.

## Serialization boundary

- Boundaries observed: 2
- Byte loss: none; canonical LayerWire re-encoding and inverse expansion are byte-identical
- Created by recursion: successor origins, successor occurrences, successor gonols, successor attachments
- Not preserved as typed edges: source-origin to target-origin semantic correspondence, source local phase/sheet transport, typed transformation-event identity

## Candidate capacities

| Capacity | Classification |
|---|---|
| exact provenance recovery | **SUPPORTED_FOR_COMPLETE_AUTHENTICATED_TRACE** |
| mutation localization | **DETECTION_ONLY_AT_AUTHENTICATION_BOUNDARY** |
| divergent-state and fork detection | **SUPPORTED_AT_NEXT_USE_AND_HOST_CAS_BOUNDARY** |
| cycle consistency and nontrivial holonomy | **ABSENT_IN_AVAILABLE_NATIVE_GRAPH** |
| synchronization between independently processed origins | **BLOCKED_MISSING_RELATION** |
| reconstruction from multiple partial projections | **SUPPORTED_ONLY_FOR_COMPLETE_PARTITION** |
| stable interlacing of three, five, and seven logical streams | **BLOCKED_MISSING_RELATION** |
| contextual authorization requiring complete relational agreement | **BLOCKED_MISSING_POLICY** |
| promotion of transformation events into the next recursive layer | **RAW_RESULT_RECURS_TYPED_EVENT_BLOCKED** |

Each capacity has its source evidence, limitation, and any missing law in the canonical JSON. Blocked branches do not stop independent supported branches.

## Unexpected findings

- The native multi-origin relation is whole-layer byte serialization followed by successor partitioning, not a direct relation between peer origins.
- The empty depth-one committed vector already creates many successor origins even though its source plaintext is empty.
- URPCS v1 assigns local phase to gonols and members, not to origins; origin phase/sheet would require a new law.
- Recursion preserves source bytes exactly while dropping the type of the transformation event: resulting bytes recur, the event does not.

## Explicit nonclaims

This work does not establish traversal utility, compression, entropy, confidentiality, encryption security, IND-CPA or IND-CCA security, production suitability, PCEA compatibility, UCNS-gonol identity, UCHC cache behavior, absolute winding recovery, release authority.

## hmmm

Whether the exact byte-provenance relation warrants a typed origin transport, synchronization, traversal, or event-promotion law remains unresolved; v1 supplies none of those laws.
