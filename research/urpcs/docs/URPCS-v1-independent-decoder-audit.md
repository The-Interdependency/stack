# URPCS v1 independent-decoder sufficiency audit

**Frozen:** 2026-09-21

**Base commit:** `db5635c7d48652d6506c3bd343f8ead0bb53872e`

**Classification:** `BLOCKED_NOT_INDEPENDENTLY_SPECIFIED`

The committed public contract does not determine a URPCS v1 decoder. No
independent decoder was implemented, because filling the gaps below would invent
missing laws. This result preserves URPCS as Stack-local authenticated-codec
research. It makes no confidentiality, encryption-security, PCEA-compatibility,
or UCNS-gonol claim.

The blocker was frozen without importing, copying, or inspecting
`urpcs_v1_reference.py` or its reference tests. The audit used only the committed
specification, vector JSON, framing bytes present in the vectors, source receipt,
and workspace declarations.

## Sufficiency result

The public specification normatively defines the five-element deterministic-CBOR
witness, its row schemas, canonical set ordering, the 32-bit `R_cap` encoding, and
the single legal finished traversal cursor. It lists the names of Laws 1 and 3–12,
but does not state their executable rules.

The smallest missing public rules are:

1. **Frame and authentication (Law 11).** Define every `URPCF001` header field,
   width, byte order, canonical constraint, and length relation. Define the exact
   KMAC256 invocation: key, message transcript, associated-data encoding,
   customization string, output length, tag placement, comparison rule, and
   failure order.
2. **Bootstrap boundary (Law 1).** Define every `URPCS001` header field and the
   exact composition and consumption of `C_0`: witness length, depth/cap field,
   final-layer boundary, trailing-byte rule, and size checks.
3. **Layer wire and reverse operation (Laws 3–10, including the Law 9 patch).**
   Define the complete `URGON001` schema and canonical re-encoding, all row and
   identifier validation needed by decoding, and deterministic pseudocode that
   reconstructs each preceding byte string from the authenticated final layer and
   witness. In particular, the public contract must say how pairs, carries,
   leftovers, occurrences, attachment order, and exact-depth halt recover the
   plaintext.
4. **Receipt and linear advance (Law 12).** Define the receipt byte transcript and
   primitive, then the exact derivation of all three successor keys, origin nonce,
   and retained `R_cap`, including domain separation, output sizes, exhaustion,
   and failure atomicity.

Publishing examples alone cannot select these rules. A decoder that hard-coded the
three committed ciphertexts could agree with the vectors while implementing no
URPCS law; guessing field meanings or KMAC domain strings from repeated bytes would
likewise be an invented contract.

## Observed framing facts, not inferred laws

The three positive ciphertexts each have 56 bytes beyond `C_0`: an observed
24-byte prefix beginning `URPCF001` and an observed 32-byte suffix. Each `C_0`
has an observed 24-byte prefix beginning `URPCS001`, followed by the committed
`beta_hex` bytes and the last listed `URGON001` layer. These equalities hold for
the fixtures, but the public specification does not assign normative field
semantics to the prefixes or define the authentication transcript.

For `empty_r1`, `C_0` contains the final 30,308-byte layer, not both layer wires:

```text
24 + 115,822 + 30,308 = 146,154
```

That observation makes the missing reverse-layer algorithm load-bearing: the
plaintext cannot be recovered by merely slicing an embedded original layer.

## Exact committed byte identities

The public contract files audited at the base commit have these identities:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `docs/urpcs-v1-spec.md` | 4,583 | `45d9020545117926a80f6f2379ad8246e53e6ce1d41313c9718f3acbfaa139ce` |
| `vectors/urpcs-v1-vectors.json` | 904,545 | `1d96299a016feed6f2e0881a5d4d21c20229714dab5eaa9338008d5282c2dfe6` |
| `SOURCE_RECEIPT.json` | 2,697 | `b3806d51dc5d2313274c4ff03be18c0a15ae6710bdcad364060a237789de0cf2` |

The vector artifact is 904,545 bytes with SHA-256
`1d96299a016feed6f2e0881a5d4d21c20229714dab5eaa9338008d5282c2dfe6`,
equal to its integrated source receipt.

All positive vectors use the same 15 associated-data bytes:

```text
555250435320766563746f72207631
```

Their SHA-256 identity is
`b9663436beff15b0563d459bc761826b4c5a316f7350f106be02f7c3675c2745`.

| vector | plaintext hex | beta bytes / SHA-256 | C0 bytes / SHA-256 | ciphertext bytes / SHA-256 | deterministic receipt |
|---|---|---|---|---|---|
| `empty_r0` | empty | 66 / `2995f550367c1cb4ead278f47dead1bd8dd0cc8c37537520ee550ebbfeedae28` | 149 / `f748cf7bea1a34629eadb1ccb846e785ab2bb573e77a3b1ba5f4a98de6065251` | 205 / `60fc120c11bb02533aef7f8cf0ad62ff2b09b26571998fd3adaae800e8c58552` | `528070861f8226b8518c39707e05f4841724b315256e588cf2d5c3e8c5926426` |
| `empty_r1` | empty | 115,822 / `7ce3775b5b8dd9cd9930b772e710dafff36be0aa31d2bbc38749e6f708ca638d` | 146,154 / `246983bb69b9a4b38a15d06d20f9483b178c62601291422ab7e79f55573f4696` | 146,210 / `eb17f5674651d83ba79065bab09bba2c405aec6732915ca9fc06a3ddb68ad565` | `1432924dd876e1fec74ad7b04084309bce62fc7ad98fde5cd250b607b68eff74` |
| `odd_09_r0` | `09` | 1,938 / `3142e72095c71500b4be2df1eba7cb33a1a415d7dc18abea2b5e88e9dacd5d7a` | 2,478 / `fdba402813e2bcb49470ab30285778c9cb6237c2554db2e6220153820da3300b` | 2,534 / `878f3f828afcc27fd55ea5daaf240710bd09ae05d2a68dc4ea943309c0a57173` | `294734d163bf393292465421d7384a56cf7d07fc00a515beadd4d6483ebd93f1` |

