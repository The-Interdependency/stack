# Asynchronous gonol-key research

**Standing:** candidate research. Not PCEA runtime, not UCNS canon, not a security claim.

## Observation to preserve

A gonol construction has produced the observed progression:

```text
157 -> 2881 -> 54837698421
```

The exact 157-position Public Gonol is established in current UCNS authority, while the recursive-scale transition law remains unresolved. Therefore the later values are preserved here as observed constructor outputs pending independent replay, not promoted as a mathematical law.

## Cryptographic placement

The useful candidate placement is a deterministic asynchronous key **schedule/state topology**, not an entropy source.

```text
real shared secret / approved key establishment
                 |
                 v
        gonol-addressed ratchet
                 |
                 v
          one-use traffic keys
```

A large gonol can provide sparse addressability, branching, bounded rendezvous, replay coordinates, and hierarchical ratchet state without materializing every possible key. Secret strength still comes from CSPRNG/KEM/pre-shared entropy and an approved KDF.

A candidate derivation shape is deliberately generic until the constructor is replayed:

```text
traffic_key = KDF(root_secret,
                  protocol_label,
                  gonol_identity,
                  recursive_path,
                  position,
                  epoch,
                  message_counter,
                  transcript)
```

Public coordinates may identify where a receiver should derive; they must not substitute for the secret input.

## First falsification program

1. Freeze the exact gonol transition constructor and all source identities.
2. Independently replay `157 -> 2881 -> 54837698421`.
3. Compare the resulting topology against a conventional tree/ratchet with the same root entropy.
4. Measure synchronization recovery, replay rejection, compromise containment, state/storage cost, and message reordering tolerance.
5. Attack public positional metadata for state leakage and linkability.
6. Credit gonol geometry only for properties that beat or simplify the control construction.

## Actor A freeze result

Actor A materialized and verified the legacy PCEA research lane, then searched the current stack refresh, pinned UCNS authority, and migrated PCEA research files. No source-level UCNS recursive-scale transition operator for `157 -> 2881 -> 54837698421` was present.

The frozen executable result is therefore an observation-index interpolation baseline:

```text
operator_id = pcea.async_gonol.observation_second_difference.v1
y_i = y_0 + i*d_1 + (i*(i-1)//2)*d_2
y_0 = 157
d_1 = 2724
d_2 = 54837692816
```

It independently replays:

```text
157 -> 2881 -> 54837698421
```

and predicts:

```text
next = 164513086777
```

This is not a UCNS recursive-scale law. It is a falsifiable prediction for the next out-of-sample UCNS constructor value.

Executable artifacts:

```text
async_gonol_keys.py
tests/test_async_gonol_keys.py
async_gonol_key_state_freeze.json
ACTOR_A_ASYNC_GONOL_RESULT.md
```

The lazy key schedule derives one traffic key per address/path/state coordinate with HMAC-SHA256 over caller-supplied root secret plus public synchronization context. The root secret remains the only entropy-bearing input.

## 2026-09-01 refresh

Current exact live authority checks:

```text
PCEA live main = 834987cb0c1fea5f62d6ea08e5c5bb878c312646
UCNS live main = cff04c85df5a56fd3f9d3b178e7c49160d749652
stack origin/main at refresh = 04253ab5bed7e913ab3df7bbb00939340bca291e
```

Stack still pins PCEA at `91ffa8c7249dfb810ca64a0bbc500481c0bd12a9` and UCNS at `1975fe70cf4e0826a8020c2da3047569e277af64`.

The actual recursive UCNS gonol constructor remains unresolved in live UCNS. Therefore:

```text
actual_next_gonol = hmmm
prediction = 164513086777
baseline_outcome = UNRESOLVED
linear/tree/gonol key-addressing comparison = DEFERRED
```

Once UCNS supplies the actual next value, compare it directly:

```text
mismatch -> interpolation candidate FALSIFIED
match -> SURVIVED one out-of-sample test
```

## Usage guidance

Do not implement this in `The-Interdependency/pcea` while it remains candidate research. Prototype and attack it here. If a bounded ratchet behavior survives and is useful, promote only that completed behavior to PCEA through an explicit owning-repository change.

## hmmm

The load-bearing unknown is still the exact UCNS recursive transition operator. Independent replay now exists for the supplied observation under a named interpolation baseline, but gonol scale remains a research coordinate, not cryptographic hardness, entropy, or canon.
