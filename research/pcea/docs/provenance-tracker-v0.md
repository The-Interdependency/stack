# PCEA provenance tracker candidate v0

Status: stack-local research note, not canon.

Actor lane: A.

## Source identity

This candidate is bound to `research/pcea/BASE.json`:

```text
source_repository = The-Interdependency/pcea
source_commit = 4d2c581448b97bfb71da92b35487e74e6e3bcedc
canon_path = ../../libs/pcea
standing = stack-local-research
```

`../../libs/pcea/` is read-only imported canon for this workspace. Any accepted
runtime PCEA change must route upstream to `The-Interdependency/pcea` first, then
return through a refreshed stack pin.

## Candidate claim

PCEA can be evaluated as a deterministic state-lineage transform for provenance
tracking:

```text
same previous state + same current state + same address/config -> same lineage output
changed previous state/current state/address/config -> changed lineage output
```

This is a replay and fork-detection claim. It is not a public authenticity,
timestamp, ownership, dataset-truth, or cryptographic-hardness claim.

## Receipt envelope

A defensible provenance receipt should bind at least:

```text
schema
source_repository
source_commit
stack_manifest_digest
pcea_word_bits
state_shape
state_digest
last_state_digest
previous_receipt_digest
pcea_lineage_digest
public_projection_digest
created_by_actor_lane
hmmm
```

The `pcea_lineage_digest` can be a SHA-256 digest of canonical JSON containing
the PCEA output and exact config. That digest is evidence for byte-identical
replay under the same local inputs. It does not identify who produced it unless
another layer authenticates the receipt.

## Public Gonol position

The UCNS Public Gonol carrier may be used only as public projection or
vocabulary identity here. The stack-pinned UCNS carrier declares:

```text
module = ucns.public_gonol
arity = 157 positions
digest = 55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5
```

That means a receipt may point to an exact public position/glyph vocabulary.
It does not mean the Public Gonol supplies authentication, encryption, ordering
truth, or a hidden operation. Any such operation needs its own construction and
evidence.

## Non-claims

This candidate does not establish:

- public authorship;
- trusted timestamping;
- dataset provenance truth;
- third-party verifiability;
- resistance to forged receipts;
- cryptographic security of PCEA;
- Public Gonol security or position operations.

Those require separate mechanisms such as digital signatures, HMAC verifier
keys, transparency logs, trusted timestamps, or institutional attestations.

## Next executable gate

The first implementation gate should be a deterministic receipt generator under
`research/pcea/`, with tests proving:

```text
receipt replay is byte-identical
changing current state changes the receipt
changing last_state changes the receipt
changing source_commit changes the receipt
public projection digest is stable and separately labeled non-authenticating
libs/pcea is not modified
```

Until that exists, the standing is:

```text
PCEA_AS_PROVENANCE_TRACKER = PROPOSED
PUBLIC_AUTHENTICITY_RECEIPTS = UNRESOLVED
PUBLIC_GONOL_ROLE = OPTIONAL_PUBLIC_PROJECTION_ONLY
SECURITY_CLAIM = NOT_MADE
```

## hmmm

- The stack PCEA base is `4d2c5814...`, while later arity work may exist in the
  upstream PCEA repository. Do not transfer those results here without an
  explicit stack pin refresh or separate receipt.
- The right public authenticity layer is not selected.
- The right canonical JSON/state serialization for large neural state is not
  selected.
- Public Gonol projection may be useful for display, indexing, or semantic
  routing, but that remains separate from receipt authenticity.
