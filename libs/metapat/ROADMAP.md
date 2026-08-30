# METAPAT Roadmap

## Current state

METAPAT is the canonical semantic authority for Meta Energy Theory. It exposes:

- exact root canon constants and byte-complete deterministic canon identity;
- immutable, strictly validated `MetapatModuleEnvelope` records;
- a complete addressable semantic catalog of 40 doctrine modules and 52 exact declared derivation edges;
- strict semantic-relation records with bounded claim status and deterministic identity;
- strict catalog-bound application modules with explicit evidence firewalls;
- a source-checked quantum-magnetism application fixture bound to twelve exact catalog modules;
- deterministic canon, catalog, and application contract checks with explicit non-validation boundaries;
- an optional adapter that constructs actual `ucns.UCNSObject` geometry while retaining the complete semantic envelope in a serializable record;
- an explicit canon-bound Phi policy that may authorize ordered simultaneous constitutive children without inferring semantics from geometry;
- a source-CONTRACTS/test-CHECKS audit and generated msdmd collection;
- package, wheel, base, canon-integrity, catalog-integrity, application-integrity, Phi-policy, and actual-UCNS integration gates.

## Architecture

Authority:

```text
METAPAT canon
    |
    +-- addressable catalog constrains terms, interpretation, derivation, and claim status
    |
    +-- application modules bind domain uses to exact catalog identities and evidence limits
    v
UCNS adapters and EDCM consumers
```

Runtime:

```text
source evidence -> EDCM parsing -> actual UCNS representation -> EDCM readouts
                                     ^
                                     |
                          METAPAT-derived semantic constraints
```

Proof status does not transfer from UCNS into METAPAT ontology or EDCM measurement validity.

## Phase 0 — Canon stability

Status: implemented and continuously required.

- Preserve Chapter Zero and exact root strings.
- Keep root/tool/domain separation.
- Bind consumers to `CANON_VERSION`, `CANON_IDENTITY_SCHEMA_VERSION`, `canon_digest()`, and the complete canon-file manifest.
- Fail closed when any canon-bearing Markdown file changes without an explicit manifest update.
- Check repeated root-spine text against `AXIOMS.md` and `CHAPTER_ZERO.md` rather than protecting inconsistent copies independently.
- Keep unresolved details marked `hmmm`.
- Classify public claims in `docs/claims-ledger.md`.

## Phase 1 — Semantic module envelope

Status: implemented at schema `1.2.0`.

- `MetapatModuleEnvelope` is immutable and versioned.
- Exact source references and statements survive serialization.
- The root spine is a neutral `canon-module`; it is not classified as a simplex by constructor convenience.
- Constraints, permitted interpretations, unresolved constraints, canon identity, and provenance digest remain distinct.
- Unknown, missing, or incorrectly typed schema fields fail closed.
- Canon or constraint rotation changes provenance identity.
- No measured EDCM values are present.
- The canonical root-spine fixture is packaged and checked against the live constructor.

## Phase 2 — Addressable semantic module catalog

Status: implemented at catalog schema `1.0.0` and catalog version `metapat-semantic-catalog-v2`.

- Catalog v2 contains exactly one root, twelve axioms, seven postulates, eight theorems, and twelve theories.
- Every module has a stable ID, contiguous ordinal, doctrine class, bounded claim status, exact envelope, and deterministic module digest.
- `WORKING-POSTULATE` keeps revisable postulates distinct from root stipulations and internal derivations.
- Theory 10 remains `CROSS-DOMAIN-HYPOTHESIS`; ordinary theorem and theory derivations do not inherit formal-proof status.
- Fifty-two `derived-from` edges reproduce exact declarations already present in `THEORIES.md`.
- Every relation binds exact source text, evidence status, unresolved constraints, and a deterministic relation digest.
- Source verification fails if a file, heading, exact statement, or `Derived from:` declaration drifts.
- Catalog construction rejects inferred `constitutive-simultaneous` relations without a separate `UCNSForkAuthorization`.
- The packaged `semantic-module-catalog-v2.json` fixture must remain byte-current with the live constructor.

Remaining:

- hmmm: define migration consequences for future catalog or canon rotations.
- hmmm: decide whether non-theory declared relations require additional relation kinds in a later catalog version.

## Phase 3 — Actual UCNS geometry adapter and Phi authority

Status: adapter implemented for ordered statement-count geometry; semantic authorization implemented at policy `1.0.0`.

