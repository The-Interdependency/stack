# Chapter 5: One Architecture, Four Layers

*Chapter 5 of the distributed Interdependency textbook. Chapter 0 lives in
`metapat/CHAPTER_ZERO.md`; Chapter 1 in `ucns/docs/chapter-1.md`; Chapter 2 in
`edcm/docs/chapter-2.md`; Chapter 3 in `skill-lib/docs/chapter-3.md`; Chapter
4 in `interdependent-lib/docs/chapter-4.md`. Each chapter is bound by the
license and status vocabulary of the repository that carries it; no theorem,
proof, or empirical status crosses a chapter boundary by citation.*

Chapter 4 drew the map. This chapter walks the territory: **PTCNA**, the
Prime Tensor Circled Neural Architecture — one package, four layers, and two
invariants that the entire design exists to protect.

The architecture did not arrive in this shape. It arrived as three separate
repositories, each with its own four-letter name, its own packaging, and its
own copy of logic the others also needed. The consolidation that produced
this package was not a merge of three things into one container. It was the
recognition that there had only ever been one thing: the repositories were
*layers of a single architecture* that had been mistaken for siblings. The
chapter therefore begins where the repair began — with what the separation
had been costing.

## 5.1 The Dissolution of a Naming Problem

The three predecessor names differed by the transposition of two letters, and
the transposition was live ammunition: internal symbols in one repo carried
the other repo's prefix, aggregation logic that belonged to a layer lived in
the engine of a different layer, and every cross-reference was one
typo away from naming the wrong architecture entirely.

Consolidation dissolved the problem rather than solving it. Inside one
package, the competing four-letter dists become module directories with
ordinary names — `neural`, `circle`, `seed`, `core` — and the historical
acronyms survive only as descriptive expansions in provenance notes. A class
of error was not guarded against but *made inexpressible*: there is no longer
a wrong sibling to import. The lesson generalizes and earns its place in a
textbook: when two names are permanently confusable, the durable fix is
rarely more care — it is a structure in which the distinction no longer needs
to be made.

The repair was honest about its edges. Public class names that carry a
historical prefix but sit in the correct layer were deliberately kept: they
are published API, and they are *true* — the layer they name is the layer
they live in. Renaming them would trade user breakage for cosmetic purity,
and the migration log records the decision rather than hiding it.

## 5.2 The Division Chain and the One Invariant

The four layers form a chain of composition, each layer dividing its
predecessor's tensors into the next aggregate:

```text
neural tensors ──► circles ──► seeds ──► cores
```

Across the chain, exactly one structural invariant holds:

> **Every circle, every seed, and every core is itself a tensor.**

Composition counts are variable — how many neural tensors form a circle, how
many circles a seed, how many seeds a core, are all tunable choices. Any
specific count a realization uses, however meaningful in that realization, is
a parameter and not a law of the architecture. The invariant is deliberately
minimal, and its minimality is the point: because every aggregate is a
tensor, the same composition algebra applies at every level, and the chain
can be extended, audited, and reasoned about with one vocabulary instead of
four. It is Chapter 0's axiom made structural — the tensor is primitive, and
everything built here is an arrangement within it.

## 5.3 The Jurisdiction of the Gradient

The second invariant is a jurisdiction boundary:

> **Back-propagation lives only in the neural layer.**

The neural layer is the sole differentiable layer — the only place gradients
flow, the only place training happens, the only source of weights. The
circle, seed, and core layers are **auditing and timing tensors**: they
observe the neural substrate, aggregate it, and schedule it. They do not
differentiate, and no gradient may be routed through them.

The boundary is enforced at the operator level: differentiability descends
through scalar payloads only, and the composition operator `⊠` never appears
on the autodiff tape — `∂(⊠)` is never taken. Composition is structure, not
computation-to-be-optimized. An implementation that let gradients leak into
an auditing layer would not have extended training; it would have destroyed
the audit, because an auditor whose readings are adjusted by the process it
audits reports nothing. Chapter 2 drew this line for measurement instruments;
here it is drawn inside the architecture itself: the layers that watch must
be causally downstream of the layer that learns, and never the reverse.

## 5.4 fiqs — Two Gradients, Distinguished

The core layer propagates internally, and its propagation is *gated in time*
by structures called **fiqs**, governed by Fick's first law of diffusion:

```text
J = −D ∇φ
```

Flux runs down the gradient of the core's field: `φ` the field, `∇φ` its
gradient, `D` the diffusivity, `J` the resulting flux. Structure diffuses
from where it is concentrated toward where it is not, and the fiqs use that
law to decide *when* a core propagates internally.

The word "gradient" now appears in two claims in this chapter, and the
architecture's clarity depends on never conflating them. The `∇φ` of a fiq
is a **field gradient** — a spatial fact about the arrangement of structure,
driving diffusion, owing nothing to any loss function. The gradient of §5.3
is an **autodiff gradient** — the derivative of an objective, driving
learning, confined to the neural layer. Fick-gated propagation is timing, not
gradient descent. The two mechanisms share a word, an ancestry in calculus,
and nothing else; the non-transfer discipline that the textbook applies
between repositories applies here between homonyms.

## 5.5 Consolidation as Ongoing Honesty

The migration status is recorded in this repository the way Chapter 3
demands: done items named specifically, deliberate non-goals distinguished
from omissions, and remaining items marked `hmmm` rather than rounded up to
complete. Aggregation logic was extracted out of the neural engine into the
layers that own it; the neural layer was swept clean of the historical
prefixes; the seed and core layers were re-identified under the consolidated
name with provenance preserved; and the aggregator upstream was rewired to a
single registry entry. An application server that lived beside a predecessor
was ruled out of scope explicitly — it was infrastructure near the
architecture, not architecture — because a consolidation that absorbs
everything adjacent to its subject has stopped consolidating and started
accumulating.

What this chapter adds to the textbook is the shape of a completed
recognition: three names revealed as one thing, a naming hazard dissolved by
structure, and two invariants — everything is a tensor; only the neural layer
learns — small enough to memorize and strong enough to carry the layers
above, where Chapter 6 will put the architecture to work.

The predecessor repositories are now archived, and the circle layer owns both
its aggregation and the shared `CircleTensor` primitive. The kept historical
class names in the core layer remain a standing compatibility choice — right
layer, published API, revisitable, and recorded so that revisiting it starts
from evidence rather than surprise.

**hmmm — the exact default initialization now has a reviewed UCNS candidate
receipt, but continuous seven-fold geometry and sustained-load behavior across
the complete four-layer seam remain unfalsified.**
