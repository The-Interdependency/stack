# Weave: current questions and proposed answers

**Approval status: PENDING.** The proposed answers below are not implemented defaults.
The byte/star repair is authorized separately; it does not approve a new cipher.
Existing Q1-Q10 identities remain in the disposition register below.

## Settled; do not ask again

- The input is raw bytes, not Unicode or an English-word prerequisite.
- Each message is an origin; each byte has eight bits and an eight-circle construction.
- One big circle plus seven small circles remains eight. The big circle participates
  dynamically and carries a bit; it is not merely an external reference.
- Public degeneration uses two circles at a time. One is always the big circle.
  The earlier four-circle proposal and arbitrary/disjoint pairings are superseded.
- Every circle uses the complete 720-degree return.
- Circle-space relationships vary per key set; do not impose a universal relation.
- The stated ciphertext expansion is twofold. Do not obtain it by copying or
  independently coding each bit twice.
- UCNS geometry and UCHC origin-axis relations retain their respective authorities.

## Next question set for approval

### Q11 — Is the placement operation relocating values or changing them?

**Probable answer:** Preserve each bit's value and occurrence identity in the
positional layer; transform its place and its relationships as part of the complete
byte. The ciphertext encodes the resulting relation jointly. Do not install a
separate two-symbol substitution for each bit.

**Still to construct:** the actual joint placement and its exact inverse. This answer
does not prohibit a separately authorized transformation in another Weave layer.

### Q12 — What information does the public whole-plus-one pair retain?

**Probable answer:** A forward positional relation derived from the complete
eight-circle configuration, with the inverse-completing relationships omitted. It is
not merely a raw copy of two otherwise independent private circle records. The sender
can operate with its public object; the full private configuration supplies recovery.

**Still to construct:** a concrete degeneration and recovery operation. Reduced key
exposure is not itself evidence of computational difficulty or strongest security.

### Q13 — What carries forward between successive byte constructions?

**Probable answer:** The key-set geometry and an evolving message-scoped relational
state carry forward. Each byte keeps its own occurrence identity and eight placements.
G0 participates in each relation; the active small circle is selected within that
key-defined evolution, not by an added universal schedule, fixed four-pair partition,
or a rule that emits two public bits for every source bit.

**Still to construct:** a deterministic forward/recovery state transition that uses
the established native relations. No numerical feedback formula is selected here.

### Q14 — What do the additional eight ciphertext bits represent?

**Probable answer:** One joint 16-bit relational codeword for the complete source
byte, rather than eight independent two-bit codes. Its additional capacity carries
recoverable placement/relation information; exact circle positions may be reconstructed
through the key rather than dumped as arbitrary coordinates into the wire format.

**Still to construct:** the actual 16-bit mapping, its length accounting and unique
recovery. No field split, extra header, or claim of two possible lifts is assumed.
Two public circles alone do not mathematically force twofold expansion.

### Q9 — Should identical messages under one key repeat the same trajectory?

**Probable answer, carried forward:** No. Fresh per-message input should participate
in the origin/placement relation, and authorized recovery must obtain its needed
state. Any transmitted origin metadata must be accounted for within the agreed
length policy, not silently added after claiming exact twofold expansion.

**Still to construct:** a concrete native variation mechanism and recovery path.
A namespace called `O_M`, a counter, or a public nonce alone is not a secrecy result.

## Earlier questions: preserved disposition

| ID | Current disposition |
|---|---|
| Q1 — Native plaintext admission | Raw-byte, byte-scoped shape is settled. This repair constructs occurrence/placement records, not native encryption. No text database is a prerequisite. Actual geometric transformation and serialization remain Q11/Q14. |
| Q2 — Private gonol/public counterpart | Eight full circles and G0-plus-one public shape are settled. The actual public/private transformation is Q12. |
| Q3 — Threads | Preserve complementary native contributions, source occurrences and cross-thread relationships. Existing lane routing is a transport trial, not the native relation. |
| Q4 — Corpus | Preserve actual selected material and its construction/recovery role. The existing left/right traversal formula remains an assistant-selected transport trial; native attachment is not settled by it. |
| Q5 — Join/final operation | Preserve explicit route execution and the literal final last/first interleave. The demonstrated cyclic join is not a private route generator or a new universal rule. |
| Q6 — Arity composition/remainders | Existing experiment uses sequential passes and quotient/remainder sections, preserving order, repetitions and empty sections. Keep its proposed policy separate from user-ratified general design. |
| Q7 — Sender boundary | Intended public-side sender must not require recipient private state. API separation alone is not a mathematical asymmetric construction. |
| Q8 — Control derivation | Key/message relation and inverse planning must provide controls before they are needed. No private encoder trace is silently supplied as ciphertext or an inverse plan. See Q12/Q13. |
| Q9 — Repeated-message variation | Carried forward above; the earlier proposed answer remains pending, not newly approved. |
| Q10 — Integrity/length/replay | Remains a distinct unresolved mechanism. Authentication is independently switchable and is not silently made a replacement for Weave or a newly mandatory layer by this repair. |

## Removed premises

The PR #73 per-bit sheet code and PR #74 bit-axis feedback code were specification
mismatches. Their attacks do not adjudicate the requested construction. The premise
that changing private-only data must change ciphertext while every sender input is
held fixed is also removed; it is not a valid private-recovery-dependence test.
See [EIGHT_CIRCLE.md](EIGHT_CIRCLE.md) for exact historical identities and repair scope.

## Usage guidance

Approve or amend by ID, for example `Q11 approve; Q12: ...`.
Approved descriptions guide construction; they do not constitute an implemented
algorithm, a proof, or permission to silently fill missing mathematics with a substitute.
No additional decision about a particular degree, space offset, or universal circle
visitation order is required merely to retain the repaired structure.

## hmmm

The actual positional cipher remains unimplemented. These are the next proposed
construction answers, not another round of declarations that it already works.
