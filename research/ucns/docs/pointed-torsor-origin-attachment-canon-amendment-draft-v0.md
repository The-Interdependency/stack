# Structural Null jurisdiction and unresolved attachment record v1

## Repository identities

- Stack research authority: `The-Interdependency/stack` at working base
  `7e570117c88244e7ca6f2594a9e345f496a67998`. This document is stack-local
  research and is not UCNS canon.
- UCNS patch base: `The-Interdependency/ucns` at
  `dbffe8473349b385be57753141bfb2ca1906e8f9`.
- UCNS wording commit:
  `fdc0cf9b91895e991bc85922ffd5454f4d3c69e9`.
- UCNS review: [PR #220](https://github.com/The-Interdependency/ucns/pull/220),
  open and intentionally unmerged when this record was revised.

## Status split

```text
jurisdictional model      = RATIFIED
UCNS canon wording        = PR_OPEN_UNMERGED
existing behavior         = COMPATIBLE_BUT_PARTIAL
attachment                = UNRESOLVED
attachment implementation = ABSENT
implementation evidence   = HMMM
constructor modified       = false
PCEA modified              = false
```

The jurisdictional decision and the attachment question are independent. The
missing attachment codomain does not block the ratified rule about which object
owns a relation involving Structural Null.

## A. Ratified Jurisdictional Reconciliation

There is exactly one Structural Null `N`. It is singular and is not ordinary
numeric zero.

In this research record, `Int(N)` abbreviates the **intrinsic content assigned
to `N`**. It is not the topological interior operator and makes no topological
interior claim.

```text
Int(N) = empty
```

Intrinsically, `N` contains no coordinate, payload, frame, orientation, or
other structural distinction. An ambient carrier may identify, place, compare,
or relate `N` extrinsically. Every such placement or relation belongs to the
carrier and does not become intrinsic structure of `N`.

The native Mobius carrier may therefore place `N` as its singular origin
without putting an origin coordinate inside `N`:

```text
"N has an internal coordinate"                  is forbidden
"the carrier places N at its origin"            is permitted
"N internally retains a carrier relation"       is forbidden
"a carrier-owned relation has N as an endpoint" is permitted
"N carries provenance"                          is forbidden
"a receipt evidences a carrier relation to N"   is permitted
```

This is the smallest reconciliation of the prior `CANON_CONTRADICTION`. It
does not introduce a second origin and does not derive any attachment from the
intrinsically null character of `N`.

### Applied UCNS wording

The upstream patch changes only the existing Structural Null paragraph in
`CANON.md`:

```diff
-Structural Null is the singular origin of the native Mobius construction. It is not ordinary numeric zero.
+Structural Null is singular. Intrinsically, it contains no coordinate, payload,
+frame, orientation, or other structural distinction. The native Mobius carrier
+extrinsically places Structural Null as its origin, and an ambient carrier may
+place or relate it extrinsically. External placement or relation belongs to the
+carrier and does not become intrinsic structure of Structural Null. Structural
+Null is not ordinary numeric zero.
```

No source module, test, constructor, receipt, or runtime behavior is changed by
the upstream commit.

## Compatibility Verdict

Existing behavior is `COMPATIBLE_BUT_PARTIAL`.

### `carrier.py`

The singleton null sentinel has no instance payload, coordinate, metadata,
provenance, frame, or relation. Existing placement and participation are
carrier-owned operations:

```text
carrier_from_breadth(0) = N
project_C(N) = N
deck_translate_C(N) = N
lifted_preimages_C(N) = (N,)
same_position_C(N, N) = true
```

Ambient faithful breadth `B = 0` maps to the null sentinel, while numeric-zero
payload on a non-null carrier does not collapse the carrier. Numeric zero and
Structural Null remain distinct.

### `direct_mobius.py`

`STRUCTURAL_NULL_ORIGIN` is an ambient placement descriptor with an origin id
and carrier position. Under the ratified jurisdiction it is evidence about the
carrier's relation to the single `N`; its fields are not intrinsic fields of
`N`. The phase-zero `NativeMobiusState` is likewise a coordinate representative
of the framed quotient, not an internal coordinate of `N`.

The implementation does not yet expose the jurisdiction as a typed relation,
which is why compatibility is partial rather than implementation evidence for
an attachment.

### Existing receipts

Frozen origin receipts remain evidence about carrier-owned placement and
operations. Their provenance belongs to the receipt and the ambient relation,
not to `N`. They are not rewritten by this wording decision and contain no
implemented attachment or downstream constructor output.

## UCNS Gate Evidence

The one-file wording commit was checked in a clean worktree from its exact base:

```text
complete UCNS pytest suite         130 passed
skill-lib contract graph           closed
sdist and wheel build              passed
Twine check, wheel                 passed
Twine check, sdist                 passed
git diff --check                   passed
GitHub geometry CI, Python 3.10    passed
GitHub geometry CI, Python 3.12    passed
GitHub CodeQL                      passed
```

These gates establish that the wording patch does not break the current UCNS
repository. They do not provide attachment implementation evidence.

## B. Unresolved Attachment

Attachment remains `hmmm`. The earlier abstract target-space notation is
withdrawn because current UCNS canon defines no corresponding native vertex
ontology. No new ontology is inferred to rescue that notation.

The unresolved candidate has only this licensed boundary:

```text
source object      = the single Structural Null N
attachment name    = iota (research placeholder only)
codomain           = hmmm
target             = hmmm
pointing           = hmmm
map                = absent
evidence           = hmmm
```

No residual-symmetry consequence is currently claimed. A residual `C2`
reversal was a conditional consequence of the earlier pointed-torsor proposal,
not a consequence of the jurisdictional reconciliation alone.

The next comparison must use only native UCNS target candidates:

1. the visible phase basepoint;
2. its `C2`-invariant two-lift fiber.

Neither candidate is selected by this record. The comparison must determine
whether either target is already native, whether attachment to it is
well-typed, and whether selection introduces a frame or orientation. Source
order, storage order, numeric order, implementation defaults, observed gonol
values, and PCEA expectations remain prohibited selectors.

The earlier symmetry receipt still establishes that an unframed homogeneous
rational-displacement candidate cannot intrinsically select one object. That
research result remains useful but does not establish a canonical attachment
target.

## Falsifiers And Boundaries

The jurisdictional reconciliation is contradicted by any of the following:

1. adding payload, coordinate, frame, orientation, provenance, or an internally
   retained relation to `N`;
2. treating an ambient placement descriptor as a second Structural Null;
3. identifying `N` with ordinary numeric zero;
4. assigning a carrier-owned relation to the intrinsic content of `N`.

This record does not authorize an attachment implementation. Any attachment
change requires a separately licensed codomain, target, contract, tests, and
machine-readable evidence. It must not alter current branch, collapse, motion,
or return behavior merely to manufacture an address.

## Rollback Boundary

The UCNS wording change can be reverted independently because it changes only
`CANON.md`. Attachment research can be withdrawn or replaced without changing
the ratified jurisdictional rule. No rollback may create a second origin or
move ambient relation data into `N`.

## hmmm

The attachment is alive but currently has no mathematically licensed address.
