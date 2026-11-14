# English construction qualification

Scope: the English density renderer and its complete source-replay protocol.
Python construction has a separate dependent PR and qualification instrument.

The renderer now reads scalar, position, count and fraction values from each
letter record. The measured density JSON stays unchanged; its Markdown projection
is regenerated from those values. The regression checks concrete measured rows.

English CI uses hash-locked dependencies and rejects empty, skipped, failed or
errored JUnit evidence. Run the tests from `research/english-gonol`:

```bash
python -m pytest -q tests ../../tools/tests/test_english_qualification.py --junitxml=/tmp/english-tests.xml
python ../../tools/qualify_english_gonols.py check-tests /tmp/english-tests.xml
```

To qualify two complete constructions, build them in separate processes and new
directories using `english_gonol.full_construct_run`, then run:

```bash
python tools/qualify_english_gonols.py compare FIRST SECOND
```

Comparison rejects aliased artifacts, invokes complete replay on each, checks
SQLite integrity and counts, and binds the existing frozen complete manifest.
Matching artifact contents alone do not authenticate independent execution.

The frozen [English evidence](evidence/english-gonol-20260919/summary.json)
projects the English records from the original 2026-09-19 qualification.
Its two evidence files retain their original bytes and hashes. The recorded
85 tests and two independent complete builds apply to that implementation:
164,864 words, 185,155 definitions and 3,535,375 definition components.
Those receipts do not certify later runtime changes.

The source corpus is OEWN at `dc343f2683279ecbb13fab4e2fd778d7b162d287`;
the historical construction carrier is UCNS at
`4f863ad37096b7baab8f62820ad5cb937b62a3a7`.

hmmm: active scalar-geometry migration, semantic utility and independent UCHC
release standing remain separate from this rendering and replay repair.
