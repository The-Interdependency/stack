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
# optional deeper: nested U after A cover (inline in re-exam session)
ls v2_recovered/*.txt | grep -v RECOVERED | wc -l
```

## Recovered (proven, this re-exam)

**554 / 1841** byte-exact plaintexts with
`Prediction <32-hex>: …\nmy human needs my help\n`.

Prior claim 427 still holds (subset); re-exam added transport C-free, N→S order,
and small-WRA1 space cover.

| Family (prediction text) | Count |
|---|---:|
| permutation rules / selected order | 344 |
| lane rules and route controls | 92 |
| reflections cancel | 68 |
| source-guided / hidden placement (A) | 29 |
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

## Unrecovered (~1287)

| Class | ~Count | Blocker |
|---|---:|---|
| opaque (no magic after B/R) | 497 | Deep/mixed schedules |
| WLN1 | 301 | Almost all need **C** + `corpus_hex` |
| WNM | 186+7B | Deeper mixes / A after N / 3×S |
| WRA1 | 158+20B | Larger `src_len` space search; nested A |
| WNC | 106+9B | Nested / post-S / recipes |
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
