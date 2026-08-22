# ratios: loc_comments=69:94 imports_exports=3:3 calls_definitions=20:6
"""Composition routing and the coherence-prime guard.

`ptcna.seed` (formerly the standalone `pcta` repo — PCTA, Prime Circled Tensor
Architecture) is the **seed layer** of the prime-tensor stack: it covers circles
represented by the shared local `ptcna.circle.CircleTensor` and composes them
into **seeds**. The single source of
truth for the stack's role-and-boundary map is
`The-Interdependency/interdependent-lib : docs/prime-tensor-stack.md` — this
repo *cites* it and does not import it. No theorem / proof / empirical status
moves between repos by naming these terms.

What is canonical here:
  - the neural layer (`ptcna.neural`, the only back-propagating layer) produces
    neural tensors; the circle layer (`ptcna.circle`) divides them into
    **circles** (each circle is itself a tensor) and offers those circles here;
    **the seed layer composes circles into seeds** (each seed is itself a
    tensor) and offers those seeds to the core layer (`ptcna.core`), which
    composes seeds into **cores** for `a0(zfae)`.
  - **Composition counts are VARIABLE.** The number of circles in a seed is not
    fixed — the only invariant is that every circle is a tensor and every seed is
    itself a tensor. (`HEPTAGRAM_VERTICES` / `SEED_ROUTING_STEP` describe the
    routing *motif*, not a required circle count.)
  - The composition is **structural / non-differentiable** — back-propagation
    lives ONLY in the neural layer. The seed layer organizes; it does not train.

"Motion" — the structural / phase-harmonic output a seed hands upward — is
formally the **Fickian gradient flux** ``J = −D ∇φ`` (Fick's first law:
structure diffuses down its field gradient). It is structural / non-differentiable
(the ``∇φ`` is a field gradient, not an autodiff gradient). A
PTCNA-specific UCNS higher-gonol producer profile remains `hmmm`; local
composition makes no UCNS claim.
"""
from __future__ import annotations

import threading
from typing import List

# === MODULE_BUILD ===
# id: seed_constants
#   module_name: constants
#   module_kind: engine
#   summary: seed-layer heptagram routing motif and the recursive coherence-prime guard (composition counts are variable)
#   owner: Erin Patrick Spencer
#   public_surface: NOMINAL_CIRCLES_PER_SEED, SEED_ROUTING_STEP, HEPTAGRAM_VERTICES, is_coherence_prime, coherence_primes_up_to, nth_coherence_prime
#   internal_surface: _build_coherence_up_to, _is_prime, _prime_factors
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_constants
#   rollout: default_enabled (imported by seed.compose via ptcna.seed.__init__)
#   rollback: none (greenfield module; revert the file)
#   requires: coherence_primes (mirrored from interdependent_lib, NOT imported — importing the aggregator would invert the dependency graph)
#   since: 2026-06-05 (greenfield scaffold of the seed package, pre-consolidation `pcta`)
#   unresolved: none (PCTA acronym, variable-count rule, and "motion" = Fickian flux J = −D ∇φ all resolved by maintainer)
# === END MODULE_BUILD ===

# --- routing motif (NOT a required circle count) -----------------------------
# Composition counts are variable: a seed may carry any number of circles, the
# only invariant being that every circle is a tensor and the seed is itself a
# tensor. The heptagram is the routing *motif* (7 phase vertices), not a cap on
# how many circles a seed composes.
HEPTAGRAM_VERTICES: int = 7   # heptagram phase vertices (routing motif)
NOMINAL_CIRCLES_PER_SEED: int = 7  # nominal heptagram base case; NOT a hard limit

# --- routing step ------------------------------------------------------------
# {n/3} assigns the star-polygon anchor order over however many circles a seed
# carries. For the nominal n=7 case this is the {7/3} heptagram, mirroring
# `ptcna.core.prime_core`'s SEED_ROUTING_STEP; the circle-level step ({7/2},
# tensors -> circle) belongs to the circle layer (`ptcna.circle`), not here.
SEED_ROUTING_STEP: int = 3

