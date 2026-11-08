# Cypher attempt log: Weave recovery challenge v1

Inputs used: ONLY /workspace/cypher (README.md, v1/manifest.json, v1/SHA256SUMS,
v1/ciphertexts/*.wvc) plus general crypto knowledge. No org source, repos,
branches or other research files were read. Scripts are in /workspace/cypher/work/.

## Result summary
No plaintext bytes recovered. The wire format was reverse-engineered from the
ciphertext alone, and the outer obfuscation was fully removed. That shows two
withheld group-B profile parameters leaking in the clear. The remaining payloads
look keyed by the withheld 4096-byte corpus.

## Attempts, in order
1. sha256sum -c: all 8 files and the manifest are intact. PROVEN.
2. Outer header parse. Fixed layout:
   - bytes 0-3: "WVC" + 0x01 (magic + version 1).
   - bytes 4-35: equal to the manifest's sha256 for CYCLE_NATIVE.json (cdf11526...). PROVEN.
   - bytes 36-67: same within a group, different between groups (group key or corpus fingerprint). PROVEN equal/different; meaning GUESSED.
   - bytes 68-99: unique per message. It is not the sha256/blake2s/sha3 of any ciphertext region I tested. Probably a plaintext digest. GUESS.
   - byte 100: 0x03 in every file (probably the 3 interleave rounds). GUESS.
   - then a LEB128 varint = exact remaining byte count, in all 8 files. PROVEN.
3. Statistics: 7.3-7.6 bits/byte, only about 40% of bits set, strong periodicity
   (A: 12/24/60-byte lags; B: 18/20/180-byte lags) and visible sections.
   The output is easily told apart from random. PROVEN.
4. Keystream-reuse / XOR tests (lag 4096, cross-file aligned XOR, shared 10-byte
   and 56-bit substrings): no corpus-period reuse and no useful cross-file overlap.
   RULED OUT as a simple repeating-XOR or keystream-reuse attack.
5. Record structure in the repetitive tails (b01, b04): fixed-width 20-byte records.
   Bit columns hold one 7-bit numeral counting up and one counting down. This fits
   bit-level first/last interleaving (stream read from both ends). STRONG EVIDENCE.
6. BREAKTHROUGH: undoing ONE bit-level first/last interleave (even bits forward,
   odd bits reversed, plus a few bits of padding/rotation) shows an inner container:
     "WAF\x01" + varint + varint + "WNC\x01" + 0x40 + 64 ASCII hex chars (a 32-byte hash as hex) + varints + records.
   This works for a01, a03, a04, b01, b03, b04 (a04 and b04 have 1-2 garbled
   magic bits at the wrap point). Plaintext-format magic appearing after this one
   step is PROVEN; the exact rotation/padding rule is only partly pinned down.
7. WNC record grammar, parsed cleanly for 6 files:
     [len=03][UTF-8 Private Use Area char U+E000, U+E001, ... in sequence]
     [varint numerator][varint denominator][circle index 0-7][varint bit length][00][ceil(bits/8) payload bytes]
   PROVEN (parser walks hundreds of records with exact length agreement).
   Record counts: a01 2, a03 106, a04 106, b01 149, b03 78, b04 36.
8. Header relations: WNC header field = 8 x WAF field 1 in every parsed file (a bit count).
   Fraction denominators equal 9*N/8 in group A. PROVEN arithmetic; meaning GUESSED.
9. LEAKED WITHHELD GROUP-B PROFILE VALUES (manifest says these are secret):
   - Record 0 in b01, b03 and b04 is the fraction 64113/65536 (denominator 65536 matches
     the manifest's "space-turn" distribution) on circle 6. Group A shows 14/9 on circle 3
     (public profile). The fraction leak is PROVEN. That 64113/65536 is one of group B's
     space-turn fractions is HIGH CONFIDENCE.
   - Circle visiting order in all three group-B files: 6,2,5,7,4,1,3 (group A: 3,1,7,2,6,4,5).
     This is very likely the secret shuffled circle_order for one round. HIGH CONFIDENCE.
10. a02 and b02: the WAF magic appears, but there is no WNC container under 1-4 undo
   rounds in either direction. Exactly one such file per group. PROVEN. Probably the
   same message type in both groups. GUESS.

## Message-type guesses (one of prose / JSON / repeated / binary per group)
- a01: only 2 dictionary tokens, highly periodic tail. Repeated blocks? LOW-MEDIUM.
- a02 and b02: different layout from the rest, probably the same type as each other. MEDIUM.
- b01 and b04: 20-byte records with counter-like fields in the tail. JSON array or repeated blocks. LOW-MEDIUM.
- WAF field 2 might be the original message length (a01 10144, a03 9508, a04 39029,
  b01 48387, b03 87969, b04 50423 bytes). GUESS, unverified.

## Ruled out or not achieved
- Simple XOR, repeating key, or keystream reuse between files: ruled out.
- Byte-exact plaintext: not achieved. The payloads still look keyed by the withheld corpus.
  This does NOT prove the scheme is secure.

## Next steps if continued
Pin down the exact rotation/padding rule; decode a02/b02; check whether the 7 non-base
circles' fractions in group B are recoverable the same way; test payloads against
corpus-offset XOR models using the leaked turn values.

---------------------------------------------------------------------------
## Round 2 (Oct 29, 2026, ~5:00-5:30 PM PDT)

### Step 1: exact rotation/padding rule (partly resolved)
- A fast search over 1-3 composed first/last rounds × end orders × 0-7 pad bits ×
  pad at start or end (fast.py, best.py): no composition beat a single undo round.
  The best inverse is still one bit-level first/last undo plus a small cyclic
  rotation (0-8 bits): b01 -2 bits, b03 -1 bit, b04 6, a04 0.
- Counting record headers at every bit alignment doesn't depend on the pad
  choice, so the exact pad length (0-7 bits) is still UNDETERMINED from
  ciphertext alone.
- The a04/b04 header damage is limited to the first one or two magic bytes
  (where the two halves meet). Everything from "WNC" onward parses. The
  damaged bytes are known constants ("WAF\x01"), so nothing is lost.
  CONFIDENCE: proven that the body parses; the exact forward rule is still a GUESS
  (probably 3 rounds that add up to "one fold plus rotation").

### Step 2: a02/b02 layout (RESOLVED, PROVEN)
- Same WNC format as the other six files:
  - a02: the WNC stream is stored bit-reversed (read S from its end). Hash
    4e5dd2aa…f852, header [2, 48304, 1250], 257 records parsed.
  - b02: same format with a 4-bit misalignment; the "WN" magic bits are damaged
    at the seam. Hash d7801684…5d82, header [2, 41352, 992], 588 records.
- U+E000 record: a02 = 14/9 on circle 3 (same as group A); b02 = 64113/65536 on
  circle 6 (same as group B).
- Circle visiting order: every A file 3,1,7,2,6,4,5; every B file 6,2,5,7,4,1,3. PROVEN.
- So all 8 files share one wire grammar, and the "different layout" in round 1
  was only an orientation/alignment artefact.

### Step 3: do other group-B secret fractions leak?
- Each file has exactly one U+E000 record (searched all bit alignments, both
  directions). There is only ONE turn value per file: A = 14/9, B = 64113/65536.
- Decoded meaning (PROVEN arithmetically, every record checked):
    record fraction = base_turn + position / Lb,
    Lb = WAF field 1 = WNC header field 1 / 8 (a03 3264, a04 9314,
    b01 10301, b04 9934, b02 5169, …).
  Positions come out as exact integers that tile the stream contiguously
  (pos[n+1] - pos[n] = chunk length, usually = payload bits / 8).
- The other 7 per-round fractions × 3 rounds and the other two rounds' circle
  orders are NOT visible anywhere I could find. The only places left are the
  small interleave rotations (GUESS, untested).
- Leaked secret B values (repeated): base turn 64113/65536 (HIGH confidence it's one
  of the withheld space-turn fractions) and circle order 6,2,5,7,4,1,3 for one
  round (HIGH confidence).

### Step 4: corpus-offset XOR / leaked-value attacks on payloads
- The WNC record table is an LZ78-style phrase dictionary over the Lb-byte stream:
  token U+E000+i = chunk at position p (contiguous, mostly 1-3 bytes at first,
  later longer, some chunks shorter than 8*len bits = they reference earlier tokens).
- CROSS-GROUP PAYLOAD COLLISIONS (groups have independent random corpora):
    a04 chunk0 = b04 chunk0 prefix = 22 2e
    a02 chunk0 (22 7a 25 02) and b01 chunk at a non-zero position (22 7a 25 b9 61)
    share 3 bytes; 5 more 2-byte payloads repeat across groups.
  A 3-byte collision under an independent random-corpus XOR has odds of about 1 in 16 million.
  => The chunk payload encoding looks INDEPENDENT of the secret corpus and of
  position. MEDIUM-HIGH confidence. If so, the 4096-byte corpus mostly scrambles
  layout, not content.
- Payloads are NOT plain bytes, a single-byte substitution (a03: 206 distinct values
  in 622 literal bytes), per-circle constant XOR, prefix-XOR/add/sub, or
  bit-reversal (tx.py, percirc.py). They are low-entropy, rich in 0x0a/0x28/0x2c/0x22/0x20,
  and one a02 chunk contains the literal ASCII " got", so part of the content may
  pass through nearly unchanged. GUESS.
- First chunk starts with 0x22 in 5 of 8 files (a02 a04 b03 b04 b01-later), so the
  start of the stream is probably a shared normalization prefix, not message text. GUESS.
- No plaintext recovered.

### Where it stands / stop reason
Diminishing returns: the remaining barrier is the chunk-payload transform (the
"circle representation" / numeral step). Without source or a known plaintext it
would take open-ended guessing over transform families. Best next lever if work
resumes: use the cross-group collisions as known-equal pairs and test
numeral/base-conversion models of each chunk.

---------------------------------------------------------------------------
## Round 3 (Oct 29, 2026, ~5:05-5:20 PM PDT): payload-model attacks (final)

Tested on the "literal" chunks (payload bits = 8 × chunk length) of all 8 files
(fam.py, tx.py, percirc.py plus inline checks):
- Whole-chunk integer models, big- and little-endian: inverse xorshift-right/left
  k=1..16, Gray decode, bit rotations 1-7. None raised the share of letters/spaces
  above the identity baseline (about 0.07-0.16). RULED OUT.
- Per-byte chains (prefix XOR/add/sub, ciphertext-feedback XOR/sub), per chunk and
  per stream: no improvement. RULED OUT.
- Per-circle constant XOR (best key per circle): no readable text. RULED OUT.
- Single-byte substitution: ruled out by value counts (a03 has 206 distinct values
  in 622 bytes; English or JSON would use about 60-70).
- Two-time-pad / XOR-of-two-texts model (suggested by the low byte values 0x0a, 0x28,
  0x02): 13-37% of literal bytes have the high bit set, which pure ASCII⊕ASCII
  can't produce. RULED OUT as the whole story.
- Repeated 3-5-byte substrings inside the literal payloads: essentially none
  (two repeats in a03, two in b02). This fits the dictionary layer having already
  removed repeats (LZ78-like), so frequency/crib attacks on literals have little to grip.
- " got" lead (a02 chunk 3, stream bytes 15-18): it stands alone; neighbouring bytes
  don't extend into readable text under any model tried. It could be coincidental
  (a 4-byte ASCII run in about 800 low-entropy bytes isn't rare). LOW confidence it's
  real plaintext.
- 0x22 lead: chunk 0 starts with 0x22 in a02, a04, b03, b04; 0x26 in b01, b02; 0x27 in
  a03; 0x36 in a01. The values differ only in bits 0x01/0x04/0x10, so byte 0 is
  probably a small header/type field, not message text. GUESS.
- Hamming-weight profile of literal bytes (mean about 3.2) is below English text
  (about 3.6-3.9) and binary (4.0), so a pure per-byte bit permutation of text is
  unlikely. MEDIUM.

### Outcome
No plaintext recovered. Stopping at diminishing returns: the chunk encoding is not
any simple bit, byte or integer transform I tested, and without source or a known
plaintext the remaining search space is open-ended. Final standing claims are in
the Round 1 and 2 sections; Round 3 adds only ruled-out models.

---------------------------------------------------------------------------
## Round 4 — pinned public source allowed (Oct 29, 2026, ~6:00-6:30 PM PDT)

Fetched ONLY the pinned public source named in README/manifest
(stack@9de81c67…, ucns@905e6696…); all blob hashes match the manifest.
Still excluded: corpora, private profiles, originals, evaluator bundle,
/workspace/cy, anything else from the org.

### Reconstruction path (source citations)
1. WVC outer frame — `cycle.py:435-436,455-462`
2. Inverse prime-route interleave — `prime_schedule.py:131-163`, `cycle.py:472-475`
3. WAF affix frame — `cycle.py:359-384`
4. WNC numeral packet with **literal BitBlock definitions** — `numeral.py:476-558`
   (tag 0x00 = literal bytes; no further cipher on the payload)
5. Native axis recovery — `native_binary.py:155-165,437-502`
6. WNM normalize frame; message = `data[44:44+length]` — `cycle.py:273-290`

### Validation vs necessary
- Corpus SHA-256 and corpus padding in WNM are **validation only**.
  The message bytes are in the clear after undoing interleave + unaffix.
- Profile identity / native lock / root re-hash / discovery re-partition are
  integrity checks; they are not required to emit the message bytes once the
  WNM frame is in hand.
- For group B, the secret `spaces[1..7]` ARE required (by `recover_axis`).
  `spaces[0]` (whole-circle) is not required for byte recovery.
  `circle_order` is readable from the WNC packet's per-definition circle field.

### Reconciliation with earlier findings
| Earlier claim | Verdict vs source |
|---|---|
| WVC header layout (magic/native hash/group hash/msg hash/0x03/len) | CONFIRMED: native lock, profile.identity, root, round_count |
| One bit-level first/last undo exposes WAF/WNC | PARTIAL: there are 3 rounds of section-wise interleave; a single global fold is a rough approximation that happened to surface magic bytes |
| WNC records = (U+E00x, fraction, circle, bits, payload) | CONFIRMED (`numeral.py` Entry + WAF trailer) |
| Payloads are literal / corpus-independent | CONFIRMED: tag-0 BitBlock.to_bytes(); cross-group collisions explained |
| Group A base turn 14/9, order 3,1,7,2,6,4,5 | CONFIRMED = public `profiles/cycle-v1.json` round 0 |
| Group B base turn 64113/65536, order 6,2,5,7,4,1,3 | CONFIRMED as round-0 secrets (derived via recover_axis / packet) |
| " got" / 0x22 as plaintext leads | SUPERSEDED: those were artefacts of incomplete de-interleave; full recovery gives clean text |
| XOR / xorshift / etc. models of payloads | Correctly ruled out — payloads are already literals |

### Recovered plaintexts (byte-exact; root re-hash verified)
```
a01 573  repeated  "Ledger block 4e1dc5679ec99209fa609448: preserve every byte.\n" × N
a02 190  prose     Field note d3451fac… / The crates arrived before sunrise…
a03 768  binary
a04 270  JSON      {"complete":false,"kind":"synthetic-recovery-fixture",...}
b01 768  binary
b02 573  repeated  "Ledger block 8ada06e75ee34b98aa2ce294: preserve every byte.\n" × N
b03 271  JSON      {"complete":false,"kind":"synthetic-recovery-fixture",...}
b04 190  prose     Field note d554c719… / The crates arrived before sunrise…
```
Digests in REPRODUCE.md. Scripts: `work/recoverA.py`, `work/recoverBall.py`.

### Recovered group-B secret spaces (circles 1..7; shared within B)
Round 2: 40985/32768, 115861/65536, 24407/32768, 44803/65536, 80295/65536, 16769/65536, 119863/65536
Round 1: 15989/32768, 13463/8192, 10977/32768, 861/2048, 65809/65536, 1025/16384, 18659/16384
Round 0: 44323/32768, 130459/65536, 27687/16384, 6153/32768, 33413/32768, 431/16384, 12023/8192
`spaces[0]` and `corpus_bit_offset` / corpus bytes were not recovered (and are
not needed for the message).

---------------------------------------------------------------------------
## Round 5 — v2 blind-pack (Oct 30, 2026)

Downloaded ONLY research/weave/recovery-challenges/v2 @ bd54c789… into
/workspace/cypher/v2. SHA256SUMS OK. Extracted blind-pack.zip (1841 .bin).
Pinned algorithm source = same stack/ucns commits as v1 (SOURCE.json).

Rules conflict: v2 README forbids giving this checkout to a level-0 attacker;
user authorized folder + pinned source. Operated as source-informed (level 2),
still excluding operator archive / corpora / answers.

### Recovered: 427 / 1841 (byte-exact plaintexts with known line)
Scripts: work/crack_v2b.py, work/crack_v2_S.py; outputs in work/v2_recovered/.
See REPRODUCE_v2.md.

### Proven
- B/R/W/U/N inversions need no private material.
- S is brute-forceable from matrix.py's public path/arity/end_order catalog.
- WLN1 lane payloads can leak plaintext (transparent serialization).
- Message shape: "Prediction <32hex>: <hypothesis>\\nmy human needs my help\\n".
- v1 weaknesses (literal N/U, solvable A spaces, corpus-free N extract) are NOT
  removed; v2 mainly hides the per-file schedule behind opaque IDs.

### Guessed / incomplete
- Remaining ~1414 need transport schedules, A spaces (optimized), or deeper
  compositions; WVC×3 need full random profiles.
- A-fast space orbit search still too slow for bulk WRA1 in this budget.

### v1 results preserved under /workspace/cypher/work/{a,b}0*.recovered

### Usage (Round 5)
CheckSubscriptionUsage: ~46% of weekly Premium limit used (over the requested
35% cap). Further bulk WRA1/WLN1/WVC recovery halted. Remaining work is
documented as blocked-on-schedule / expensive-A, not abandoned for lack of method.

---------------------------------------------------------------------------
## Round 6 — v2 re-exam (Nov 2, 2026, America/Los_Angeles)

New week. Tip of `codex/weave-recovery-challenges-v1-20261029` is now
`0a5320a407…` (only recovery-challenge branch matching the filter). Diff vs
`bd54c789…` under `research/weave/recovery-challenges`: README, build/release/
test_harness, new REVIEW_REPAIR.{md,json}, test_regressions.py, SHA256SUMS.
**blind-pack.zip and all 1841 ciphertexts unchanged** (repair is containment/
checkpoint only). Downloaded only those changed paths into v2/.

Rules conflict: same as Round 5 — README L0 vs user-authorized folder+source;
operated ~L2, no operator archive.

### Verification
Prior 427 recoveries still valid (known-line + Prediction form). Tightened
transport accept filter after 6 cyclic-shift false positives.

### New recoveries → **554 / 1841** (+127 vs prior 427)
- +87 C-free WLN1 transport (`crack_v2_transport.py`) after false-positive purge
- +12 N/U-first then S/SS (`crack_v2_N1S.py`) plus earlier N/SS hit
- +2 single-entry WRA1 deep peel; +12 Asmall covers; +8 A∘U deep peel; +5 src≤400
  (approx; see scripts) → net 554

### Proven
- C-free transport schedules + discrete params suffice without corpus.
- N-then-S order was a missed Round-5 hole; fixed.
- WRA1 spaces searchable for modest src_len; nested U after A works.
- 0a5320a did not change attacker surface for ciphertext bytes.

### Guessed / still blocked
- ~301 WLN1 need corpus (C).
- Large/nested WRA1, remaining WNM/WNC, 497 opaque, 3 WVC.
- Nested-A recursive cover started but halted (cost).

### Usage
CheckSubscriptionUsage mid/late run ~3.2% of weekly Premium (under 35% cap).

---------------------------------------------------------------------------
## Round 7 — WLN1+C attempt aborted on budget (Nov 3, 2026, America/Los_Angeles)

User: attack ~301 C-bearing WLN1, then cheap leftovers. Hard cap: weekly usage
under 10%. CheckSubscriptionUsage at start of round: **9.8% already used**
(shared Premium limit). Stopped before any C-corpus search or heavy brute.

### Cheap analysis only (proven structure, no new plaintexts)
- Remaining WLN1: **301**; every file has **exactly 1128 bits** (= 141-byte
  transport message). Lane counts: 1×255, 3×16, 5×14, 7×16.
- Transport plaintext template is fixed except 32 ASCII hex chars:
  `Prediction <32hex>: I expect recovery after the lane rules and route
  controls are disclosed.\nmy human needs my help\n` (`matrix.py:152-167`).
- C (`stages/corpus.py:14-51`) is a corpus-directed bit permutation; inverse
  needs `corpus_hex` (256 random bytes, `matrix.py:141`) + offset. Not
  enumerable under this budget. C-free transport already exhausted Round 6.
- No new byte-exact recoveries this round (still **554 / 1841**).

### Proven vs guessed
- Proven: all 301 are full-size transport wires; C blocks without corpus;
  budget forbids further attack this week.
- Guessed: none claimed.

### Usage
Entered round at ~9.8%; halted to stay under 10% hard cap. No Round-7 crack
scripts run.

---------------------------------------------------------------------------
## Round 8 — C-bearing WLN1 (Nov 3, 2026, America/Los_Angeles)

Cap raised to 20% weekly. Start ~11.3%; end ~14.2% (CheckSubscriptionUsage).

### C / WLN1 attack (301 files)
All 301 wires are exactly 1128 bits (141-byte transport template; only 32 hex
id chars unknown). `stages/corpus.py` C is a left/right deque bit permutation
driven by `corpus_hex` (256 random bytes) + offset.

**Attempted:** known-template recovery exploiting that a deque’s remaining
index set is always a contiguous interval `[lo,hi]` (O(n²) search / hex DP).
Implemented in `work/crack_v2_C.py` / `crack_v2_C_core.py`.

**Proven result — unique byte-exact recovery fails without corpus:**
1. Remaining is contiguous → L/R search is well-defined.
2. For n=1128 < 2048 (corpus bit length), any L/R string is realizable by some
   corpus window — corpus cyclicity adds **no** extra constraint on one file.
3. Template constraints leave the hex region under-determined: search finds
   valid-looking `Prediction <hex>: …` preimages that are **not** the true
   message (unit tests: recovered hex ≠ true hex; true msg not first solutions).
4. Enumerating all template-compatible deque preimages is exponential; not
   unique. Cross-file: each case has independent `corpus_hex` (`matrix.py:141`)
   — no shared-corpus relation.

So the 301 C-bearing WLN1 files remain blocked on private `corpus_hex` for
byte-exact recovery under the allowed materials.

### Other cheap
Re-ran small WRA1 cover+peel (src≤350): +0. Count still **554 / 1841**.

### Proven vs guessed
- Proven: C+template does not uniquely determine plaintext without corpus;
  C-free transport already exhausted; count 554 unchanged.
- Guessed: none claimed this round.