- Base METAPAT remains importable without UCNS.
- Adapter calls without UCNS raise a clear dependency error.
- Adaptation constructs actual `ucns.UCNSObject` instances.
- Stable hash and UCNS serialization version are recorded.
- Exact statements, references, constraints, permitted interpretations, and unresolved `hmmm` survive in a strict serializable record.
- The adapter default remains `external-provenance`; METAPAT statements remain outside UCNS payloads and UCNS payloads remain unit.
- METAPAT contains no local normalization, product, factorization, star/disk-flip, or theorem-status algebra.
- `UCNSPhiPolicy` requires explicit authorization and permits only the `constitutive-simultaneous` relation.
- `UCNSForkAuthorization` binds parent identity, ordered child identities, source references, canon identity, policy version, unresolved constraints, and a deterministic authorization digest.
- Temporal succession, adjacency, provenance, alternatives, fiq connectivity, external symmetry action, arbitrary association, catalog ancestry, and application binding remain prohibited as payload-containment meanings.
- Phi policy and authorization records transfer no theorem status and make no METAPAT validity claim.

Remaining:

- hmmm: define the downstream topology-binding record for exact UCNS parent identity, payload path, ordered child hashes, authorization digest, and encoding-policy version.
- hmmm: add a fail-closed linter that rejects missing declarations, order drift, object-hash drift, canon drift, and external-edge-as-containment substitution.
- hmmm: consume an official versioned UCNS bridge record if UCNS standardizes one.
- hmmm: ratify any semantic mapping beyond default external provenance and explicitly authorized constitutive-simultaneous forks.

## Phase 4 — Evidence and metadata integrity

Status: implemented as a standing gate.

- Source modules own `CONTRACTS`; tests own `CHECKS`.
- `tools/check_contract_graph.py` audits without imports and is negative-tested.
- `metapat_msdmd.ts` is generated from bounded product surfaces through the pinned collector.
- `tools/generate_catalog.py --check` verifies the packaged catalog fixture.
- Catalog source checks resolve exact statements against canon sections.
- `tools/generate_application_fixtures.py --check` verifies packaged application fixtures.
- Application checks validate exact catalog bindings and exact source statements.
- `COMPLIANCE.md` names the current pin, commands, evidence boundaries, and downstream exclusion.
- CI enforces graph closure, generated metadata freshness, complete canon-file integrity, catalog integrity, application integrity, explicit Phi-policy tests, packaged fixture identity, ordinary tests, builds, and wheel smoke checks.

## Phase 5 — Application-module vertical slices

Status: first vertical slice implemented at application schema `1.0.0`.

The quantum-magnetism application now:

- binds twelve applied METAPAT terms to exact catalog module IDs, module digests, and declared claim statuses;
- retains `CROSS-DOMAIN-HYPOTHESIS` status and root impact `none`;
- distinguishes nuclear, atomic, crystalline, and magnetic-domain scales;
- preserves what transfers and what does not transfer;
- keeps physics evidence answerable to physics;
- deliberately excludes Theory 10;
- preserves unresolved “field-space” meaning as `hmmm`;
- packages a deterministic source-checked fixture;
- makes every ontology, domain, measurement, theorem-transfer, and UCNS-topology validation field false.

Remaining:

- hmmm: define physical variables and boundaries precisely enough to test the mapping.
- hmmm: produce predictions that differ from a restatement of established physics.
- hmmm: compare those predictions with experimental or computational evidence.
- hmmm: add later application modules only with separate source, status, and domain evidence declarations.

## Phase 6 — EDCM semantic consumer

Status: separate downstream implementation required.

EDCM must:

- accept the exact versioned catalog module, application module, or envelope;
- retain catalog digest, module digest, application digest, canon digest, source refs, statements, constraints, permitted interpretations, unresolved `hmmm`, and provenance digest;
- keep semantic labels separate from metric values;
- preserve UCNS geometry identity, EDCM policy identity, METAPAT canon and catalog identity, application identity, and any Phi authorization identity as separate provenance components;
- create a new epoch when canon, catalog, application policy, or measurement policy identity changes;
- fail closed on malformed schema or provenance.

## Phase 7 — Shared stack fixture

Status: hmmm / next cross-repository gate after a downstream consumer exists.

The deterministic fixture must prove:

1. METAPAT root canon remains byte-stable;
2. catalog, application, and envelope round-trip without loss;
3. selected modules and application statements resolve to exact source;
4. an actual UCNS object is constructed;
5. stable hash and complete semantic provenance survive adaptation;
6. EDCM consumes constraints without making them metric values;
7. theorem status does not transfer;
8. `hmmm` fields survive the complete path;
9. canon, catalog, application, or policy rotation produces a distinct epoch identity;
10. any constitutive fork is backed by a valid METAPAT authorization and exact UCNS topology binding.

## hmmm

Catalog v2 now has one complete application-module vertical slice. Application provenance is implemented; physics validation is not. The topology-bound Phi fixture and EDCM consumer remain cross-repository work.
