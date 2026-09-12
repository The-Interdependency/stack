# Affinization coupling geometry v0

Status: stack-local research machinery, not UCNS or METAPAT canon.

Actor lane: A.

## Purpose

This pass formalizes the second missing mechanic:

```text
UCNS affinization/affixiation and coupling geometry
```

It consumes mechanic 1 closed Public Gonol operation receipts and defines an
explicit ordered incidence-coupling candidate. It does not infer coupling from
overlap, adjacency, ambient membership, provenance, glyph semantics, or
successor observations.

## Authority Identities

```text
UCNS authority = The-Interdependency/ucns
UCNS pinned commit = 1975fe70cf4e0826a8020c2da3047569e277af64
METAPAT authority = The-Interdependency/metapat
METAPAT pinned commit = 34d954aa1e2092e615b03a180500f6b6977f501e
METAPAT relation policy = constitutive-simultaneous, explicit-only
mechanic_1_receipt_sha256 = 351d91a1d27f9b29b4222325df0a359682c9c8dd0903fdfef8d4f73c13074194
```

Pinned source files bound into the receipt include:

```text
research/ucns/BASE.json
research/metapat/BASE.json
stack-manifest.json
libs/ucns/CANON.md
libs/ucns/docs/GEOMETRY.md
libs/metapat/README.md
libs/metapat/UCNS_IMPLEMENTATION.md
libs/metapat/src/metapat/ucns_phi.py
research/ucns/public_gonol_functional_operations.py
```

## Executable Definition

Mechanic 2 is now defined as explicit ordered incidence geometry:

```text
participant:
  occurrence-addressed item with participant id, scale, role, and source digest

coupling:
  explicit ordered relation over two or more participants

admitted relation kind:
  constitutive-simultaneous

degree:
  slot-sensitive incidence count over explicit couplings

closure:
  deterministic whole retaining intrinsic relation and recoverable participants

forbidden inference:
  overlap, adjacency, ambient membership, and provenance alone do not create a
  coupling
```

Sample closed affinization:

```text
whole_id = ucns.affinization:026030f844d47b679dff6a1b24c473162caf8ad5ea2a2461aabeb1b0f5026ecc
sample_digest = 1f7ea6d1c205f9bb590203069c97425aa037ac1fe7ccc38b51e8575468eb9a03
```

The sample couples two mechanic-1 closed Public Gonol operations:

```text
slot 0 = mechanic1.closed-operation.identity
slot 1 = mechanic1.closed-operation.cyclic-step-one
```

## Tests

The tests verify:

- pinned UCNS, METAPAT, and mechanic-1 receipt identities are bound;
- only explicit ordered couplings are admitted;
- prohibited relation kinds fail closed;
- duplicate occurrence ids fail closed;
- overlap-derived coupling fails closed;
- reversing participant order rotates the coupling digest;
- degree records slot-specific incidence;
- closed affinization receipts replay byte-identically.

## Rejected Alternatives

- overlap-derived coupling;
- adjacency-derived coupling;
- ambient power-set coupling;
- order-insensitive coupling;
- provenance-only containment;
- theorem or measurement status transfer;
- successor-number fitting.

## Falsification Conditions

Mechanic 2 is falsified or must be revised if:

- pinned UCNS, METAPAT, or mechanic-1 source identities change without
  refreshing this receipt;
- a coupling is accepted without an explicit ordered participant tuple;
- a prohibited relation kind is accepted as constitutive coupling;
- duplicate participant occurrence ids are accepted inside one coupling;
- overlap, adjacency, ambient membership, or provenance alone creates a
  coupling;
- reversing participant order leaves the coupling digest unchanged;
- degree fails to retain slot-specific incidence;
- closure receipts are not byte-identical under deterministic replay;
- closed receipts fail to preserve participant identity, scale, role, source
  digest, slot, and coupling digest;
- later UCNS authority requires a coordinate coupling law incompatible with this
  incidence candidate.

## Promotion Evidence

To promote this from candidate machinery to usable UCNS research machinery:

- UCNS research must bind this incidence layer to an explicit coordinate or
  topological coupling realization;
- METAPAT constitutive relation authorization must remain exact and
  status-transfer fields must remain false;
- negative tests must keep rejecting prohibited relation kinds and
  overlap-derived closure;
- mechanic 3 must consume the closed affinization receipt without changing
  mechanic 2 after outcome inspection.

## Receipt And Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/affinization_coupling_geometry.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_affinization_coupling_geometry.py
```

Frozen receipt:

```text
receipt_schema = the-interdependency.stack-research.ucns.affinization-coupling-geometry
receipt_version = 0.1.0
producer_code_reference = sha256:65c5bbee87fa1a5cb9119c19a8e186b62827e55a91b17c4111aa06b8df0ce21a
receipt_sha256 = a59d291b77c0110ffc0c401dcc94d25ad63a3372c51eab26989a5b6acf9ff68d
```

## Claims Supported

- Closed Public Gonol operation receipts can be consumed by an explicit ordered
  coupling candidate.
- Coupling order, participant identity, scale, role, source digest, degree, and
  slot incidence are executable and test-backed.
- Coupling is not inferred from overlap or ambient membership.

## Claims Not Supported

This pass does not establish:

- UCNS canon;
- METAPAT canon;
- the final coordinate embedding of UCNS coupling;
- a successor constructor;
- theorem, ontology, measurement, or proof-status transfer;
- cryptographic security, entropy, hardness, replay resistance, or public
  authenticity.

## hmmm

- Exact coordinate embedding of coupling on the UCNS carrier remains unresolved.
- Whether ordered incidence is sufficient geometry for recursive-scale
  transition remains unresolved.
- Direct coupling across distant scales remains unresolved.
- How completed affinization receipts become Public Gonol participants remains
  unresolved until mechanic 3.

## Next Dependency-Complete Action

Research mechanic 3: derive recursive-scale transition over closed affinization
receipts without changing mechanics 1 or 2 after outcome inspection.
