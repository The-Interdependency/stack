# Hilbert inference candidate

Status: **Stack-forged candidate**. This document records the mathematical
contract requested for UCHC inference without prematurely transferring English
Gonol implementation/public-contract authority out of Stack.

Work graph:
[`../HILBERT_INFERENCE_WORK_GRAPH.json`](../HILBERT_INFERENCE_WORK_GRAPH.json).

## Construction

The correction is recursive basis formation:

```text
admitted glyph axes
  -> ordered glyph-axis tensor
  -> closed word
  -> word axis
  -> ordered higher-scale tensor
```

There is no intervening Cartesian `x/y/z` embedding. The glyph's existing
axis participation is the basis direction at `O_G`. Closing a word preserves
its ordered glyph construction and promotes the completed word into its existing
axis at `O_W`. A higher-scale construction consumes the closed word axis rather
than repeatedly flattening the word back into glyph coordinates.

For an admitted glyph-axis set `G` and an explicitly selected scalar field
`F ∈ {R, C}`, the bounded glyph space is

[
H_G(F) = \ell^2(G; F).
]

The admitted glyph axes are an orthonormal basis inside that origin:

[
\langle g_i \mid g_j \rangle = \delta_{ij}.
]

For a word with exact construction

[
w = g_1 g_2 \ldots g_n,
]

the pre-promotion state is

[
|g_1\rangle \otimes |g_2\rangle \otimes \cdots \otimes |g_n\rangle.
]

Order and multiplicity are constitutive. `ab`, `ba`, and `aa` are distinct
tensor states. Closure promotes that construction to

[
|w\rangle \in H_W(F),
]

where the word is now itself an axis available to later construction. Definition
construction repeats the same rule over its exact ordered closed components.

Every emitted axis carries both the logical construction receipt and the
physical artifact SHA-256. Corpus-local numeric IDs are never sufficient axis
identity.

## Domain-qualified mathematical claims

These records resolve the meaning-bearing terms used by the candidate. Their
mathematical senses are borrowed rather than redefined.

| Claim ID | Term | Included sense | Excluded sense / collision | Status |
| --- | --- | --- | --- | --- |
| `stack.english-gonol.inference-math.hilbert-space` | Hilbert space | complete inner-product space over explicitly selected `R` or `C`; bounded origin spaces are finite-dimensional and therefore complete | not a synonym for UCNS carrier geometry, a renderer, or an O/S/C candidate channel tuple | operator-ratified candidate placement; independent UCHC authority pending graduation |
| `stack.english-gonol.inference-math.basis` | basis | the already-declared construct-qualified glyph/word/definition axes at their respective origins | not Cartesian `x/y/z`; not Public Gonol carrier position | operator-ratified candidate placement |
| `stack.english-gonol.inference-math.vector` | Hilbert state vector | a mathematical element of one declared origin-local Hilbert space | **not** METAPAT `Vector`; not UCNS displacement vector; no state-altering semantic property is imported | collision resolved by domain qualification; candidate |
| `stack.english-gonol.inference-math.inner-product` | inner product | origin-local orthonormal basis product; complex case conjugates the left factor | no cross-origin angle or similarity law is implied | candidate; cross-origin law remains hmmm |
| `stack.english-gonol.inference-math.tensor-product` | tensor product | ordered product of already-closed axis factors, preserving order and multiplicity | not concatenation, averaging, bag-of-axes flattening, or mandatory adjacent-scale traversal | operator-ratified candidate placement |

### Authority source and collision record

- English Gonol Construction owns the text-domain construction candidate.
- UCNS owns the consumed Public Gonol/geometric construction.
- METAPAT retains its own `Vector` semantic term. The Python type
  `HilbertStateVector` is deliberately named and scoped so no equivalence is
  implied.
- The operator direction on 2026-10-01 fixes the candidate architecture:
  UCHC inference is Hilbert-space based; glyph axes replace Cartesian coordinate
  axes; closed words form their own axes. An immutable public transcript identity
  for that direction remains `hmmm`.
- UCHC remains the intended independent repository. Current release,
  reconsumption, and authority-transition records do not yet establish completed
  graduation, so this executable candidate remains in Stack.

