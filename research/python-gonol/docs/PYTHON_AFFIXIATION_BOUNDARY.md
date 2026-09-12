# Python source affixiation boundary

**Status:** implemented stack-local Python 3.12 file-input candidate.
**Scope:** determine and implement how Python source affixiates into gonols from
the lowest admitted source units upward.
**Root impact:** none.

## Governing relation

Python Gonol Construction applies METAPAT's affixiation meaning: already-bounded
participants remain individually addressable, with identity and provenance
preserved, while their declared relation may close as a higher-scale
object-whole.  A closed whole may participate recursively without erasing its
constituents.

UCNS owns any exact geometric realization.  Python Gonol Construction owns the
Python source profile, admission, lexical relations, delimiter closure, grammar
relations, and receipts.  Tokens, AST nodes, compiler objects, and metadata own
none of the construction.

## Source floor: letters

Python 3.12 reads program text as Unicode code points.  This construction admits
each decoded Unicode scalar occurrence in exact source order and closes it as one
letter gonol.

`letter` here means the irreducible admitted source occurrence.  It includes an
alphabetic character, digit, space, tab, newline, quote, operator, delimiter, or
other exact source scalar without introducing UCNS letter/punctuation subclasses.
The original file bytes, detected Python encoding, decoded-source digest,
occurrence index, line/column span, scalar value, source identity, and optional
observed Public Gonol position remain receipt-bound.

Repeated equal values have distinct occurrence addresses.  No normalization,
identifier NFKC replacement, case folding, trimming, gap deletion, or
deduplication changes the admitted source.

## Lexical affixiation

After every letter closes, Python's lexical witness identifies nonempty lexical
forms.  Each lexical form closes solely from the exact ordered letter gonols in
its source span.  Source gaps that Python uses to separate forms also close as
`python.lexical.INTERTOKEN`; this preserves whitespace the tokenizer does not
emit as a token.

The lexical relation, exact form class, source length, role order, and CPython
3.12 witness provenance live inside the lexical gonol.  The runtime `TokenInfo`
does not.

Zero-width `INDENT`/`DEDENT` witness events have no source occurrence from which
to form a separate gonol.  They therefore remain identity-bearing properties of
the consuming module/source relation.  The actual indentation characters remain
letter and lexical gonols.

## Larger construction affixiation

Matched `()`, `[]`, and `{}` relations close from lexical gonols and already
closed nested delimiter gonols.  Opener, content order, nested multiplicity, and
closer belong inside the delimiter gonol.  Missing or mismatched closure becomes
`hmmm`.

After those closures, the CPython 3.12 grammar witness supplies accepted grammar
relations and child roles.  A grammar construction closes over:

1. already-closed child grammar gonols;
2. already-closed delimiter gonols intersecting its concrete source relation;
3. remaining already-closed lexical forms in its exact source span; and
4. identity-bearing relation properties such as operator or grammar-field roles.

Construction proceeds postorder.  Thus every member identity in a parent receipt
was closed earlier.  Overlapping relations—such as a call's argument role and
the parentheses enclosing its arguments—may both reference the same canonical
source occurrences; they do not duplicate those occurrences.

Some CPython witness records have no independent source span, including an
empty `arguments` record and `TypeIgnore`.  Such a record cannot honestly close
as a separate gonol.  Its relation is retained as an intrinsic property of the
source-built parent that contains the exact delimiter or comment gonols.  The
witness object is then discarded.  Decorated function and class spans are
extended to the exact leading `@` lexical gonol so the decorator relation does
not lose its constitutive marker.

The module gonol closes last and covers every source occurrence, including
comments, blank space, redundant parentheses, and other concrete source material
that abstract grammar nodes omit.

## Recognition is not substitution

CPython's tokenizer and AST are bounded recognition witnesses for the Python
3.12 language profile.  They determine where accepted lexical and grammar
relations apply.  They are discarded after each relation is translated into
source-occurrence membership, closed-gonol references, order, roles, and
provenance.

The following never serve as a gonol identity or participant:

- token numbers or `TokenInfo` instances;
- AST instances or AST dumps;
- compiled code objects;
- evaluated literal values;
- symbol-table/compiler objects;
- whole-source hashes standing in for visible construction.

SHA-256 identifies a complete visible gonol or receipt payload.  The visible
payload—not its hash—is the construction.

## Failure and replay

Tokenizer, delimiter, or grammar failure does not erase completed work.  The
constructor closes a `python.source.hmmm` root over every lower construction it
can honestly retain, records the exact unresolved finding, and sets receipt
standing to `hmmm`.

Replay checks:

- exact original bytes and encoding;
- exact source reconstruction from ordered letter gonols;
- one contiguous letter floor with distinct occurrence addresses;
- every member references an earlier closed gonol by exact address and identity;
- every larger gonol's exact span equals the union of its atomic closed-child
  spans, without flattening descendant leaves back into the parent;
- every gonol identity and the final receipt digest recompute; and
- the root covers every source occurrence.

Replay proves deterministic construction integrity only.  It does not execute
the source or prove behavior, equivalence, safety, semantic quality, geometry,
measurement validity, or canon.

## Python profile

The implemented profile is CPython 3.12 file input.  It covers any exact source
accepted by `ast.parse(..., mode="exec", type_comments=True,
feature_version=(3, 12))`, including Python 3.12 type statements/type parameters,
pattern matching, exception groups, asynchronous constructs, comprehensions,
formatted strings, comments within formatted replacement fields, Unicode
identifiers, explicit/implicit line joining, and all ordinary expression and
statement forms.

The committed broad-surface fixture exercises these relations but does not claim
that one finite fixture enumerates all possible programs.  Generic traversal,
rather than a hand-selected statement dispatcher, is what keeps the constructor
open over the complete accepted 3.12 grammar.

## Usage guidance

```bash
cd research/python-gonol
python -m pytest -q tests
python -m python_gonol ../../some-file.py --out /tmp/some-file.gonol.json
python -m python_gonol --verify /tmp/some-file.gonol.json
```

Prefer `affixiate_python_bytes()` for files.  Use
`affixiate_python_source()` only when exact original file bytes are unavailable
or irrelevant to the declared source profile.

## hmmm

- exact UCNS function operation for each Public Gonol position;
- exact UCNS Möbius-carrier affixiation/coupling geometry;
- whether and how Python 3.13+ language profiles share or revise this constructor;
- streaming or checkpointed materialization for source large enough that a full
  in-memory visible receipt would exceed available resources.
