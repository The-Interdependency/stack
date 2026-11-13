# Reproducing Cypher's recovery of Weave v2 challenges

## Rules conflict (reported)

- **User authorization:** files under `recovery-challenges/v2` + pinned public
  source in SOURCE.json / README; exclude corpora, private profiles, originals,
  evaluator/operator archive, other org paths, `/workspace/cy`.
- **v2 README:** do not give this checkout to a no-clue (level-0) attacker;
  level 2 is source-informed.
- **Resolution:** operated as **source-informed (~ladder level 2)** — public v2
  folder + pinned stack/ucns only. No operator archive, no `private.json`, no
  answer keys, no corpora. RESULTS/COVERAGE/CHECKS/REVIEW_REPAIR are generation
  / integrity metadata (not answers) and were read.

## Inputs

```
branch tip 0a5320a407… (codex/weave-recovery-challenges-v1-20261029)
prior freeze bd54c789… — blind-pack.zip / ciphertexts / matrix UNCHANGED
0a5320a adds REVIEW_REPAIR.*, test_regressions.py, containment/checkpoint fixes
SOURCE.json pins stack@9de81c67… and ucns@905e6696… (same algorithms as v1)
blind-pack.zip → 1841 opaque .bin under blind/files/
```

Verify: `cd /workspace/cypher/v2 && sha256sum -c SHA256SUMS`

## Decode path (file:line) — validation vs byte recovery

| Stage | Where | Secrets needed for bytes? |
|---|---|---|
| **B** | `operations.py:137-138` bit-reverse (involution) | No |
| **R** | `operations.py:139-142` 3-byte reverse (involution) | No |
| **W** | `stages/whole.py` + `probe.py` last/first | No |
| **U** | `operations.py:124-128` → numeral restore | No (literal BitBlock) |
| **N** | `operations.py:109-111`; message at `cycle.py:290` `data[44:44+L]` | Corpus only validates padding (`cycle.py:286-289`) |
| **S** | `operations.py:129-132` prime interleave | Yes: path/arities/end_order — **catalog in `matrix.py:126-136` is small → brute-forceable** |
| **A** | `operations.py:112-123` WRA1; spaces via `recover_axis` + exact cover | Yes: spaces (circle_order leaks from packet entry circles, `cycle.py:388-390`) |
| **transport** | `transport_cases.py:106-127` WLN1 | C needs `corpus_hex`; X/J/I/W params (`thread_count`∈{3,5,7}, `lane_rotation`∈0..6, `inter_arity`∈{3,5,7}) brute-forceable for **C-free** schedules (`matrix.py:92-108`) |
| **cycle** | `operations.py:158-160` WVC | Full random profile + corpus |

## Repro commands

```sh
cd /workspace/cypher/work
python3 crack_v2b.py              # B/R/W/U/N + shallow WLN1
python3 crack_v2_S.py             # S catalog brute
python3 crack_v2_transport.py     # C-free transport (strict Prediction/line check)
python3 crack_v2_N1S.py           # N/U-first then S(/S)
python3 crack_v2_Asmall.py        # WRA1 space cover for small src_len + peel
python3 crack_v2_NA_fast.py       # N/U-first then inner WRA1
python3 crack_v2_opaque_fast.py   # opaque after B/R via W/S
python3 crack_v2_A_parallel.py    # parallel WRA1 cover bands (use timeouts)
# optional: crack_v2_NA_cont.py continuation; SIGALRM on try_cover
ls v2_recovered/*.txt | grep -v RECOVERED | wc -l   # expect 608
```

## Candidate outputs (format-validated; evidence limits)

**608 / 1841** candidate plaintexts pass a **strict format filter only**:
`Prediction <32-hex>: …\nmy human needs my help\n`.

This is **not** an independent byte-exact comparison to the excluded original
plaintexts or evaluator answers. Prior Cypher reports that called these
"byte-exact" overclaimed relative to that stronger standard. The outputs remain
useful cryptanalysis candidates under the allowed materials; they are not
owner-oracle confirmed. v1 recoveries are separately root-verified (see
REPRODUCE.md) and should not be conflated with this v2 filter.

