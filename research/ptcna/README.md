# PTCNA — Prime Tensor Circled Neural Architecture

## 2026-08-17 construction correction

The **intended PTCNA has not yet been built**.

PTCNA is supposed to be derived from UCNS auditing a functioning conventional
neural network:

```text
functioning conventional neural network
        ↓
UCNS audit
        ↓
source-bound relational evidence
        ↓
PTCNA construction derived from that evidence
```

Until that audit evidence exists, intended PTCNA construction is **BLOCKED**.
The executable four-layer system currently in this repository predates recovery
of that prerequisite and is retained as a **historical pre-audit experimental
scaffold**. Its layer/ring/weight choices are not evidence that the intended
architecture has been derived.

For the intended language path, the primitive input object is a **UCNS Unicode-
character gonol**. Conventional tokenizer ids, subword ids, whole-string hashes,
and opaque external embedding vectors are not substitutes for that primitive.
The exact route through the future audit-derived architecture remains `hmmm`.

See [`docs/INTENDED_CONSTRUCTION_GATE.md`](docs/INTENDED_CONSTRUCTION_GATE.md).

## Historical scaffold

The repository currently implements one architecture with four layers. The
material below documents that executable scaffold and its provenance; where it
conflicts with the construction correction above, the correction governs.

Each scaffold layer's tensors divide into the next; every circle, seed, and core
is itself a tensor.

| Module | Layer | Divides… → … | Tensor kind | Back-propagation |
|---|---|---|---|---|
| `ptcna.neural` | neural | (base) neural tensors | **neural** | **yes — the only differentiable layer** |
| `ptcna.circle` | circle | neural tensors → circles | auditing / timing | no |
| `ptcna.seed` | seed | circles → seeds | auditing / timing | no |
| `ptcna.core` | core | seeds → cores | auditing / timing | no |

- **Back-propagation lives only in the neural layer** in this scaffold.
- **fiqs** gate when scaffold cores propagate internally, per the existing
  Fick-inspired timing implementation.
- **PCEA** remains a separate orthogonal repository, not a PTCNA layer.

None of those scaffold choices is promoted into the intended PTCNA merely by
being executable.

## Provenance

| Layer | Migrated from | Was |
|---|---|---|
| neural | `The-Interdependency/pcna` (`core/`) | Prime Circular Neural Architecture |
| seed | `The-Interdependency/pcta` | Prime Circled Tensor Architecture (circles → seeds) |
| core | `The-Interdependency/pcsa` (`ptca/` + `prime_core/`) | Prime Tensor Core Architecture (was `PTCA`) |
| circle | *new* (audit extracted from the neural engine — see `docs/architecture.md`) | previously unnamed |

This provenance explains the scaffold's construction history. It does not
satisfy the required UCNS audit of an independently functioning conventional
neural network.

## Install & test

```bash
pip install -e ".[dev]"
pytest
```

These commands exercise the historical scaffold and its repository contracts.
They do not construct the intended PTCNA.

## Historical target and fallback runtime

The scaffold and a simpler fallback share one task interface but retain separate
identities. Existing callers can still inspect/replay that research surface.

```python
from ptcna import PTCNARuntime

runtime = PTCNARuntime()
target = runtime.infer("question")
fallback = runtime.infer("question", backend="fallback")
continued = runtime.infer("question", fallback_on_error=True)
runtime.reward(continued, outcome=1.0)
```

The scaffold target consumes the bundled UCNS candidate receipt pinned to
`The-Interdependency/ucns@b7b6f35cce69c273860923489a1c8b5372d14eb0`
and independently verifies the exact `157×7×7×53` positive-zero state.
That receipt established compatible construction for the scaffold only. It is
not the prerequisite neural-audit evidence from which intended PTCNA is to be
derived.

The scaffold also uses a whole-string SHA-derived input projection. That input
representation is historical and **not** the intended Unicode-character-gonol
language input.

## Frozen historical evaluation

The preregistered critical role-acquisition program remains sealed evidence for
the exact scaffold that was tested:

- target `ptcna.experimental.v1`: `0.3333333333` accuracy;
- hashed-linear fallback: `0.9444444444` accuracy;
- absolute usefulness: **FALSIFIED** for the declared in-sample scope;
- superiority over the fallback: **FALSIFIED** for the declared in-sample
  scope.

Do not rewrite or erase that result. It does **not** evaluate the intended PTCNA,
because the intended PTCNA could not yet have been constructed under the
restored audit prerequisite.

## Current status

- **Intended PTCNA:** BLOCKED on UCNS audit of a functioning conventional neural
  network.
- **Historical four-layer scaffold:** implemented and preserved.
- **Historical scaffold evaluation:** sealed; both declared role-acquisition
  claims FALSIFIED for that exact scope.
- **Intended language primitive:** UCNS Unicode-character gonol; no tokenizer or
  whole-string-hash substitution.
- **Next PTCNA work:** preserve evidence and define the future consumer boundary;
  do not repair or elaborate architecture before the UCNS audit-derived contract
  exists.

History and the detailed scaffold record live in `docs/architecture.md`.

License: MPL-2.0.
