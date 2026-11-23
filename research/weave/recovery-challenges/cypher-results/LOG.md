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

---------------------------------------------------------------------------
## Round 9 — N/U→A, opaque peel, A-parallel (Nov 8, 2026, America/Los_Angeles)

User raised shared weekly ceiling to **80% total**; stop soft around 76–78%.
Exclusions unchanged (only recovery-challenges + SOURCE-pinned public code;
no corpora / private profiles / operator archive / `/workspace/cy` / other org
research / teammate bots). Blind-pack tip still `0a5320a407…` (ciphertexts
unchanged vs `bd54c789`).

### Interrupt recovery (this pass)
Prior run interrupted mid-batch. Measured usage at recovery start: **55.3%**
(well under soft stop). Inspected own shells: terminal `428949` (WRA1 src
400–2500 parallel, 4 workers) was still running; no duplicate launch. Batch
finished cleanly: +1 (`8021bf986cc8ee0d.bin`) → **608 / 1841**. No cracker
processes remain afterward.

### Recoveries this round (554 → 608, +54)
Methods / scripts (all under `/workspace/cypher/work/`):
- `crack_v2_NA_fast.py` / `crack_v2_NA_cont.py` — N/U-first then inner WRA1
  cover+peel
- `crack_v2_opaque_fast.py` — opaque W/S reveal after B/R
- `crack_v2_A_parallel.py` + inline WRA1 parallel cover (src bands, SIGALRM
  timeouts on `try_cover`) — raised source-guided/A family

Strict validation unchanged: `Prediction ` + 32 hex + known second line
`my human needs my help`. Re-validated all on-disk `.txt`: **608 good, 0 bad**.
IDs refreshed in `work/v2_recovered/RECOVERED_IDS.txt`; `SUMMARY.json` updated.

### Family counts (608)
| Family | Count |
|---|---:|
| permutation / selected order | 348 |
| lane rules / route controls | 92 |
| source-guided / A | 79 |
| reflections cancel | 68 |
| literal containers | 21 |

### Unrecovered (1233)
| Tag | Count | Blocker |
|---|---:|---|
| opaque | 485 | Deep/mixed schedules beyond cheap W/S |
| WLN1 | 301 | C + private `corpus_hex` (see Round 8 correction) |
| WNM | 176 | Deeper mixes / nested A |
| WRA1 | 159 | Larger/nested spaces; cover timeouts |
| WNC | 109 | Nested / post-S recipes |
| WVC | 3 | Full random multi-round profiles |

### Round 8 C/WLN1 wording correction (carried)
Free L/R deque+template finds template-compatible **non-unique** preimages;
n=1128 < 2048 corpus bits ⇒ free L/R overapproximates real C. Unique
byte-exact recovery still needs `corpus_hex` under allowed materials. Do **not**
overstate “ciphertext shorter than key ⇒ impossible.” Not a proof that secrets
are always required in every model — only that this attack does not uniquely
recover without corpus.

### Failed / halted avenues
- Unbounded `try_cover` hung → fixed with SIGALRM per-file timeouts.
- GeneratorExit / recursion / unsound fail-memo on earlier C search (Round 8).
- C-bearing WLN1 unique recovery still blocked without corpus.
- Large WRA1 src>2500 / deep nested A not exhaustively searched (cost).
- Interrupted parallel batch recovered and completed; do not relaunch duplicates.

### Proven vs guessed
- Proven: +54 new byte-exact under strict filter; N/U→A and opaque W/S peel
  work without private archive; validated total **608/1841**.
- Guessed: none claimed as wins without independent validation.

### Usage (Round 9 recovery pass)
Start of this completion pass: **55.3%** shared weekly Premium
(CheckSubscriptionUsage). Soft stop 76–78%; headroom sufficient for validate +
docs only after batch exit. No pushes / external messages.

### v1 preserved
`/workspace/cypher/work/{a,b}0*.recovered` untouched.


---------------------------------------------------------------------------
## Publication evidence correction — Nov 8, 2026 evening (America/Los_Angeles)

Append-only clarification for website/publication readers. Historical round
entries above are retained byte-for-byte as written at the time; this section
corrects overclaim language rather than rewriting them.

1. **v2 counts (427 → 554 → 608)** are counts of on-disk outputs that satisfy
   the strict expected form `Prediction <32-hex>: …` plus the common second
   line `my human needs my help`. They are **not** independently confirmed
   byte-exact matches against excluded original plaintexts or the evaluator
   archive. Calling them "byte-exact" in Rounds 5–9 overstated the evidence.
2. **v1** remains separately root-verified: reconstructed message-origin roots
   match the 32-byte values in each WVC header (see REPRODUCE.md). That check
   does not apply to v2's Prediction/phrase filter.
3. Round 9's "+54 new byte-exact under strict filter" should be read as
   **+54 new format-valid candidates**. Unrecovered remainder: **1233**.
