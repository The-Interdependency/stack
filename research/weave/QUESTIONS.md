# Weave — questions and provisional answers

These are proposals for Erin to correct, improve or approve. Implementation does not
constitute approval. Existing Q1–Q10 identities from ASSEMBLY.md are retained.

## Q6 — Stage composition and uneven partitions
**Question:** Should each arity act on the preceding output, with the remainder assigned
left-to-right? **Proposed answer:** Yes. First r sections get one extra bit; preserve
empty sections if arity exceeds length. Preserve supplied repetitions and allow one
stage. **Implemented provisionally**, independently reversible and tested. Arity is
not level count, and thread count is a third distinct parameter.

## Q3 — What are the threads?
**Question:** Are they complementary native contributions from one full plaintext
gonol, rather than independent copies or arbitrary byte chunks?
**Proposed answer:** Complementary native contributions, retaining occurrence identities
and cross-thread relations. **Native rule still open.** Implemented now: exact
occurrence-to-lane routing and inverse; the demo chooses cyclic assignment. That is an
explicit transport witness, not a claim to have implemented the native projection or
proved every thread necessary. Repeated/structured inputs may be recoverable from less.

## Q4 — What should the actual corpus do?
**Question:** Should material govern traversal, supply native axes/origin attachments,
change values, or combine these roles?
**Proposed answer:** Keep traversal and native-context variants distinct, and compare
both inside the eventual full construction. **A traversal trial is implemented:**
material bit 0 consumes the left end of the current lane, bit 1 the right end. Bits are
MSB-first, starting at the specified offset and repeating when exhausted. This exact
formula is a new assistant proposal, NOT a rule previously attributed to Erin. It
uses content, not a filename hash or XOR mask. Only the visited material bits influence
a run; unused material is not counted as secrecy. Native axes/origin binding remains open.

## Q5 — Joining and the final operation
**Question:** How should transformed threads be interlaced, and when is the final pass?
**Proposed answer:** An explicit context-derived lane route, then one final last/first
pass over the whole joined stream. **Supplied routes are implemented.** The demo cycles
through [2,0,1], skipping exhausted lanes; it does not derive that route from a key.
A private/native route generator still needs its constitutive relation.

## Q1 — Native plaintext admission
**Question:** Should one native admission cover arbitrary binary files, alongside
language-aware constructions for admitted text?
**Proposed answer:** Yes; preserve exact bytes without normalization. **Implemented:
a source-pinned read/recovery adapter for already-constructed UCHC words.** That returns
the actual upstream object, not a new label tree. General binary admission,
whole-message native composition and its transport serialization remain open. The
adapter's successful real-corpus path has NOT been executed in this session.

## Q2 — Private gonol and public counterpart
**Question:** Does the private gonol restore a missing origin/attachment relation,
a member, an embedding, or another constitutive relation?
**Proposed answer:** First examine a private origin/attachment relation that selects
the recoverable embedding, paired with a public forward construction. **Unimplemented.**
The research task is to derive concrete native maps and test inversion; approval of
this direction is not a proof, and Erin is not being asked to supply one. No password
check, random permutation seed or conventional cryptosystem substitutes for it.

## Q7 — What can an independent sender know?
**Question:** Must the sender operate using public-side material without recipient
private-gonol knowledge or private schedules?
**Proposed answer:** Yes, for the intended noninteractive asymmetric mode. Secret
corpus selections must have a usable public forward counterpart where needed.
**The API separates the two sides; the mathematical relation is not implemented.**
The transport experiment supplies the same explicit routing/material recipe to both
sides and makes no asymmetric claim.

## Q8 — Control derivation and recovery order
**Question:** Are thread counts, routes, corpus locations and arities derived from the
native key/context rather than simply stored as a private plan?
**Proposed answer:** Derive them from native key relations plus available message
context. Reverse operations must obtain needed controls before they need to recover
the hidden content those controls protect. **Explicit control execution is implemented;
native derivation remains open.** Forward and recovery compile the transport recipe
independently; no encoder trace is supplied to recovery.

## Q9 — Repeated-message variation
**Question:** Should repeated input under one public key produce distinct outputs?
**Proposed answer:** Yes: fresh per-message input should alter applicable native
relations/controls; a fixed value allows deterministic tests. **No native randomness
coupling is implemented.** Merely appending a nonce is not used as a substitute.

## Q10 — Integrity, length and replay
**Question:** Must modified, incomplete and replayed messages be rejected, and which
metadata may be public?
**Proposed answer:** Require those properties for a usable final encryption profile;
retain a distinct integrity/state module and choose its actual mechanism explicitly.
**Unimplemented.** The lab format checks syntax, lengths and experiment identities,
but does not authenticate data. Wrong material or a same-length bit change can return
incorrect bytes without an integrity error. Lab recipe metadata is not a selected
production ciphertext format.

## Usage

Reply using the existing Q numbers, for example “Q4: corpus supplies origin attachments;
keep the traversal candidate only for comparison.” Each changed answer can be traced
to the owning module and tested without silently changing the others.

## hmmm

The working transport is not the desired native encryption construction. Questions
Q1–Q4 and Q7–Q9 carry the remaining native relations. Concrete rules, not renamed
placeholders or successful transport tests, will close those boundaries.
