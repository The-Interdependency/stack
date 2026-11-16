# URPCS v1 independent decoder replay

**Frozen:** 2026-09-21

**Public-contract base:** `d3a38d4ef5e401bc43902face41f805462d88877`

**Implementation freeze:** `5d205978f2a034969782e743c59f62aca83fc92c`

**Classification:** `SURVIVED_INDEPENDENTLY`

An independently structured JavaScript decoder reproduced the committed URPCS
v1 plaintexts, deterministic receipts, and successor states. It also rejected
wrong associated data and an authenticated-body mutation at tag verification.

The decoder was constructed from `docs/urpcs-v1-spec.md`, the committed vector
JSON, framing bytes, and source receipt. Before the implementation freeze and
first vector comparison, its construction did not import, copy, or inspect
`urpcs_v1_reference.py` or its tests. Expected plaintext, receipt, and successor
state values are supplied only to the comparison harness after `decode` returns;
the decoder itself receives the committed ciphertext, initial state, and
associated-data bytes directly.

This result preserves URPCS as Stack-local authenticated-codec research. It
makes no confidentiality, encryption-security, production-suitability,
PCEA-compatibility, or UCNS-gonol claim.

## Frozen artifacts

| artifact | SHA-256 |
|---|---|
| repaired public specification | `295cd721a19475e683b1831f1a15b3c7eed521cec551d68cd031bfed4757423e` |
| committed vector JSON | `1d96299a016feed6f2e0881a5d4d21c20229714dab5eaa9338008d5282c2dfe6` |
| independent decoder at freeze | `c9490f772b41934ba1c878a2d081477974ef19387f048ed489359ea8bfda089d` |
| independent replay harness at freeze | `8fb1af64a87249755157ee1f72ed92fa82bf807fa8513e2e9f87966de99c2bc8` |

The implementation freeze preceded the first ciphertext replay. No decoder
correction was required after that comparison.

## Exact replay identities

All positive vectors use these 15 associated-data bytes:

```text
555250435320766563746f72207631
```

Their SHA-256 identity is
`b9663436beff15b0563d459bc761826b4c5a316f7350f106be02f7c3675c2745`.

| vector | ciphertext bytes / SHA-256 | recovered plaintext | deterministic receipt |
|---|---|---|---|
| `empty_r0` | 205 / `60fc120c11bb02533aef7f8cf0ad62ff2b09b26571998fd3adaae800e8c58552` | empty | `528070861f8226b8518c39707e05f4841724b315256e588cf2d5c3e8c5926426` |
| `empty_r1` | 146,210 / `eb17f5674651d83ba79065bab09bba2c405aec6732915ca9fc06a3ddb68ad565` | empty | `1432924dd876e1fec74ad7b04084309bce62fc7ad98fde5cd250b607b68eff74` |
| `odd_09_r0` | 2,534 / `878f3f828afcc27fd55ea5daaf240710bd09ae05d2a68dc4ea943309c0a57173` | `09` | `294734d163bf393292465421d7384a56cf7d07fc00a515beadd4d6483ebd93f1` |

The independently derived successor states exactly equal the committed states:

| vector | next `k_pair` | next `k_integrity` | next `k_advance` | next `nu_origin` | `R_cap` |
|---|---|---|---|---|---:|
| `empty_r0` | `264799e279acd7204425a174e26893dd8aa9f2524e96d124aaa58c3efe751124` | `86e9d0da678bd21bd3ac50f300236f1c3f8c00b7e0da9ae2174c74c749873cda` | `874a8872a56f50dfb6cddcab8aa82571573c24eee4e81434cf32bb60c3bfe3e4` | `0000000000000000000000000000000000000000000000000000000000000001` | 0 |
| `empty_r1` | `81d0a453e4eb0710eac2efaf82fc48a5b0ea6bfa25eef96396d197784cd9ea97` | `44fbd6ae562a7761aa58db4b11c9c40122983b181ca5a7b090092211ad766fb3` | `f918b5ece11d3dd5d258e7c5324e58ebe2c281c6ec7d44637aeaf0fc43aa9d72` | `0000000000000000000000000000000000000000000000000000000000000001` | 1 |
| `odd_09_r0` | `60066a03db229c15c3ef97cc908ebff6b1682f08668ea8e49cd86f6cdb3be4a0` | `ddfd57437a7244a44bc0b70ea88190723574ea2714f4d1ab2a343be3f16aef46` | `dcad41208c9bb3585d6a16dfa2f439c5b827a63998b726d4b0abf6968d6d94b0` | `0000000000000000000000000000000000000000000000000000000000000001` | 0 |

## Authentication rejection

- The 16-byte wrong associated data
  `555250435320766563746f7220763121` has SHA-256
  `70736147b2dc31d6a78163e18d73c32cf03c86356c02eec909d06fda57a9b632`
  and is rejected at tag verification.
- The 2,534-byte authenticated-body mutation has SHA-256
  `94de735983fe1fe37ffec2bf4b6c0140523a0a18edae7a3708537c1f6f62d828`.
  It changes zero-based ciphertext offset 1,986 from `0x55` to `0x54` and is
  rejected at tag verification.

Both failures occur before bootstrap parsing, plaintext recovery, receipt
construction, or state advance.

## Independent KMAC256 check

The decoder contains its own BigInt Keccak-f[1600], cSHAKE256, and KMAC256
implementation. Before ciphertext replay, it reproduced NIST SP 800-185 KMAC
Sample #4 for key bytes `0x40` through `0x5f`, data `00010203`, customization
string `My Tagged Application`, and a 64-byte output:

```text
20c570c31346f703c9ac36c61c03cb64c3970d0cfc787e9b79599d273a68d2f7
f69d4cc3de9d104a351689f27cf6f5951f0103f33f4f24871024d9c27773a8dd
```

OpenSSL's external `KMAC-256` implementation reproduced the same official
known-answer output. This confirms the primitive implementation and does not
make an encryption-security claim for URPCS.

## Usage guidance

Run the independent KMAC known-answer check:

```bash
node research/urpcs/urpcs_v1_independent.js --kat
```

Decode one committed vector from ciphertext, state, and associated data:

```bash
node research/urpcs/urpcs_v1_independent.js \
  --vector empty_r0 research/urpcs/vectors/urpcs-v1-vectors.json
```

Run the full independent replay and negative checks:

```bash
node research/urpcs/tests/test_independent_decoder.js
```

## Claim boundary

- **Established:** the repaired public contract is sufficient for an
  independently structured decoder to reproduce the three required plaintexts,
  receipts, successor states, and authenticated rejection behavior.
- **Preserved:** the historical blocked audit remains correct for its older,
  incomplete specification input.
- **Unclaimed:** confidentiality, encryption security, production suitability,
  PCEA compatibility, UCNS-gonol identity, or independent release authority.

## hmmm

The mirror has a door for the committed bounded profile. That door establishes
independent decoding interoperability, not a security model or production
system.