4. Round 8's failed C/WLN1 attack shows non-unique preimages under the free
   L/R+template model without `corpus_hex`. That is **not** a general proof
   that those ciphertexts are secure against every method.
5. Access boundary for published work: recovery-challenges public materials +
   SOURCE-pinned public code only; no corpora, private profiles, originals,
   operator/evaluator archive, or `/workspace/cy`.
6. Personal/shared weekly usage percentages appear in operational notes for
   budget discipline; they are not cryptographic evidence and are not part of
   any canonical skill-lib doctrine text.


---------------------------------------------------------------------------
## Round 10 — Nov 9, 2026 morning (America/Los_Angeles), pre-reset window

Recorded after the fact by the Nov 9 10:00 run: the 07:00 pre-reset run did the
compute below but ended (run marked failed) before logging or publishing. Its
artifacts were found intact under `work/r10/` and are published unchanged.

- `work/r10/census.py` → `census.json`: per-file reachability census of the
  public v2 wire formats (blind files only).
- `work/r10/sched_attack.py` + `fastA.py`: walk the trie of reversed schedules
  from the PUBLIC `v2/matrix.py` catalog with public inverses (B, R, W, N, U,
  A analytic space recovery, S over 30 public specs). Run logs `run1.log`,
  `run2.log`, `progress.jsonl`; 28-file retry list `retry.txt`.
- Result: **608 → 1537** format-valid candidates (+929, files in `work/r10/new/`
  and merged into `work/v2_recovered/`). `validate.py` → `validate_out.json`:
  0 bad, 0 orphans. Remaining after Round 10: WLN1 301, WVC 3.
- `work/r10/verify_roots.py` → `root_verify.json` (independent re-derivation
  plus header-root check). U packets publicly expose the per-case `scope`; A
  (WRA1) headers store `message_origin = digest(schema, version, scope, length,
  sha256(A input))`. Recomputing that with pinned public `native_binary.ByteOrigin`:
  - Tier 1 (verified A input IS the candidate plaintext): **42**
  - Tier 2 (a verified A layer lies on the recovery path): **196**
  - Tier 3 (format filter only): **1201**
  - Re-derivation not reproduced by this script: 93 no-hit, 5 timeout (these
    were found by earlier round scripts; not counted as failures, not verified).
  Tier 1/2 are digest-level checks of a layer using source-informed public code;
  they are not L0 blind results and not comparisons to excluded originals.
- WLN1 work started in Round 10: `wln_coupled.py` (single C, lanes coupled by
  a shared corpus window) and `wln_multiC.py` (1–3 C stages). Not run on real
  files in Round 10.

## Round 11 — Nov 9, 2026 ~10:10–10:40 (America/Los_Angeles), daily check

Challenge branch `codex/weave-recovery-challenges-v1-20261029` still at
`0a5320a4075a…`; no new or changed challenge files. Usage at start 0.1% of the
shared weekly limit (reset just occurred); session ceiling frozen at ~49.9%.
Rechecked mid-session at 0.6%.

- Synthetic self-tests (random corpora, public forward code, not challenge data):
  - `test_wln_coupled.py`: single-C solver recovers the planted message
    (`test_coupled.log`). Some test schedules are not in the public catalog.
  - `test_wln_multiC.py`: **multi-C solver FAILS its own self-test** — 0
    solutions on all five planted cases, budget hit while reporting
    "exhausted" (`test_multiC.log`). Treated as broken; not run on real data.
- Ran `wln_coupled.py` on all 301 remaining WLN1 files (180 s cap per file,
  `wln_real.jsonl`): 14 files produced template-consistent messages; 287 none.
- `wln_unique.py` → `wln_unique.json`: re-solved each hit with maxsol=1000,
  20M-step budget, across every matching parameter set:
  - 11 files: exactly one distinct message, search exhaustive for each
    matching parameter set.
  - 2 files (`15775eebc4c7ffb1`, `cc7443d364e0de10`): one distinct message
    among the first 1000 corpus-window solutions; search not exhaustive.
  - 1 file (`3e0d65a6a011c174`): **two** distinct hex ids (differ in two hex
    digits) — ambiguous, NOT accepted.
- Accepted 13 as format-valid candidates (`work/r11_new/`, merged into
  `work/v2_recovered/`). `validate.py` → `validate_out_r11.json`:
  **1550 / 1841**, 0 bad, 0 orphans. Remaining: WLN1 288, WVC 3.
  (`validate_out.json` restored to the Round 10 snapshot; Round 10 copy also
  kept as `validate_out_r10.json`.)

### Correction to Round 8 / Round 9 WLN1 wording
Round 8 found non-unique preimages for C-bearing WLN1 under a model that let
each lane's left/right route vary freely. The public `transport_cases.contexts`
makes every lane read the same corpus window shifted by one bit per lane; using
that coupling, 11 files have a unique template-consistent message without the
corpus. So "unique recovery needs `corpus_hex`" was a limit of the earlier model,
not of the files. The remaining 288 WLN1 files are not shown secure either.

