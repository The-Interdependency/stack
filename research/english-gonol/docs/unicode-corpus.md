# English Unicode corpus

The Stack English entry point constructs words from their ordered source glyphs using the UCNS Unicode constructor. The corpus retains all 103,053 admitted words, 4,698 observed or property-selected glyphs, 185,155 OEWN definitions and 4,757 inherited character-definition relations. Each glyph has a 16-bit radius, a four-byte big-endian diameter, a separate UTF-8 view and its SPACE-relative scalar bearing. Primitive occurrences share geometric radius one.

The artifact contains the complete source admission, authenticated Unicode 18.0.0 repertoire inputs, a compact database of Unicode glyphs, word receipts and inherited relations, and a manifest. The source database retains exact ordered word interiors, all higher record occurrences, lexical ownership, previous-definition links, offsets, functions, provenance and original YAML bytes. Verification checks the pinned manifest, schema and complete logical content of the opened source snapshot. It reconstructs every word from its ordered glyph rows and compares every derived row. The [complete replay](../experiments/unicode-corpus/replay.json) also checks every word placement and instantiates all inherited definitions through automatic addition as well as historical declared placements. Full Unicode scalar admission remains available through `text`. The corpus query addresses the pinned vocabulary.

From the repository root use Python 3.12.14, `requirements-language-tests.txt`, and the source commits and UCD files in the [work graph](unicode-corpus-work-graph.json). Set `PYTHONPATH=research/english-gonol` and `UCHC_UNICODE_UCNS_ROOT` to the native Unicode checkout. Given a verified structural admission and a directory containing the pinned UCD files:

```bash
python -m english_gonol profile
python -m english_gonol text 'Aë𐍈' --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python -m english_gonol build ADMISSION UCD NEW_OUTPUT --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python -m english_gonol verify NEW_OUTPUT --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python -m english_gonol query NEW_OUTPUT 'the geometry' --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python -m english_gonol definition NEW_OUTPUT 3 1 --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python -m english_gonol record NEW_OUTPUT 150508 --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python research/english-gonol/tools/verify_unicode_corpus.py NEW_OUTPUT "$UCHC_UNICODE_UCNS_ROOT" --expect research/english-gonol/experiments/unicode-corpus/replay.json
```

The record example reconstructs “sung without instrumental accompaniment,” a definition of the entire lexical entry “a cappella.” Its word interiors retain their source IDs. The character-definition example reuses the corpus word “three” as the number-name interior of “3.” The default operation adds the complete geometric results of all retained children. Punctuation and whitespace retain their scalar bearings and occurrences. No new bearing is required. Optional `--bearing` arguments select the historical declared-placement operation. The returned sum supports native recursive re-entry.

The [earlier ordinal corpus experiment](https://github.com/The-Interdependency/stack/tree/30e081a5f0e624d4be45161d96fcc09c37c9edb6/research/english-gonol) preserves its implementation, repaired verification, source identities, operator answers and historical witness at that revision. Its balanced repertoire layout, radius-halving and lexicographic word bearings belong to that earlier profile. Prior receipts retain their original producer and geometry. For historical reproduction use a separate checkout of that revision and its documented dependencies.

The current profile is `uchc.english-unicode-corpus/2`. The prior replay witness is preserved as `experiments/unicode-corpus/replay-0bbed0b.json`; its counts, primitive geometry rows and declared-placement closure digests remain unchanged. The new witness adds independent complete automatic-definition and compound-ownership checks.

**hmmm**. Physical sheet lift, semantic selection and independent English release remain separate. The complete workflow retains the artifact and verification records.
