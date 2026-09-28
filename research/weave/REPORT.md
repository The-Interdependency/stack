# Weave — first source-bound results

**Full-design verdict: not established.** These are executed results for the specified
interleaving operation and an explicitly declared sequential composition profile.
The nested gonol, private-gonol, thread/corpus and asymmetric relations remain part of
the required design. They were neither simulated with substitutes nor evaluated by
transferring a result from the interleave. This is partial evidence, not completion of
the requested full-system assessment.

## Executed results

The literal last/first inward operation has an exact inverse. It passed all **8,191
binary inputs of lengths 0 through 12**. Section-local operation and its inverse
passed **4,017 ordered positive partitions**: every partition of lengths 3 through 12
having at least three sections. Position-labelled tests prove each tested map is a
bijection for any bit values placed at those positions, not just one test plaintext.

The sequential `(5,7,3)` profile, including its final whole-sequence interleave,
recovered every position exactly at **105, 210, 420, 840, 8,400 and 67,200 bits**.
No one-byte implementation limit was introduced. Uneven section sizes are supported
when supplied explicitly; no remainder-allocation policy was invented.

At 105 bits, **all six orderings of the illustrated arities 3, 5 and 7 produce
different maps**. Thus order has a demonstrated effect in that declared domain.

## Exact inverse

For `y = I(x)`, input length `n` and valid output indices:

```text
y[2r]   = x[n - 1 - r]
y[2r+1] = x[r]

x[i] = y[2i+1]          when i < floor(n/2)
x[i] = y[2(n-1-i)]      otherwise
```

The two index families cover every input position exactly once. This derivation
holds for any finite length, including the odd-length centre. Inverting each known
section reverses a stage; undoing the final interleave and then the stages in reverse
order reverses the explicitly sequential profile.

## Schedule equivalences

The complete predeclared census examined all **9,840 schedules** over `(3,5,7)` with
one through eight stages at 105 bits. It found **9,727 distinct positional maps**.
All 363 descriptions through depth five were distinct in this domain; repeated maps
first appeared at depth six.

These schedules produce exactly the same map at 105 bits:

```text
(5,7,3)
(5,7,3,7,7,7,7,7)
```

Consequently their outputs agree for **every** 105-bit input under the declared
equal-partition sequential profile. Five applications of the arity-seven stage
restore all positions. Exact single-stage periods here: **35 for arity 3, 7 for
arity 5, and 5 for arity 7**.

Repeated arities were an experimental choice, not a recovered rule requiring your
design to permit them. The result falsifies the assistant-added universal claim that
changing stage count necessarily changes the transformation. It does not falsify
Weave, prescribe a key policy, or equate schedule counts with key strength.

## Fixed-map attack

For the fixed `(5,7,3)` profile, an attack given only input/output access and message
length recovered an equivalent inverse:

| Message length | Chosen input queries | Held-out messages recovered |
|---|---:|---:|
| 105 bits | 7 | 64 of 64 |
| 840 bits | 10 | 64 of 64 |
| 8,400 bits | 14 | 64 of 64 |

The attacker never receives the schedule. Query `j` places bit `j` of each position's
binary index at that position. Returned bits reconstruct the indices in output order.
The result is an **equivalent inverse**, not recovery of the actual schedule.

**Assumption:** one fixed length-preserving positional map across queries and held-out
messages. No result is claimed for message-dependent maps, changing maps per encryption,
or the complete Weave composition.

If a proposed composition of threads and corpus operations ultimately does nothing
but apply one fixed bit permutation, this argument extends by algebra. Whether the
full intended construction belongs to that class has **not** been established.

Bit rearrangement also preserves the number of ones. All-zero and all-one inputs
remain unchanged. Constant witnesses and 192 held-out weight checks were executed.
This scope excludes unspecified gonol encoding or corpus transformations that may
change representation or values. The full ciphertext was not tested for randomness.

## Whole-design coverage

