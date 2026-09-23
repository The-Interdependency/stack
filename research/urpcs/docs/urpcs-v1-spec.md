# URPCS v1 — normative public codec contract

Status: Laws 1–13 accepted and stated here as executable public rules.

Standing: **COMPUTATION; research, not canon**. URPCS v1 is an authenticated,
stateful recursive pairing codec. It makes no confidentiality claim. Its witness,
pairing, origins, attachment tree, phases, depth, and lengths are public.

This document is the public interoperability contract. A decoder must be
derivable from this document, RFC 8949 deterministic CBOR, NIST SP 800-185
KMAC256, and FIPS 202 SHA3-256. The reference module and committed vectors are
evidence, not normative inputs to a new implementation.

---

## 0. Conventions and failure discipline

- `h'...'` denotes bytes written in hexadecimal. `ASCII(s)` denotes the ASCII
  bytes of `s`. `||` is byte concatenation.
- Multi-byte fixed-width integers in headers are unsigned big-endian.
- Byte-string comparison is lexicographic from the first byte.
- `N(0) = h''`. For `n > 0`, `N(n)` is the minimal unsigned big-endian
  magnitude. Leading zero bytes are forbidden.
- `dCBOR` is RFC 8949 §4.2 deterministic encoding restricted in witness and
  layer objects to definite-length arrays, byte strings, and booleans. CBOR
  integers, maps, tags, floats, indefinite lengths, and trailing bytes fail.
- All formulas using KMAC256 request 256 output bits (32 bytes). The final
  argument is the KMAC customization byte string.
- Parsing uses overflow-safe length arithmetic and applies configured resource
  limits before allocation.
- `Fail` releases no plaintext and does not call `Advance`. Authentication is
  verified before parsing the bootstrap, witness, or terminal body.

The pre-message state is

```text
K_t = (k_pair, k_integrity, k_advance, nu_origin, R_cap)
```

where the first three fields are distinct 32-byte values, `nu_origin` is exactly
32 bytes interpreted as an unsigned big-endian integer, and
`0 <= R_cap <= 2^32-1`. A state is single-use.

Public parameters for the committed harness are `x = 1` byte and `M = 8`.
The algorithms below are defined for `x >= 1` and `M >= 2`; changing either is
an explicit profile change.

---

## Law 1 — bootstrap boundary v1

Let

```text
beta = EncodeWitness(W_t, K_t)
Bootstrap(W_t, K_t) = H_boot(len(beta)) || beta
C_0 = H_boot(ell) || beta || B_terminal
ell = len(beta)
```

`H_boot` is exactly 24 bytes:

| offset | size | field | required v1 value |
|---:|---:|---|---|
| 0 | 8 | magic | `ASCII("URPCS001")` |
| 8 | 2 | version | `1` |
| 10 | 2 | header length | `24` |
| 12 | 8 | witness length `ell` | `len(beta)` |
| 20 | 4 | flags | `0` |

After successful header parsing:

```text
beta       = C_0[24 : 24 + ell]
B_terminal = C_0[24 + ell :]
```

`WitnessRecover(C_0, K_t)` fails if `len(C_0) < 24`, any fixed field differs,
`ell > len(C_0)-24`, length arithmetic overflows, or `DecodeWitness` fails.
The reverse order is fixed: `Unframe`, `Verify` over all of `C_0`, parse this
header, decode `beta`, then call `DeserializeBody(B_terminal, W_t)`.

---

## Law 2 — canonical witness encoding v1

The witness is

```text
W_t = (A_t, R_t, Delta_t, T_t, L_t)
Wire(W_t) = [A_t, R_t, Delta_t, T_t, L_t]
R_t = [R_origin, R_pair, R_member, R_occur, R_attach]
```

The top-level array has exactly five elements. Law 2A, which would prepend a
version element, is not part of v1.

Every identifier (`Axis`, `Origin`, `OccId`, `GonolId`) is a CBOR byte string.
Every numeric slot below is a CBOR byte string containing `N(value)`.

```text
A row:        [N(r), N(j), g, [N(n_children), N(n_leftover)]]
R_origin:     [N(r), N(j), O]
R_pair:       [N(r), o1, o2]
R_member:     [o, g]
R_occur:      [a, O, N(position), o]
R_attach:     [g_parent, g_child, N(r)]
Delta row:    [g_parent, g_child, N(delta)]
T:            [[[N(r), N(j), g], ...], atEnd]
L:            [N(q), L_packed]
```

