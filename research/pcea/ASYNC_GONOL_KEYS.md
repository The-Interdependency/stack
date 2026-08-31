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

## Usage guidance

Do not implement this in `The-Interdependency/pcea` while it remains candidate research. Prototype and attack it here. If a bounded ratchet behavior survives and is useful, promote only that completed behavior to PCEA through an explicit owning-repository change.

## hmmm

The load-bearing unknown is the exact reproducible recursive transition operator. Until independent replay exists, gonol scale is an observed research coordinate, not cryptographic hardness, entropy, or canon.
