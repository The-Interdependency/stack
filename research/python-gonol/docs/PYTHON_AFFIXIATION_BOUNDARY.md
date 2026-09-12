# Python affixiation boundary

Status: **stack-local implemented candidate**. This document defines construction and evidence boundaries; it does not promote Python Gonol Construction to canon.

## Construction contract

Python source is admitted from the bottom up:

```text
source bytes
  -> exact decoded source
  -> occurrence-specific character gonols
  -> character-definition gonols
  -> lexical-form gonols
  -> delimiter constructions
  -> recursive grammar constructions
  -> module
```

A parent may reference only an already-closed child. Closing a larger gonol never erases the child's identity, order, multiplicity, source span, relation, or provenance.

### Character floor

Every decoded Unicode scalar occurrence closes exactly once as `scale="character"`. "Character" is a source-floor term, not an alphabetic category. Newlines, spaces, punctuation, digits, quote marks, operators, and letters are admitted identically as occurrences.

Each occurrence then receives one or more `scale="character-definition"` gonols. Every definition has exactly one `origin` member: the already-closed character occurrence. Definitions are deliberately non-exclusive. Examples include:

- `unicode-category = Pd` and `python-exact-token = MINUS` for `-`;
- `python-identifier = start` and `python-identifier = continue` for an identifier-capable character;
- `python-layout = line-break` for a newline;
- `python-delimiter = comment-introducer` for `#`.

Definitions describe capabilities or source-profile facts. They do not pre-decide the contextual lexical role of an occurrence.

### Lexical forms

CPython 3.12 `tokenize` is a recognition witness after character closure. A lexical gonol is built from the exact ordered character gonols spanning the recognized surface form. Inter-token gaps are explicit lexical gonols too, so whitespace/comments/source gaps do not disappear.

Tokenizer objects never enter the receipt.

### Delimiters and grammar

Matched `()`, `[]`, and `{}` relations close from already-closed lexical/enclosed gonols. CPython 3.12 `ast.parse(..., mode="exec", feature_version=(3, 12))` then supplies the grammar witness. The recursive constructor walks arbitrary AST fields rather than dispatching through a hand-maintained Python syntax whitelist. AST nodes themselves are discarded after their source relation has been projected onto closed source-built gonols.

Spanless parser relations that cannot honestly close as independently sourced gonols remain intrinsic relation properties on the source-owning parent rather than being invented as source objects.

## Private recognition module

`python_gonol._recognition` is the original source-recognition implementation. Its historical `letter` scale is no longer a public construction. The current public constructor consumes that module only as an internal plan and rematerializes the receipt as:

```text
character -> definitions -> lexical -> larger constructions
```

`replay_python_affixiation()` rejects any public receipt containing the deprecated `letter` scale or `#letter:` address.

This removes the deprecated contract while preserving the proven tokenizer/AST witnessing logic.

## Failure boundary

Unfinished or invalid Python remains constructible below the unresolved point. Tokenizer failure, delimiter mismatch, or grammar failure produces a `python.source.hmmm` root over the largest honest lower closures. Exact unresolved details are retained in the receipt.

No error recovery is allowed to invent the missing source.

## Geometry boundary

UCNS owns geometry. When an explicit UCNS Public Gonol authority with the pinned digest is supplied, character occurrences record their observed Public Gonol positions. When it is absent, geometry remains `hmmm`. Python Gonol Construction does not invent a UCNS function operation or Möbius coupling law.

## Replay

Replay verifies, at minimum:

1. receipt schema/profile/constructor identity;
2. exact source bytes and decoded-source digests;
3. contiguous occurrence-specific character coverage;
4. at least one definition-space gonol for every character occurrence;
5. definitions reference one already-closed character origin;
6. lexical forms are an exact partition of the closed character occurrences;
7. every larger relation references only already-closed children;
8. every non-character construction span equals the union of its atomic participants;
9. the root covers the complete source; and
10. every gonol identity plus the receipt digest reproduces deterministically.

Replay proves this construction is internally reproducible. It does not establish semantic quality, runtime equivalence, measurement validity, or canon.

## Python 3.12 surface evidence

The constructor is generic over the AST witness rather than an AST-node whitelist, and the regression fixture exercises modern Python 3.12 constructs including type aliases/generics, decorators, positional-only and variadic arguments, async constructs, comprehensions, assignment expressions, pattern matching, exception groups, f-strings, lambdas, slicing, calls, and the operator families.

That fixture is evidence, not an exhaustive grammar proof. Complete parity replay against CPython's full grammar/test corpus remains `hmmm` until run as its own declared experiment.

## Usage guidance

```bash
cd research/python-gonol
python -m pytest -q tests
python -m python_gonol example.py --out example.gonol.json --pretty
python -m python_gonol --verify example.gonol.json
```

Programmatic use:

```python
from python_gonol import affixiate_python_source, replay_python_affixiation

receipt = affixiate_python_source("answer = 40 + 2\n", source_id="example.py")
assert replay_python_affixiation(receipt).receipt_digest == receipt.receipt_digest
```

## hmmm

- exact UCNS relation geometry for Python constructions;
- full CPython 3.12 grammar/test-corpus parity replay;
- language profiles after Python 3.12;
- large-source streaming/checkpoint policy.
