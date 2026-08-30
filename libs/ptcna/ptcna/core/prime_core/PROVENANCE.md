> **Design provenance, not operating instructions.** Relocated verbatim from
> `The-Interdependency/pcsa:prime_core/CLAUDE.md` (pcsa@1f731d1) during the
> 2026-07-28 archival sweep; it predates the ptcna consolidation. Where this
> document disagrees with the repository's current facts, the root `CLAUDE.md`
> and `docs/architecture.md` govern. In particular:
>
> - **Gradient invariant:** backprop lives only in `ptcna.neural`; core/fiq
>   tensors are auditing/timing tensors. The "frozen gradient policy" below is
>   the historical design statement that invariant descends from — do not read
>   it as license to add gradient flow to the core layer.
> - **Packaging:** this code now ships as `ptcna.core.prime_core` inside the
>   `ptcna` distribution (`include = ["ptcna*"]`); the "not packaged for
>   release" status below is historical.
> - **Tests:** run `python -m pytest ptcna/core/prime_core` (or the full repo
>   `pytest`); the unittest discovery paths below refer to the pre-relocation
>   tree. Layer names (`ptca-lib`, `pcna`, `pcta`) are pre-consolidation.
> - **Current ownership:** `Scalar`, fixed seven-by-seven composition, and the
>   UCNS carrier claims below are historical. Current code uses
>   `ptcna.neural.NeuralScalar`, shared `ptcna.circle.CircleTensor`, variable
>   composition counts, local identities, and an exact-shape UCNS receipt boundary.

# CLAUDE.md — prime_core (PTCA three-stratum core)

Context for AI assistants working in `prime_core/`. This package implements the
stratified PTCA core decided in the "PTCA Core Stratification Handoff" session
(Erin Spencer + Claude). It is **independent of the published `ptca-lib`**
(flat 4-D 53-node tensor) and does not modify it.

---

## What this package is

Three strata, three ontologies (handoff §1.1). The number system changes phase
as you ascend:

| Layer  | Object                                   | Differentiable? |
|--------|------------------------------------------|-----------------|
| Tensor | scalar (`Scalar`) — autodiff leaf        | yes (backprop)  |
| Circle | UCNS carrier hosting `Fiq` opaque grafts | carrier no      |
| Seed   | epicyclic UCNS-in-UCNS grouping          | structure no    |

Composition counts: **7 tensors/circle, 7 circles/seed, 157 seeds → 7,693
fiqs**; payload width `d = 53` → **407,729 scalar params**. Routing IS the UCNS
composition: `{7/2}` composes tensors→circle, `{7/3}` composes circles→seed.

**Gradient policy (frozen, §1.2):** differentiability descends through scalar
payloads; UCNS geometry (`n_min`, `face_state`, `anchor_order`) is
non-differentiable scaffold. `compose_circle`/`compose_seed` are the `⊠`
operator — structural only, so **`∂(⊠)` never appears on the autodiff tape**.

Public surface: `build_core`, `CoreSpec`.

---

## Resolved decisions (handoff §6)

| Decision            | Resolution |
|---------------------|------------|
| prime_core home     | New top-level package in the PTCA repo; `ptca-lib` untouched (packaging `include = ["ptca*"]` excludes it). |
| graft type name     | **`fiq`** — *first iterative qualifier / full isolated query / "the tensor holding the UCNS object"*. |
| tensor dimension `d`| **53** (off the original 32/64/128 menu; itself a coherence prime, echoing the prior seed count). |
| coherence-prime status | **Design choice (tunable)** — test 5 parameterized; 53↔157 both legal. Revert SEED_COUNT→53 keeps the suite green. |
| opaque-host (§1.3)  | **Confirmed** opaque host (not encode), per the "tensors remain scalar" constraint. |
| gradient attach pts | **Nothing crosses upward; payloads only** (the §1.2 default). |

To switch the coherence-prime status to a *hard invariant*, tighten
`tests/test_constants_coherence_prime.py::test_seed_count_is_coherence_prime`
to assert membership of the live `SEED_COUNT` unconditionally.

---

## Tests

```bash
python -m unittest discover -s prime_core/tests -v
```

Covers all six §4 items: structure counts (1), opaque round-trip (2),
gradient path with no `∂(⊠)` node (3), frozen geometry (4), coherence-prime
guard (5), routing steps (6). Stdlib `unittest` only — no pytest dependency.

---

## hmmm — outstanding

- **Canon documents absent.** `canon_definitions_invariants-1.md` and
  `consciousness_primes_prediction1.pdf` are not in any accessible repo. The
  stratum definitions and composition counts are encoded here as the handoff
  *stated* them, not as verified canon.
  - **Resolved (coherence-prime rule):** `constants.py::is_coherence_prime` now
    uses the *recursive* definition (kernel factors must themselves be earlier
    coherence primes) instead of the old provisional `COHERENCE_FACTOR_UNIVERSE`
    frozen set, which silently diverged at p=4373. The canonical single source
    of truth is `interdependent_lib.coherence_primes`
    (The-Interdependency/interdependent-lib); prime_core mirrors it verbatim
    because importing the aggregator would invert the dependency graph.
- **Validator resolved.** PTCNA vendors the bounded skill-lib collection and
  collects MODULE_BUILD, CONTRACTS, CHECKS, and BOUNDARIES declarations into
  `ptcna_msdmd.ts`.
- **UCNS binding is candidate scoped.** The default `157x7x7x53` initialization
  consumes an exact reviewed UCNS receipt. Current code does not import archived
  `a0_safe`, `UCNSObject`, or `factor_search` surfaces; unmatched shapes return
  typed suspension and use explicitly local identities.
- **Packaging resolved.** `prime_core` ships under
  `ptcna.core.prime_core` in the `ptcna` distribution.
- **Seam under load.** The descend/ascend split is the whole experiment;
  unfalsified until a core is actually trained.
