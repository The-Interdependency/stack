# PCEA research workspace

Mutable PCEA research lives here. The owning `The-Interdependency/pcea` repository is the stable/runtime authority; this workspace is noncanonical research and may change freely.

## Authority boundary

```text
The-Interdependency/pcea          = completed/stable PCEA implementation authority
stack/libs/pcea/                  = manifest-pinned read-only imported view
stack/research/pcea/              = mutable PCEA research
```

Research results do not become PCEA runtime claims merely by surviving here. Promotion requires an owning-repository change with its own review and release evidence.

`BASE.json` now pins the refreshed stable PCEA view at `91ffa8c7249dfb810ca64a0bbc500481c0bd12a9`. The legacy research migration has a separate source identity because it captures the former PCEA proving ground immediately before source cleanup: `The-Interdependency/pcea@ecf2ca0dec38bef29382e02121b0edde66763aa9`. See `MIGRATION.json`.

## Legacy research migration

The former `pcea-ucns/`, its research-specific tests, and `rec.md` are deprecated at the PCEA source boundary. Git history remains permanent provenance; this workspace also carries an exact materializer so the last source snapshot can be reconstructed byte-for-byte when a lane needs continuation.

```bash
cd research/pcea
python materialize_legacy.py
python materialize_legacy.py --check
cd migrated
python -m pytest -q tests/test_attack_harness.py tests/test_positional_attack.py
```

The materializer verifies every downloaded file against its Git blob SHA before writing it. It uses only Python stdlib and the immutable source commit.

Do not edit `migrated/` as though it were current canon. Materialize a lane, then move or revise the specific active experiment in this workspace with explicit provenance.

## Current frontier

The [current research algorithm specification](docs/pcea-current-research-v1.md)
binds the stable runtime and current UCNS/Stack evidence. It records the complete
baseline, the explicit partial successor algorithm, and the outstanding gates.

The current candidate line is asynchronous PCEA key orchestration over gonol
state, with a possible new UCNS-derived encryption construction remaining a
research goal. Executable candidate carrier operations, ordered coupling, and
recursive atomic promotion now exist in Stack. They do not yet select a
recursive successor or geometry-selected traversal. The pinned traversal
contract stops at `STOP_MISSING_ORIGIN_ATTACHMENT`; later fields are
dependency-blocked.

The observed `157 -> 2881 -> 54837698421` progression remains unreconstructed
by a surviving constructor. The current prime-arity coefficient audit proves
the supplied-role update and unordered-multiset preservation, while falsifying
scalar `C(1)` as an injective structure encoding. Its full record retains
relations and provenance; it does not discover the next prime role.

PCEA keys must derive from actual secret input. Gonol size, public addressability,
scalar breadth, and surviving algebraic checks confer no cryptographic entropy
or quantum-resistance standing.

## Usage guidance

1. Read `BASE.json` and `MIGRATION.json` before starting a PCEA experiment.
2. Resolve exact current PCEA/UCNS commits needed by the experiment; do not silently substitute `latest`.
3. Materialize only legacy lanes you actually need.
4. Put new or mutating research here, never back into the stable PCEA repo.
5. Preserve negative results and attack harnesses; a passing harness grants permission for a harder attack, not a security claim.
6. Graduate only completed, bounded behavior back to `The-Interdependency/pcea` through an explicit owning-repository change.

## Current content

- [Current research algorithm specification v1](docs/pcea-current-research-v1.md), [work graph](docs/pcea-current-research-v1.work-graph.json), and [verification receipt](docs/pcea-current-research-v1.verification.json) - source-bound update, including the unchanged runtime baseline and explicit research incompletion.
- [Rooted rotation/closure audit](../ucns/docs/rooted-rotation-closure-audit-v0.md) - current-source recheck of the five-field traversal stop, explicit-assumption ribbon constructors, competing-rotation counterexample, post-freeze successor falsification, and unchanged separate cryptographic standing.
- [`docs/provenance-tracker-v0.md`](docs/provenance-tracker-v0.md) - Actor A stack-local candidate note for using PCEA as a lineage/provenance tracker, with public authenticity and security claims explicitly out of scope.
- [`docs/recursive-gonol-transition-candidates-v0.md`](docs/recursive-gonol-transition-candidates-v0.md) - Stack-local transition-family falsification and interpolation control from the observed `157 -> 2881 -> 54837698421` chain; no UCNS constructor or PCEA runtime claim.
- [`gonol_transition_candidates.py`](gonol_transition_candidates.py) - Executable candidate registry, falsification checks, and deterministic receipt bytes.
- [`docs/gonol-successor-mechanics-v0.md`](docs/gonol-successor-mechanics-v0.md) - Mechanics-derived successor-candidate gate starting from the pinned 157-position Public Gonol structure.
- [`gonol_successor_mechanics.py`](gonol_successor_mechanics.py) - Executable mechanics snapshot, successor candidate evaluation, and deterministic receipt bytes.

## hmmm

- The exact UCNS recursive transition operator producing `157 -> 2881 -> 54837698421` is not yet independently replayed here.
- No independent cryptographic/security review is implied by this migration or by the PCEA runtime tests.
- Public authenticity receipts remain unimplemented and must be supplied by a separate signature/transparency/verifier layer before any public proof claim.
- Public Gonol projection may be useful as a public vocabulary/indexing layer, but no Public Gonol position operation or authenticity property is inferred here.
- The actual UCNS recursive gonol geometry remains unresolved. The interpolation-control prediction `164513086777` has status `UNRESOLVED`: no independent UCNS constructor has produced a comparison value, so it is neither `SURVIVED` nor `FALSIFIED`.
- Executable candidate carrier operations, ordered coupling, and atomic promotion exist, but their selected geometric realization, origin attachment, next-scale placement, recursive successor, and completed 2881-gonol structure remain unresolved. Historical candidate records retain the source identities and standings of their original runs.
