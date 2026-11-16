# English Unicode corpus

The Stack English entry point constructs words from their ordered source glyphs using the UCNS Unicode constructor. The corpus retains all 103,053 admitted words, 4,698 observed or property-selected glyphs, 185,155 OEWN definitions and 4,757 inherited character-definition relations. Each glyph has a 16-bit radius, a four-byte big-endian diameter, a separate UTF-8 view and its SPACE-relative scalar bearing. Primitive occurrences share geometric radius one.

The artifact contains the complete source admission, authenticated Unicode 18.0.0 repertoire inputs, a compact database of Unicode glyphs, word receipts and inherited relations, and a manifest. The source database retains exact ordered word interiors, all higher record occurrences, lexical ownership, previous-definition links, offsets, functions, provenance and original YAML bytes. Verification checks the pinned manifest, schema and complete logical content of the opened source snapshot. It reconstructs every word from its ordered glyph rows and compares every derived row. The [complete replay](../experiments/unicode-corpus/replay.json) also checks every word placement and instantiates all inherited definitions with documented example bearings. Full Unicode scalar admission remains available through `text`. The corpus query addresses the pinned vocabulary.

From the repository root use Python 3.12.14, `requirements-language-tests.txt`, and the source commits and UCD files in the [work graph](unicode-corpus-work-graph.json). Set `PYTHONPATH=research/english-gonol` and `UCHC_UNICODE_UCNS_ROOT` to the native Unicode checkout. Given a verified structural admission and a directory containing the pinned UCD files:

```bash
python -m english_gonol profile
python -m english_gonol text 'Aë𐍈' --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python -m english_gonol build ADMISSION UCD NEW_OUTPUT --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python -m english_gonol verify NEW_OUTPUT --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python -m english_gonol query NEW_OUTPUT 'the geometry' --bearing 0 --bearing 1/2 --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python -m english_gonol definition NEW_OUTPUT 3 1 --bearing 0 --bearing 1/2 --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python -m english_gonol record NEW_OUTPUT 150508 --bearing 0 --bearing 1/4 --bearing 1/2 --bearing 3/4 --ucns-source-root "$UCHC_UNICODE_UCNS_ROOT"
python research/english-gonol/tools/verify_unicode_corpus.py NEW_OUTPUT "$UCHC_UNICODE_UCNS_ROOT" --expect research/english-gonol/experiments/unicode-corpus/replay.json
```

The record example reconstructs “sung without instrumental accompaniment,” a definition of the entire lexical entry “a cappella.” Its word interiors retain their source IDs. The character-definition example reuses the corpus word “three” as the number-name interior of “3.” The caller supplies an exact turn for each closed child, in occurrence order. Punctuation and whitespace glyphs carry their own scalar bearings. Omitting a required bearing refuses closure. The returned graph supports native recursive re-entry.

The [earlier ordinal corpus experiment](https://github.com/The-Interdependency/stack/tree/30e081a5f0e624d4be45161d96fcc09c37c9edb6/research/english-gonol) preserves its implementation, repaired verification, source identities, operator answers and historical witness at that revision. Its balanced repertoire layout, radius-halving and lexicographic word bearings belong to that earlier profile. Prior receipts retain their original producer and geometry. For historical reproduction use a separate checkout of that revision and its documented dependencies.

**hmmm**. Automatic next-scale bearings, semantic selection and independent English release remain open. Higher corpus records carry their constituents and relations until a caller supplies geometry for their closed children. The complete workflow retains both the artifact and the verification records.