Each set is encoded as an array sorted by the complete deterministic-CBOR bytes
of its rows. Duplicate rows fail. The traversal stack retains semantic order.
Pair rows require `o1 < o2`; equal occurrence identifiers fail. Delta is already
reduced to `0 <= delta < M`.

`q = len(L_t)` in bits. `L_packed` is MSB-first and has `ceil(q/8)` bytes; unused
low bits in its final byte are zero.

```text
EncodeWitness(W_t, K_t) = dCBOR(Wire(W_t))
```

In v1, `K_t` does not change these bytes and the witness is not concealed.
`DecodeWitness` applies every witness-only check from Laws 2–10 and 13; checks
that require reconstructed region bytes remain `ExpandLayer` obligations. It
then requires byte-for-byte re-encoding equality. For each admissible witness:

```text
DecodeWitness(EncodeWitness(W_t, K_t), K_t) = W_t
```

---

## Law 3 — rooted attachment forest v1

Let `V` be all gonol identifiers in `A_t` and `E` all `(parent, child)` pairs in
`R_attach`.

- Every `GonolId` is message-global and occurs in exactly one `A` row.
- Every edge endpoint is in `V`. An attach row's stored `r` must equal the unique
  layer of both endpoints, and both endpoints must share one `(r,j)` region.
- There are no self-edges, duplicate edges, directed cycles, or vertices with
  more than one parent.
- Each undirected component has exactly one indegree-zero root. An isolated
  vertex is a root.
- `(p,c)` is an edge iff exactly one `(p,c,delta)` row exists in `Delta_t`.

Each component root has phase zero. For every edge `p -> g`,

```text
b_g = (b_p + Delta[p,g]) mod M
```

The unique parent path therefore defines every `b_g`.

---

## Law 4 — occurrence partition and gonol formation v1

Region bytes are viewed in byte order with each byte MSB-first. A primitive
axis for a nonempty bit string `u` of length `q` is

```text
a(u) = dCBOR([N(q), u_packed])
```

`u_packed` uses the same MSB-first convention and has zero low padding bits.
Equal bit strings have equal `Axis` values; their occurrences remain distinct.

An occurrence `(a, O, s, o)` covers the half-open bit interval `[s,s+q)`, with
`q` and the payload recovered canonically from `a`.

For every emitted region `(r,j)`:

- exactly one origin row `(r,j,O)` exists, and an origin occurs in exactly one
  origin row;
- occurrence identifiers are message-global and unique;
- occurrence intervals are nonempty, in bounds, pairwise disjoint, and cover
  every region bit exactly once;
- each axis payload equals the covered bits.

Let `O_ids` be that region's occurrence identifiers. Pair endpoints and the
leftover set partition them:

```text
ends(mu) disjoint-union lambda = O_ids
len(lambda) = len(O_ids) mod 2
```

Each pair contains two distinct ids from the same origin. No id repeats.

For stored `o1 < o2`, identifiers for formed gonols are

```text
g_pair  = h'01' || dCBOR([O, o1, o2])
g_carry = h'00' || dCBOR([O, o])
```

Thus v1 `gamma` is injective on unordered occurrence pairs, not on payload pairs.
A carry bypasses `gamma`.

A pair gonol has exactly two member rows; a carry has exactly one. Every
occurrence belongs to exactly one gonol, every gonol has exactly one `A` row, and
there are no extra member rows. A pair row's stored `r`, and its gonol's `A` row
`(r,j)`, must equal the layer and region selected by the members' common origin;
the same `A`-row rule applies to a carry. Its shape is

```text
n_children(g) = attachment-tree out-degree(g)
n_leftover(g) = 1 for carry, 0 for pair
```

Each attachment component contains gonols from one origin.

---

## Law 5 — Detect and occurrence identity v1

For the region bit string `B = b_0 ... b_(n-1)`, define

```text
Q_B(s) = { q >= 2 :
  s+q <= n and there exists h != s with h+q <= n,
  [s,s+q) disjoint from [h,h+q), and B[s:s+q] = B[h:h+q] }

q_s = max Q_B(s), if Q_B(s) is nonempty; otherwise 1
```

The `h` value only witnesses repetition. It is not stored and need not be the
start of another emitted occurrence.

`Detect` is greedy longest-at-cursor, left to right:

```text
s = 0
while s < n:
    u = B[s : s+q_s]
    a = a(u)
    o = h'4f434301' || dCBOR([O, N(s), a])
    emit (a, O, s, o)
    s = s + q_s
```

`h'4f434301'` is `ASCII("OCC") || h'01'`. Origin does not affect cuts.

