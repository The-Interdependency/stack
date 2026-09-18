# PCEA algorithm: current research specification v1

Date: 2026-09-18. Standing: **research specification / UNRESOLVED**.

This document updates the algorithm's research description against exact current
sources. The stable implementation is fully specified below as a baseline.
The proposed successor is an explicit partial algorithm: unresolved operations
remain unresolved and produce no candidate ciphertext. This is not a completed
new cipher, a runtime promotion, or a security certification.

## Source and ownership

The [work graph](pcea-current-research-v1.work-graph.json) binds these identities:

| Repository | Commit | Role |
|---|---|---|
| PCEA | `1595842abd1a5b443c6a601a2afe935b60c4adf7` | Stable runtime |
| UCNS | `d8f0c505e6f5132e9711de0e7c24e4718e77e51a` | Geometry and incubating prime-arity research |
| Stack | `57e3f047c092a6df5435ed4f502347664513a0ff` | PR #42 research base; candidate mechanics, successor experiments, and PCEA research |
| METAPAT | `e4165b0cac9eca41daef9c2f941881028ca55d48` | Semantic and domain-restraint doctrine |
| skill-lib | `dd5027d99516831c0dcb83a176a67140d3819b66` | Build and evidence discipline |

This work is owned by `stack/research/pcea/`. It does not refresh Stack's imported
libraries or historical `BASE.json` identities. Each historical receipt remains
evidence about its original inputs. Mathematical, semantic, empirical,
measurement, certification, and security standing do not transfer between
repositories.

## Stable algorithm actually present

The move from PCEA `f6b14e664e8366e291275eb56c39c60e0b6ef65d` to the current
pin changes metadata and test witnesses. Every package blob except `kdf.py`
is identical; the old and current KDF abstract syntax trees are identical.
There is **no executable algorithm upgrade** in that revision interval.

