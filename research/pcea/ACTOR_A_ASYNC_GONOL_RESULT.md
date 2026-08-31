# Actor A result: asynchronous gonol key-state candidate

**Standing:** research result, not PCEA runtime, not UCNS canon, not a public-key or hardness claim.

## Source recovery

Actor A checked the refreshed stack boundary and materialized the exact legacy PCEA research lane from `The-Interdependency/pcea@ecf2ca0dec38bef29382e02121b0edde66763aa9`. The legacy materializer verified 36 files, including `pcea-ucns/gonal_architecture.py` at blob `a24e31110521b30ca941bf151b99458a06c910af`.

No source-level recursive gonol transition operator for:

```text
157 -> 2881 -> 54837698421
```

was present in the current stack refresh, the pinned UCNS authority, or the migrated PCEA research lane. UCNS still records the full recursive-scale transition law as `hmmm`.

## Frozen operator

The exact operator recoverable from the available evidence is therefore an observation-index candidate:

```text
operator_id = pcea.async_gonol.observation_second_difference.v1
y_i = y_0 + i*d_1 + (i*(i-1)//2)*d_2
y_0 = 157
d_1 = 2724
d_2 = 54837692816
```

This independently replays:

```text
y_0 = 157
y_1 = 2881
y_2 = 54837698421
```

and derives the next candidate gonol:

```text
y_3 = 164513086777
```

This next value is a falsifiable research coordinate under the frozen candidate operator. It is not promoted as the UCNS recursive-scale law.

## Lazy key-state candidate

The executable candidate is in `async_gonol_keys.py`. It models gonol recursion as an asynchronous address topology over ordinary secret-derived keys:

```text
traffic_key = HMAC-SHA256(root_secret,
                          protocol_label,
                          operator_id,
                          gonol_size,
                          recursive_path,
                          position,
                          epoch,
                          message_counter,
                          state_digest,
                          transcript_digest)
```

The root secret is the only entropy-bearing input. Gonol size, geometry, path, position, and receipts are synchronization/addressing context only.

The test suite exercises:

- exact replay of `157 -> 2881 -> 54837698421`;
- derivation of `164513086777` under the named candidate operator;
- lazy single-coordinate derivation without expanding the gonol;
- key changes when path, state, transcript, position, or message counter changes;
- out-of-order receive support by address;
- replay rejection by receiver-side coordinate cache;
- comparison guardrails that keep the security basis external to gonol geometry.

## Comparison

Against an ordinary linear ratchet, the gonol-addressed candidate has better natural out-of-order derivation because the receiver can derive from public path/position/epoch/message coordinates. Replay protection is not inherent; it requires a coordinate cache or equivalent nonce discipline.

Against an ordinary tree KDF, the candidate is similar: both can derive sparse branches lazily. No compromise-containment advantage is credited to gonol geometry. Containment still depends on root-secret separation, subkey erasure, and ratcheting policy.

Recovery is promising only as an addressability feature: path and state receipts can help a receiver resynchronize, but the public metadata itself becomes an attack surface for linkability and state leakage.

## Freeze receipt

Generated evidence:

```text
research/pcea/async_gonol_key_state_freeze.json
receipt_digest = cbc1343a69bc3b72a93351348ab0cba4962b25d06cd27bc9450f722a4f11814f
```

Source identities bound in the receipt:

```text
pcea_cleanup_commit = 91ffa8c7249dfb810ca64a0bbc500481c0bd12a9
stack_refresh_commit = eaec7fd6ee4e829b6fae10a2c6d520b35857137d
legacy_research_source_commit = ecf2ca0dec38bef29382e02121b0edde66763aa9
pinned_public_gonol_sha256 = 55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5
```

## hmmm

- Exact UCNS recursive-scale transition law remains unresolved.
- `164513086777` is only the next value under the frozen observation candidate.
- Any public-authenticity layer still requires normal signatures, MACs, transparency logs, timestamps, and receipt verification outside this candidate.
- Any deployment would need attack review for metadata leakage, skipped-coordinate exhaustion, replay cache persistence, state-loss recovery, and compromise recovery.