### Proven vs guessed
- Proven (reproducible from published scripts): the 13 messages are consistent
  with the public template and the wire under the public transport code; 11 are
  unique within the searched parameter sets.
- Not proven: byte-exact match to excluded originals; that the parameter sets
  searched include the true one for the 287 no-hit files.


---------------------------------------------------------------------------
## Round 12 — Nov 10, 2026 ~1:51–2:20 AM (America/Los_Angeles)

Goal: recover the remaining 288 WLN1 + 3 WVC left after Round 11. Shared weekly
usage at start 19.2%; session cap ~55%.

### What was wrong with the earlier multi-C solver
`work/r10/wln_multiC.py` reported 0 solutions on five planted cases and was
treated as broken. Replaying a planted corpus window through its waiter/trace
logic shows the *model* is fine: the true window satisfies every template
constraint. The same planted `XC` case (seed 7, `os.urandom` corpus) also
exhausts `wln_coupled.solve`'s 3M-step DFS with 0 hits. So the failure is
incomplete search (a large compatible-end tree), not a wrong transition. This
does not make the older logs wrong about "not used on real data" — that
decision was correct given the failing self-test as written.

### Single-C DP (`work/r12/wln_dp.py`)
Replaced DFS with a DP over shared window prefixes (state = per-lane left
counts). Hex id uniqueness is checked by searching 0-9a-f at each of the 32
id bytes, using `_exists` with those bits forced. Conservative: only messages
that are both accepting windows and hex-valid are counted.

Synthetic fixtures (public `transport_cases.run`, `random.randbytes` corpora,
not challenge data) in `work/r12/test_synth.py`:
- `XC` thread_count 3/5/7, seeds 7/1/3: status `unique` and byte-equal to the
  planted message. Seed 7 is the case that exhausted 3M-step DFS.
- Single-lane `C`: status `ambiguous` (same non-uniqueness Round 8 saw under
  a free L/R model).

### Applied to the 288 remaining WLN1 (m≥3 lanes live at C)
`python3 work/r12/run_1c.py 3` → `work/r12/run_1c.jsonl` (17s).
- **1 unique:** `1d27398c8e1086e8.bin`, schedule `JWXIC` (three matching
  parameter sets agreed). Format-valid candidate
  `Prediction 1395a37c21cc440681655653a4c6ce14: …`. Not an A-layer
  root check — tier-3 format+uniqueness only.
- **1 ambiguous:** `3e0d65a6a011c174.bin` on `WIXCJ` — the same file Round 11
  rejected for two hex ids. Still rejected.
- **286 none** under every catalog 1-C layout with m≥3 at C.

`validate.py`: **1551 / 1841**, 0 bad, 0 orphans. Remaining: WLN1 287, WVC 3.

### Multi-C
A unit-propagating waiter search (`work/r12/wln_multi.py`) still **times out**
on planted `CC`, `CCC`, and `XCC` (3M-step budget, ~16–30s, result `None` /
`timeout`). A Z3 array encoding of single-lane `CC` was killed by the OS
(memory). Neither was run on challenge files.

The 3 remaining WVC files share the public `CYCLE_NATIVE.json` digest
`cdf11526…` with v1; they were not opened this round. Recovering them still
appears to need per-file random profile parameters beyond the v1 group-A/B
leaks.

### Proven vs guessed
- Proven (reproducible scripts + synthetics): DP recovers planted single-C
  XC messages uniquely; one new challenge file is the unique hex-valid
  preimage under every matching m≥3 1-C catalog layout.
- Not proven: match to excluded originals; that remaining WLN1 files are
  secure (most are likely multi-C or other unsolved schedules).

---------------------------------------------------------------------------
## Round 13 — Nov 11, 2026 daily run (America/Los_Angeles), reconstructed

The Nov 11 run ended before it wrote any log, docs or commit. This entry is
reconstructed on Nov 12 from the files it left in `work/r13` and `work/r14`;
nothing in them was edited.

- `work/r13/wln_sat.py`: CNF encoding of multi-C WLN1 transport (public
  `transport_cases` only). Every C stage reads one shared corpus window;
  X/J/I/W are pushed through the public forward code as variable labels;
  each C lane is a deque route with one-hot left-count variables; hex id
  chars are constrained to 0-9a-f. Uniqueness = re-solve with a blocking
  clause on the hex bits. Solver: CaDiCaL 1.5.3 via PySAT. Corpus wrap is
  ignored, which can only add solutions.
- `work/r13/plan.py` → `jobs.json` (316,930 file/schedule/parameter jobs over
  the 287 remaining WLN1; 17 MB, regenerable, not published). Only 41 files
  fit 3–4-op schedules (XCC / XCCC); the other 246 fit only 10- or 15-op
  catalog schedules.
- Planted test (`test_synth.py`): only `XCC t=5 seed 1` is recorded:
  `unique`, byte-equal, 50.7 s. The other planted cases left empty logs.