The earlier 427 / 554 counts remain historical subsets under the same format
filter (plus false-positive tightening after Round 5); Round 9 raised the
on-disk format-valid set to 608.

| Family (prediction text) | Count |
|---|---:|
| permutation rules / selected order | 348 |
| lane rules and route controls | 92 |
| source-guided / hidden placement (A) | 79 |
| reflections cancel | 68 |
| literal containers (N/U) | 21 |

IDs: `work/v2_recovered/RECOVERED_IDS.txt`. Summary: `SUMMARY.json`.

### Methods that worked (no private archive)

1. Reflections B/R, whole W, literal U/N extract.
2. S brute over `matrix.py` public catalog (incl. N/U-first then S/SS).
3. WLN1 **without C**: enumerate accepted C-free schedules × thread/rotation/arity.
4. WRA1: parse WAF; recover spaces via `recover_axis` orbit + exact cover; peel
   N/U/S/B/R/W on restored bytes (incl. A∘U cases).

### False-positive filter (proven need)

Transport brute can emit cyclic shifts that merely *contain* the known line.
Accept only `startswith("Prediction ")` and `lines[1]=="my human needs my help"`.

## Unrecovered (1233)

| Class | Count | Blocker |
|---|---:|---|
| opaque (no magic after B/R) | 485 | Deep/mixed schedules beyond cheap W/S |
| WLN1 | 301 | C + private `corpus_hex` (non-unique without it) |
| WNM | 176 | Deeper mixes / A after N |
| WRA1 | 159 | Larger `src_len` / nested A; cover timeouts |
| WNC | 109 | Nested / post-S / recipes |
| WVC | 3 | Full random multi-round profiles |

## v1 → v2 (unchanged algorithms; harder packaging)

| | v1 | v2 |
|---|---|---|
| Cases | 8 WVC | 1841 mixed |
| Secrets | Group B spaces solvable | Per-case random; schedule hidden by opaque IDs |
| Fixed? | — | **Literals N/U still leak; S catalog still tiny; A spaces still searchable; C-free transport enumerable.** Transport **with C** and large/nested A remain hard without corpus/archive. |
| 0a5320a repair | — | Containment/checkpoint only; **ciphertexts & answers unchanged** (`REVIEW_REPAIR.md`). |

## Parameter leaks

- B/R public involutions; U/N carry message bytes.
- S parameter space = 3 paths × 5 arities × 2 end_orders.
- Transport without C: small discrete params; lane frame is transparent.
- A: circle_order on wire; spaces recoverable by geometry search for modest `src_len`.
- Predictions are frozen hypotheses in plaintext, not secrets.

## Not opened / excluded

- Operator archive / `private.json` / answer digests / corpora
- Paths outside `recovery-challenges` except SOURCE.json-pinned weave+ucns
- `/workspace/cy`, teammate bots

## Usage (this re-exam week of Nov 2)

Stopped nested large-WRA1 search while weekly usage still low (~3% reported mid-run);
target cap for the round was under 35%.

## Round 7 note (Nov 3)

Weekly usage was already ~9.8% at round start (hard cap 10%). No C-bearing
WLN1 attack executed. Structural fact: all 301 remaining WLN1 are 1128-bit
transport messages with only the 32-hex prediction id unknown; inverting C
still requires the private 256-byte `corpus_hex`. Count remains **554 / 1841**.

## Round 8 note (Nov 3)

Attacked 301 C-bearing WLN1 with known 141-byte template + contiguous-deque
search (`work/crack_v2_C_core.py`). **Proven:** without `corpus_hex`, deque
preimages under the template are **not unique** (and n=1128 < 2048 corpus bits
means any L/R string is corpus-realizable), so byte-exact recovery is blocked.
Count remains **554 / 1841**. Usage this round ~11.3% → ~14.2% weekly.

## Round 9 note (Nov 8)

