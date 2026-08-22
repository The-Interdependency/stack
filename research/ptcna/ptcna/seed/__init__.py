# ratios: loc_comments=38:26 imports_exports=6:1 calls_definitions=1:0
"""ptcna.seed — the seed layer: circles → seeds (formerly standalone ``pcta``).

Takes local circle-tensors from the circle layer (``ptcna.circle``) and
organizes a
**variable** number of circles into a seed (the seed is itself a tensor),
producing structural **motion** that the core layer (`ptcna.core`) folds into
cores and the inference cap (`zfae`, runtime in `a0`) ultimately consumes
alongside the neural layer's trained weights.

  neural (backprop) ─► circle (neural tensors → circles) ─► seed
  (circles → seeds) ─► core (seeds → cores) ─► a0(zfae) inference

Boundaries (canonical map: `The-Interdependency/interdependent-lib :
docs/prime-tensor-stack.md` — cited, not imported):
  - **Composition counts are variable.** The only invariant is that every
    circle is a tensor and every seed is itself a tensor.
  - composition is **structural / non-differentiable**; back-propagation lives
    only in the neural layer (`ptcna.neural`). Nothing here carries a gradient.
  - naming another repo's terms transfers **no** theorem / proof / empirical
    status. The coherence-prime rule is *mirrored*, never imported.

"Motion" (the structural output a seed hands upward) is formally the Fickian
gradient flux ``J = −D ∇φ`` (Fick's first law) — structure diffusing down its
field gradient; structural / non-differentiable. UCNS integration remains
explicitly suspended until a PTCNA-specific producer profile exists.
"""
from __future__ import annotations

__version__ = "0.1.1"
__author__ = "Erin Patrick Spencer <wayseer@interdependentway.org>"
__license__ = "MPL-2.0"

from .constants import (
    HEPTAGRAM_VERTICES,
    NOMINAL_CIRCLES_PER_SEED,
    SEED_ROUTING_STEP,
    coherence_primes_up_to,
    is_coherence_prime,
    nth_coherence_prime,
)
from .compose import (
    build_seed,
    compose_seed,
    heptagram_order,
    seed_motion,
)
from ..circle import CircleTensor
from .tensor import Seed, SeedMotion
from .audit import seed_audit

__all__ = [
    "__version__",
    # objects
    "CircleTensor",
    "Seed",
    "SeedMotion",
    # composition
    "compose_seed",
    "build_seed",
    "seed_motion",
    "heptagram_order",
    # auditing (extracted from the neural engine)
    "seed_audit",
    # constants / guard
    "NOMINAL_CIRCLES_PER_SEED",
    "HEPTAGRAM_VERTICES",
    "SEED_ROUTING_STEP",
    "is_coherence_prime",
    "coherence_primes_up_to",
    "nth_coherence_prime",
]
# ratios: loc_comments=38:26 imports_exports=6:1 calls_definitions=1:0