- Real run (`p1_args.txt` → `p1_out.jsonl`, 150 s cap): 81 of 82 XCC/XCCC
  jobs recorded: XCC 28 none, 11 timeout, **1 unique**
  (`2f7a28768aab060c.bin`, t=7); XCCC 41 timeout. One XCC job
  (`04be9cd9…`, t=7) is missing from the output.
- An in-process time limit crashed (`err.log`: CaDiCaL does not support
  `solve_limited` interrupts); the shell `timeout` wrapper was used instead.
- `work/r14/one600.sh` (600 s wrapper) exists but produced no output.

---------------------------------------------------------------------------
## Round 15 — Nov 12, 2026 ~10:25–11:00 AM (America/Los_Angeles), daily check

Challenge branch head unchanged (`0a5320a`, Oct 30 PDT); no new challenge
files. Shared weekly usage 55.8% at start; session ceiling frozen at ~22
points (half of remaining) — actual use far below that.

### Forward check of the Round 13 candidate (`work/r15/forward_check.py`)
Re-solve `2f7a28768aab060c.bin` under XCC (thread_count 7), pull the shared
corpus window (167 bits) out of the SAT model, then run the **public
forward** `transport_cases.run` on the candidate message with that window as
a synthetic corpus. Every output lane bit equals the challenge file
(`forward_check_2f7a.json`: `lanes_equal: true`), and the stored text is
byte-identical to the model message. The hex id is unique under XCC t=7.
Candidate: `Prediction 7a0577073d5e4119c0e2ee22d3c02082: …` (lane-rules
family). The XCCC job for the same file timed out, so uniqueness across
*every* schedule is not proven.

`validate.py`: **1552 / 1841**, 0 bad, 0 orphans. Remaining: WLN1 286, WVC 3.

### More planted tests (`work/r15/synth.sh`, 900 s cap)
- XCC t=7 seed 3: unique, byte-equal, 17 s
- XCC t=5 seed 2: unique, byte-equal, 43 s
- XCC t=3 seed 7: timeout
- XCCC t=3/5/7: all timeout

### Real XCC reruns (`work/r15/run_real.sh`, 900 s cap)
The 11 Round-13 XCC timeouts plus the missing `04be9cd9…` job: **12/12 timeout**
(`xcc_out.jsonl`). Nearly all are t=3, matching the planted t=3 timeout.

### Proven vs guessed
- Proven: one more file has an exact forward-checked preimage under a public
  catalog schedule (format-valid + reproducible re-encode). Not compared with
  excluded originals.
- Conditional: the 28 XCC "none" results mean no XCC preimage exists *if* the
  CNF is correct. It passes positive planted tests only; no planted negative
  test was run, so treat them as unconfirmed eliminations.
- Not attempted: XCCC (planted tests all time out), 10/15-op schedules
  (~317k jobs), the 3 WVC files.

### Lessons
A SAT solver turned the t=5/t=7 multi-C cases from "times out" into seconds,
but t=3 (fewer, longer lanes) is still out of reach at 15 minutes. A forward
re-encode is a much stronger check than a format match and costs ~15 s.

---------------------------------------------------------------------------
## Round 16 — Nov 13, 2026 ~10:23–11:00 AM (America/Los_Angeles), daily check

Challenge branch head moved to `f435c65` (Nov 12, 12:12 PM PST), but the
only change inside `research/weave/recovery-challenges/` is one trailing
blank line removed from `README.md`. No new or changed challenge files. (Only
the file list of the diff was used to establish this; no other folders read.)
Shared weekly usage 60.7% at start; session ceiling frozen at ~19 points
(half of remaining). Actual use far below that.

### Correction to Round 15 (append-only; Round 15 text left as written)
Round 15 says the 12 real XCC reruns were "12/12 timeout (`xcc_out.jsonl`)".
That run was **invalid**: a wrapper bug dropped the file argument, so every
job crashed and was recorded as a timeout. Its output is kept as
`work/r15/xcc_out_INVALID_argbug.jsonl` / `real_INVALID_argbug.err`. The
fixed wrapper reran only 7 of the 12 jobs (`xcc_args2.txt` → `xcc_out2.jsonl`)
and finished overnight, after the Round 15 log was written:
6 `none`, 1 recorded `timeout2400` (`187df4d1…`). The `timeout` wrapper sent
SIGTERM, which did not stop the solver inside Python; some jobs ran ~16 h.
The planted `XCC t=3 seed 7` long rerun (`synth_t3_long.log`) also timed out
at 2400 s.

### This round (`work/r16/`)
- `run_real_kill.sh`: same as `r15/run_real.sh` but `timeout -s KILL`.
- The 5 XCC jobs never validly run (`args.txt` → `out.jsonl`):
  `04be9cd9…` (t=7) and 4 t=3 files — **5/5 `none`**, 4–385 s each.
- `187df4d1…` relaunched with a 20 h kill cap (`out_187d.jsonl`); result
  pending at the time of writing.

