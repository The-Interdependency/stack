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

- Exact UCNS relational producer used by the lexical floor:
  `The-Interdependency/ucns@d7c6f51304ed6c32d48badf63132bea6de8af497`
  (module SHA-256 `b839d29c79b43d29faf6f5d9a39b7a1485f39a0f071b525fd1848cf18f061cdd`).
- Public Gonol geometry is consumed lazily from the installed `ucns` package
  when an explicit matching authority is supplied.

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

Once closed, a gonol is atomic at any scale. Closed gonols may participate
directly at any admissible scale without reopening.

## Layout

```text
research/english-gonol/
├── BASE.json
├── README.md
├── english_gonol/
│   ├── gonol.py                  # unified candidate constructor (identity edcm.gonol)
│   ├── language/                 # English lexical evidence over UCNS carrier
│   └── orthogonal_carrier_sweep.py  # 1-7 carrier experimental sweep
├── tools/build_oewn2025_embeddings.py
├── tests/
├── docs/
│   ├── GONOL_LANGUAGE_BOUNDARY.md
│   └── orthogonal-carrier-sweep-v0.md
└── experiments/
    ├── lexical/                  # frozen lexical-floor run artifacts
    └── orthogonal-carrier-sweep-v0.json
```

## Entry points

Tests (run from `research/english-gonol/`):

```bash
python -m pytest -q tests
# or, for the unittest-only constructor suite:
python -m unittest discover -s tests -p 'test_gonol_constructor.py'
```

The gonol constructor is importable directly:

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

The orthogonal unit-circle carrier sweep (experimental, meaning-agnostic):

```bash
python -m english_gonol.orthogonal_carrier_sweep \
  --out experiments/orthogonal-carrier-sweep-v0.json
```

See [`docs/orthogonal-carrier-sweep-v0.md`](docs/orthogonal-carrier-sweep-v0.md).

The full-corpus definition re-affixiation run (no sampling, no hash
placement, no carrier buckets; reuses each closed word gonol once):

```bash
python -m english_gonol.definition_affixiation_run \
  --source-root /path/to/oewn-2025/src/yaml \
  --out-dir experiments/oewn-affixiation-v0 --workers 2
```

See [`docs/oewn-orthogonal-affixiation-v0.md`](docs/oewn-orthogonal-affixiation-v0.md).
The large `records.jsonl` is local persisted state and is not committed; the
committed `manifest.json` binds it via `records_sha256`.

## Research status

Standing: **stack-local research, not canon**. The construction is an
implemented candidate; no scale option set or relation is selected canon, and
construction does not activate measurement. See
[`docs/GONOL_LANGUAGE_BOUNDARY.md`](docs/GONOL_LANGUAGE_BOUNDARY.md) for the
governing boundary and [`BASE.json`](BASE.json) for provenance.

## hmmm

- exact UCNS geometric operation of Public Gonol function positions;
- UCNS Möbius-carrier affixiation/coupling law;
- source-supported complete English morphology law;
- which scales and relations, if any, are later selected.
