# Cypher recovery results — Weave v1/v2

Snapshot of local cryptanalysis artifacts, published 2026-11-07.

## Results

- **v1: 8/8 byte-exact recoveries.** Each recovered message was checked against
  the message-origin root in its WVC header; digests are in REPRODUCE.md.
- **v2: 554/1841 reported byte-exact recoveries**, retained in
  `work/v2_recovered/` with RECOVERED_IDS.txt and SUMMARY.json. Each contains
  a per-case Prediction line followed by `my human needs my help`.
  No private evaluator/answer archive was used; the v2 acceptance filter is
  described in REPRODUCE_v2.md. This publication does not independently rerun
  or strengthen that validation.
- Literal N/U payload containers do not require corpus bytes for extraction;
  some hashes and corpus-padding checks validate rather than recover bytes.
  Circle order leaks on wire; v1 group-B spaces were recovered by geometry
  and exact-cover search. Small schedule catalogs and C-free transports are
  enumerable.
- **1287 v2 cases remain unrecovered.** Attempts on C-bearing WLN1 gave
  nonunique preimages, not recoveries; larger/nested placement and opaque
  schedules also remain unresolved. No general claim of cryptographic
  security follows from failed attacks.

## Contents and scope

LOG.md preserves the historical attempt log, including superseded guesses
and corrections. REPRODUCE.md covers v1; REPRODUCE_v2.md covers v2 and limits.
`work/*.py` includes successful recovery programs and exploratory/failed
attacks, unmodified. `work/*.recovered` contains the eight v1 outputs.

Only result artifacts are added here: no challenge ciphertext copies, blind
pack, downloaded source, manifests, private corpora/profiles, originals,
operator/evaluator bundle, or material from `/workspace/cy`.
The analysis was source-informed, not a blind level-0 attempt.

## Reproduction / paths

These are archival scripts, not a self-contained installer. They assume the
original layout under `/workspace/cypher` (some paths are absolute):

- this folder's `work/` -> `/workspace/cypher/work/`;
- obtain the authorized v1 challenge inputs separately under
  `/workspace/cypher/v1/` (ciphertexts in `v1/ciphertexts/`);
- obtain the v2 blind pack separately and extract its files under
  `/workspace/cypher/v2/blind/files/`;
- obtain only authorized pinned public source separately under
  `/workspace/cypher/src/`, including `sources/`, public `profiles/`, and
  `ucns/` as described in REPRODUCE.md. Pins: stack
  `9de81c67b271df09c1d9ba5422660c96fe8af7ac`, ucns
  `905e66964a495d7596a577bb64e4158db9465864`.

Use Python 3, with dependencies required by the pinned source (optional
experimental scripts may require additional packages such as z3). Review
scripts before running; use a separate scratch layout if preserving outputs.

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
```

See both reproduction documents for details and parameter findings. Some
historical proof snippets are illustrative placeholders, and the v2 notes
mention an inline nested-U step not supplied as a standalone command; thus
the archived commands should not be mistaken for a fully automated rebuild
of every reported result. The recovered outputs and IDs are included so
another investigator can inspect and verify the exact published snapshot.
