# URPCS v1 — frozen maps and laws

Status: Laws 1–13 accepted.
Law 2 decision: five-element `Wire` remains in force. Law 2A is future-version only.
Byte-exact vectors: implemented and verified under the bounded harness profile.
Confidentiality: unclaimed. Wire is authenticated glass.

---

## Closed decision — Law 2 retained

```
Wire(W_t) = [ A_t, R_t, Δ_t, T_t, L_t ]
```

DecodeWitness requires exactly one top-level **five**-element array that consumes all of β.

Bootstrap (`URPCS001`) and frame (`URPCF001`) already select the v1 grammar.
An extra element inside β would duplicate that boundary and change every
downstream byte. Law 2A is not part of v1.

---

## Law 2 row schemas (verbatim authority)

CBOR profile: RFC 8949 §4.2 deterministic encoding.
Allowed major types: definite-length arrays, byte strings, booleans.
No maps, tags, floats, or CBOR integers.

`N(0) = h''`. For n > 0, `N(n)` is the minimal big-endian magnitude.
Every `N(·)` slot is a CBOR byte string. Leading zero bytes fail.

Identifiers (`Axis`, `Origin`, `OccId`, `GonolId`) are CBOR byte strings.

```
A row:        [ N(r), N(j), g, [ N(n_children), N(n_leftover) ] ]
R_origin:     [ N(r), N(j), O ]
R_pair:       [ N(r), o1, o2 ]
R_member:     [ o, g ]
R_occur:      [ a, O, N(position), o ]
R_attach:     [ g_parent, g_child, N(r) ]
Δ row:        [ g_parent, g_child, N(δ) ]
T:            [ [ [N(r), N(j), g], ... ], atEnd ]
L:            [ N(q), L_packed ]
```

```
R_t = [ R_origin, R_pair, R_member, R_occur, R_attach ]
```

`q = |L_t|`. Bits packed MSB-first; unused low bits of the last packed byte are zero.
Law 10: `L_t = BE32(R_cap_t)`, so `q = 32` and `L_packed` is exactly 4 bytes.

Sets: array sorted by the complete deterministic-CBOR bytes of each row. Duplicate rows fail.
Pairs: `o1 <_bytes o2`.
Traversal stack keeps semantic order and is never sorted.

```
EncodeWitness(W_t, K_t) = dCBOR(Wire(W_t))
```

v1: `K_t` does not alter β bytes.

---

## Law 13 — Traversal cursor v1

After successful `WitnessBuild`, the only legal cursor is

```
T_t = [ [], true ]
```

Empty stack. `atEnd = true`.

Reverse traversal is derived from the canonical relations and layer objects,
not from a live cursor in `T_t`. The field exists because Law 2 put it on
the wire; v1 assigns it a single finished value so β is unique.

`DecodeWitness` fails any other stack or `atEnd` value.
`WitnessBuild` must emit exactly this cursor.

A later wire version may delete `T_t`. That is not v1.

---

## Accepted law index

| Law | Name |
|---|---|
| 1 | Bootstrap boundary v1 (`URPCS001` + ℓ) |
| 2 | Canonical witness encoding v1 (five-element Wire) |
| 3 | Rooted attachment forest v1 |
| 4 | Occurrence partition and gonol formation v1 |
| 5 | Detect and occurrence identity v1 |
| 6 | Keyed pairing v1 |
| 7 | Origin generation v1 |
| 8 | Canonical attachment tree v1 |
| 9 | Layer object and serialization v1 (`URGON001`) |
| 9 patch | LayerWire re-encode equality (required by Law 12) |
| 10 | Exact-depth halt v1 |
| 11 | Integrity and framing v1 (`URPCF001`, KMAC256 tag) |
| 12 | Receipt-bound linear advance v1 |
| 13 | Traversal cursor v1 (`T = [[], true]`) |

---

## K_t

```
K_t = (k_pair, k_integrity, k_advance, ν_origin, R_cap)
```

Three 256-bit keys pairwise distinct.
`ν_origin = 2^256−1` exhausts the chain.

---

## Test harness profile (not wire)

```
x = 1 byte
M = 8
|D|_max = 1 byte
R_max = 1
|D^{(r)}|_max = 1 MiB
|LayerWire|_max = 1 MiB
|β|_max = 4 MiB
|C_0|_max = 8 MiB
|TraceWire|_max = 16 MiB
```

Exceeding a harness cap is test failure / codec Fail, never an alternate Halt.

Implemented vectors:

1. empty D, R = 0
2. empty D, R = 1
3. D = 0x09 (Detect: three occurrences, one carry)
4. wrong AD
5. authenticated-body mutation
6. replay after successful Advance
7. concurrent reuse, one CAS winner
8. sender/receiver receipt and K_{t+1} equality

Reference artifacts:

- `urpcs_v1_reference.py` — dependency-free encoder, decoder, and tests
- `urpcs-v1-vectors.json` — byte-exact fixtures and deterministic receipts
- `URPCS-v1-vector-report.md` — verification summary and usage guidance

Verification standing: 8/8 named vectors passed; every one-byte plaintext
round-tripped at depth 0 (256/256); the depth-1 empty-input fixture passed.
These are computations from one reference implementation, not independent
interoperability evidence.

---

## Not claimed

Confidentiality; hiding of R, μ, leftovers, lengths, or β;
PCEA compatibility; UCNS-gonol identity;
rollback-resistant storage as a codec theorem;
post-compromise security.