| Required part | Actual evidence |
|---|---|
| Nested hyperspace/gonol construction | The real UCHC module was located and inspected. Its glyph, word and definition promotion/recovery code exists. Its full corpus was not replayed. |
| Private gonol required in recovery | Requirement preserved. No executable Weave binding was present in the inspected workspace. No hash, scalar, password or generic tree was substituted. |
| Multiple related threads | Preserved. No recovered split/recombination law was executed; no round-robin or secret-sharing substitute was selected. |
| Thread-associated corpus/material | Preserved. No corpus was selected on the user's behalf; no filename hash or decorative role was substituted. |
| Section-local interleave | Literal operation implemented and tested; explicit partitions retained. |
| Final whole interleave | Executed on the composed-operation profile, not represented as a full ciphertext test. |
| Asymmetric public/private relation | Not executed: no retrieved complete forward/public and inverse/private binding. Missing implementation is not mathematical impossibility. |

At inspected Stack head `247af26527d0d76558dac1dd7fd05e41ce83112e`, `research/weave/`
contained only `BASE.json`, `README.md` and `SPECIFICATION.md`. The full algorithm was
not implemented there. This is a source finding, not a claim that the user never
explained the missing relations.

The UCHC source inspected was `human/english/english_gonol/hyperspace_construct.py`,
Git blob `8b55823805c87ad8c4cc9d7451dc2eb90bdedd3a`. Its
`promote_word(db, word_id)` and `recover_word(db, word_id)` operate on constructed
corpus records. They are real construction/recovery functions, not a supplied
private-gonol encryption binding.

## Corrections to assistant-authored requirements

“Arity three, minimum” does not say “at least three stages.” The assistant imposed
`k >= 3` without source support. Stage count and section arity must remain distinct.

The earlier specification prescribed schedule-order and stage-count sensitivity as
blanket invariants while also asking whether schedules collide. Retain the supplied
order/count exactly and measure induced equivalence; do not reject a faithful
implementation because it finds a collision. The full architecture remains in scope.

## Reproduce and verify

`probe.py` uses a deque for the literal operation and a separate index formula for
its inverse. `verify.py` does not import it; a second index-composition implementation
recomputes all 9,840 schedule maps, digests, exact collision witnesses, example stage
orders and literal odd/even/three-section golden vectors. Both implementations were
written by the same assistant. This is **not an independent author's review**.

Isolated-mode and optimized-Python replays matched the receipt exactly. Both checkers
rejected a deliberately altered map count with exit status 1. These are evidence
integrity checks, not authenticated encryption.

From `research/weave/`:

```bash
python probe.py > receipt.json
python probe.py --check receipt.json
python verify.py receipt.json > verified.json
```

Expected SHA-256 of the exact receipt bytes:

```text
0c66b2dc2a6b36a00969d7e3c1421cacd44dbd7082bcdf4c5b79f7403f0226c3
```

The runtime uses Python's standard library only. Hashes identify source and evidence;
they do not supply encryption. `PLAN.md` was written before the first local run. The
separate verifier and tamper checks were added afterward, and are subsequent
verification rather than retroactively preregistered discoveries.

## Sources and provenance

- Stack source at the inspected head: [Weave source](https://github.com/The-Interdependency/stack/tree/247af26527d0d76558dac1dd7fd05e41ce83112e/research/weave).
- UCHC producer: [hyperspace_construct.py](https://github.com/The-Interdependency/uchc/blob/main/human/english/english_gonol/hyperspace_construct.py), identified above by exact Git blob.
- Original user last/first and private-gonol statements were recovered from conversation context; PLAN.md distinguishes them from experimental choices.
- Retrieved Library URPCS law files describe the retired authenticated codec and were excluded as authorities for the desired encryption.

## hmmm

The original pre-substitution thirteen-law conversation was not recovered. Precise
thread/corpus rules and private-gonol/public-key binding were not recovered as an
executable contract. Those are retrieval/implementation boundaries, not a verdict
against the idea. Until the actual composition can be run, **neither a pass nor a
failure of the full design is supported**. No substitute result closes that gap.