The initial byte identities are:

```text
k_pair      = 000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
k_integrity = 202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f
k_advance   = 404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f
nu_origin   = 0000000000000000000000000000000000000000000000000000000000000000
R_cap       = 0 (`empty_r0`, `odd_09_r0`) or 1 (`empty_r1`)
```

The committed successor states are:

| vector | next `k_pair` | next `k_integrity` | next `k_advance` | next `nu_origin` | `R_cap` |
|---|---|---|---|---|---:|
| `empty_r0` | `264799e279acd7204425a174e26893dd8aa9f2524e96d124aaa58c3efe751124` | `86e9d0da678bd21bd3ac50f300236f1c3f8c00b7e0da9ae2174c74c749873cda` | `874a8872a56f50dfb6cddcab8aa82571573c24eee4e81434cf32bb60c3bfe3e4` | `0000000000000000000000000000000000000000000000000000000000000001` | 0 |
| `empty_r1` | `81d0a453e4eb0710eac2efaf82fc48a5b0ea6bfa25eef96396d197784cd9ea97` | `44fbd6ae562a7761aa58db4b11c9c40122983b181ca5a7b090092211ad766fb3` | `f918b5ece11d3dd5d258e7c5324e58ebe2c281c6ec7d44637aeaf0fc43aa9d72` | `0000000000000000000000000000000000000000000000000000000000000001` | 1 |
| `odd_09_r0` | `60066a03db229c15c3ef97cc908ebff6b1682f08668ea8e49cd86f6cdb3be4a0` | `ddfd57437a7244a44bc0b70ea88190723574ea2714f4d1ab2a343be3f16aef46` | `dcad41208c9bb3585d6a16dfa2f439c5b827a63998b726d4b0abf6968d6d94b0` | `0000000000000000000000000000000000000000000000000000000000000001` | 0 |

The wrong-AD fixture supplies 16 bytes,
`555250435320766563746f7220763121`, with SHA-256
`70736147b2dc31d6a78163e18d73c32cf03c86356c02eec909d06fda57a9b632`.
The authenticated-body mutation remains 2,534 bytes, has SHA-256
`94de735983fe1fe37ffec2bf4b6c0140523a0a18edae7a3708537c1f6f62d828`,
and differs from `odd_09_r0` only at zero-based ciphertext offset 1,986:
`0x55` becomes `0x54`.

These values record the expected fixtures. Because Law 11 is incomplete, this
audit cannot independently establish either negative rejection; because Law 12
is incomplete, it cannot independently establish receipt or next-state equality.

## Independent KMAC256 primitive check

OpenSSL 3.0.13's external `KMAC-256` implementation reproduced NIST's official
SP 800-185 KMAC Sample #4. Inputs were key bytes `0x40` through `0x5f`, data
`00010203`, customization string `My Tagged Application`, and a 64-byte output.

```bash
printf '\x00\x01\x02\x03' | openssl mac \
  -macopt hexkey:404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f \
  -macopt size:64 \
  -macopt 'custom:My Tagged Application' \
  KMAC-256
```

Observed and official output:

```text
20c570c31346f703c9ac36c61c03cb64c3970d0cfc787e9b79599d273a68d2f7
f69d4cc3de9d104a351689f27cf6f5951f0103f33f4f24871024d9c27773a8dd
```

Official sample:
<https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/KMAC_samples.pdf>

This confirms the available KMAC256 primitive, not the absent URPCS-specific
KMAC transcript.

## Usage guidance

Recheck the audited base identities without reading the reference module. The
explicit revision keeps later source-receipt clarifications from changing the
historical input set:

```bash
git show db5635c7d48652d6506c3bd343f8ead0bb53872e:research/urpcs/docs/urpcs-v1-spec.md | sha256sum
git show db5635c7d48652d6506c3bd343f8ead0bb53872e:research/urpcs/vectors/urpcs-v1-vectors.json | sha256sum
git show db5635c7d48652d6506c3bd343f8ead0bb53872e:research/urpcs/SOURCE_RECEIPT.json | sha256sum
```

Future decoder work may resume only after the public specification supplies the
four rule groups above. The repaired contract should be reviewed before any
reference comparison, and a new implementation should consume only
`ciphertext_hex`, `initial_state`, and `ad_hex`; `plaintext_hex`, `receipt_hex`,
and `next_state` remain comparison outputs.

## Claim boundary

- **Established:** the committed public contract is insufficient to select a
  decoder, and OpenSSL's KMAC256 matches the cited official known-answer sample.
- **Not evaluated independently:** plaintext recovery, receipt equality,
  successor-state equality, wrong-AD rejection, or body-mutation rejection.
- **Unclaimed:** confidentiality, encryption security, production suitability,
  PCEA compatibility, or UCNS-gonol identity.
