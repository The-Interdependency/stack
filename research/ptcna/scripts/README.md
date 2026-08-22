# scripts

Verification annexes that are not part of the packaged `ptcna` suite.

- `proof_check.py` — spectral-graph analysis of single-offset circulant
  topologies on `n = 7` (eigenvalues, spectral gap, BFS diameter). Relocated
  verbatim from `The-Interdependency/pcna:proof_check.py` (pcna@e384b32) during
  the 2026-07-28 archival sweep. Requires `numpy` and `scipy`; run directly with
  `python scripts/proof_check.py`.

  **What it does and does not show:** for `n = 7`, the offset-1 ring and the
  offset-3 "heptagram" are isomorphic circulant graphs (relabel vertex `i` as
  `3i mod 7`), so their spectra, spectral gap, and diameter are identical — and
  the script's output confirms exactly that. It is therefore a
  relabeling-equivalence check on the two adjacency descriptions, **not**
  empirical evidence for choosing 7:3 over 7:1. Any property that actually
  distinguishes the routing choices (e.g., multi-offset neighborhoods or
  stride interaction with larger prime rings) would need a different
  comparison. Preserved verbatim as provenance; no theorem status is claimed
  or transferred.
