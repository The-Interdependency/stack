# Python Gonol Construction

Stack-local research implementation that affixiates Python 3.12 source into
gonols using the exact construction method used by English Gonol.

## Construction

```text
exact decoded source occurrences
    -> one shared identity per pinned Public Gonol glyph
    -> ordered occurrence references (address, line, column, provenance)
    -> control constructions: TAB, LF, FF, CR
    -> logical newlines: LF, CR, CR+LF
```

Every source occurrence remains independently addressable. Every admitted
glyph has one shared character identity; occurrences reference it in exact
order and multiplicity. Tokens and AST nodes verify construction; they never
substitute for it.

## Carrier boundary

UCNS owns geometry and the exact 157-position Public Gonol carrier. This
builder consumes the pinned carrier (`ucns@62e08ee`) and its digest; it never
copies, extends, or reinterprets it. The four control scalars
(`U+0009`, `U+000A`, `U+000C`, `U+000D`) are constructed from the carrier
glyphs of their Unicode names and code points:

```text
CHARACTER TABULATION + U+0009 -> TAB
LINE FEED          + U+000A -> LF
FORM FEED          + U+000C -> FF
CARRIAGE RETURN    + U+000D -> CR
```

Names and code points are constitutive participants, not metadata. TAB
affixiates with enough SPACE gonols to reach the next eight-column stop. CR,
LF, and CR+LF construct logical newlines while preserving their exact source
constituents and remaining source-distinct. Any other off-carrier source
scalar is recorded as hmmm with its exact address, never assigned an invented
position.

## Artifacts

One compact SQLite construct plus a small manifest:

```text
construct.db   characters, occurrences, control_identities, controls, newlines, source_bytes, meta
manifest.json  schema, source digests, counts, carrier pin, receipt_sha256, hmmm
```

No giant JSON receipt.

## Usage

```bash
python -m python_gonol source.py --out-dir construct --ucns-source-root ~/src/ucns
python -m python_gonol --verify construct --ucns-source-root ~/src/ucns
python -m pytest -q tests
```

Python API:

```python
from pathlib import Path
from python_gonol import affixiate_python_bytes, verify_construct

result = affixiate_python_bytes(
    Path("example.py").read_bytes(),
    source_id="example.py",
    ucns_source_root="/home/wayseer_interdependentway_org/src/ucns",
    state_dir=Path("construct"),
)
verify_construct(Path("construct"), "/home/wayseer_interdependentway_org/src/ucns")
```

## Acceptance gates

Version 2.0.0 corrects tab expansion and CR-only physical addresses. Rebuild
1.x constructs from their original sources; replay rejects the old version.
Occurrence columns and `controls.start_column` are one-based source-scalar
addresses. TAB widths use a separate zero-based expanded column, advancing
through earlier tabs. LF, CR, and CRLF reset that expanded column; FF resets
the indentation column. Version 2 also preserves original source bytes in the
database and binds every row in a logical digest. Replay reconstructs the
complete database in an isolated temporary directory and compares the entire
manifest and logical digest. CRLF retains both source scalars on the preceding
physical line and advances the next scalar to line + 1, column 1.

- `x=1\n` produces no not-on-pinned-carrier.
- LF replays as exact `U+000A`.
- TAB preserves `U+0009` and expands correctly at every starting column.
- LF, CR, and CR+LF remain source-distinct.
- Tampering with identity, relation, order, or provenance fails replay.
- The declared corpus completes within preflighted storage limits.

## hmmm

- deeper geometric functions of Public Gonol positions remain unresolved;
- admission of arbitrary Unicode source characters remains unresolved and is
  preserved without invention.
