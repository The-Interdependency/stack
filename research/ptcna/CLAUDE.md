# CLAUDE.md — ptcna

AI-assistant guidance for `The-Interdependency/ptcna`.

## What this repo is

**PTCNA — Prime Tensor Circled Neural Architecture.** One package, four layers
(`neural`, `circle`, `seed`, `core`). It consolidates three formerly-separate
repos that were never actually separate things — they are layers of one
architecture:

- `neural/` ← `pcna` (`core/`) — neural tensors; **the only back-propagating layer**
- `seed/`   ← `pcta` — auditing/timing tensors, circles → seeds
- `core/`   ← `pcsa` (`ptca/` + `prime_core/`) — auditing/timing tensors, seeds → cores; fiqs
- `circle/` ← new — auditing/timing tensors, neural tensors → circles

`ptcna` is the single upstream that feeds `interdependent-lib` (one `ptcna`
registry key/extra replaces the former `pcna`/`pcta`/`pcsa` entries). `pcea`
(encryption guardian) is a separate, orthogonal repo — not a layer.

## Core invariants (do not violate)

- **Backprop only in the neural layer.** Circle/seed/core tensors are auditing
  and timing tensors; they are non-differentiable. Do not add gradient flow to
  them.
- **Every circle, seed, and core is itself a tensor.** Composition counts are
  variable; this invariant is not.
- **fiqs** gate core internal propagation per Fick's law `J = −D ∇φ` — timing,
  not gradient descent. The fiq substrate is `ptcna.core.prime_core`.
- No theorem/proof/empirical status transfers between layers or from UCNS by
  naming these terms.

## Layout

```text
ptcna/
  __init__.py            exposes neural, circle, seed, core
  neural/  (numpy)       pcna.py, ring_core.py (RingCore), tensor_engine, theta,
                         sigma, merge, memory_core, topology, zeta, scalar, ...
  circle/                tensor.py, compose.py, audit.py
  seed/    (stdlib)      compose.py, tensor.py, constants.py, audit.py (seed_audit)
  core/    (stdlib)      tensor, sentinels, exchange, instance, primes, provenance
    prime_core/          fiq.py (fiqs/Fick), core.py, constants.py
docs/architecture.md     consolidation spec + status log
pyproject.toml           name=ptcna; deps=[numpy]; testpaths=ptcna
```

## Build / test

```bash
pip install -e ".[dev]"
pytest                   # all tests must pass; never hard-code a stale count
```

## Migration status

Consolidation is **complete** for the items an agent can land in this repo:

- **Done:**
  - One shared `ptcna.circle.CircleTensor` is used by circle, seed, and core
    composition. Structural types are non-differentiating and composition
    counts are variable.
  - `ptcna.neural.NeuralScalar` is the sole reverse-mode scalar. The core
    layer no longer owns a duplicate scalar/autodiff implementation.
  - UCNS integration is a typed suspended boundary. Archived UCNS surfaces do
    not activate it, and local identities make no UCNS representation claim.
  - The shadow `ptcna.neural.edcm` module was removed. Zeta consumes an
    explicitly injected external measurement provider or returns
    `measurement_suspended`.
  - Circle/seed audit extraction: `ptcna.circle.circle_audit` and
    `ptcna.seed.seed_audit` own the aggregation; the neural engine delegates.
  - `neural/ptca_core.py` → `neural/ring_core.py`; class `PTCACore` → `RingCore`.
    The neural layer carries no `ptca` token.
  - Seed layer re-identified as `ptcna.seed` (docstrings/metadata no longer
    present it as the standalone `pcta` package); core-layer docs no longer
    show `from ptca ...` imports or claim the `ptca-lib` dist identity.
  - interdependent-lib rewiring landed in that repo (single `ptcna` registry
    key/extra; `docs/prime-tensor-stack.md` rewritten around the 4-layer model).
- **Deliberately kept:** core-layer public class names `PTCATensor` /
  `PTCAInstance` (the layer "was PTCA"; they are in the right layer and are
  published API — a `core.*` rename is possible later cleanup, not migration).
- **Out of scope, not migrated:** pcna's `backend/` app server (llm/server/sms)
  — application infra, not architecture; its `test_edcm_engine.py` was dropped.
- **Done (2026-07-28 archival sweep):** the source repos `pcna`, `pcta`, `pcsa`
  are archived on GitHub with tombstone READMEs pointing here. Unique content
  was rescued first (`scripts/proof_check.py` from pcna;
  `ptcna/core/prime_core/PROVENANCE.md` from pcsa — see PR #6).
- **Remaining evidence boundary (`hmmm`):**
  - A reviewed PTCNA-specific UCNS higher-gonol producer profile does not yet
    exist.
  - Sustained-load behavior across the complete four-layer seam remains
    unfalsified.

Do not hand-wave the remaining items as done. Mark unknowns `hmmm`.