Raised **format-valid** count **554 → 608** (+54) via N/U→inner WRA1, opaque W/S
peel, and parallel A cover (`crack_v2_NA_fast.py`, `crack_v2_opaque_fast.py`,
`crack_v2_A_parallel.py`). Strict Prediction/known-line filter; 0 bad files on
disk. Interrupt recovery: finished leftover shell `428949` (+1) without duplicate
compute. Soft stop 76–78% of 80% ceiling; this pass started ~55.3% weekly.
C/WLN1: unique recovery still needs corpus under allowed materials (Round 8
non-uniqueness result stands; do not overclaim impossibility). No pushes that
day.

### Evidence correction (publication, Nov 8 evening)

"Validated" / earlier "byte-exact" wording for v2 means **format filter only**,
not oracle comparison to excluded originals. Failed C attacks are not a proof
of security. Reproducibility gaps remain: some Round 6 nested-U steps were
inline; scripts assume `/workspace/cypher` absolute paths; historical LOG
entries retain superseded claims for audit.

## Round 10 (Nov 9 morning)

    python3 work/r10/census.py            # census.json
    python3 work/r10/sched_attack.py      # public-catalog schedule trie; writes work/v2_recovered/
    python3 work/r10/validate.py          # strict format filter; RECOVERED_IDS.txt
    python3 work/r10/verify_roots.py      # root_verify.json: tiers 1/2 = A-layer header roots match

Format-valid count 1537. Root tiers: 42 tier 1, 196 tier 2, 1201 tier 3, 98
not re-derived by this script. Scripts assume `/workspace/cypher` paths and the
pinned public source under `src/` and `v2/`.

## Round 11 (Nov 9, daily run)

    python3 work/r10/test_wln_coupled.py  # synthetic self-test (passes)
    python3 work/r10/test_wln_multiC.py   # synthetic self-test (FAILS; multi-C solver unused)
    xargs -P 7 -n 1 timeout 180 python3 work/r10/wln_coupled.py < work/r10/wln_remaining.txt > work/r10/wln_real.jsonl
    python3 work/r10/wln_unique.py        # wln_unique.json; accept only 1 distinct message
    python3 work/r10/validate.py

Format-valid count 1550 / 1841 (13 new WLN1; 1 ambiguous file rejected).

## Round 12 (Nov 10, early morning)

    python3 work/r12/test_synth.py        # single-C DP synthetics (must pass)
    python3 work/r12/run_1c.py 3          # remaining WLN1, m>=3 at C; run_1c.jsonl
    python3 work/r10/validate.py          # 1551 / 1841; validate_out.json

Do **not** run `work/r12/wln_multi.py` / `work/r12/test_multi_synth.py` on
challenge files: planted CC/CCC/XCC existence checks time out (see LOG
Round 12). `work/r10/test_wln_multiC.py` remains a failing DFS self-test;
the DP above replaces DFS only for exactly-one-C.

New format-valid candidate: `work/v2_recovered/1d27398c8e1086e8.txt`
(JWXIC, unique under the hex-filtered DP). Root-tier script was not re-run;
tiers stay 42 / 196 from Round 10.

## Rounds 13 and 15 (Nov 11–12): multi-C SAT (requires `pip install python-sat`)

    cd work/r13 && python3 test_synth2.py XCC 5 1   # planted; must print unique True
    bash one.sh 2f7a28768aab060c.bin XCC 1 7 0 3     # real file; unique
    python3 work/r15/forward_check.py 2f7a28768aab060c.bin XCC 1 7 0 3  # lanes_equal true
    python3 work/r10/validate.py                     # 1552 / 1841

`work/r13/plan.py` rebuilds `jobs.json` (not published, 17 MB). Planted
XCC t=3 and all XCCC cases time out at 900 s; do not treat timeouts as
negatives. XCC `none` results are unconfirmed eliminations (positive planted
tests only).

## Round 16 (Nov 13): remaining XCC jobs

    bash work/r16/run_real_kill.sh work/r16/args.txt /tmp/out.jsonl 72000 5   # 5 x none

Use the SIGKILL wrapper: plain `timeout` (SIGTERM) does not stop CaDiCaL
running inside Python.
