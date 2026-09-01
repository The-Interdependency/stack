# Actor A result: asynchronous gonol key-state candidate

**Standing:** research result, not PCEA runtime, not UCNS canon, not a public-key or hardness claim.

## 2026-09-01 provenance refresh

Stack branch `research/pcea-async-gonol-keys-a` was refreshed from prior Actor A commit `ce41ceb86b0e4819bfbb976f3ce187567391af48` and merged with stack `origin/main@04253ab5bed7e913ab3df7bbb00939340bca291e`, producing branch parent `675836eef7bbcdaaa2edc4f8246591617e161955` before this refresh commit.

Current exact authority identities checked:

```text
stack/libs/pcea pinned source = The-Interdependency/pcea@91ffa8c7249dfb810ca64a0bbc500481c0bd12a9
PCEA live main = The-Interdependency/pcea@834987cb0c1fea5f62d6ea08e5c5bb878c312646
stack/libs/ucns pinned source = The-Interdependency/ucns@1975fe70cf4e0826a8020c2da3047569e277af64
UCNS live main = The-Interdependency/ucns@cff04c85df5a56fd3f9d3b178e7c49160d749652
UCNS public_gonol.py blob = c1955e46e2dc918fb657cb346e42106d71937e91
PCEA pyproject.toml blob = a4c2d9449c77765c0698afb869ecfd08bc1c5483
```

The relevant UCNS Public Gonol carrier blob remains unchanged between the stack-pinned UCNS snapshot and live UCNS main. Live UCNS `CANON.md` still records the full recursive-scale transition law as `hmmm`; no actual recursive UCNS gonol constructor value for the next step was available.

## Source recovery

Actor A checked the refreshed stack boundary and materialized the exact legacy PCEA research lane from `The-Interdependency/pcea@ecf2ca0dec38bef29382e02121b0edde66763aa9`. The legacy materializer verified 36 files, including `pcea-ucns/gonal_architecture.py` at blob `a24e31110521b30ca941bf151b99458a06c910af`.

No source-level recursive gonol transition operator for:

```text
157 -> 2881 -> 54837698421
```

was present in the current stack refresh, the pinned UCNS authority, or the migrated PCEA research lane. UCNS still records the full recursive-scale transition law as `hmmm`.

## Interpolation baseline

The exact replay baseline recoverable from the available evidence is therefore an observation-index interpolation candidate:

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

and predicts the next candidate gonol:

```text
y_3 = 164513086777
```

This next value is frozen as a prediction under the interpolation baseline. It is not promoted as the UCNS recursive-scale law and must be compared with the actual UCNS constructor output once that constructor exists.

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
- prediction of `164513086777` under the named interpolation baseline;
- unresolved actual-UCNS constructor status and the match/mismatch comparison rule;
- lazy single-coordinate derivation without expanding the gonol;
- key changes when path, state, transcript, position, or message counter changes;
- out-of-order receive support by address;
- replay rejection by receiver-side coordinate cache;
- deferral of linear/tree/gonol key-addressing comparison until the out-of-sample UCNS value exists.

## Out-of-sample gate

The actual UCNS recursive gonol constructor is still unresolved. The current comparison state is:

```text
actual_next_gonol = hmmm
prediction = 164513086777
baseline_outcome = UNRESOLVED
```

When the actual UCNS constructor supplies a next value:

```text
actual != 164513086777 -> quadratic/interpolation candidate FALSIFIED
actual == 164513086777 -> SURVIVED one out-of-sample test
```

The linear/tree/gonol key-addressing comparison is deferred until that out-of-sample gate resolves. When it runs, all schemes must use the same standard KDF and root entropy; gonol size or geometry still does not contribute entropy or hardness.

## Freeze receipt

Generated evidence:

```text
research/pcea/async_gonol_key_state_freeze.json
schema = pcea.async-gonol-key-state.freeze.v2
receipt_digest = e15e34b8dde02088ca74502ae2d583d6f0b273c298e5e690fe4030668bffdcee
```

Source identities bound in the receipt:

```text
pcea_stack_pinned_commit = 91ffa8c7249dfb810ca64a0bbc500481c0bd12a9
live_pcea_main_commit = 834987cb0c1fea5f62d6ea08e5c5bb878c312646
ucns_stack_pinned_commit = 1975fe70cf4e0826a8020c2da3047569e277af64
live_ucns_main_commit = cff04c85df5a56fd3f9d3b178e7c49160d749652
stack_pcea_refresh_commit = eaec7fd6ee4e829b6fae10a2c6d520b35857137d
stack_origin_main_at_refresh = 04253ab5bed7e913ab3df7bbb00939340bca291e
stack_branch_parent_at_refresh = 675836eef7bbcdaaa2edc4f8246591617e161955
prior_actor_a_commit = ce41ceb86b0e4819bfbb976f3ce187567391af48
legacy_research_source_commit = ecf2ca0dec38bef29382e02121b0edde66763aa9
pinned_public_gonol_sha256 = 55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5
```

## hmmm

- Exact UCNS recursive-scale transition law remains unresolved.
- `164513086777` is only a prediction under the frozen interpolation baseline.
- Any public-authenticity layer still requires normal signatures, MACs, transparency logs, timestamps, and receipt verification outside this candidate.
- Any deployment would need attack review for metadata leakage, skipped-coordinate exhaustion, replay cache persistence, state-loss recovery, and compromise recovery.