### XCC tally over the 41 files that fit 3–4-op schedules
1 unique (`2f7a2876…`, forward-checked, Round 15), 39 `none`,
1 unresolved (`187df4d1…`). `validate.py` count unchanged at **1552 / 1841**.

### Proven vs guessed
- The 39 `none` results only eliminate XCC (one schedule out of several each
  file could fit) and only if the CNF encoding is complete. Positive planted
  tests pass; no independent proof of completeness exists. Treat them as
  conditional.
- XCCC and all 10/15-op schedules remain untried on the real files.

### Lessons
Check that a background batch is actually running the intended jobs before
writing results down; the Round 15 log recorded a crashed batch as timeouts.
Use SIGKILL caps for C solvers called from Python.

---------------------------------------------------------------------------
## Round 17 — Nov 16, 2026 ~7:34–8:15 AM (America/Los_Angeles), pre-reset window

Shared weekly usage 76.2% at start, reset 9:10 AM PST (1h35m away), so the
pre-reset allowance applied (98% absolute ceiling). Used ~2–3 points.

### Challenge branch check
Branch head is now `978951d` (Nov 15, 9:23 PM PST). Inside
`research/weave/recovery-challenges/` the changes since `f435c65` are
infrastructure repairs in `v2/`: frozen-source bundle and loader, checkpoint,
census and release repairs, new SHA256SUMS lists, `SOURCE_REPLAY_VECTORS.json`.
`blind-pack.zip`, `transport_cases.py` and `matrix.py` hashes are unchanged,
so no new or changed ciphertexts. (Only that folder's diff was read.)

### 1. Round 16 pending job finished
`187df4d1…` XCC t=3 → `none` after 27,306 s (`work/r16/out_187d.jsonl`).
XCC tally over the 41 files that fit 3–4-op schedules: **1 unique
(`2f7a2876…`), 40 `none`, 0 unresolved.** `validate.py` count unchanged at
1552 / 1841.

### 2. Independent check of the local forward model
The new public `SOURCE_REPLAY_VECTORS.json` (copied unchanged to
`work/r17/SOURCE_REPLAY_VECTORS.978951d.json`) has one transport vector
(schedule XCIJW, lane_rotation 1), sealed with the original adapters. My
local `transport_cases` pipeline (with the stubbed `operations` module)
reproduces its wire **byte for byte** (`replay_transport.py` →
`replay_transport.out`). This is the first check of my transport model
against a vector I did not generate.

### 3. Planted tests for the XCC SAT encoding (`work/r17/`)
`negpos.py` plants XCC wires (n=1, rot=0, arity 3 — same configuration as
the real runs), `run.sh` runs 20 jobs, 6 at a time, `timeout -s KILL 900`.
Args, empty `err.log` and run times were checked before this write-up.

- **Truth admitted** (true plaintext bits fixed as unit clauses; solver must
  find a corpus window): t=3 6/6 SAT (102–380 s), t=5 2/2 (27–38 s),
  t=7 1/1 (3 s). (A manual t=7 seed 1 run, not in `out.jsonl`, was also SAT.)
  So the CNF does not exclude the true solution on any planted case,
  including t=3, where full recovery still times out.
- **Planted negatives, random wires** (same lane shape, random bits; a
  preimage is astronomically unlikely, roughly 2^-600 by counting free versus
  constrained bits): t=3 3/3 `none` (97–478 s), t=7 1/1 `none`.
- **Planted negatives, near-miss** (1 or 8 wire bits flipped in a planted
  wire): t=7 2/2 `none` (3 s); t=3 5/5 **killed at 900 s (inconclusive)**.

### Proven vs guessed
- The 40 XCC `none` results now rest on: positive planted recovery (t=5, t=7),
  truth admission at t=3/5/7, and planted negatives on random wires. They are
  still eliminations of **XCC with n=1, rot=0, arity 3 only**, and only within
  the planted-test coverage (no proof of encoding completeness). The near-miss
  negatives at t=3 did not finish, so false-negative behaviour close to a
  real wire is not tested at t=3.
- 1-bit flips returning `none` at t=7 is expected but not guaranteed (a flip
  could have a real alternative preimage); none was found.
- XCCC and 10/15-op schedules remain untried on the real files.

### Lessons
Fixing the known truth and asking only "is it still satisfiable?" is a cheap
completeness test that works even where full recovery times out (t=3).
Near-miss negatives are much harder for the solver than random ones.

---------------------------------------------------------------------------
## Round 18 — Nov 17, 2026 ~10:33–11:00 AM (America/Los_Angeles), daily check

Shared weekly usage 27.6% at start (reset Mon Nov 23, 9:10 AM PST); session
ceiling frozen at ~36 points (half of remaining). Actual use: a few points.

### Challenge branch check
Branch head still `978951d` (Nov 15, 9:23 PM PST). No new or changed
challenge files.

### XCCC planted tests launched (`work/r18/`)
Round 15's XCCC planted recoveries all hit 900 s (and used SIGTERM caps).
Before any real XCCC run, the encoding needs planted evidence, so this round
launched six planted XCCC jobs (n=1, rot=0, arity 3; same config as the real
`r15/xccc_args.txt`) with `timeout -s KILL 14400` (4 h):
- `negpos4.py` = `r17/negpos.py` with the schedule as a 5th argument
  (default XCC, so r17 behaviour is unchanged).
- `args.txt`: truth-admission t=7 seeds 3,4; t=5 seed 1; t=3 seed 7;
  random-wire negative t=7 seed 1; full planted recovery (`pos`) t=7 seed 3.
- Checked at ~1.5 min: all six intended jobs running, `err.log` empty.
- At ~12 min: **none finished**, not even truth admission at t=7 (XCC took
  3 s there). Results go to `out.jsonl`; pending at the time of writing.

### Proven vs guessed
Nothing new proven. The 12-min observation only says XCCC is far harder for
this CNF than XCC; it says nothing about completeness. Real XCCC runs stay
on hold until the planted jobs report.

---------------------------------------------------------------------------
## Round 19 — Nov 18, 2026 ~10:33–11:20 AM (America/Los_Angeles), daily check

Shared weekly usage 30.7% at start (reset Mon Nov 23, 9:10 AM PST); session
ceiling frozen at ~34 points (half of remaining). Actual use: a few points.

### Challenge branch check
Branch head still `978951d` (Nov 15, 9:23 PM PST). No new or changed
challenge files.

### Round 18 XCCC planted batch — results (`work/r18/out.jsonl`)
| job | result |
|---|---|
| truth-admission t=7 seed 4 | `sat_truth_admitted` after 16754 s wall |
| truth-admission t=7 seed 3 | killed at 4 h SIGKILL cap |
| truth-admission t=5 seed 1 | killed at cap |
| truth-admission t=3 seed 7 | killed at cap |
| random-wire negative t=7 seed 1 | killed at cap |
| full planted recovery t=7 seed 3 | killed at cap |
Batch wrote `{"DONE":1}`; `err.log` empty.

**Run-integrity caveat.** The box rebooted/restored at 01:32 AM Nov 18
(`uptime -s`). The five surviving jobs showed process start time 07:10 AM
Nov 18 in `ps`, yet `truth 7 4` was not re-run and its Nov 17 15:13 line
was kept, so these look like the original processes resumed rather than a
fresh relaunch (not confirmed). Consequences: the 4 h SIGKILL caps appear
to have restarted at 07:10 AM, so total solver time per job is
uncertain (≥4 h, possibly much more). The 16754 s wall figure for seed 4 is
above both its 14000 s internal timer and the 14400 s cap, which also
suggests the process was paused for part of that time; treat it as wall
time, not CPU time.

### Proven vs guessed
- Proven (planted, tier: solver admits known truth): the XCCC encoding
  (n=1, rot=0, arity 3) admits the true plaintext in 1 of 1 finished case,
  so it is not obviously over-constrained.
- Not shown: XCCC full recovery, XCCC negatives, and every truth-admission
  check below t=7 — all timed out. No XCCC "none" result on a real file
  would count as an elimination right now.
- Practical result: XCCC with the current CNF + CaDiCaL is far too slow
  (≥hours per planted case vs 3 s for XCC). Real XCCC runs stay on hold;
  a different encoding or a reduced search would be needed first.

### Lessons
After a box restart, check process start times and the KILL-cap clock
before trusting reported runtimes; a resumed process can silently reset
`timeout`.


---------------------------------------------------------------------------

## Round 20 — Nov 19, 2026 ~10:29–10:50 AM (America/Los_Angeles), daily check

Shared weekly usage 54.1% at start (reset Mon Nov 23, 9:10 AM PST; others'
use since yesterday counts); session ceiling frozen at ~74% (half of the
remaining 45.9 points, with margin). Actual use: a few points.

### Challenge branch check
Branch head is now `207883c` (Nov 16, 8:57 PM PST), but the
`research/weave/recovery-challenges` tree SHA is identical at `207883c` and
`978951d` (`3e3b71bf…`). No new or changed challenge files. (Correction to
Rounds 18–19: "branch head still 978951d" was the last commit touching the
folder, not the branch head; the conclusion — no folder changes — stands.)

### XCCC solver portfolio launched (`work/r20/`, planted only)
Round 19 showed CaDiCaL 1.5.3 needs ≥4.7 h to admit the known truth on XCCC
t=7 seed 4. Cheap novel question: is that the encoding or the solver?
Same CNF and unit clauses as `r18/negpos4.py` truth mode, different pysat
back-ends (`portfolio.py`, solver = 6th arg), `timeout -s KILL 7200`:
- XCCC t=7 seed 4 (known SAT): glucose4, maplechrono, minisat22, kissat404
  (`portfolio2.py` / `run2.sh`, plain `solve()` fallback).
- XCCC t=7 seed 3: glucose4, maplechrono.
- Control: XCC t=7 seed 1 with glucose4 (CaDiCaL: SAT in seconds, r17).
- Failed launches, kept as-is: lingeling does not support `solve_limited`
  (traceback in `err.log`); the non-daemon timer kept the process alive
  until I killed it, so its `out.jsonl` line **"killed7200" is a crash, not a
  timeout**. `cryptosat` is not built into this pysat install
  (`NoSuchSolverError`, `out2.jsonl` "exit1"). `run2.sh` records exit codes
  to avoid that mislabel.
- Checked at ~1.5 min: the 6 + 1 intended jobs running. Pending at write-up;
  results go in a later session.

### Proven vs guessed
Nothing new proven. These are planted truth-admission tests only; even a fast
SAT would show solver speed, not completeness, and no real file is touched.

### Lessons
Branch-head checks should compare the folder tree SHA, not path-filtered
commit history. A pysat `threading.Timer` must be daemon or cancelled on
every path, or a crash looks like a timeout.

---------------------------------------------------------------------------
## Round 21 — Nov 20, 2026 ~10:31–11:10 AM (America/Los_Angeles), daily check

Shared weekly usage 66.9% at start (reset Mon Nov 23, 9:10 AM PST); session
ceiling frozen at ~82% (half of the remaining 33.1 points), aiming far
below. 67.3% at mid-session recheck.

### Challenge branch check
Branch head still `207883c` (Nov 16, 8:57 PM PST), so the challenge folder
is unchanged. No new or changed challenge files.

### Round 20 portfolio — results (`work/r20/out*.jsonl`)
Batch wrote `{"DONE":1}` in both files; `err*.log` hold only the two known
launch failures (lingeling, cryptosat).
| job (planted truth admission) | result |
|---|---|
| XCCC t=7 seed 4, **kissat404** | `sat_truth_admitted`, 207.5 s wall |
| XCCC t=7 seed 4, glucose4 / maplechrono / minisat22 | `timeout` (7000 s internal timer) |
| XCCC t=7 seed 3, glucose4 / maplechrono | `timeout` |
| XCC t=7 seed 1 (control), glucose4 | SAT, 16842.8 s wall (CaDiCaL: seconds) |
**Timing caveat.** The reported `secs` (~26609 s) exceed the 7200 s SIGKILL
cap, and all r20 files carry the same Nov 19 ~11:03 PM mtime; the box
appears to have been paused/restored (it was up only since 09:34 AM today).
`secs` is wall time from `time.time()`, while the interrupt timer is
monotonic, so the "timeout" rows most likely mean ~7000 s of solver time,
not 26609 s. All r20 times are wall-clock and should be read as upper
bounds on compute. r21 scripts log wall, monotonic and CPU separately.

### Round 21 — kissat follow-up (`work/r21/`, `kport.py`, `kport2.py`)
Same CNF as r18/r20 (`wln_sat.build`, n=1, rot=0, arity 3), kissat404 via
pysat, `timeout -s KILL 3600`, exit codes recorded.
- Control XCC t=7 seed 1 truth: SAT in 9.1 s (`control.jsonl`).
- XCCC t=7 seed 3 truth: **SAT in 45.4 s CPU** (CaDiCaL ≥4 h, glucose4 /
  maplechrono ~7000 s without answer).
- XCCC t=7 seed 3 **full planted recovery** (`pos`): first model = planted
  message after 108.6 s; uniqueness re-check with a fresh solver → **unique**,
  1252 s CPU total. This is the first planted XCCC recovery by any of my
  solvers, at the tier "recovered message equals the planted one and the
  CNF has no second hex solution".
- First `pos` launch crashed (exit 134): kissat is non-incremental, so
  `add_clause` after `solve` aborts. Kept in `out.jsonl`/`err.log`;
  `kport2.py` rebuilds a fresh solver for the uniqueness step.
- XCCC t=5 seed 1 truth and XCCC t=7 seed 1 random-wire planted negative:
  still running at write-up (cap 3600 s); results next session.

### Real XCCC files with kissat (`work/r21/real_k.py`, `run_real.sh`)
All 41 XCCC parameter rows from `r15/xccc_args.txt` (13 × t=7, 14 × t=5,
14 × t=3), t=7 first, 3 parallel, nice 10, `timeout -s KILL 1800`. On SAT
the script forward re-encodes with the public `transport_cases.run` and
compares every lane (same check as `r15/forward_check.py`), saving
candidates to `r21/cand/`. Checked at 2 min: the three intended t=7 jobs
running. At write-up: 3 rows done, all `none_UNCONFIRMED` (05ae019f…,
04be9cd9…, and 2f7a2876… — the file already uniquely recovered under XCC,
so a none here is the expected answer). Rest pending (several hours).

### Proven vs guessed
- Proven (planted): with kissat, the XCCC encoding recovers a planted t=7
  message uniquely, and admits the truth at t=7 on seeds 3 and 4. The
  bottleneck in r18–r20 was the solver, not the encoding.
- Not yet shown: XCCC planted negatives (random and near-miss), and
  anything at t=3/5. So the real-file `none` rows are **not eliminations**
  yet; they are labelled `none_UNCONFIRMED` in the data itself.
- No new real recovery.

### Lessons
Try a small solver portfolio before redesigning an encoding: one solver
swap turned "hours, no answer" into ~1–2 minutes. Check incremental
support per solver before reusing an incremental script.



## Round 21 batch results — written up Nov 23 (from `work/r21/*.jsonl`, unchanged)
- Planted batch (`out.jsonl`): XCCC t=7 seed 1 random-wire negative and XCCC
  t=5 seed 1 truth both hit the 3600 s SIGKILL cap (exit 137). No answer.
- Real XCCC batch (`real.jsonl`, `{"DONE":1}` present, `real.err` empty):
  41 rows → **14 none_UNCONFIRMED** (11 × t=7, 3 × t=5) and **27 exit137**
  (1800 s cap: 2 × t=7, 11 × t=5, 14 × t=3). No SAT, so no candidates
  (`r21/cand/` never created). The t=7 none for 2f7a2876… is the expected
  answer (that file is uniquely recovered under XCC).

## Round 22 — Nov 23, 2026 7:37–9:21 AM (America/Los_Angeles), pre-reset window, reconstructed
The 07:00 pre-reset run started this batch and ended (run marked failed)
before writing any log, diary or commit. This entry was written by the Nov 23
10:36 daily run from the leftover files in `work/r22/`, which are published
unchanged. Script `kport.py` is the r21 script; cap 4200 s SIGKILL, 4 parallel.
- XCCC t=7 seed 2 random-wire planted negative (kissat404): **none** in
  1554.7 s (wall = mono, CPU 1551.9 s). Correct answer — first completed
  XCCC planted negative.
- XCCC t=7 seed 1 random negative (kissat404 and cadical195) and XCCC t=5
  seed 1 truth (kissat404): all exit 137 at 4200 s. No answer.

## Round 23 — Nov 23, 2026 ~10:36–11:30 AM (America/Los_Angeles), daily check
Shared weekly usage 0.7% at start (weekly reset happened Nov 23, 9:10 AM PST;
next Mon Nov 30, 9:10 AM PST). Session ceiling frozen at ~50% (half of the
remaining 99.3 points), aiming far below. 1% at mid-session recheck.

### Challenge folder check
`research/weave/recovery-challenges` tree SHA on
codex/weave-recovery-challenges-v1-20261029 is still `3e3b71bf…`; the last
commit touching it is still `978951d` (Nov 16). No new or changed files.
(Process slip: to get the folder's tree SHA I listed the parent
`research/weave` directory, which returned sibling file names. No sibling
content was opened or used. Next time fetch the folder SHA via the
branch's commit tree path only.)

### XCCC near-miss planted negatives (`work/r23/`)
`kport3.py` = r22 `kport.py` + mode `nearK`: the planted t=7 seed 3
message's wires with K random wire bits flipped (rng seed 3000+seed).
kissat404, `timeout -s KILL 2400`, 3 parallel, nice 5.
- near1 (1 bit flipped): **none**, 1156.4 s (wall = mono, CPU 1156.3 s).
- near8 (8 bits flipped): **none**, 1107.3 s (CPU 1107.2 s).
- rand seed 3: exit 137 at 2400 s, no answer.
A first launch was aborted within ~1 minute because a here-doc patch failed
and the unpatched script started; it was killed and its outputs deleted
before relaunch (no results lost). While killing it I used
`pkill -f run.sh`, which matches any process with that name on the shared
box; nothing else appeared affected, but next time kill by recorded PID.

### Where the XCCC t=7 "none" rows stand
Completed XCCC t=7 planted negatives: 3 of 3 correct (random seed 2, near1
and near8 on seed 3). Timeouts: random seed 1 (twice, 3600/4200 s), random
seed 3 (2400 s) — no wrong answers. So the t=7 none rows now meet my bar of
"passes a random and a near-miss planted negative for this schedule and
size". The 10 real t=7 XCCC none rows (excluding 2f7a2876…, solved under
XCC) are now **conditional eliminations** of the hypothesis "XCCC, t=7,
n=1, rot=0, arity 3" for those files — conditional on my model of the public
encoder and on a single planted message for the near-miss test. The original
rows in `r21/real.jsonl` stay labelled none_UNCONFIRMED (append-only data);
this paragraph is the upgrade. t=5 and t=3 rows are still unconfirmed or
timed out; t=5 truth admission has never finished (3600 s and 4200 s caps).

### Proven vs guessed
- Proven (planted): kissat on the XCCC t=7 encoding rejects a 1-bit and an
  8-bit near-miss and one random wire set.
- Not shown: anything at t=5/3; random seeds 1 and 3 never finished.
- No new real recovery.

### Lessons
A near-miss negative can finish faster than a random one here (≈19 min vs
>40 min), so it is the cheaper first check. Write patch scripts to files
rather than inline here-docs inside a templated command, and kill by PID.

