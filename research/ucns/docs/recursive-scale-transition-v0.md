# Recursive scale transition v0

Status: stack-local research machinery, not UCNS canon.

Actor lane: A.

## Purpose

This pass formalizes the third missing mechanic:

```text
recursive-scale transition
```

It consumes mechanic 2 closed affinization receipts and defines how a closed
whole becomes one atomic participant at a declared consuming scale. It does not
run successor validation and does not use successor observations.

## Authority Identities

```text
UCNS authority = The-Interdependency/ucns
UCNS pinned commit = 1975fe70cf4e0826a8020c2da3047569e277af64
METAPAT authority = The-Interdependency/metapat
METAPAT pinned commit = 34d954aa1e2092e615b03a180500f6b6977f501e
mechanic_1_receipt_sha256 = 351d91a1d27f9b29b4222325df0a359682c9c8dd0903fdfef8d4f73c13074194
mechanic_2_receipt_sha256 = a59d291b77c0110ffc0c401dcc94d25ad63a3372c51eab26989a5b6acf9ff68d
```

Pinned source files bound into the receipt include:

```text
research/ucns/BASE.json
research/metapat/BASE.json
stack-manifest.json
research/ucns/public_gonol_functional_operations.py
research/ucns/affinization_coupling_geometry.py
libs/ucns/CANON.md
libs/metapat/UCNS_IMPLEMENTATION.md
```

## Executable Definition

Mechanic 3 is now defined as digest-bound atomic promotion:

```text
input:
  a closed affinization receipt whose participants are recoverable and whose
  relation is intrinsic to the whole

transition:
  closed affinization receipt -> atomic participant

atomic identity:
  digest-bound source whole id, source digest, source scale, target scale, and
  coupling digest

occurrence:
  separately addressable from stable atomic identity

constituent policy:
  recoverable by receipt, not reopened by default at the consuming scale
```

Sample transition:

```text
atomic_id = ucns.atomic:45ec51dd8b19dbcd9f63e23b7c4496de844d815456961a6c3914b58902a10087
sample_digest = f6ddd881c3a4f306d656a6bb3514f8727efa5888fdc10f8619279edbf18e7e0a
```

## Tests

The tests verify:

- pinned UCNS, METAPAT, mechanic-1, and mechanic-2 identities are bound;
- only closed affinization receipts can be promoted;
- participants must remain recoverable;
- the relation must remain intrinsic to the whole;
- the same source whole and target scale produce the same atomic identity;
- repeated occurrences remain separately addressable;
- changing target scale rotates atomic identity;
- constituent references remain recoverable without reopening by default;
- transition receipts replay byte-identically.

## Rejected Alternatives

- promoting unclosed couplings;
- dropping constituent provenance at atomic scale;
- reopening constituents by default in the consuming construction;
- collapsing repeated occurrences into one occurrence address;
- using successor observations to tune atomic identity.

## Falsification Conditions

Mechanic 3 is falsified or must be revised if:

- pinned UCNS, METAPAT, mechanic-1, or mechanic-2 source identities change
  without refreshing this receipt;
- promotion accepts a value without a closed affinization receipt;
- promotion accepts a closed receipt whose participants are not recoverable;
- promotion accepts a closed receipt whose relation is not intrinsic to the
  whole;
- the same source whole and target scale produce different atomic identities
  under replay;
- different target scales do not rotate atomic identity;
- repeated occurrences collapse into one occurrence record;
- source whole id, source digest, source scale, target scale, coupling digest,
  or constituent references are lost;
- later UCNS authority supplies an incompatible recursive-scale transition law.

## Promotion Evidence

To promote this from candidate machinery to usable UCNS research machinery:

- UCNS research must decide whether digest-bound atomic promotion is sufficient
  or requires carrier-coordinate placement;
- the transition must consume mechanic-2 closed receipts without modifying
  mechanics 1 or 2 after outcome inspection;
- negative tests must keep rejecting unclosed, provenance-dropping, and
  non-intrinsic relation inputs;
- only after review should the successor experiment be resumed with mechanics 1
  through 3 frozen.

## Receipt And Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/recursive_scale_transition.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_recursive_scale_transition.py
```

Frozen receipt:

```text
receipt_schema = the-interdependency.stack-research.ucns.recursive-scale-transition
receipt_version = 0.1.0
producer_code_reference = sha256:882b2defbc88c686011a3c66d1e7d080adc9623b219a91a4253c0378b69292f1
receipt_sha256 = 3297ced3efb9c127a01337d479ce8382b771ea9d2ab66faa7e79a0ec2a197496
```

## Claims Supported

- Closed affinization receipts can be promoted into atomic participants at a
  declared consuming scale.
- Atomic identity is deterministic and scale-sensitive.
- Occurrences remain separately addressable.
- Source constituents remain recoverable by receipt.

## Claims Not Supported

This pass does not establish:

- UCNS canon;
- the selected recursive-scale law;
- next-scale carrier placement;
- a successor constructor;
- PCEA runtime behavior or key research;
- cryptographic security, entropy, hardness, replay resistance, recovery, or
  public authenticity.

## hmmm

- Whether digest-bound atomic promotion is the selected UCNS recursive-scale law
  remains unresolved.
- Exact next-scale carrier placement remains unresolved.
- Direct coupling across non-adjacent recursive scales remains unresolved.
- Successor validation remains paused until the three mechanics are reviewed as
  dependency-complete.

## Next Dependency-Complete Action

Review mechanics 1 through 3 as a frozen dependency chain before resuming any
successor validation experiment.
