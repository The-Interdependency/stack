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

The current candidate line is asynchronous PCEA key orchestration over gonol state. The observed `157 -> 2881 -> 54837698421` progression is research evidence, not yet a cryptographic hardness claim or UCNS recursive-scale law.

Actor A froze the observation-level replay in `async_gonol_keys.py`, generated `async_gonol_key_state_freeze.json`, and recorded the narrative in `ACTOR_A_ASYNC_GONOL_RESULT.md`. The independently replayed observation derives `164513086777` as the next candidate value under `pcea.async_gonol.observation_second_difference.v1`. That operator is a falsifiable observation candidate, not the unresolved UCNS recursive-scale law.

PCEA keys must still derive from real secret entropy; gonol state may organize, address, ratchet, or synchronize that entropy but must not be credited with entropy merely because the address space is large.

## Usage guidance

1. Read `BASE.json`, `MIGRATION.json`, and any current result receipt before starting a PCEA experiment.
2. Resolve exact current PCEA/UCNS commits needed by the experiment; do not silently substitute `latest`.
3. Materialize only legacy lanes you actually need.
4. Put new or mutating research here, never back into the stable PCEA repo.
5. Preserve negative results and attack harnesses; a passing harness grants permission for a harder attack, not a security claim.
6. Graduate only completed, bounded behavior back to `The-Interdependency/pcea` through an explicit owning-repository change.

## hmmm

- The exact UCNS recursive transition operator producing `157 -> 2881 -> 54837698421` is still not recovered; only a named observation-level replay candidate exists here.
- No independent cryptographic/security review is implied by this migration or by the PCEA runtime tests.
