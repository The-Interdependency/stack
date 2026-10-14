# Ordinal construction: answers and remaining work

The selected implementation is `english.ordinal/1`; inspect it with
`PYTHONPATH=research/english-gonol python -m english_gonol profile`.
Run `verify OUTPUT` before using a generated field. These boundaries do not
reopen the specified ordinal-distance/carrier-angle rule or block its use.

## Already answered and implemented

For zero-based ordinal i among n participants, radius is R/2**(n-i); the newest
participant is at R/2. Angle is the participant's exact index/arity on its
explicit carrier. Closed interiors survive recursive atomic participation.
The initial equidistant field and its circular placement are distinct stages;
planar placement is not claimed to preserve all initial pairwise distances.

This selected version uses balanced insertion around inherited scalar anchors,
and orders its word carrier by sequences of public-gonol indexes. These are
explicit implementation choices, not discovered semantic laws. This merge keeps
them fixed; changing either requires a new profile and rebuilt receipts.

## Construction answers and questions, ordered by dependency

### 1. Nested attachment: SPACE — specified; transport unverified

Operator answer to the nested-frame attachment question: `1. space`.
SPACE supplies the attachment reference between a closed construction's local
frame and its consuming frame. Do not ask the operator to select that reference
again. The already-specified ordinal-distance and carrier-angle laws remain in
force; this answer does not authorize substituting a different construction.

In `../english_gonol/ordinal_construct.py`, both `Factory.word` and
`Factory.record` already declare `origin='SPACE'`; `_independent_frame` checks
the same origin in frame rows and closure receipts. That existing declaration
is not an evaluated transport between frames.

Current behavior: preserve separate local frames and their links. Remaining
implementation/evidence boundary: an explicit UCNS transport using the specified
SPACE attachment, with nested-order recovery and a tested composition law.
Do not invent an implicit rotation, translation or scale law to turn the stored
origin name into a completion claim. Record the implemented transport and its
evidence here when available; keep specification and implementation distinct.

### 2. Compound definition attachment: SPACE — specified; witness outstanding

Operator answer to the compound definition-origin question: `2. space`.
SPACE supplies the attachment reference for a multiword lexical entry's
definition, as it does for nested frames in answer 1. Do not ask the operator
to select that reference again or substitute a constituent word as the origin.

Preserve the compound entry's exact source ownership, constituent order and
definition succession. Apply the specified SPACE reference when implementing
its attachment; naming the reference does not establish evaluated transport.

Completion witness: every compound definition has a source-bound SPACE
attachment that preserves its entry, constituent order and definition
succession. Record the implemented attachment and independent verification here
when available; the reference is specified, while that witness remains
outstanding.

### 3. Native Mobius integration: not required

Operator answer to the native Mobius integration question: `3. not required`.
Native Mobius lifting, sheet-state transport and 360/720-degree return tests are
outside the required scope of `english.ordinal/1`. They are neither outstanding
construction questions nor completion or merge prerequisites for this profile.
This scope decision does not claim a verified lift, retire UCNS native Mobius
work, or remove the SPACE attachment obligations in answers 1 and 2.

### 4. Which admitted operator positions perform which actions?

A numeral, mathematical sign or logical operator currently receives an exact
scalar identity and angle. Admission does not implement arithmetic, implication,
quantification or any other action. What source-owned operation supplies each
function, and how does applying it change a construction?

Current behavior: preserve literal position and occurrence only. Completion
witness: declared operations with positive and adversarial behavioral tests.

### 5. How should previously unseen words and future carrier members enter?

Current behavior: exact pinned repertoire; queries refuse unknown words and
unadmitted scalars, with no normalization or dynamic carrier mutation. A new
carrier/profile must rebuild all affected placements because changing N or order
changes angles. Supporting open-text word closure requires an explicit composite
carrier admission rule; it must not use a last-glyph angle or an invented hash
angle as a substitute.

Completion witness: deterministic growth/upgrade policy, old-profile replay, and
no silent reinterpretation of previously constructed objects.

## Engineering work, not questions to send back to the operator

- Separate the source-admission helper closure from the historical builder modules
  before physically removing those modules. They are retired as new-construction
  routes now; deleting dependencies first would break the replacement's verifier.
- Migrate the extracted UCHC candidate and each pinned EDCM/ZFAE/a0 consumer through
  its own exact input and replay contract. This source selection is not an
  independent release, deployment, or retroactive recertification.
- Publish the complete generated artifact on a durable, versioned distribution
  surface; GitHub Actions artifacts have their own retention lifecycle.
- Select a concrete downstream task and predeclared comparison to test utility.
  Exact construction and recovery do not establish inference quality.

## hmmm

SPACE is the specified attachment reference for both nested frames and compound
definitions. Their transport/attachment witnesses remain outstanding. Only
questions 4 and 5 remain open. Merge closes source integration and default
selection, not these implementation/evidence boundaries or downstream migration.
