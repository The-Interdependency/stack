# URPCS relational carrier v0 — read-only architecture audit

Classification: **RELATION_PRESENT_SHEET_RELATION_NOT_INVARIANT**.

The native multi-origin relation is present, but narrower than a global or peer-origin coordinate: canonical `LayerWire(G^r)` bytes become the exact input to layer `r+1`, where they are partitioned into successor origins and occurrence spans. Pairing and attachment remain local to one origin. URPCS v1 defines no origin phase, origin-to-origin phase transport, synchronization, traversal, or typed event-promotion law.

The proposed relative visible phase is invariant under equal native motion, but the naive endpoint sheet product is not. Therefore the proposed `(delta_phase, sheet_product)` relation does **not** satisfy the requested common-rotation invariance without an additional coordinate-covariant comparison/transport law.

This analyzer is read-only. It changes no v1 serialization, state transition, vector, receipt, traversal, or UCNS law.

## Evidence identity

- Canonical receipt SHA-256: `f415c486df88cd3d0f8c6ad861d375e01553eba58f3f5a2807e1e23b097b419b`
- Receipt payload SHA-256: `c6c1f165bb6c10b5e88fa74d86d27eca0191ab71ef6dd3cb399ef3d6a069aff5`
- Measurement SHA-256: `e92f610bae2fe6b59c6c3ea41e680edf703365b11181a58912e2b5082bf9b355`
- Aggregate graph SHA-256: `0cb0323135ffdc6aed5270b41ead24c43d80e189aae27593238386c74b0fbe15`
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
- Equal native-motion checks: 120; relative-phase changes: 0; naive sheet-product changes: 44.
- Common-action classification: **PHASE_INVARIANT_SHEET_PRODUCT_NOT_INVARIANT**. No privileged global zero was selected.

| Added component | Colliding pairs separated |
|---|---:|
| sheet/frame | 0 |
| origin | 1015708 |
| gonol identity | 172 |
| arity and shape | 1066 |
| provenance | 1237 |
| full transformation history after provenance | 0 |

Within pairs still joined at `(origin, gonol, phase, sheet)`, arity/shape alone separates 0, provenance alone separates 171, both differ for 1066, and neither differs for 0.

The frame supplies no additional distinction in this declared corpus. Origin and gonol identity contribute at their declared lattice steps; arity/shape and provenance contributions overlap as quantified above. Transformation history adds no further split after case-scoped provenance is already included. These are representation contributions, not utility or security claims.

The requested torsor-style check exposes a missing law: equal native Möbius motion preserves relative visible phase, but the naive product of endpoint frame signs can change when one endpoint crosses the quotient seam. A coordinate-covariant frame comparison would require an explicit native comparison/transport law; this audit does not invent one.

## Serialization boundary

- Boundaries observed: 2
- Byte loss: none; canonical LayerWire re-encoding and inverse expansion are byte-identical
- Created by recursion: successor origins, successor occurrences, successor gonols, successor attachments
- Not preserved as typed edges: source-origin to target-origin semantic correspondence, source local phase/sheet transport, typed transformation-event identity

## Candidate capacities

| Capacity | Classification |
|---|---|
| common-rotation-invariant relative phase and sheet | **PHASE_INVARIANT_SHEET_PRODUCT_NOT_INVARIANT** |
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
- Equal native Möbius motion preserves relative visible phase but can change the naive product of endpoint frame signs; v1 has no covariant frame-comparison transport law.

## Explicit nonclaims

This work does not establish traversal utility, compression, entropy, confidentiality, encryption security, IND-CPA or IND-CCA security, production suitability, PCEA compatibility, UCNS-gonol identity, UCHC cache behavior, absolute winding recovery, release authority.

## hmmm

Equal native motion falsifies invariance of the naive endpoint sheet product, so a coordinate-covariant frame comparison remains a missing law. Whether exact byte provenance warrants typed origin transport, synchronization, traversal, or event promotion is also unresolved; v1 supplies none of those laws.