```text
Detect(empty, O) = []
Pair([], K_t) = (empty matching, empty leftover)
```

On reverse, `ExpandLayer` reconstructs a region, reruns `Detect`, and requires
occurrence-for-occurrence equality. Hash acceleration is permitted only after
byte-for-byte equality of candidate substrings.

---

## Law 6 — keyed pairing v1

`Pair` is evaluated in the context of one region origin `O`; `O` is explicit for
an empty occurrence list and recoverable from every entry otherwise. For
occurrence `o` under `O`, compute

```text
rank(o) = KMAC256(
    k_pair,
    dCBOR([O, o]),
    256,
    ASCII("URPCS/PAIR/v1"))
```

Sort a region's occurrences by `(rank(o), o)`, both bytewise. Pair adjacent
items `(v_0,v_1), (v_2,v_3), ...`; store each row with its identifiers bytewise
ascending. If the count is odd, the final sorted occurrence is the sole carry.

`Pair` fails unless its list contains unique Law 5 identifiers from exactly one
origin and is exactly that origin's occurrence set. `DecodeWitness` recomputes
pairing from `K_t` and requires exact equality. This construction does not claim
uniform sampling from all perfect matchings, and the published witness reveals
the result.

---

## Law 7 — origin generation v1

`nu_origin` is a namespace, not secret key material. Define

```text
OriginGen(K_t, r, j) =
    h'4f524701' || dCBOR([nu_origin, N(r), N(j)])
```

`h'4f524701'` is `ASCII("ORG") || h'01'`. The exact 32-byte `nu_origin`, including
leading zeros, is encoded as a byte string. `WitnessBuild` emits one origin per
region, including an emitted empty region. `DecodeWitness` reconstructs every
origin and rejects extra, missing, duplicate, or unequal rows.

A state is single-use. Concurrent branches require distinct preallocated state
chains; reusing a state repeats origins at equal `(r,j)`.

---

## Law 8 — canonical attachment tree v1

For each origin, classify its gonols with

```text
kappa(g) = (0, g) for pair gonols
kappa(g) = (1, g) for the carry gonol
```

Sort lexicographically by `kappa`, then by identifier bytes. There is at most one
carry and it sorts last. For sorted gonols `g_0 ... g_(m-1)`, attach each `i >= 1`
to heap parent `g_floor((i-1)/2)`. Store the origin's layer on each edge.

- `m=0`: no vertices or edges;
- `m=1`: one isolated root;
- `m>=2`: one binary tree rooted at `g_0`.

For child at sorted index `i >= 1`, store

```text
Delta_i = 1 + ((i-1) mod (M-1))
```

There is one Delta row per edge and none otherwise. `WitnessBuild` emits exactly
this tree; `DecodeWitness` rebuilds it and requires exact equality of attachment,
Delta, and shape rows.

---

## Law 9 — layer object, serialization, and reverse expansion v1

For pair members stored as `o0 < o1`, define local displacements

```text
delta(g,o0) = 0
delta(g,o1) = floor(M/2)
```

For a carry member, `delta(g,o) = 0`. Member phase is

```text
theta(g,o) = (b_g + delta(g,o)) mod M
```

The layer object is

```text
G^(r) = [N(r), N(len(D^(r))), [Region_(r,j) for j=0..m-1]]

Region_(r,j) =
  [N(j), N(len(B_(r,j))), O_(r,j), [Gonol_g ...]]

Gonol_g = [g, N(b_g), [[o, N(theta(g,o))] ...]]
```

Regions sort by `j`, gonols by Law 8 `kappa`, and members by occurrence-id
bytes. Pair gonols have two members and carries one.

Partition `D^(r)` as follows. If `L = len(D^(r)) > 0`, emit
`ceil(L/x)` regions: every nonfinal region has `x` bytes and the final has
`1..x` bytes. If `L=0`, emit exactly region `j=0`, with empty bytes, its Law 7
origin, and no gonols.

```text
LayerWire(G) = ASCII("URGON001") || dCBOR(G)
Serialize(G^(r)) = LayerWire(G^(r))              for r < R
SerializeBody(G^(R), W_t) = LayerWire(G^(R))
```

`SerializeBody` is defined only when `G^(R)` equals the terminal witness slice.
`R` is `R_cap` and the maximum layer index in `R_origin`. Origin rows must exist
at every layer `0..R`; the `A` rows may be empty at a layer but cannot use an
index outside that range.

`Deserialize` consumes all bytes, checks the magic and restricted canonical
CBOR, validates layer shape, ordering, partition, member counts, numeric ranges,
and requires byte-for-byte `LayerWire` re-encoding equality. `DeserializeBody`
adds the requirement that its layer index equals `R`.

