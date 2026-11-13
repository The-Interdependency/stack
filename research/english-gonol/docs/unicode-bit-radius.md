# UCHC gonols: 16 b rad, big-endian

Research area: **UCHC**, priority 2 after UCNS. Stack owns this language entrypoint;
UCNS owns the returned gonol objects, bearing and representation. The shared
[work graph](unicode-bit-radius-work-graph.json) fixes the participating sources.

## Operator decision

Erin Spencer set UCHC gonol bit radius to 16 on 2026-11-13 and specified
big-endian storage: ASCII receives three leading zero bytes.

`uchc.gonol.bit_radius` names the encoding width of one radial half: **16 bits**.
The complete diameter is **32 bits**, stored as **four big-endian bytes**.
This is the operator-selected representation policy implemented by UCNS's
`unicode_gonol` version 2. The neighboring geometric placement `radius` remains
an independent exact quantity.

| Scalar | Big-endian diameter | Original UTF-8 anatomy |
|---|---|---|
| NUL | `00 00 00 00` | `00` |
| A | `00 00 00 41` | `41` |
| ë | `00 00 00 EB` | `C3 AB` |
| 𐍈 | `00 01 03 48` | `F0 90 8D 88` |

The diameter encodes the scalar value as UTF-32BE without an inserted BOM.
Source U+FEFF and NUL remain ordinary retained scalars. No normalization or
trimming occurs. A text sequence contains one complete diameter per scalar;
the 32-bit width is not a total capacity limit on a word, sentence or document.
Precomposed and decomposed sequences, repeated scalars and source order remain
distinct. Neither a closed word's bearing nor affixiation is derived from this
encoding choice.

## Run

Check out the exact UCNS commit in the work graph. From `research/english-gonol`:

```sh
python -m english_gonol.unicode_construction 'Aë𐍈' --ucns-source-root /path/to/ucns
UCHC_UNICODE_UCNS_ROOT=/path/to/ucns python -m pytest -q unicode_tests
```

The runtime verifies the native module's SHA-256 before executing those same
bytes. It imports no ambient UCNS package and contains no replacement geometry.
The CLI emits the exact producer identity and native frame receipt.

The four scoped source identities also appear in the root `stack-manifest.json`
and `STACK_MANIFEST.md`. Run `python tools/check_stack_consistency.py` from the
repository root to verify their exact identities, authority and relations. This
gate rejects missing or divergent projections while preserving historical pins;
the Unicode tests exercise those rejection paths.

```python
from english_gonol.unicode_construction import construct_glyph, encode_text, decode_text

root = "/path/to/ucns"
glyph = construct_glyph("A", ucns_source_root=root)
assert (glyph.bit_radius, glyph.bit_diameter) == (16, 32)
assert glyph.utf32_be == bytes.fromhex("00000041")
data = encode_text("Aë𐍈", ucns_source_root=root)
assert decode_text(data, ucns_source_root=root) == "Aë𐍈"
```

Invalid diameters, surrogate values and source drift are errors. Exact source
identity is reproducibility evidence, not producer authentication. No semantic,
proof, certification or measurement standing transfers between repositories.

## hmmm

This completes primitive scalar width and transport. The ongoing corpus
replacement in Stack #88, higher-scale affixiation/bearing, and extraction of
this entrypoint into the UCHC distribution remain separate work. Historical
corpus, ordinal and attachment receipts keep their pinned producers and cannot
be relabeled as this Unicode representation. Roll back the entrypoint and its
source pin together; no stored historical receipt is rewritten.
