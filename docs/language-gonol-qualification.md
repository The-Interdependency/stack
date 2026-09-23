# Language construction qualification

Status: the recorded 2026-09-19 qualification applies to its frozen implementation.
The 2026-09-23 repair additionally binds SQLite schema objects, declared JUnit
aggregates, exact qualification provenance and counts, and distinct artifact paths.
Its complete Python-corpus requalification is pending; local adversarial gates pass.
Artifact agreement alone does not authenticate two independent executions.
Geometry, language understanding, runtime equivalence, and canon promotion remain hmmm.

## Observed results

| Check | Observed outcome |
| --- | --- |
| English tests | 85 passed; zero skipped, failed or errored |
| Python and qualification-gate tests | 47 passed (42 construction, 5 gate); zero skipped, failed or errored |
| English full builds | Two independent process builds reproduce the existing manifest and logical receipt |
| English inventory | 164,864 words; 185,155 definitions; 3,535,375 definition components; 866,183 semantic evidence rows |
| Python full passes | Two complete independent process passes; inventory, outcomes and receipts are byte-identical |
| Python inventory | All 1,052 tracked files; 20,732,440 source bytes; 1,049 constructed and replayed, 3 explicitly rejected for encoding |
| Python retained boundaries | 113 files have off-carrier scalars; 6 have negative AST witnesses; no tokenizer witness failures |
| Stack consistency and ratios | Structural check passed; all 36 ratios across six changed Python files verified |

The [result receipt](evidence/language-gonol-20260919/summary.json) indexes every
evidence file and digest. The [English proof](evidence/language-gonol-20260919/english-replay.json)
contains the complete original manifest. The [Python proof](evidence/language-gonol-20260919/python-replay.json)
binds the exact implementation, source inventory and per-file outcomes.
The identical full Python [inventory](evidence/language-gonol-20260919/python-inventory.json.gz)
and [outcomes](evidence/language-gonol-20260919/python-outcomes.jsonl.gz) are retained
once, using deterministic gzip; decompress before inspecting the JSON/JSONL.
The [English test outcomes](evidence/language-gonol-20260919/english-tests.xml) and
[Python test outcomes](evidence/language-gonol-20260919/python-tests.xml) preserve
individual test cases.

English logical receipt:
`12277b4959c0c72b7af12097b8a77bf91866bbf669e7f4ac07b6a5f1426ebb57`.
Python complete outcome SHA-256:
`5a38fb2ff50c0ab0cae636a5d8e57110506e263a775f0c17b7b56baa0c6e4bf1`.

## Frozen scope and evidence

- Stack starting source: `bcaba85900716e5209150a504660fa2ca5158299`.
- Minimum repair: `8c84d3dc9e05ef0a4373f215da1bcf20801ed663`
  (tabs, physical source addresses, density rendering).
- Qualification implementation: `64698061fb0ff0b92ccc4dfdc8538680fccbbfd2`.
  Python receipts additionally bind each implementation file by SHA-256.
- Operational doctrine: `The-Interdependency/skill-lib@dd5027d99516831c0dcb83a176a67140d3819b66`.
  This exact invocation does not refresh Stack's vendored snapshot or transfer authority.
- English: every file admitted by the existing OEWN 2025 loader, from
  `globalwordnet/english-wordnet@dc343f2683279ecbb13fab4e2fd778d7b162d287`.
- English UCNS authority: `4f863ad37096b7baab8f62820ad5cb937b62a3a7`.
- Historical lexical test authority: `d7c6f51304ed6c32d48badf63132bea6de8af497`.
- Python UCNS authority: `62e08ee1cf3b5d7b6e48c927b1047509e6328b5c`.
- Python corpus: every tracked `.py` file beneath CPython `Lib/test/` at the
  `v3.12.14` commit `2abcf904b8dac8c999d2b3aac76681abb333798a`. Exact source inventory is frozen before the run.
  Files that violate the existing encoding admission rule remain explicit
  rejection evidence with original byte hashes. Invalid syntax and off-carrier
  Unicode remain represented, with their existing witness flags and hmmm.

## Acceptance

1. Run every existing English and Python workspace test with exact dependencies;
   require actual call outcomes, zero skips, zero failures, and nonempty suites.
2. Rebuild all admitted English input twice in separate processes and empty
   output directories. Verify SQLite integrity, logical replay, complete counts,
   unchanged source inventories, and identical logical receipts/manifests.
3. Enumerate the complete Python corpus before construction. Each eligible file
   must have two independent process builds, exact source recovery, replay,
   matching canonical database content and manifest, and an explicit outcome.
4. Check tab widths and physical addresses against independent source-based
   witnesses. Verify provenance and constitutive control data, and reject
   targeted changes to identity, order, source, relation and receipt fields.
5. Generated databases remain local execution state. Commit compact provenance,
   outcome and digest receipts; do not substitute a sample for the declared scope.

## Resource preflight and stopping