`ExpandLayer(G^(r), W_t, r)` performs these deterministic steps:

1. Require exact agreement with the layer-`r` witness slice: origins, gonol ids,
   members, component phases, member phases, shapes, tree, and region order.
2. For each origin, parse every primitive axis, place its payload at its recorded
   bit interval, require nonoverlap and complete coverage, then rerun Law 5
   `Detect` and Law 6 pairing for exact agreement.
3. Require the stitched bit length be divisible by eight and equal the recorded
   region byte length; pack bytes MSB-first.
4. Concatenate regions by increasing `j` and require the result length equal the
   layer's `len(D^(r))` field.

Reverse the authenticated body with:

```text
G = DeserializeBody(B_terminal, W_t)       # G^(R)
for r from R down to 0:
    D^(r) = ExpandLayer(G, W_t, r)
    if r > 0:
        G = Deserialize(D^(r))              # must be G^(r-1)
return D^(0)
```

After the loop, the set of recovered `(r,j)` region keys must equal the set of
all `R_origin` row keys. Extra witness regions, missing decoded regions, and
duplicate region keys fail. Any other mismatch fails. This construction is not
a compressor; serialized layers may grow substantially.

---

## Law 10 — exact-depth halt v1

The halt seed is exactly

```text
L_t = BE32(R_cap)
```

so Law 2 encodes `q=32` and four packed bytes. After a valid layer is built,

```text
Halt((r, len(D^(r)), len(LayerWire(G^(r)))), L_t, r)
    is true iff r == R_cap
```

Exactly `R_cap+1` layers, indexed `0..R_cap`, are built. Empty input at depth zero
still has one layer-0 empty origin and may have no `A` rows. Missing origin
layers, gaps, an extra layer, or disagreement among `K_t.R_cap`, `L_t`, and the
maximum origin layer fail. Resource limits cause `Fail`, never an alternate halt.

---

## Law 11 — integrity and framing v1

`k_integrity` is a 32-byte key distinct from `k_pair`. The frame header is
exactly 24 bytes:

| offset | size | field | required v1 value |
|---:|---:|---|---|
| 0 | 8 | magic | `ASCII("URPCF001")` |
| 8 | 2 | version | `1` |
| 10 | 2 | header length | `24` |
| 12 | 8 | `C_0` length `n` | `len(C_0)` |
| 20 | 2 | tag length | `32` |
| 22 | 2 | flags | `0` |

Let `H_frame(n)` be those bytes. The authentication transcript is an array of
three CBOR byte strings:

```text
X = dCBOR([H_frame(len(C_0)), C_0, AD])
tau = KMAC256(k_integrity, X, 256, ASCII("URPCS/TAG/v1"))
C = H_frame(len(C_0)) || C_0 || tau
```

`AD` is a byte string and may be empty. `len(C_0)` must fit unsigned 64 bits and
`tau` is exactly 32 bytes.

`Unframe` fails unless `len(C) >= 56`, all fixed fields are exact, arithmetic is
safe, and `len(C) = 24+n+32` with no trailing bytes. It returns

```text
C_0 = C[24 : 24+n]
tau = C[24+n : 24+n+32]
```

`Verify` reconstructs `H_frame(n)`, recomputes the tag, and compares all 32 bytes
in constant time. False, including wrong `AD`, fails before any bootstrap,
witness, body, plaintext, receipt, or state operation.

---

## Law 12 — receipt-bound linear advance v1

`k_advance` is a third distinct 32-byte key. `nu_origin = 2^256-1` is exhausted:
encryption must not start and increment never wraps.

For the witness and the complete ordered layer sequence, define

```text
Trace = (W_t, (G^(0), ..., G^(R)))
TraceWire = dCBOR([
    EncodeWitness(W_t, K_t),
    [LayerWire(G^(0)), ..., LayerWire(G^(R))]
])

q_t = SHA3-256(dCBOR([
    ASCII("URPCS/RECEIPT/v1"),
    TraceWire
]))
```

All four items in the advance context are CBOR byte strings:

```text
Y_t = dCBOR([nu_origin, N(R_cap), C, q_t])
```

Derive three candidates:

```text
z_pair = KMAC256(k_advance, Y_t, 256, ASCII("URPCS/ADV/PAIR/v1"))
z_int  = KMAC256(k_advance, Y_t, 256, ASCII("URPCS/ADV/INTEGRITY/v1"))
z_root = KMAC256(k_advance, Y_t, 256, ASCII("URPCS/ADV/ROOT/v1"))
```

