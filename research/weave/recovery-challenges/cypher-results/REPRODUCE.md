# Reproducing Cypher's recovery of Weave v1 challenges

Inputs: `/workspace/cypher` (challenge pack) + the **exact pinned public source**
named in `README.md` / `v1/manifest.json`. No corpora, private profiles,
originals, or evaluator bundle.

Pinned sources (hashes match the manifest):
```
commit 9de81c67b271df09c1d9ba5422660c96fe8af7ac  (stack)
commit 905e66964a495d7596a577bb64e4158db9465864  (ucns)
```
Fetched into `/workspace/cypher/src/` (weave modules) and
`/workspace/cypher/src/ucns/` (UCNS geometry).

## Recovery path (from source)

Outer → inner (cite `cycle.py` / `numeral.py` / `prime_schedule.py` / `native_binary.py`):

1. **WVC frame** (`cycle.py:435-436,455-462`): magic `WVC\x01` +
   `sha256(CYCLE_NATIVE.json)` + `profile.identity` + 32-byte message-origin
   root + varint round count + blob of interleaved payload.
2. **Per-round inverse interleave** (`prime_schedule.py:131-163`,
   `cycle.py:472-475`): public `prime_path`/`arities`/`end_order` determine the
   bit split; undo `first-last`/`last-first` section-wise.
3. **WAF frame** (`cycle.py:359-384`): magic `WAF\x01` + source length +
   embedded **WNC packet** + 7 circle counts + one Fraction per occurrence.
4. **WNC packet** (`numeral.py:476-558`): origin + round_id + declared bit
   length + definition table (symbol, angle, circle, **literal BitBlock**) +
   occurrence stream. Literals are the plaintext chunks — no further
   transform.
5. **Native placement** (`native_binary.py:437-502` `recover_sequences`):
   for each occurrence, `Geometry.recover_axis(origin, byte_length, position, spaces[circle])`
   yields the source byte offset; blocks are concatenated in offset order.
6. **Normalize frame** (`cycle.py:273-290`): magic `WNM\x01` + 8-byte length +
   `sha256(corpus)` + **message bytes** + corpus padding.

### Validation-only vs necessary for bytes

| Check | Needed to recover message bytes? |
|---|---|
| `sha256(CYCLE_NATIVE.json)` matches header | No (integrity) |
| `profile.identity` matches header | No (integrity); but the **profile fields** themselves are needed for the inverse interleave / unaffix |
| message-origin root re-hashes | No (integrity); recovery still yields the bytes |
| `sha256(corpus)` in WNM header | No |
| corpus padding bytes match | No — **message sits in cleartext after the WNM header** (`cycle.py:290`) |
| discovery re-partition agrees | No (integrity) |
| `spaces` / `circle_order` | **Yes for group B** (needed by `recover_axis`); for group A they are public |

## Group A (public profile `profiles/cycle-v1.json`)

```sh
cd /workspace/cypher/work
python3 recoverA.py
# writes a01.recovered .. a04.recovered
sha256sum a0*.recovered
```

Uses the real `cycle.reverse` path down to the normalized frame, then reads
`data[44:44+length]` without the corpus. Root reconstruction is verified.

## Group B (secret spaces + circle_order)

Public unchanged fields (manifest): schema, selection, split, scope,
bucket_bytes, round count, each `prime_path`, each `arities`, each `end_order`.
Withheld: corpus, `corpus_bit_offset`, per-round shuffled `circle_order`,
per-round eight space-turn fractions.

`circle_order` is readable from the WNC packet (each definition stores its
circle). The seven occurrence-circle spaces are recovered by brute-forcing
`numerator/65536` (reduced) per circle via `Geometry.recover_axis`, then
solving an exact-cover placement on the resulting offsets. `spaces[0]` (whole
circle) is not required for byte recovery.

```sh
cd /workspace/cypher/work
python3 recoverBall.py
# writes b01.recovered .. b04.recovered
sha256sum b0*.recovered
```

## Parameter-leak proofs

### 1. Group-B base turn / circle order (ciphertext-only, pre-source)
```sh
python3 - <<'PY'
# After one bit-level first/last undo, every B file's U+E000 record is
# 64113/65536 on circle 6; circle sequence is 6,2,5,7,4,1,3.
# See LOG.md Round 1–2; scripts: work/e000.py, work/parse.py
PY
```

### 2. Full group-B secret spaces (from source-assisted recovery)
```sh
python3 recoverBall.py 2>&1 | grep spaces
# Round 2 (shared): 40985/32768, 115861/65536, 24407/32768, 44803/65536,
#                   80295/65536, 16769/65536, 119863/65536
# Round 1 (shared): 15989/32768, 13463/8192, 10977/32768, 861/2048,
#                   65809/65536, 1025/16384, 18659/16384
# Round 0 (shared): 44323/32768, 130459/65536, 27687/16384, 6153/32768,
#                   33413/32768, 431/16384, 12023/8192
# (circles 1..7; spaces[0] not recovered / not needed for bytes)
```

### 3. Corpus SHA-256 (leaked in WNM header; corpus bytes themselves withheld)
```sh
python3 - <<'PY'
from pathlib import Path
for k in ['a01','b01']:
    # After recovery to normalized frame the header exposes sha256(corpus)
    pass
# Group A corpus sha256: cbe9c840a43b373ebc1dfa472e594b8a69891b6ee453af250233faf130228a26
# Group B corpus sha256: a8b66f6f5570cf099cd5fd50a90c0b4d7cfa63782b95957d9039ba8a203a33d8
PY
```

## Recovered plaintext digests

```
a01 573  d2a49166a8412e01dedc38bb6bf2d7886f58b9878e8b4ec0afc376ee9b0cfb2b  repeated Ledger block
a02 190  771011b870a52adf10edf08b7f56764588ad218935eb19b623eb705b4b75ac4d  prose Field note
a03 768  9480947d87aa2795076af7acefa0af405b8f44a89d3545ec82b802987dd8bef1  binary
a04 270  8cb73c13ef360f212a80db5c68b98d3943e29b763a6b18cf759b831dda39066b  JSON fixture
b01 768  bb89585822aa2e5554976e5b28711f4907878a9239c50f9ba55e804153e90241  binary
b02 573  a4098953d43b333acd68956803c91cc2e0e99ac3329376ddb2666bdc695215e9  repeated Ledger block
b03 271  b8e1a332308de49cbc80b38ae82e935770b794b75ddcf42699a02e330cc49e81  JSON fixture
b04 190  b1fe401b4ab801abc6994501679e3823be0913d0540485808f8224113536d3f5  prose Field note
```

Evidence of exactness (no oracle): for every file the reconstructed
message-origin root matches the 32 bytes in the WVC header
(`native_binary.py:223-229`, `cycle.py:478-479`).
