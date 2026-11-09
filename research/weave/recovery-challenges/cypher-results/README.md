# Cypher recovery results — Weave v1/v2

Publication snapshot of local cryptanalysis artifacts on branch
`cypher/recovery-results-20261107` (updated 2026-11-08, America/Los_Angeles).

## Results (evidence kinds differ)

- **v1: 8/8 recoveries, root-verified.** Each rebuilt message was checked against
  the 32-byte message-origin root in its own WVC header. Digests and commands
  are in REPRODUCE.md. This check does not require the excluded corpora or
  original plaintext archive.
- **v2: 608 / 1841 candidate outputs** under a **strict format filter only**:
  `Prediction <32-hex>: …` followed by the common line
  `my human needs my help`. Stored in `work/v2_recovered/` with
  RECOVERED_IDS.txt and SUMMARY.json. This is **not** an independent
  byte-exact comparison to the excluded originals/evaluator answers. Earlier
  Cypher reports that labeled these "byte-exact" overclaimed; see LOG.md
  (Publication evidence correction) and REPRODUCE_v2.md.
- **1233 v2 cases unrecovered** under allowed materials (opaque schedules,
  C-bearing WLN1, larger/nested placement, WNM/WNC/WVC leftovers).
- Analysis was **source-informed** (public challenge folder + SOURCE-pinned
  public code). It is not a blind level-0 attempt as defined in the v2 README.

## What held / what did not

- Literal N/U containers expose message bytes without needing corpus bytes for
  extraction; some hashes and padding checks validate rather than recover.
- Circle order can appear on the wire; modest WRA1 spaces remain searchable;
  small S catalogs and C-free transports are enumerable.
- Failed C/WLN1 attacks produced non-unique preimages without `corpus_hex`.
  That is **not** a proof of cryptographic security.
- v1 weaknesses around literal payloads were not eliminated by v2 packaging.

## Contents and exclusions

LOG.md is an append-only attempt log (including superseded claims and later
corrections). REPRODUCE.md (v1) and REPRODUCE_v2.md (v2) document methods,
limits, and reproducibility gaps. `work/*.py` includes recovery programs and
failed/exploratory attacks, unmodified. `work/*.recovered` holds the eight v1
outputs. `PUBLICATION_DIARY.md` is labelled for website publication and is
written last each session.

Published here: result artifacts only. **Not** included: challenge ciphertext
copies, blind-pack.zip, downloaded source trees, manifests as challenge
inputs, private corpora/profiles, originals, operator/evaluator bundle,
`crypto-testing-draft` / skill drafts, or anything from `/workspace/cy`.

## Reproduction / path notes

Archival scripts, not a self-contained installer. Many paths are absolute under
`/workspace/cypher`:

- this folder's `work/` corresponds to `/workspace/cypher/work/`;
- obtain authorized v1 inputs separately under `/workspace/cypher/v1/`;
- obtain the v2 blind pack separately under `/workspace/cypher/v2/blind/files/`;
- obtain only authorized pinned public source under `/workspace/cypher/src/`
  (pins in REPRODUCE.md: stack `9de81c67…`, ucns `905e6696…`).

```sh
cd /workspace/cypher/work
python3 recoverA.py
python3 recoverBall.py
sha256sum *.recovered
python3 crack_v2b.py
python3 crack_v2_S.py
python3 crack_v2_transport.py
python3 crack_v2_N1S.py
python3 crack_v2_Asmall.py
python3 crack_v2_NA_fast.py
python3 crack_v2_opaque_fast.py
python3 crack_v2_A_parallel.py
```

Some historical LOG/REPRODUCE snippets are illustrative; some nested steps were
inline and are not standalone scripts. Do not treat the command list as a fully
automated rebuild of every reported candidate. Inspect the published outputs and
IDs directly.