# --- coherence-prime ladder (consciousness primes) ---------------------------
# Prime-consciousness theory: primes whose (p-1) factorization is square-free are
# more likely to fall into stability as part of a triadic recursion set. The
# membership rule encodes that as a *recursive* test: a prime's kernel (p-1)//4
# must be square-free and factor only into earlier coherence primes (genealogical
# ancestry), not into a fixed pre-listed universe. A frozen-universe cap silently
# disagrees with this rule for the first time at p=4373, whose kernel 1093 is
# itself a coherence prime above any small cap.
#
# CANON: the single source of truth for this sequence is
#   interdependent_lib.coherence_primes  (The-Interdependency/interdependent-lib)
# `ptcna` cannot import it — interdependent-lib optionally depends on the leaf
# libraries, so importing the aggregator here would invert the dependency graph.
# The recursive algorithm is therefore mirrored verbatim; behaviour MUST match
# canon, whose shared test oracle includes the p=4373 regression.
_COHERENCE_BASE = frozenset({3, 5, 7})
_coherence_known: set = set(_COHERENCE_BASE)
_coherence_scanned_to: int = max(_COHERENCE_BASE)
# Guards the shared cache below. The membership *rule* is the verbatim mirror of
# interdependent_lib.coherence_primes; this lock only makes the cache build
# thread-safe (results are identical to the single-threaded mirror).
_coherence_lock = threading.Lock()


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def _prime_factors(n: int) -> List[int]:
    factors: List[int] = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def _build_coherence_up_to(limit: int) -> None:
    """Admit every coherence prime ``<= limit`` in ascending order so the
    recursive ancestry check can consult the already-admitted set. Idempotent:
    ``_coherence_scanned_to`` guards against re-scanning."""
    global _coherence_scanned_to
    if limit <= _coherence_scanned_to:                  # fast path, no lock
        return
    with _coherence_lock:
        if limit <= _coherence_scanned_to:              # re-check inside the lock
            return
        for p in range(_coherence_scanned_to + 1, limit + 1):
            if not _is_prime(p) or p in _COHERENCE_BASE or (p - 1) % 4 != 0:
                continue
            factors = _prime_factors((p - 1) // 4)
            if len(set(factors)) != len(factors):       # square-free
                continue
            if set(factors) <= _coherence_known:        # recursive ancestry
                _coherence_known.add(p)
        _coherence_scanned_to = limit


def is_coherence_prime(p: int) -> bool:
    """Coherence-prime membership test.

    ``p`` is a coherence prime iff either:
      - ``p`` is in the base set ``{3, 5, 7}``, or
      - ``p`` is prime, ``p % 4 == 1``, ``q = (p - 1) // 4`` is square-free, and
        every prime factor of ``q`` is itself a coherence prime (recursive).

    Mirrors ``interdependent_lib.coherence_primes`` exactly — see the CANON note
    above. The ladder begins 3, 5, 7, 13, 29, 53, 61, 157, 349, 421, ...
    """
    if p < 2:
        return False
    if p in _COHERENCE_BASE:
        return True
    if not _is_prime(p) or p % 4 != 1:
        return False
    _build_coherence_up_to(p)
    return p in _coherence_known


def coherence_primes_up_to(limit: int) -> List[int]:
    """Ascending list of coherence primes ``<= limit`` (base set included)."""
    if limit < 0:
        return []
    _build_coherence_up_to(limit)
    return sorted(p for p in _coherence_known if p <= limit)


def nth_coherence_prime(n: int) -> int:
    """The ``n``-th coherence prime, 0-indexed (``nth_coherence_prime(0) == 3``).

    Used to address seeds on the coherence ladder. This helper only enumerates
    the ladder; it asserts no composition count (those are variable — every
    composed object is simply itself a tensor).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    limit = 16
    while True:
        ladder = coherence_primes_up_to(limit)
        if len(ladder) > n:
            return ladder[n]
        limit *= 2
# ratios: loc_comments=69:94 imports_exports=3:3 calls_definitions=20:6
