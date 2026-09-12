# Public Gonol functional operations v0

Status: stack-local research machinery, not UCNS canon.

Actor lane: A.

## Purpose

This pass formalizes the first missing mechanic before any successor experiment
continues:

```text
Public Gonol functional operations
```

The goal is not to discover the next gonol. The goal is to define what can be
executed on the pinned 157-position Public Gonol object without importing glyph
semantics, numerical interpolation, or successor observations.

## Authority Identities

```text
UCNS authority = The-Interdependency/ucns
UCNS pinned commit = 1975fe70cf4e0826a8020c2da3047569e277af64
stack_work_graph_sha256 = 0760abd60f089266405aa589063a7533f485761e2bd25faa44f2eac64fb89f7d
public_gonol_sha256 = 55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5
```

Pinned source files bound into the receipt:

```text
research/ucns/BASE.json
stack-manifest.json
libs/ucns/CANON.md
libs/ucns/docs/GEOMETRY.md
libs/ucns/src/ucns/public_gonol.py
```

UCNS canon and `stack/libs/ucns` remain untouched.

## Executable Definition

Mechanic 1 is now defined as a carrier-operation layer:

```text
carrier address:
  one exact index/glyph pair on the pinned 157-position object

operation:
  a total function from carrier positions to carrier positions

admissible transformation:
  a total bijection over all 157 carrier positions

composition:
  second operation after first operation, by carrier index

closure:
  deterministic receipt over operation identity, mapping digest, complete
  transform, carrier provenance, standing, nonclaims, hmmm, and falsification
  conditions

participation:
  occurrence-addressed application retaining occurrence identity, relation
  context, input address, output address, operation identity, operation digest,
  and carrier digest
```

Implemented operations:

| Operation | Standing | Basis | Closure digest |
|---|---|---|---|
| `public_gonol.identity` | pinned-carrier-identity | identity | `78525a317ca8882b37fe190d7bdce78cc29f6060ca724604cc366d59a43c13d1` |
| `public_gonol.cyclic_order_motion:+1` | stack-local-candidate | cyclic order motion | `843690f88f7c0e3a3996ab69e6335fe5dd7d4a757e8fdfa0c9a2eaa4910c89b2` |
| `public_gonol.cyclic_order_motion:+2` | stack-local-candidate | cyclic order motion | `bcf1194389f3579ee483b6e42ba5bd9e103887986e073f5b46a4cc77c030ab4b` |
| `public_gonol.cyclic_order_motion:+3` | stack-local-candidate | composed cyclic order motion | `fcdfb521a32a07442b90ad146a97e729799dcfac64fabe978d7fb9066051d1d2` |

The cyclic operations are executable research machinery. They are not selected
UCNS canon until UCNS authority confirms wrap topology and orientation.

## Composition And Closure

The tests verify:

- identity is a two-sided neutral operation;
- cyclic operations compose deterministically by carrier index;
- composition is associative under application;
- admissible transformations are bijective over all 157 positions;
- malformed cyclic motions, out-of-carrier outputs, and non-bijective
  transformations are rejected;
- closure receipts replay byte-identically.

## Rejected Alternatives

- glyph class operations;
- Unicode name operations;
- punctuation or grammar operations;
- lexical or mathematical symbol interpretation;
- partial carrier maps;
- non-bijective transformations promoted as admissible transformations;
- successor-number fitting.

## Falsification Conditions

Mechanic 1 is falsified or must be revised if:

- the pinned UCNS source commit or Public Gonol digest changes without refreshing
  this receipt;
- an operation maps any input outside the pinned 157-position carrier;
- an admissible transformation is not bijective over all 157 positions;
- composition fails identity or associativity checks under application;
- closure receipts are not byte-identical under deterministic replay;
- participation records omit occurrence identity, input, output, operation
  identity, carrier digest, or operation digest;
- later UCNS authority rejects cyclic order motion as a valid Public Gonol
  topology;
- later UCNS authority supplies position-specific function operations that
  conflict with this carrier-only operation layer.

## Promotion Evidence

To promote this from candidate machinery to usable UCNS research machinery:

- UCNS canon or an accepted UCNS research receipt must explicitly authorize at
  least one non-identity Public Gonol operation;
- the authorized operation must retain exact carrier membership, occurrence
  identity, and deterministic replay;
- the operation must be consumed by an executable coupling geometry without
  changing its definition after outcome inspection;
- negative tests must demonstrate rejection of non-total, out-of-carrier,
  non-bijective, or provenance-dropping variants.

## Receipt And Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/public_gonol_functional_operations.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_public_gonol_functional_operations.py
```

Frozen receipt:

```text
receipt_schema = the-interdependency.stack-research.ucns.public-gonol-functional-operations
receipt_version = 0.1.0
producer_code_reference = sha256:bf81a18b9074ce10232e73afa42d23690f4172c9b60b0284a986abbf5738a1d3
receipt_sha256 = 351d91a1d27f9b29b4222325df0a359682c9c8dd0903fdfef8d4f73c13074194
```

## Claims Supported

- The pinned 157 Public Gonol now has an executable stack-local operation layer.
- Composition, admissible transformation checks, closure receipts, and
  occurrence-addressed participation records are test-backed.
- The mechanic does not use successor observations or interpolation controls.
- The mechanic does not assign glyph semantics.

## Claims Not Supported

This pass does not establish:

- UCNS canon;
- a successor constructor;
- PCEA runtime behavior or key research;
- glyph, Unicode, punctuation, lexical, mathematical, or grammar semantics;
- cryptographic security, entropy, hardness, replay resistance, or public
  authenticity.

## hmmm

- Cyclic order motion remains a stack-local candidate until UCNS canon confirms
  wrap topology and orientation.
- The exact operation expressed by each Public Gonol function position remains
  unresolved.
- Coupling geometry that consumes closed Public Gonol operations remains
  unresolved.
- Recursive-scale participation of closed operations remains unresolved.

## Next Dependency-Complete Action

Research mechanic 2: use closed Public Gonol operations as inputs to an
executable affinization/affixiation coupling geometry candidate without changing
mechanic 1 after outcome inspection.
