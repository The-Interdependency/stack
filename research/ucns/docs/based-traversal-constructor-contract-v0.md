# Based-traversal constructor contract v0

**Standing:** stack-local fail-closed constructor contract. Not UCNS canon,
not a completed traversal constructor, and not PCEA work.

## Purpose

The provenance audit established that current and historical material does not
define a canonical based traversal. This contract makes the dependency boundary
executable. It does not fill missing geometry.

The five fields are evaluated in this order:

```text
origin attachment
    -> directed tangent / chirality
        -> rotation system
            -> marked outgoing dart
                -> closure rule
```

The first field without an authority-bound intrinsic UCNS derivation stops the
constructor. No later field is guessed or evaluated after that point.

## Admission rule

A field derivation must bind:

- `The-Interdependency/ucns` authority;
- the exact pinned UCNS commit;
- an identified geometric operation and source paths;
- the input geometry digest;
- a machine-readable output;
- intrinsic-geometry selection basis;
- a deterministic replay digest.

Carrier tuple order, source text order, caller order, API defaults, construction
or commit order, prose adjacency, ids, hashes, PCEA expectations, and observed
gonol numbers are forbidden selector bases.

Structurally valid evidence is still not admitted automatically. A derivation
must be explicitly registered in the contract from canonical UCNS geometry.
The current registry is empty.

## First field

Pinned authority contains three relevant primitives:

```text
Public Gonol carrier origin index               = 0
direct Mobius Structural Null carrier position  = 0
carrier Structural Null                         = coordinate-free
```

The recursive groupoid research also has a model base object. What is absent is
the geometric morphism between them:

```text
Public Gonol / Structural Null origin
    -- no authoritative attachment operation -->
one recursive return-groupoid object
```

An origin address is not an attachment. The contract therefore stops before it
asks which tangent or chirality leaves that object.

## Sequential result

| Field | Result |
|---|---|
| `origin_attachment` | `MISSING_AUTHORITATIVE_GEOMETRIC_DERIVATION` |
| `directed_tangent_or_chirality` | `NOT_EVALUATED_DEPENDENCY_BLOCKED` |
| `rotation_system` | `NOT_EVALUATED_DEPENDENCY_BLOCKED` |
| `marked_outgoing_dart` | `NOT_EVALUATED_DEPENDENCY_BLOCKED` |
| `closure_rule` | `NOT_EVALUATED_DEPENDENCY_BLOCKED` |

```text
STATUS     = STOP_MISSING_ORIGIN_ATTACHMENT
HMMM FIELD = origin_attachment

constructor certificate = null
traversal word           = null
attaching word           = null
monodromy                = null
arithmetic readout       = null
successor                = null
PCEA handoff permitted   = false
```

This is not a claim that fields two through five are impossible. They are not
evaluated because their prerequisite is absent.

## Completion contract

If all five fields later become authority-bound and executable, a completed
UCNS constructor must emit:

- exact UCNS repository, commit, tree, constructor, and input identities;
- all five ordered field derivations and their replay digests;
- attached origin object;
- selected direction;
- rotation system;
- marked outgoing dart;
- closure witness;
- deterministic traversal word;
- canonical certificate digest.

Independent replay must recompute every field and traversal from the pinned
input geometry and reproduce the certificate digest. Only that completed
certificate may cross the UCNS-to-PCEA boundary.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/based_traversal_constructor_contract.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_based_traversal_constructor_contract.py -v
```

Frozen identities:

```text
UCNS pinned tree                         = 06c2fe6cf2e148d610808c6f00f4a26e85f43d62
geometry-selection receipt payload       = 4c4f06aae237fd4ce771dc7849738617b0cbc9ab3cc5bd6685ffec84b2921a09
provenance-history receipt payload        = ed08c5315ab7dc6988985455d7226ced9151481883b7b8bbb0050ffc2bbc82e2
constructor-contract module sha256        = c31dd280c1c5e91a986214fa0ba646aa655cc36044c7374db83b526c79ec20e1
test module sha256                        = e1fb76c75947a004888d6a3784f7f6a6dd7c05e5db2619ff643899c0ca339ef4
canonical receipt payload sha256          = 12100f1bd08d76d2b86bd3d4b7786b5e7bde07fda789dc2937817990c7a5849a
formatted receipt file sha256             = 9688ff0407d3c72f5b7adb4c2bdb8bd0fb5602635987cf31eb0dba5528e41874
```

## hmmm

`origin_attachment` requires an authoritative UCNS operation identifying the
intrinsic source origin, the recursive target path object, and why that map is
geometrically selected. Until that operation exists, constructor research stops
at this field.
