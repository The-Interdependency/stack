# URPCS Möbius projection v0 — bounded measurement

Classification: **DISTINCTION_ABSENT_IN_BOUNDED_DOMAIN**.

This is a read-only measurement of UCNS native Möbius state already derivable from authenticated URPCS v1 witnesses. It is not a traversal profile and does not modify the frozen URPCS v1 wire or codec behavior.

## Exact evidence identity

- Canonical receipt SHA-256: `34950d37dbf882cd6de331a98a555862c57edddc3749512c75db180d0539a6eb`
- Receipt payload SHA-256: `b2e83d932102ad5c10748a0e03eb3c3b205a147d14bb6fe9d5e668f1be0f8da2`
- Aggregate result SHA-256: `b83a6bbfe1223f047c9d4e96ae8b105cb305129dc2eb9fc7a64efd9f5f4290e2`
- Input domain SHA-256: `1de7d25896deb06106ef73249baaca15e559e804e352fabcf460f3bdace1d506`
- Stack input commit/tree: `2fadd145db09e352f84146fa490be03dbfa708d4` / `1d0aa08624ccb6c618b852779b5f1688514f8cdc`
- UCNS commit/law: `4086ab82399c4d142b0eacfbc09e0a69ed151aa5` / `ucns.native-mobius-root-loop@1.0.0`
- skill-lib commit: `abd259b4722901317e4388d774a20d6819d959c2`

## Complete bounded domain

The run completed all **514** cases in `({epsilon} union {00,...,ff}) x (R_cap in {0,1})` under the frozen vector state and associated data.

| Record class | States | Phase buckets | (phase, frame) buckets | Opposite-frame phase splits | Records in split buckets | Maximum S | Maximum q |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gonol | 288615 | 3 | 3 | 0 | 0 | 2 | 0 |
| Member | 546956 | 6 | 6 | 0 | 0 | 6 | 0 |

Phase is represented canonically as `(r,M)` and all projection arithmetic is exact. The canonical JSON retains every source-case and structural identifier in each opposite-frame phase split using the documented lossless record encoding.

Gonol and occurrence identifiers distinguish structural objects only within their declared message/session construction. Native complete local state intentionally does not retain absolute winding count: for example, `S=2` and `S=18` have the same phase and frame at `M=8`. URPCS-derived displacements in this run are nonnegative; negative values occur only in mathematical conformance fixtures.

## Authentication and interpretation boundary

KMAC256 authenticates `C_0` before witness recovery, body parsing, or plaintext reconstruction. The frame is public and deterministically derived from authenticated witness rows. It supplies no entropy or confidentiality and adds no replay protection, rollback resistance, or state-reuse protection. Same-phase/opposite-frame observations are **opposite-frame phase splits**: visible phases coincide while complete local states remain distinct.

## Explicit nonclaims

This work does not establish traversal utility, compression, entropy, confidentiality, encryption security, IND-CPA or IND-CCA security, production suitability, PCEA compatibility, UCNS-gonol identity, UCHC cache behavior, absolute winding recovery, release authority.

## hmmm

No opposite-frame phase split occurred in the complete bounded domain, so integration ends for this bounded profile. Whether such a distinction exists outside this fixed harness remains unresolved and authorizes no traversal change.
