# English Gonol Construction

Stack-local research component for English lexical/gonol construction.

## Authority

```text
METAPAT  -> affixiation semantics
UCNS     -> gonol / Möbius / Public Gonol geometry
English  -> text admission and linguistic/semantic construction
EDCM     -> measurement/evaluation only
```

English construction consumes UCNS geometry; it does not invent geometry or
move English semantics into UCNS.

## Active invariants

```text
every admitted character is a gonol
one exact scalar  -> one shared character identity
one exact surface -> one shared word identity

glyph axes
  -> ordered glyph-axis tensor
  -> closed word
  -> word axis
```

Once closed, a gonol is atomic at an admissible consuming scale. Reuse preserves
identity while order, multiplicity, relation, source position, and provenance
remain recoverable.

The Stack-forged Hilbert inference candidate treats those already-declared axes
as mathematical basis directions rather than inserting Cartesian coordinates.
A word's ordered glyph-axis construction is preserved when the closed word
becomes its own higher-scale axis. Exact construct identity travels with every
basis axis. See [Hilbert inference candidate](docs/hilbert-inference.md).

This mathematical use of vector is domain-qualified as `HilbertStateVector`.
It is not METAPAT `Vector` and not a UCNS displacement vector. The canonical
scalar field, cross-origin inner products, amplitudes/phases and inference
operators remain unresolved.

Corpus occurrences, sense ids, and synset ids are evidence/provenance, not
independent gonols. Definitions are word-anchored constructions: each retains
the shared word origin, exact ordered constituent word/whitespace-character
identities, source ordinal, direct binding, and chain predecessor.

## Full construct v2

`english_gonol.full_construct_run` builds the complete pinned OEWN 2025 corpus
without promoting bookkeeping into geometry.

```text
word origin -> D1 -> D2 -> ... -> Dn     # chain topology
word origin -> D1, D2, ... Dn            # direct topology

ordinal evidence
+ semantic evidence
+ exact sentence-context evidence
-> preponderance relative to the rest of the sentence in which the word appears
-> hmmm until UCNS derives the displacement geometry
```

Definitions preserve their source exactly: every maximal non-whitespace run
reuses one shared word identity and every whitespace scalar reuses one shared
character identity. No normalization is applied.

The builder does not create sentence/sense/synset/n-gram singleton objects,
occurrence-object ledgers, closure graphs, synthetic relation circles,
tangencies, attention frames, or duplicate JSON copies of the database. It does
not synthesize weights, displacement vectors, Cartesian coordinates, centers,
radii, motion, or tangency. The separate Hilbert candidate constructs
mathematical state vectors from axes already declared by this construction; it
does not supply a displacement law.

### Verified full-corpus result

Evidence is committed in `experiments/full-construct-v2/`.

- 118 shared character identities
- 164,864 shared word identities
- 1,739,949 ordered word-character references
- 185,155 word-anchored definitions
- 3,535,375 exact ordered definition components
- 866,183 resolved semantic evidence rows
- 0 unresolved semantic evidence rows
- SQLite integrity: `ok`
- logical receipt: `12277b4959c0c72b7af12097b8a77bf91866bbf669e7f4ac07b6a5f1426ebb57`
- generated database: 306,331,648 bytes
- build wall time: 1:34.79
- peak RSS: 286,692 KiB

The database itself remains generated state; the compact manifest, integrity
receipt, and resource receipt are committed.

## Run

```bash
python -m english_gonol.full_construct_run \
  --source-root /path/to/oewn-2025/src/yaml \
  --ucns-source-root /path/to/ucns \
  --out-dir experiments/full-construct-v2
```

Tests:

```bash
python -m pytest -q tests
```

See [`docs/full-construct-v2.md`](docs/full-construct-v2.md).

## Four-view full-corpus audit

The [complete view report](docs/hyperspace-views-full-v1.md) covers all **164,864 words**,
all fifteen nonempty view combinations, and three complete address-renumbering controls.
Native and independent evidence agree exactly, including per-word native reconstruction.
The synthesis distinguishes 137,013 values. Removing view 1, 2, or 3 loses 10,267,
20,042, or 125,813 distinctions respectively; removing view 4 loses none.

View 1 is nullable constituent-overlap metadata, view 2 is the terminal phase/frame,
view 3 carries coarse address/provenance information, and view 4 is a derivable witness.
Their inference usefulness requires a task beyond distinctness. The frozen protocol is
[`FULL_VIEW_AUDIT.json`](FULL_VIEW_AUDIT.json); complete receipts are in
[`experiments/hyperspace-views-full-v1/`](experiments/hyperspace-views-full-v1/).
The report contains the exact source/database bindings and full replay commands.

## Historical research

The orthogonal-carrier sweep and earlier definition-affixiation run remain
separate experiments and supply no placement law to v2. The falsified
`full_singleton_run.py` architecture and its UCNS singleton-axis support were
deleted rather than retained as an active precedent.

## Migration standing

The current lifecycle record is [`MIGRATION.json`](MIGRATION.json). UCHC is
extracted and has a clean-installed immutable candidate verified in Stack, but
stable publication, released-artifact reconsumption, severance of the local
implementation path and a scoped authority-transition receipt remain incomplete.
Stack therefore remains the implementation forge for this new candidate.

## hmmm

The exact UCNS law mapping ordinal + semantic + sentence-context evidence to
geometric displacement remains unresolved. No English-layer rule may fill that
boundary with invented weights, directions, distances, displacement vectors,
Cartesian coordinates, centers, radii, tangencies, or motion.

For the Hilbert candidate, the canonical scalar field (`R` or `C`),
cross-origin inner products/angles, amplitudes/phases, learned inference
operators, sense selection, sentence-axis promotion and completed UCHC
graduation remain unresolved.
