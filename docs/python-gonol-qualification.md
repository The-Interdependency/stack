# Python construction qualification

Scope: Python source construction and replay. The separate English dependency
PR owns density rendering, English CI and English evidence.

Schema 3 assigns a native UCNS identity to every decoded Unicode scalar.
It retains the exact UTF-32BE diameter, UTF-8 spelling, SPACE-relative bearing
and optional Public Gonol position. It preserves original source bytes, physical CR/LF/CRLF
addresses, and Python tab expansion. Form-feed consumes one expanded column;
it does not reset the tab stop. Replay binds SQLite schema objects, every
constitutive row and provenance field, and reconstructs from the retained bytes.

Comparison requires two distinct artifact directories with matching contents,
exact source/runtime/implementation provenance and the frozen complete CPython
inventory: **1,052 files, 20,732,440 bytes**, canonical inventory digest
`1dd99a2c8e27e10c669dfd46a29b2e0107da15279f18aac94eb5453052bb41e1`.
Each constructed manifest must bind its schema/version, producer, source,
counts and receipt. Exactly three pinned sources fail encoding admission:

- `Lib/test/tokenizedata/bad_coding.py`
- `Lib/test/tokenizedata/bad_coding2.py`
- `Lib/test/tokenizedata/badsyntax_pep3120.py`

Their exact byte hashes and `SyntaxError` outcomes are frozen in the comparator.
A fresh raw-byte retrieval at the pinned commit reproduced all three failures.
Every other input requires a complete constructed manifest. Relabeling valid
inputs as rejected, including an all-rejected corpus, fails even after rebinding
the outer digests and counts. Artifact agreement alone cannot authenticate
independent process executions.

## Reproduction

Use Python 3.12.14 and `pip install --require-hashes -r requirements-language-tests.txt`.
Set `UCNS_SOURCE_ROOT` to UCNS `ee8addc0af36f02b64b42cb355734cb72a126ea5`.
From `research/python-gonol`:

```bash
python -m pytest -q tests ../../tools/tests/test_python_qualification.py --junitxml=/tmp/python-tests.xml
python ../../tools/qualify_python_gonols.py check-tests /tmp/python-tests.xml
```

From Stack's root, run `python-pass` twice in separate processes and new output
directories, then compare. Install the [hash-locked wheel](../integration/uchc/python-requirements.txt)
in the second interpreter. CPython must be at
`2abcf904b8dac8c999d2b3aac76681abb333798a` (the observed v3.12.14 tag target).

```bash
python -I tools/qualify_python_gonols.py python-pass CPYTHON UCNS FIRST
/path/to/clean-wheel-venv/bin/python -I tools/qualify_python_gonols.py python-pass --installed CPYTHON UCNS SECOND
python tools/qualify_python_gonols.py compare FIRST SECOND
```

The runner inventories the complete tracked `Lib/test` Python tree, verifies
every eligible file, records explicit rejected inputs, and checks unchanged
sources and implementation after execution. Temporary constructs are removed
after each file. Corpus code is never executed. Preflight free storage against
the largest input and allow the declared scope to finish without arbitrary cuts.

## Full schema 3 qualification

The [comparison](evidence/python-gonol-unicode-v3/comparison.json) binds the Stack
constructor, installed UCHC 0.2.0a4 wheel and native UCNS producer. Two independent
processes produced identical inventories, per-file outcomes and receipts. Each
constructed 1,049 files and verified all **20,728,462** scalar occurrences against
their source and glyph identities. The three pinned encoding fixtures were
rejected before construction. Six files retained a negative AST witness.

The [per-file manifests](evidence/python-gonol-unicode-v3/outcomes.jsonl.gz) and
[receipt](evidence/python-gonol-unicode-v3/receipt.json) preserve the result. The
inventory is byte-identical to the archived inventory. The regression test also
constructs all 290 distinct scalars that the historical Public Gonol lookup
flagged in 113 files. Each has a native Unicode identity. The former flag
describes coverage of the optional 157-position projection.

## Earlier evidence

The [Python evidence projection](evidence/python-gonol-20260919/summary.json)
retains the original 2026-09-19 file bytes and hashes: two complete independent
passes, 1,049 constructs and three encoding rejections; 113 files retain
off-carrier scalars and six have negative AST witnesses. Those receipts certify
their frozen implementation, not this repair. Historical schema 1.x artifacts
require explicit rebuilding under schema 2.0.0.

The first historical attempt failed after 671 files with SQLite's
`attempt to write a readonly database`; its recorded prefix matched subsequent
completed passes. Later 2026-09-23 attempts also encountered this error.
The failed attempts remain evidence and do not count as completed qualification.

The cause of the earlier SQLite failure remains unresolved. Both schema 3 runs
completed. Python grammar relations and runtime equivalence need separate evidence.
