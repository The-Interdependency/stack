# Python Gonol Construction

Stack-local research implementation for affixiating Python source into gonols
from its lowest admitted units upward.

## Construction

```text
exact decoded source occurrences
    -> letter gonols
    -> Python lexical-form gonols
    -> matched delimiter gonols
    -> recursive Python grammar-construction gonols
    -> module gonol
```

Every source occurrence remains independently addressable.  Every larger gonol
contains an identity-bearing relation whose ordered, role-bearing members refer
only to already-closed gonols.  A parent consumes a child's atomic identity; the
receipt registry keeps the complete child recoverable.

`letter` is the name of the source-floor construction, not a Unicode alphabetic
classification.  Python program text is read as Unicode code points, so spaces,
newlines, digits, operators, and delimiters each begin as their own letter gonol
occurrence too.  Nothing is normalized, deduplicated, trimmed, or silently
discarded.

## Authority boundary

```text
METAPAT                         affixiation semantics
    -> UCNS                     geometry and Public Gonol positions
        -> Python Gonol         Python source admission and construction
            -> later consumers no authority transfer
```

This workspace uses CPython 3.12 `tokenize` and `ast` only as recognition
witnesses after the letter floor has closed.  Token, AST, compiler, and code
objects never become gonols and never replace the source-built relation graph.
The source bytes, every decoded occurrence, every closed construction, and all
constitutive relations remain visible in the receipt.

Standing: **implemented stack-local candidate; not canon and not an independent
release**.

## Usage guidance

Run from this directory with Python 3.12:

```bash
python -m python_gonol path/to/source.py --out source.gonol.json --pretty
python -m python_gonol --verify source.gonol.json
python -m pytest -q tests
```

Use the bytes entrypoint for files so an encoding declaration and the exact
original bytes remain bound:

```python
from pathlib import Path
from python_gonol import affixiate_python_bytes, replay_python_affixiation

path = Path("example.py")
receipt = affixiate_python_bytes(path.read_bytes(), source_id=path.as_posix())
replay_python_affixiation(receipt)
```

For invalid or unfinished source, the constructor retains all admitted lower
closures, closes a `python.source.hmmm` root, records the exact tokenizer,
delimiter, or grammar boundary, and the CLI exits `2`.  This makes a missing end
parenthesis visible without throwing away the construction completed beneath it.

See [`docs/PYTHON_AFFIXIATION_BOUNDARY.md`](docs/PYTHON_AFFIXIATION_BOUNDARY.md)
for the full contract and [`WORK_GRAPH.json`](WORK_GRAPH.json) for exact inputs.

## hmmm

- exact UCNS geometric operation of Public Gonol function positions;
- exact UCNS Möbius-carrier affixiation/coupling law;
- Python language profiles after Python 3.12 file input;
- streaming/checkpointed receipt materialization for unusually large source
  trees.
