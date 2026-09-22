# URPCS v1 reference vectors

**Standing:** COMPUTATION under the accepted Laws 1–13 and bounded harness
profile. The vectors establish deterministic codec behavior, integrity failure
boundaries, and synchronized state advancement. Confidentiality remains
unclaimed.

## Results

| Vector | Result | Load-bearing observation |
|---|---:|---|
| `empty_r0` | PASS | Empty plaintext round-trips at depth 0. |
| `empty_r1` | PASS | Empty plaintext round-trips through one serialized recursive layer. |
| `odd_09_r0` | PASS | `0x09` yields three detected occurrences and exactly one carry. |
| `wrong_ad` | PASS | Verification fails before bootstrap parsing. |
| `authenticated_body_mutation` | PASS | A terminal-body bit change fails tag verification before parsing. |
| `replay_after_advance` | PASS | The accepted ciphertext fails under the advanced integrity key. |
| `concurrent_state_rejection` | PASS | One in-memory compare-and-swap wins; the second use of the same state is rejected. |
| `receipt_and_state_equality` | PASS | Every positive fixture gives equal sender/receiver receipts and `K_{t+1}`. |

Additional coverage:

- all 256 possible one-byte plaintexts round-trip at depth 0;
- KMAC256 was checked against one fixed known answer and three independent
  OpenSSL 3 KMAC-256 computations;
- regenerating the JSON produced byte-identical output;
- the Python module compiles without third-party packages.

Post-merge review adds separate regression coverage for witness origin/region
completeness, pre-authentication `MAX_C0` enforcement, true process-local
concurrent single-winner state-slot behavior, and the independent decoder's
bounded `R_cap <= 1` profile gate. These repairs do not change the frozen vector
bytes; they harden acceptance around those bytes.

## Positive-vector receipts

| Vector | `|β|` | `|C₀|` | `|C|` | Receipt |
|---|---:|---:|---:|---|
| `empty_r0` | 66 | 149 | 205 | `528070861f8226b8518c39707e05f4841724b315256e588cf2d5c3e8c5926426` |
| `empty_r1` | 115,822 | 146,154 | 146,210 | `1432924dd876e1fec74ad7b04084309bce62fc7ad98fde5cd250b607b68eff74` |
| `odd_09_r0` | 1,938 | 2,478 | 2,534 | `294734d163bf393292465421d7384a56cf7d07fc00a515beadd4d6483ebd93f1` |

The depth-one empty fixture demonstrates the admitted expansion problem:
recursive structure turns an empty input into a 146,210-byte authenticated
frame. The harness cap contains the experiment; the codec remains unsuitable
as a compressor.

## PR #44 integration receipts

These hashes identify the exact artifacts integrated by PR #44. They are
historical integration receipts, not assertions that later repaired source
retains the same source-file hash. The vector hash remains the byte-exact frozen
fixture identity.

| Artifact | SHA-256 |
|---|---|
| `urpcs-v1-vectors.json` | `1d96299a016feed6f2e0881a5d4d21c20229714dab5eaa9338008d5282c2dfe6` |
| `urpcs_v1_reference.py` at PR #44 integration | `3bcdfcd7a81ea3ce32b757b5912ffffcb5371ae63990f2e7146f03ce6e439650` |

## Usage guidance

From `research/urpcs/`, run the complete positive, negative, and post-merge
regression suite:

```bash
python3 urpcs_v1_reference.py --self-test
python3 -m unittest discover -s tests -p 'test*.py'
```

Regenerate the deterministic JSON:

```bash
python3 urpcs_v1_reference.py --write-vectors urpcs-v1-vectors.json
```

Then compare the regenerated vector file with the committed fixture. Python 3.10
or newer is required; the implementation uses only the standard library.

## Claim boundary

- `COMPUTATION`: the listed fixtures and exhaustive one-byte/depth-zero tests
  passed in the reference implementation.
- `SURVIVED_INDEPENDENTLY`: the separately implemented JavaScript decoder
  reproduced the three committed positive plaintexts, deterministic receipts,
  successor states, and authenticated rejection behavior for the bounded
  profile. See `URPCS-v1-independent-replay.md` for the frozen replay evidence.
- `UNCLAIMED`: confidentiality, rollback-resistant storage, fork merging,
  post-compromise security, or production suitability.

## hmmm

Independent replay closes decoder interoperability for the committed bounded
profile. Confidentiality, durable production state, and independent release
authority remain outside this report.