Observed available resources before execution: 26 GiB free disk, 21.5 GiB RAM,
Python 3.12.14. The recorded English run needs about 293 MiB output and 280 MiB
RSS; two serial builds fit. Python file pairs are verified and removed one pair
at a time, keeping compact per-file evidence. Preflight the largest input and
storage estimate before starting. These are local persistent processes; no
arbitrary scientific wall-clock cutoff is imposed. Stop on completion or a
recorded computational/admission failure; retain failures and all hmmm.

## Reproduction

Run the workspace tests from their own directories. Supply
`ENGLISH_GONOL_UCNS_ROOT` for the exact historical lexical producer and
`UCNS_SOURCE_ROOT` for the Python producer. Use Python 3.12.14 and install
`requirements-language-tests.txt` with `pip install --require-hashes`.

```bash
# From research/english-gonol, with ENGLISH_GONOL_UCNS_ROOT set:
python -m pytest -q tests --junitxml=/tmp/english-gonol.xml

# From research/python-gonol, with UCNS_SOURCE_ROOT set:
python -m pytest -q tests ../../tools/tests/test_language_qualification.py --junitxml=/tmp/python-gonol.xml

# From the Stack root, after both suites:
python tools/qualify_language_gonols.py check-tests /tmp/english-gonol.xml /tmp/python-gonol.xml
python tools/check_stack_consistency.py
```

Build the English corpus twice with the existing
`english_gonol.full_construct_run` CLI, separate empty output directories,
the frozen OEWN `src/yaml` directory, and the English UCNS checkout above.
Then run `python tools/qualify_language_gonols.py english-compare <first> <second>`.

Run `python tools/qualify_language_gonols.py python-pass <cpython-checkout>
<python-ucns-checkout> <new-output-directory>` in two separate processes,
each with a distinct new output directory. The runner inventories all tracked
Python files, checks original bytes, physical addresses and tab expansion,
and rebuilds every admitted construct for complete logical comparison.
It checks unchanged input and implementation hashes again before accepting.
Then run `python tools/qualify_language_gonols.py compare <first> <second>`.

Corpus code is parsed as witness data; it is never executed. Invalid encodings
must agree with an independent encoding-admission check and appear as explicit
rejections. Invalid syntax and off-carrier characters are retained.

Passing this protocol qualifies its explicit construction profiles only.
UCNS retains geometry authority; Stack retains active construction ownership;
EDCM retains measurement authority. Independent repository graduation is outside
this qualification.

## CPython provenance correction

The former `2d7d957248038635334b62b27f650220213d8e5d` pin cannot be fetched
from the declared upstream (`not our ref`). The annotated `v3.12.14` tag
`4b65faa0b452113bf130086fb1519be6d9cd9b06` resolves to
`2abcf904b8dac8c999d2b3aac76681abb333798a`. BASE and the Python work graph
now use that observed source identity; the graph digest is recomputed.
No language profile or geometry authority changes. The root Stack manifest
contains no CPython pin and its authority projection remains applicable.

## Repair behavior

The minimum repair separates one-based raw source columns from expanded tab
columns, treats CR, LF and CRLF as physical newline sequences, and renders
density values instead of dictionary keys. The density JSON is unchanged.

Python construction now preserves exact source bytes, including BOM and declared
encodings, and binds every constitutive SQLite row and provenance field.
Verification opens the supplied database read-only, checks its integrity and
complete content digest, and reconstructs the full artifact from the preserved
bytes with the exact authority producer. Targeted changes to carrier positions,
control membership, occurrence roles, source provenance and truncated inventories
are rejected, including attempts that recompute the outer digests.

Python construct version 2.0.0 requires rebuilding 1.x artifacts from original
source. Replay requires temporary storage for a complete second construct.
The exact-dependency CI jobs reject skipped, empty, failed or errored test evidence.

## Recorded unsuccessful attempt

The first Python corpus attempt stopped after 671 completed files while verifying
`Lib/test/test_logging.py`: SQLite reported `attempt to write a readonly database`
during `PRAGMA integrity_check`. Its completed outcomes exactly match the first
671 outcomes of the successful complete pass. The same file passed three isolated
build/integrity/replay probes with identical receipts. No implementation or
verification rule changed for the replacement full run.

The underlying database error remains hmmm. The [failure record](evidence/language-gonol-20260919/python-attempt-a.json)
and [original log](evidence/language-gonol-20260919/python-attempt-a.log) are retained;
the unsuccessful attempt is not counted as a completed qualification pass.

## 2026-09-23 repair and runtime boundary

The construct digest now includes all SQLite schema objects, including constraints,
indexes, triggers and views. Rebinding a tampered digest still fails independent
reconstruction. Comparison rejects aliased directories/files and validates the
schema, source pins, implementation identities, runtime and recomputed aggregates.
JUnit totals must agree with the observed cases and failure/skip evidence.

Complete local attempts with the bundled SQLite 3.53.1 stopped with
`attempt to write a readonly database`; these attempts are failed evidence,
not partial qualification. Explicit connection closure and memory-backed SQLite
temporary work did not eliminate the observed failure. SQLite runtime identity
is now part of qualification receipts. The causal mechanism remains hmmm.
