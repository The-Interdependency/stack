# Python construction qualification

Scope: Python source construction and replay. The separate English dependency
PR owns density rendering, English CI and English evidence.

The repaired constructor preserves original source bytes, physical CR/LF/CRLF
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
Set `UCNS_SOURCE_ROOT` to UCNS `62e08ee1cf3b5d7b6e48c927b1047509e6328b5c`.
From `research/python-gonol`:

```bash
python -m pytest -q tests ../../tools/tests/test_python_qualification.py --junitxml=/tmp/python-tests.xml
python ../../tools/qualify_python_gonols.py check-tests /tmp/python-tests.xml
```

From Stack's root, run `python-pass` twice in separate processes and new output
directories, then compare. CPython must be at
`2abcf904b8dac8c999d2b3aac76681abb333798a` (the observed v3.12.14 tag target).

```bash
python tools/qualify_python_gonols.py python-pass CPYTHON UCNS FIRST
python tools/qualify_python_gonols.py python-pass CPYTHON UCNS SECOND
python tools/qualify_python_gonols.py compare FIRST SECOND
```

The runner inventories the complete tracked `Lib/test` Python tree, verifies
every eligible file, records explicit rejected inputs, and checks unchanged
sources and implementation after execution. Temporary constructs are removed
after each file. Corpus code is never executed. Preflight free storage against
the largest input and allow the declared scope to finish without arbitrary cuts.

## Historical evidence and current boundary

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

All **83 current Python construction and qualification tests pass**, without
skips. Complete CPython requalification of the repaired implementation remains
pending. hmmm: the SQLite failure cause, active scalar-geometry migration,
off-carrier admission, grammar/runtime equivalence and independent release.
