# Changelog

## Unreleased

- Consumed the exact UCNS `157×7×7×53` candidate-state receipt from merged
  producer commit `b7b6f35cce69c273860923489a1c8b5372d14eb0`.
- Added independent state materialization verification and fail-closed receipt
  tamper rejection; shapes outside the receipt remain locally attributed.
- Added a public `PTCNAEngine` receipt spanning neural, circle, seed, and core.
- Added a deterministic hashed-linear fallback behind the same task interface.
- Added explicit, attributed fallback routing; target failures still raise by
  default.
- Added immutable evaluation plans and terminal evidence receipts that freeze
  workload, training schedule, comparator, post-training metric, thresholds,
  resource limits, stopping, and failure propagation before execution.
- Removed the broken deprecated FastAPI seed runner that imported nonexistent
  `src.core` modules; `PTCNARuntime` is its supported replacement.

## 0.1.1 — 2026-07-29

- Added the shared `ptcna.circle.CircleTensor` and one structural composition
  path across circle, seed, and core layers.
- Moved reverse-mode scalar ownership to `ptcna.neural.NeuralScalar`; core and
  fiq objects are now opaque, non-differentiating structural hosts.
- Made seed/core composition counts variable and preserved neural payloads
  without transferring gradient ownership.
- Added a typed, fail-closed suspended UCNS integration boundary.
- Removed `ptcna.neural.edcm`; Zeta now consumes an explicitly injected
  external measurement provider or reports measurement suspension.
- Added repository-local doctrine, machine-readable work-graph inputs,
  executable contracts, drift collection, and release gates.

## 0.1.0 — 2026-07-28

- Consolidated the neural, circle, seed, and core architecture into the
  `ptcna` package.
