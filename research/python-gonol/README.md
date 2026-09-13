# Python Gonol Construction

Stack-local research implementation for affixiating Python source into gonols from its lowest admitted source units upward.

## Construction

```text
exact decoded source occurrences
    -> character gonols
    -> character-definition gonols sharing each character origin
    -> Python lexical-form gonols from closed character occurrences
    -> matched delimiter gonols
    -> recursive Python grammar-construction gonols
    -> module gonol
```

Every source occurrence remains independently addressable. Every character may close multiple definition gonols without changing the character's identity: Unicode category/name, Python identifier eligibility, exact-token membership, layout role, quote/comment introducer role, and other profile-backed definitions may coexist. Lexical forms consume the already-closed character occurrences atomically; larger constructions consume already-closed lexical or construction gonols atomically.

`character` means one exact decoded Unicode scalar occurrence. Spaces, newlines, digits, operators, delimiters, letters, and punctuation are all character gonols. Nothing is normalized, deduplicated, trimmed, or silently discarded.

## Recognition boundary

```text
METAPAT                         affixiation semantics
    -> UCNS                     geometry and Public Gonol positions
        -> Python Gonol         Python source admission and construction
            -> CPython          pinned recognition witness only
```

The private `_recognition` module uses the pinned CPython 3.12.14 `tokenize`, `ast`, and non-executing compiler validation after the source occurrence floor has been admitted. Recognition normalizes CRLF and classic-Mac CR line boundaries while all gonol spans and reconstructed bytes remain bound to the original source. Its former public "letter" vocabulary is deprecated and removed from the public receipt: it is now only an internal recognition plan. Token, AST, compiler, and code objects never become gonols and never replace the source-built relation graph.

Any valid Python 3.12.14 file-input source accepted by the pinned recognition witness is traversed iteratively without a grammar-node whitelist. Compiler-invalid file inputs remain `hmmm` even when `ast.parse` accepts them. The broad Python 3.12 surface fixture remains a regression witness; exhaustive parity against CPython's complete grammar/test corpus remains `hmmm` rather than being claimed from that fixture alone.

Standing: **implemented stack-local candidate; not canon and not an independent release**.

## Usage guidance

Run from this directory with CPython 3.12.14:

```bash
python -m python_gonol path/to/source.py --out source.gonol.json --pretty
python -m python_gonol --verify source.gonol.json
python -m pytest -q tests
```

Use the bytes entry point for files so an encoding declaration and exact original bytes remain bound:

```python
from pathlib import Path
from python_gonol import affixiate_python_bytes, replay_python_affixiation

path = Path("example.py")
receipt = affixiate_python_bytes(path.read_bytes(), source_id=path.as_posix())
replay_python_affixiation(receipt)
```

For invalid or unfinished source, the constructor retains every admitted character, character-definition, lexical, and matched-delimiter closure available beneath the failure, closes a `python.source.hmmm` root, records the exact tokenizer/delimiter/grammar boundary, and the CLI exits `2`. A missing end parenthesis therefore remains visible without discarding prior construction.

See [`docs/PYTHON_AFFIXIATION_BOUNDARY.md`](docs/PYTHON_AFFIXIATION_BOUNDARY.md) for the contract and [`WORK_GRAPH.json`](WORK_GRAPH.json) for exact inputs.

## hmmm

- exact UCNS geometric operation of Public Gonol function positions;
- exact UCNS Möbius-carrier affixiation/coupling law;
- exhaustive parity replay against the complete CPython 3.12 grammar/test corpus;
- Python language profiles after Python 3.12 file input;
- streaming/checkpointed receipt materialization for unusually large source trees.
