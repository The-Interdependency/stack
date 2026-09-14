# English Gonol Construction

Stack-local research component for English lexical/gonol construction.

## Purpose

English Gonol Construction owns the English text-domain gonol construction
concern:

- English lexical/gonol construction through declared scale option sets;
- relational carrier construction (direct-atomic and molecular OEWN branches);
- recursive / epicyclic carrier experiments;
- attachment and composition rules (affix inventory, rendering, morphology);
- reconstruction and collision tests;
- English → UCNS representation mapping.

The code was moved out of `libs/edcm/` into `research/english-gonol/` without
redesign. Frozen constructor/schema/commit identities are retained for receipt
continuity: the candidate constructor identity remains `edcm.gonol`, while the
Python import path is now `english_gonol.gonol`.

## UCNS prerequisite

Dependency direction:

```text
UCNS
  ↓
English Gonol Construction
  ↓
EDCM / later consumers
```

UCNS owns gonol geometry, the native Möbius/Public Gonol carrier, and
geometrically established operations. English Gonol Construction consumes UCNS
geometry only from explicit authorities and never invents UCNS operations.

- Exact UCNS relational producer used by the historical lexical floor:
  `The-Interdependency/ucns@d7c6f51304ed6c32d48badf63132bea6de8af497`
  (module SHA-256 `b839d29c79b43d29faf6f5d9a39b7a1485f39a0f071b525fd1848cf18f061cdd`).
- The current full construct pins the cleaned Public Gonol authority and
  consumes only the established 157-position carrier lookup. It does not
  restore the removed singleton-axis/closure/tangency machinery.

## Architectural boundary from EDCM

English Gonol Construction is not EDCM.

- METAPAT defines affixiation semantics.
- UCNS owns any exact geometric realization.
- English Gonol Construction applies affixiation to text-domain gonols and
  owns text-domain admission and linguistic/semantic gonol construction.
- EDCM may evaluate English Gonol outputs but must not define the construction.
  English Gonol construction does not validate EDCM measurement, and English
  Gonol construction and EDCM measurement remain separate.

For active English Gonol text construction:

```text
every admitted character is a gonol
```

The full construct additionally enforces one shared identity for each exact
character scalar and one shared identity for each exact word surface. Corpus
occurrences, sense ids, synset ids, and definition records are evidence about
those identities; they are not promoted into independent gonols.

## Full-construct contract

`english_gonol.full_construct_run` is the current full-corpus construction
builder. Its fixed boundary is:

```text
one exact scalar -> one character identity
one exact surface -> one word identity
word -> exact ordered/multiplicity-preserving character references
word origin -> ordered definitions
ordinal evidence + semantic evidence + ordered sentence context
-> preponderance relative to the rest of the sentence
-> hmmm until UCNS establishes the exact geometric displacement law
```

The builder does **not** create sentence, sense, synset, n-gram, occurrence,
closure, relation-circle, tangency, attention-frame, or Mobius-frame objects.
It does not synthesize weights, vectors, coordinates, centers, radii, motion,
or tangency. Those quantities may only appear when established geometry derives
them.

The materialized output is normalized once in `construct.db` with a small
`manifest.json`. It is not duplicated into a giant canonical JSON artifact.

## Layout

```text
research/english-gonol/
├── BASE.json
├── README.md
├── english_gonol/
│   ├── gonol.py                  # unified candidate constructor (identity edcm.gonol)
│   ├── full_construct_run.py     # normalized full-corpus construct
│   ├── definition_affixiation_run.py  # earlier full-corpus definition experiment
│   ├── orthogonal_carrier_sweep.py    # 1-7 carrier experimental sweep (control)
│   ├── primitive_layer_run.py    # character definitions + corrected suffixiation
│   └── language/
│       ├── source.py             # OEWN 2025 ingestion; preserves source sense order
│       ├── character_definitions.py
│       ├── suffixiation.py
│       └── data/
├── tools/build_oewn2025_embeddings.py
├── tests/
├── docs/
│   ├── GONOL_LANGUAGE_BOUNDARY.md
│   ├── full-construct-v1.md
│   ├── orthogonal-carrier-sweep-v0.md
│   ├── oewn-orthogonal-affixiation-v0.md
│   └── primitive-layer-correction-v0.md
└── experiments/
    ├── lexical/
    ├── orthogonal-carrier-sweep-v0.json
    ├── primitive-layer-v0.json
    └── oewn-affixiation-v0/
```

## Entry points

Tests (run from `research/english-gonol/`):

```bash
python -m pytest -q tests
# or, for the unittest-only constructor suite:
python -m unittest discover -s tests -p 'test_gonol_constructor.py'
```

The current full construct:

```bash
python -m english_gonol.full_construct_run \
  --source-root /path/to/oewn-2025/src/yaml \
  --ucns-source-root /path/to/ucns \
  --out-dir experiments/full-construct-v1
```

This writes only `construct.db` and `manifest.json`. See
[`docs/full-construct-v1.md`](docs/full-construct-v1.md).

The gonol candidate constructor is importable directly:

```python
from english_gonol.gonol import construct_gonol, replay_gonol

word = construct_gonol(scale="word", source="try", source_id="example:try")
assert word.receipt_digest == replay_gonol(receipt=word).receipt_digest
```

The historical lexical-floor builder (requires PyYAML and exact checkouts):

```bash
python tools/build_oewn2025_embeddings.py \
  --source-repo /path/to/oewn-2025-checkout \
  --ucns-source-root /path/to/ucns-at-d7c6f51304ed6c32d48badf63132bea6de8af497 \
  --output /path/to/output --acquire --resume
```

The orthogonal unit-circle carrier sweep remains a meaning-agnostic control:

```bash
python -m english_gonol.orthogonal_carrier_sweep \
  --out experiments/orthogonal-carrier-sweep-v0.json
```

The earlier full-corpus definition re-affixiation experiment remains separate
historical research and supplies no placement law to the current construct:

```bash
python -m english_gonol.definition_affixiation_run \
  --source-root /path/to/oewn-2025/src/yaml \
  --out-dir experiments/oewn-affixiation-v0 --workers 2
```

The primitive-layer correction and extension:

```bash
python -m english_gonol.primitive_layer_run \
  --out experiments/primitive-layer-v0.json
```

## Research status

Standing: **stack-local research, not canon**. The full construct now preserves
the specified identity and evidence structure without promoting corpus
bookkeeping into geometry. Construction does not activate EDCM measurement.

## hmmm

- the exact UCNS law mapping ordinal + semantic + sentence-context evidence to
  geometric displacement;
- exact UCNS geometric operation of Public Gonol function positions beyond the
  established carrier identity;
- UCNS Möbius-carrier affixiation/coupling law;
- source-supported complete English morphology law.