For a 32-byte candidate `z` and finite forbidden set `F`, v1 `Avoid` is:

```text
base = unsigned_big_endian_integer(z)
for i in 0 .. len(F):
    candidate = BE256((base + i) mod 2^256)
    if candidate not in F:
        return candidate
```

The loop always succeeds because it examines `len(F)+1` distinct consecutive
values against only `len(F)` forbidden values. This explicit definition records
the already-shipped v1 behavior; it does not amend vector bytes.

```text
k_pair'      = z_pair
k_integrity' = Avoid(z_int,  {k_pair'})
k_advance'   = Avoid(z_root, {k_pair', k_integrity'})
nu_origin'   = BE256(int(nu_origin) + 1)
R_cap'       = R_cap
```

`Advance(K_t, C, q_t)` returns that state. On decrypt, the receiver reconstructs
the complete trace only after authentication and full expansion, computes its
local receipt, and advances. Current-message success does not transmit or compare
receipts; sender/receiver receipt equality is a correctness obligation, while a
mismatch forks the successor state and is normally detected by the next tag.

Host obligations: use compare-and-swap or equivalent durable single-use state;
persist `(C,K_(t+1))` before releasing `C`; retransmit stored `C` rather than
encrypting again under `K_t`; never advance on failure; use separately allocated
chains for concurrent branches. Rollback resistance and fork recovery are not
codec theorems.

---

## Law 13 — traversal cursor v1

After successful `WitnessBuild`, the only valid traversal field is

```text
T_t = [[], true]
```

Reverse traversal is derived from canonical relations and layer objects, not a
live stack. `DecodeWitness` rejects every other cursor.

---

## Complete forward and reverse composition

`WitnessBuild(D,K_t)` performs Laws 5–10 for each layer, accumulates
`W_t`, `(G^(0),...,G^(R))`, and the canonical trace, and emits the single
`BuildResult`. It does not perform a second construction pass.

```text
Encrypt(D, K_t, AD):
    require K_t valid and not exhausted
    (W_t, layers, trace) = WitnessBuild(D, K_t)
    beta = EncodeWitness(W_t, K_t)
    body = SerializeBody(layers[R], W_t)
    C_0 = H_boot(len(beta)) || beta || body
    tau = Tag(k_integrity, C_0, AD)
    C = Frame(C_0, tau)
    q_t = ReceiptGen(trace)
    K_next = Advance(K_t, C, q_t)
    return (C, K_next)
```

```text
Decrypt(C, K_t, AD):
    (C_0, tau) = Unframe(C) or Fail
    Verify(k_integrity, C_0, AD, tau) or Fail
    W_t = WitnessRecover(C_0, K_t) or Fail
    recover B_terminal from the Law 1 boundary
    recover D and all G layers by the Law 9 reverse loop or Fail
    require Law 10 schedule consistency
    q_t = ReceiptGen(W_t, recovered layers)
    K_next = Advance(K_t, C, q_t)
    return (D, K_next)
```

Correctness for every permitted input is

```text
(C, K_next_E) = Encrypt(D, K_t, AD)
(D_prime, K_next_D) = Decrypt(C, K_t, AD)
D_prime = D and K_next_D = K_next_E
```

and sender/receiver canonical trace receipts are equal.

---

## Committed bounded harness profile

These limits are test policy, not additional wire fields:

```text
x = 1 byte
M = 8
len(D)_max = 1 byte
R_max = 1
len(D^(r))_max = 1 MiB
len(LayerWire)_max = 1 MiB
len(beta)_max = 4 MiB
len(C_0)_max = 8 MiB
len(TraceWire)_max = 16 MiB
```

Crossing a cap is `Fail`, never another halt.

The committed reference computation reports eight named vectors, all 256
one-byte plaintexts at depth zero, and the depth-one empty fixture. Those results
show one implementation agreeing with these vectors; independent interoperability
requires a separately implemented decoder using this document as its only URPCS
law source.

## Not claimed

Confidentiality; IND-CPA or IND-CCA security; hiding of witness contents,
matching, origins, attachments, phases, depth, lengths, or leftovers; compression;
rollback-resistant storage; fork merge; post-compromise security; production
suitability; PCEA compatibility; or UCNS-gonol identity.

## hmmm

The old public sheet named the machine's organs but omitted their motions. This
contract publishes the motions. The historical independent audit remains correct
for its frozen input; a new clean-room decoder must decide whether this repair is
sufficient.
