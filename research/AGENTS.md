# UCNS/PCEA research instructions

These additional instructions apply to `research/ucns/`, `research/pcea/`, and
their joint experiments. Other research workspaces retain their own scope.
The repository-root `AGENTS.md` continues to govern Stack authority and topology.

## Objective and working method

Recover and test constructions that could advance UCNS-based PCEA. Read existing
definitions and executable evidence before inventing replacements. Recheck old
STOP labels against the exact sources available now; distinguish missing
implementation, missing selection, and a mathematical obstruction with stated
assumptions. Continue useful authorized work beyond a failed candidate by
recording the counterexample and identifying a materially different next test.

Preserve the user's intended meaning. In particular, an assertion about
"arity 19" concerns a possible nineteen-role construction; do not silently
reinterpret it as the prime factor 19 or arithmetic modulo 19. Find an existing
definition first. If none is recoverable, record the ambiguity and make each
candidate interpretation explicit before testing it.

Use concise progress reports focused on findings and unresolved assumptions.
Ask only for information that materially changes the construction or scope;
perform independent authorized work while clarification is pending.

## Source and custody

- Read each affected workspace's `BASE.json`, README, and relevant migration
  record. Resolve applicable skill-lib and METAPAT definitions at exact commits.
- Inspect relevant local branches, worktrees, and unpublished VM research when
  available. Bind uncommitted evidence by content hash as well as its base commit.
- Preserve unrelated edits and historical receipts. A changed source identity
  requires a new receipt, not a rewrite of an old result into a pass.
- Keep experiments in Stack. Promote completed geometry through UCNS and stable
  runtime behavior through PCEA with owning-repository review. Follow the root
  structural-update gate for changes to workspace authority, placement, or pins.

## Retained structure and selection

Retain `R = (C_k(t), relations, provenance)`, including ordered participants,
occurrence identity, multiplicity, and recoverable constituents. Preserve the
full coefficient vector of `C_k(t) = product_i (1 + p_i*t)`.

The update `e'_j = e_j + q*e_(j-1)` consumes a supplied `q`; it does not select
one. A successor claim must expose `q_next = S(R)` and identify every input.
Return an explicit candidate set or unresolved result when selection is ambiguous.
Factor count is UCNS arity only when the factors occupy mutually constraining
roles under a stated admission rule. Scalar breadth and radius may be lossy;
they cannot replace the retained object.

Audit the dependency chain:

`origin attachment -> direction/chirality -> rotation system -> marked outgoing dart -> closure`

For each field, show why the requested output needs it, what existing operation
provides it, and whether its selection is derived or assumed. Record the actual
native transition law. Traversing a closed orbit does not by itself authorize
filling a face, installing a relator, or introducing torsion or a trapdoor.

## Experiments and falsifiers

- State explicit candidate assumptions and implement the smallest coherent
  constructor. Competing assumptions must remain distinguishable in receipts.
- Freeze source bytes, inputs, parameter ranges, algorithms, work limits, and
  readout rules before evaluating known comparators. Targets already seen in
  this conversation are retrospective checks, not independent predictions.
- Test `157 -> 2881 -> 54837698421` only after freezing. Stop that candidate's
  recursive prediction at its first mismatch. Do not fit the integer sequence;
  `164513086777` is only the quadratic interpolation control.
- For an arity-19 hypothesis, define the roles, relations, admission rule, and
  claimed change at nineteen. Test neighboring arities and matched structures
  under the same frozen rule. Choosing nineteen because an output looks useful
  does not establish a structural threshold.
- Include known hits and breaks, alternative primes, reordered relations,
  shuffled storage, repeated occurrences, matched controls, and malformed input
  where relevant. Preserve order sensitivity when the relation declares order.
- Distinguish `C4` from `C2 x C2` even when quotient cardinalities agree.
  Incomplete factorization is `UNRESOLVED_FACTORING`, never a negative control.
- Emit deterministic JSON and readable Markdown with source identities, hashes,
  assumptions, exact commands, results, and the smallest counterexample found.
  Check byte-identical replay of deterministic computations; model-generated
  proposals are not presumed deterministic.

## Verdicts and cryptography

Classify the precise claim: `SURVIVED` (or `SURVIVED_LOCALLY`), `FALSIFIED`,
`UNRESOLVED`, or `BLOCKED`. A local survival is bounded by its assumptions and
tests. Missing evidence is not a counterexample. A falsified candidate does not
falsify every possible construction.

Assess geometric correctness separately from cryptographic security. Compare
transport with AES-GCM and ChaCha20-Poly1305; compare state evolution with
appropriate ratcheting schemes. Security equivalence is sufficient to proceed,
but must be demonstrated under matched assumptions and threat models.

Test known/chosen plaintext, nonce/state reuse, modification, truncation,
reordering, replay, rollback, desynchronization, partial/full state or seed
compromise, authentication, forward secrecy, and post-compromise recovery as
applicable. Assume the adversary knows all algorithms and public structure.
Primes, geometry, public branches, scale, representation fidelity, and round-trip
correctness alone establish no secrecy. Preserve existing attack witnesses.

## Verification and handoff

Run focused tests appropriate to the changed behavior. The rooted-closure suite is:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  research.ucns.tests.test_rooted_rotation_closure_constructor -v
```

Report inherited failures and source drift separately from new regressions.
Hand off code, exact source identities, replay receipts, scoped verdicts, the
first remaining irreducible assumption, and the next experiment that could
resolve it. State whether work is local, committed, pushed, reviewed, or merged.