Sources: [cipher](https://github.com/The-Interdependency/pcea/blob/1595842abd1a5b443c6a601a2afe935b60c4adf7/pcea/cipher.py),
[codec](https://github.com/The-Interdependency/pcea/blob/1595842abd1a5b443c6a601a2afe935b60c4adf7/pcea/codec.py),
[KDF](https://github.com/The-Interdependency/pcea/blob/1595842abd1a5b443c6a601a2afe935b60c4adf7/pcea/kdf.py),
[session](https://github.com/The-Interdependency/pcea/blob/1595842abd1a5b443c6a601a2afe935b60c4adf7/pcea/instance.py),
[primes](https://github.com/The-Interdependency/pcea/blob/1595842abd1a5b443c6a601a2afe935b60c4adf7/pcea/primes.py).

For current state `S`, previous state `L`, address `(i,c,t)`, and width `W`:

1. Admit exact integer cells in nonempty seeds of shape 7 by 7. Plaintext and
   previous-state cells lie in `[-2^(W-1), 2^(W-1)-1]`; default `W=64`.
2. Let `P` be the first 53 primes. Select `p=P[(7c+t) mod 53]`.
   The current layout uses only the first 49 primes, 2 through 227.
3. Set `u=S[i][c][t] mod 2^W`; choose the least `k` with `p^k >= 2^W`.
   Expand `u` into exactly `k` little-endian base-`p` digits `v[j]`.
4. Gather contributors in the order
   `[L[i][c][t], L[i][(c-3) mod 7][t], L[i][(c+3) mod 7][t]]`.
5. Encode an integer `z` as one sign byte (1 if negative, otherwise 0),
   an eight-byte unsigned big-endian magnitude-byte count, and its unsigned
   big-endian absolute magnitude. Zero uses one magnitude byte.
6. For each hash-block counter `q=0,1,...`, concatenate the bytes
   `b"PCEA-KDF-INT-v1\x00"`, the contributor count 3 in eight unsigned
   big-endian bytes, each encoded contributor, then encoded
   `i,c,t,k,p,q`, in that order. Concatenate SHA-256 digests until at least
   `k` bytes exist; take the first `k` bytes and set `K[j]=byte[j] mod p`.
7. Encrypt with `e[j]=(v[j]+K[j]) mod p`, independently without digit carries.
   Return `E[i][c][t]=sum(e[j]*p^j)`, an integer in `[0,p^k)`.
8. Decrypt by expanding `E`, reproducing `K`, and subtracting modulo `p`.
   Reduce the reconstructed value modulo `2^W`, then interpret its upper
   half as negative by subtracting `2^W`.
9. Stateless functions leave `L` with the caller. `PCEAInstance` sets
   `L_next=deepcopy(S)` after nonempty encryption or recovered plaintext after
   nonempty decryption. Empty input returns `[]` without advancing the state;
   nonempty states must have the same seed count as `L`.

The supplied initial state is the secret input; this implementation generates
no random initial secret. Its codec's “Mobius” label names the implemented
signed/unsigned mapping, not a proof of a full native UCNS frame-bearing lift.
The algorithm has no authentication tag or replay ledger.

## What current research changes

| Area | Current evidence | Consequence for a successor specification |
|---|---|---|
| Public Gonol operations | Executable carrier-operation and closure candidate | Retain complete operation records; glyph meanings do not select operations |
| Coupling | Explicit ordered incidence candidate with separate occurrences | Preserve participant order, multiplicity, and intrinsic relation |
| Recursive promotion | Closed whole becomes a digest-bound atomic participant | Preserve recoverable constituents; an identity receipt does not determine next-scale placement |
| Ordered return layer | Fox and degree-two Magnus data distinguish six based words that share one homology vector | Preserve ordered words; a rank or scalar cannot replace them |
| Prime-arity coefficients | Exact update and unordered-multiset preservation; scalar collisions | Keep coefficient layers plus relations and provenance |
| Recursive successor | No surviving constructor in the pinned experiments | Do not replace the 53-prime table with an asserted derived ladder |
| Rooted ribbon completion | Five fields execute under explicit assumptions; paired and sign-block rotations disagree | Preserve the constructor as Stack research; do not promote an assumed attachment or select a rotation post-hoc |
| Displacement selection | Current correction selects no candidate | Do not import the withdrawn selection as a settled geometric law |

Sources:
[carrier operations](https://github.com/The-Interdependency/stack/blob/545e135e2efbbcf29f033ab5530ac4876a68b718/research/ucns/docs/public-gonol-functional-operations-v0.md),
[ordered coupling](https://github.com/The-Interdependency/stack/blob/545e135e2efbbcf29f033ab5530ac4876a68b718/research/ucns/docs/affinization-coupling-geometry-v0.md),
[atomic promotion](https://github.com/The-Interdependency/stack/blob/545e135e2efbbcf29f033ab5530ac4876a68b718/research/ucns/docs/recursive-scale-transition-v0.md),
[ordered return audit](https://github.com/The-Interdependency/stack/blob/545e135e2efbbcf29f033ab5530ac4876a68b718/research/ucns/docs/ordered-return-invariant-audit-v0.md),
[current rooted rotation/closure audit](../../ucns/docs/rooted-rotation-closure-audit-v0.md),
[prime-arity audit](https://github.com/The-Interdependency/ucns/blob/d8f0c505e6f5132e9711de0e7c24e4718e77e51a/docs/prime-arity/audit_coefficient_breadth.py),
[displacement correction](https://github.com/The-Interdependency/ucns/blob/d8f0c505e6f5132e9711de0e7c24e4718e77e51a/docs/displacement-law/DECISION_2026-09-17_CORRECTION.md).

### Retain the mathematical object

For caller-supplied prime roles, the coefficient experiment defines

\[
C_k(t)=\prod_{j=1}^{k}(1+p_jt),\qquad
R=(C_k(t),\mathrm{relations},\mathrm{provenance}).
\]

For a supplied next prime role `q`:

\[
C_{k+1}(t)=C_k(t)(1+qt),\qquad
e'_j=e_j+q e_{j-1}.
\]

The update is exact. It does not discover `q`. The observed factorizations are:

| Observation | Prime factors |
|---|---|
| 157 | 157 |
| 2881 | 43, 67 |
| 54837698421 | 3, 11, 1661748437 |

They are not nested role sets, so appending one factor does not construct the
observed progression. Factor count is not automatically UCNS arity: roles
require an explicit mutually-constraining relation.

A concrete scalar collision is

\[
(1+3t)(1+11t)=1+14t+33t^2,
\qquad
(1+5t)(1+7t)=1+12t+35t^2,
\]

while both give `C(1)=48` and radius `47/48`. Therefore neither `C(1)`,
`log C(1)`, nor that radius may stand in for the retained object. The full
polynomial preserves the unordered prime multiset; order and provenance still
require separate retained structure.

The 13-layer prime-arity map remains an incubating calibration scaffold. Its
base carriers 2, 3, 5, 7 and candidate load recurrence are not a selected
key schedule or a new PCEA base table.

### Preserve the exact traversal dependency

The pinned Stack constructor contract stops at:

`STOP_MISSING_ORIGIN_ATTACHMENT`.

It requires, in order: origin attachment; directed tangent/chirality; rotation
system; marked outgoing dart; closure rule. The remaining fields are
dependency-blocked, not disproven. The current UCNS canon still describes
origin representation and higher recursive transitions as candidate-scoped or
unresolved; this update does not claim that the old Stack audit has been
re-executed against current UCNS. The follow-on rooted rotation/closure audit
now performs that recheck. It confirms that the canonical attachment remains
missing, then supplies every field only as an explicit candidate assumption.
Two valid rank-two rotations preserve the same earlier fields while producing
different face closures and genus, so current retained structure does not
select the rotation. Both frozen candidates derive cellular order `1` from the
one-role state and are falsified by the first `2881` comparator; neither is
recursed on the second observation.

Sources:
[constructor contract](https://github.com/The-Interdependency/stack/blob/545e135e2efbbcf29f033ab5530ac4876a68b718/research/ucns/docs/based-traversal-constructor-contract-v0.md),
[current canon](https://github.com/The-Interdependency/ucns/blob/d8f0c505e6f5132e9711de0e7c24e4718e77e51a/CANON.md).

## Research successor: explicit partial algorithm

The following is the updated candidate contract, not a completed implementation.
It replaces the old research summary's blanket claim that all three mechanics
are simply absent with their actual executable, candidate-scoped standing.

1. **Admit the complete construction.** Bind exact source identities,
   participant occurrences, ordered relations, closure and provenance.
   If coefficient projections are used, preserve `R` alongside the
   geometry; do not use a scalar projection as object identity.
2. **Obtain a geometric address certificate.** For the recursive-gonol lane,
   require the completed five-field traversal certificate and any required
   successor/placement rule, with independent replay. Missing evidence stops
   this lane before traffic-key or ciphertext generation.
3. **Bind a genuine secret independently of public coordinates.** Preserve the
   asynchronous research shape:
   `traffic_key = KDF(root_secret, protocol_label, gonol_identity,
   recursive_path, position, epoch, message_counter, transcript)`.
   The KDF, canonical transcript, state lifecycle, and component security
   assumptions must be frozen explicitly. A large address space contributes
   no demonstrated secret entropy by itself.
4. **Specify the encryption transformation.** Freeze plaintext/ciphertext
   domains, the keyed transformation, inverse, randomness requirements, and
   rejected inputs. A claimed asymmetric construction additionally needs
   explicit key generation, public and private maps, and its hard problem.
   Those operations are `hmmm` for the UCNS-derived successor here.
5. **Bind message validity and conversation state.** If replacing the
   authenticated/ratcheted system in the reported comparison, define
   authenticated framing, ordering policy, replay/rollback checks, and
   truncation/completion semantics. Merely placing counters in a record
   does not implement these checks.
6. **Advance only under the frozen acceptance rule.** Define secret-state
   evolution, old-key deletion, and compromise-recovery input explicitly.
   Do not silently carry over the baseline rule `L_next=plaintext` as a
   security-qualified ratchet.
7. **Attack and compare before promotion.** Freeze matched secret entropy,
   adversary access, admissible state reuse, and security targets. Compare
   against ordinary tree/ratchet and encryption controls. Quantum resistance
   requires its own attack model and analysis. Reference constructions are
   controls, not evidence that the UCNS candidate has already been completed.

At present step 2 has no admitted recursive traversal certificate, and steps
3 through 6 contain unresolved cryptographic choices. No runnable successor
encryption or ciphertext format is supplied by this specification.

The research goal may be a new UCNS-derived cipher. It is not satisfied merely
by attaching gonol addresses to another cipher. Conversely, the absence of a
completed construction is not a result against every future construction.

## Validation performed for this update

See [verification receipt](pcea-current-research-v1.verification.json).

- Verified fetched runtime, audit, and edited-entrypoint bytes against their
  Git blob identities.
- Compared all PCEA package blob identities across the two exact commits and
  compared the changed KDF's parsed syntax trees.
- Executed the unchanged current coefficient audit twice: 126 finite cases,
  byte-identical output, overall `UNRESOLVED`.
- Checked the work-graph digest and documentation references.

Stack geometry results above are reported from their pinned source records.
The follow-on audit independently replayed 14 rooted-constructor/adversarial
tests, the exact six-test crypto-audit commit `0b49672`, and the unpublished
ten-test trapdoor-lift audit. Complete package suites were not rerun.

## Usage guidance

Read this specification with its work graph before continuing PCEA research.
Use the source pins to reproduce a claim; retain each older experiment's own
pins when replaying it. To replay the coefficient audit in a UCNS checkout at
the recorded commit:

```bash
python docs/prime-arity/audit_coefficient_breadth.py
```

The five-field audit has now been rebound in the linked follow-on audit. The
next dependency-complete action is the frozen native attachment-target
stabilizer comparison: visible phase basepoint, `C2`-invariant two-lift fiber,
and a singly framed lift as a stronger control. Keep subsequent fields
unpromoted until one target is intrinsically selected.
For any independent bounded cipher experiment, declare a separate candidate
and explicit supplied geometry rather than bypassing this recursive lane's
gate.

## hmmm

- The exact recursive successor and next-scale placement remain unresolved.
- The complete geometry-selected traversal certificate remains unavailable in
  the inspected sources.
- Local Git object `0b49672862a30cec0a0ee24e39a34241c9626f27`
  is now independently replayed: its PCEA cryptographic verdict is
  `FALSIFIED`. A local equivalence-threshold extension reaches the same result
  across eight failed parity criteria but remains unpublished working-tree
  evidence.
- The unpublished trapdoor-lift audit is now source-hashed and replayed. Its
  existing-UCNS trapdoor standing is `UNRESOLVED_NOT_RECONSTRUCTED`; the
  minimal fourth-power candidate is `FALSIFIED`.
- New key derivation, encryption, authentication, state evolution, and quantum
  security remain construction-specific research obligations.