## Implemented candidate

`english_gonol.hilbert_inference` supplies:

- `ConstructRef`: logical receipt + physical artifact SHA-256 (an expected identity, not verification by itself);
- `VerifiedConstruct`: private read-only snapshot whose copied bytes and complete logical rows match that expected identity before helpers can consume it;
- `AxisRef`: origin and axis identity bound to that exact construct;
- `HilbertStateVector`: sparse origin-local vector arithmetic;
- explicit `R` or `C` selection, with no default;
- origin-local orthonormal inner product and norm;
- `OrderedTensor`: exact ordered basis factors;
- `AxisPromotion`: lower-scale tensor -> already-existing higher-scale axis;
- direct SQL dimension reads for word and definition spaces;
- word and definition promotion helpers.

No inference weight, phase, probability, meaning score, sense choice, or learned
operator is synthesized.

## Usage guidance

Open a standalone, checkpointed `construct.db` using hashes from trusted evidence.
The candidate validates the complete logical receipt once on open; subsequent
space dimensions use direct SQL counts. Bare SQLite connections are rejected.

```python
from english_gonol.hilbert_inference import (
    ConstructRef, VerifiedConstruct, word_promotion, word_space,
)

# expected_logical_receipt and expected_artifact_sha256 come from trusted evidence.
ref = ConstructRef(expected_logical_receipt, expected_artifact_sha256)
with VerifiedConstruct("construct.db", ref) as db:
    space = word_space(db, ref, scalar_field="R")
    promoted = word_promotion(db, db.inventory, admitted_word_id, ref, scalar_field="R")
```

Primitive `glyph_axis`, `word_axis`, `definition_axis`, and `glyph_space` helpers
also require the verified handle as `db=db`; supplied gonols/inventories must match
that snapshot. Source-file replacement or later source writes cannot change the
private snapshot. Live WAL/uncommitted data is outside the standalone artifact
contract. Closing the handle releases its temporary copy and blocks further reads.
Opening costs one artifact copy plus complete logical replay and requires scratch
disk for that copy; it is not repeated per helper call. Hashes identify contents,
not producer authentication.

Word factors dereference the declared ordered `word_characters` IDs and reject a
surface disagreement, including one with the same length. Finite inputs whose
inner products overflow are rejected. Sparse coordinates are canonicalized at
construction: zero and underflowed products disappear, preserving equality and
hash identity through scaling and cancellation.

## Failure definition

The candidate is falsified if any of these occur:

1. an external Cartesian basis replaces the admitted UCHC/English-Gonol axes;
2. construct identity is dropped so equal local IDs from different artifacts
   compare as the same axis;
3. word construction loses order or multiplicity;
4. a closed word fails to become its existing word axis;
5. requesting a space dimension reconstructs every member instead of reading
   the verified count directly;
6. a cross-origin or cross-construct vector inner product is silently invented;
7. `R` and `C` are mixed implicitly;
8. an O/S/C displacement/readout candidate is promoted into the definition of
   the Hilbert basis;
9. METAPAT `Vector` semantics are imported by name collision.

Run:

```bash
cd research/english-gonol
python -m pytest -q tests/test_hilbert_inference.py
```

The normal English Gonol suite remains the broader compatibility gate.

## Migration boundary

This candidate does **not** complete UCHC graduation. The independent repository
may receive this implementation only through the existing lifecycle sequence:
exact candidate artifact, forge verification, stable release, released-artifact
reconsumption, severance of the local implementation path, and a scoped
authority-transition receipt.

The existing UCHC extraction can document this as its target contract. It must
not pretend that a copied source file or a green test alone transferred
implementation authority.

## hmmm

- canonical scalar field: `R` or `C`;
- cross-origin inner products and angles;
- amplitude and phase assignment;
- learned inference operators and sense selection;
- sentence-axis promotion and later recursive scales;
- immutable public identity of the operator-ratifying design conversation;
- stable UCHC release, released-artifact reconsumption, and scoped
  implementation/public-contract authority transition.

The unresolved relations are allowed to remain unresolved because the basis and
recursive promotion contract can fail independently without inventing them.
