# METAPAT claims ledger

Date: 2026-07-21

This ledger classifies public doctrine and executable assertions without changing Erin Spencer's canon text. Executable checks of definitions and encoded conditions are contract tests; they are not independent empirical evidence, formal proof, or validation of Meta Energy Theory as external truth.

## Status vocabulary

```text
ROOT-STIPULATION
DEFINITION
WORKING-POSTULATE
INTERNAL-DERIVATION
IMPLEMENTED-CONTRACT
CROSS-DOMAIN-HYPOTHESIS
EMPIRICAL-FRONTIER
RETRACTED_OR_SUPERSEDED
```

`WORKING-POSTULATE` names a revisable commitment that organizes application but may not rewrite root axioms. It was added so postulates are not flattened into either root stipulations or internal theorem claims.

## Root canon and doctrine classes

| Statement or surface | Status | Source | Boundary |
|---|---|---|---|
| “Legible difference is distinction.” | ROOT-STIPULATION | `AXIOMS.md`, `CHAPTER_ZERO.md`, `metapat.canon.ROOT_SPINE[0]` | Substrate-independent canon; not inferred from UCNS or EDCM. |
| “Distinction defines boundaries.” | ROOT-STIPULATION | same root sources | Canon statement. |
| “Boundaries define simplex.” | ROOT-STIPULATION | same root sources | Canon statement. |
| “Boundary is simplex of distinction.” | ROOT-STIPULATION | same root sources | Canon statement. |
| “Simplex holds or modifies energy in a state of being.” | ROOT-STIPULATION | same root sources | Canon statement. |
| Tensor as primitive simultaneous arrangement of energy-states | DEFINITION | `AXIOMS.md`, `metapat.canon.PRIMITIVE_EXTENSION` | Definition; deterministic tests only preserve encoding. |
| Time as sequential tensor alteration | DEFINITION | `AXIOMS.md`, `metapat.canon.TIME_DEFINITION` | Definition; no empirical theory of time is established by a boolean helper. |
| Registration | DEFINITION | `GLOSSARY.md`, `metapat.canon.definitions()` | Distinct from time and consciousness. |
| Observer role | DEFINITION | `GLOSSARY.md`, `metapat.canon.definitions()` | Observer does not necessarily mean mind. |
| Question as bounded unresolved energy-state | DEFINITION | root documents, `metapat.canon.definitions()` | Definition; unresolved questions remain unresolved. |
| Seven current postulates | WORKING-POSTULATE | `POSTULATES.md`, catalog modules `metapat.postulate.1` through `.7` | Revisable application commitments; may not rewrite axioms or inherit proof status. |
| Eight current theorems | INTERNAL-DERIVATION | `THEOREMS.md`, catalog modules `metapat.theorem.1` through `.8` | Internal reductions and proof sketches, not formal or empirical proofs. |
| Theories 0–9 and 11 | INTERNAL-DERIVATION | `THEORIES.md`, corresponding catalog modules | Organized application lenses reducible to current doctrine; remain demotable. |
| Theory 10, Symbolic and Memetic Transfer | CROSS-DOMAIN-HYPOTHESIS | `THEORIES.md`, `metapat.theory.10.symbolic_and_memetic_transfer` | Remains application-layer pending symbolic vertex tables, receiver tests, and UCNS-gonol mappings. |

## Internal derivations and checks

| Surface | Status | What it checks | What it does not establish |
|---|---|---|---|
| `boundary_earns_its_keep` | INTERNAL-DERIVATION plus IMPLEMENTED-CONTRACT | With supplied source/target held present, changed boundary and changed outcome satisfy the encoded condition. | Causal truth, empirical validation, theorem proof. |
| `tensor_precedes_time` | INTERNAL-DERIVATION plus IMPLEMENTED-CONTRACT | A tensor value is present and an ordered alteration sequence has at least two states. | Metaphysical or physical proof of temporal priority. |
| `registration_is_not_time` | INTERNAL-DERIVATION plus IMPLEMENTED-CONTRACT | Sequence may exist without registration; supplied registration preserves the sequence exactly. | Empirical validation of time or registration. |
| `observer_role_by_registration` | INTERNAL-DERIVATION plus IMPLEMENTED-CONTRACT | Supplied simplex record preserves the supplied sequence. | Mind, consciousness, intent, or lived observer status. |
| `consciousness_is_optional` | INTERNAL-DERIVATION plus IMPLEMENTED-CONTRACT | A non-conscious registration value is present whether or not a separate conscious story is supplied. | Detection or proof of consciousness. |

## Implemented architecture and evidence contracts

| Surface | Status | Contract |
|---|---|---|
| `metapat.canon.canon_digest()` | IMPLEMENTED-CONTRACT | Deterministically identifies the exact importable canon surface and complete canon-file manifest. |
| `CANON_FILE_BLOBS` and `assert_canon_files_match()` | IMPLEMENTED-CONTRACT | Bind every canon-bearing Markdown file byte-for-byte and fail closed on drift or absence. Git SHA-1 is used only as repository blob identity; aggregate identity is SHA-256. |
| `MetapatModuleEnvelope` | IMPLEMENTED-CONTRACT | Immutable schema `1.2.0` semantic-authority and provenance envelope; exact references, statements, constraints, permitted interpretations, unresolved `hmmm`, canon identity, and provenance digest survive strict serialization. |
| `MetapatModuleRelation` | IMPLEMENTED-CONTRACT | Strict schema `1.0.0` record with bounded relation kind, evidence status, exact endpoints and source provenance, unresolved constraints, and deterministic digest; no theorem or measurement status transfer surface. |
| `MetapatSemanticCatalog` | IMPLEMENTED-CONTRACT | Catalog schema `1.0.0` contains exactly 40 ordered modules and 52 exact source-declared derivation edges, binds canon identity, round-trips strictly, and rejects undeclared or inferred constitutive containment. |
| `assert_catalog_complete()` | IMPLEMENTED-CONTRACT | Fails unless doctrine counts are exactly root 1, axioms 12, postulates 7, theorems 8, and theories 12. |
| `assert_catalog_sources_match()` | IMPLEMENTED-CONTRACT | Resolves every module and relation statement against its exact declared Markdown section and fails on source drift. |
| `tools/generate_catalog.py` | IMPLEMENTED-CONTRACT | Generates or checks the packaged `root-spine-envelope-v2.json` and `semantic-module-catalog-v2.json` fixtures byte-for-byte. |
| `ApplicationCatalogBinding` | IMPLEMENTED-CONTRACT | Binds exact catalog module ID, digest, claim status, application role, and application statement without altering the module or transferring status. |
| `MetapatApplicationModule` | IMPLEMENTED-CONTRACT | Strict schema `1.0.0` preserves domains, scales, source, catalog identity, bindings, transfer limits, evidence requirements, unresolved `hmmm`, and explicit false validation/status-transfer fields. |
| `validate_application_against_catalog()` | IMPLEMENTED-CONTRACT | Fails on catalog version or digest drift and on any bound module identity, digest, or claim-status mismatch. |
| `assert_application_sources_match()` | IMPLEMENTED-CONTRACT | Resolves every identity, binding, mapping, transfer, evidence, and `hmmm` statement against the exact application Markdown section. |
| `quantum_magnetism_application_module()` | IMPLEMENTED-CONTRACT | Emits the first source-checked catalog-bound application fixture with twelve exact bindings and `CROSS-DOMAIN-HYPOTHESIS` status. |
| `tools/generate_application_fixtures.py` | IMPLEMENTED-CONTRACT | Generates or checks the packaged quantum-magnetism and three-phase electromagnetic-pipe application fixtures byte-for-byte. |
| `metapat.ucns.adapt_envelope_to_ucns` | IMPLEMENTED-CONTRACT | Constructs an actual `ucns.UCNSObject`; keeps METAPAT statements as external provenance; retains the complete semantic envelope; transfers no theorem status. |
| `DEFAULT_UCNS_PHI_POLICY` | IMPLEMENTED-CONTRACT | Keeps `external-provenance` as default, requires explicit authorization for a semantic fork, permits only `constitutive-simultaneous`, and transfers no theorem or validity status. |
| `UCNSForkAuthorization` and `authorize_constitutive_fork` | IMPLEMENTED-CONTRACT | Bind exact parent module, ordered child modules, canon digest, source references, policy version, unresolved constraints, and authorization digest. The record does not prove downstream topology. |
| `validate_fork_authorization` | IMPLEMENTED-CONTRACT | Fails closed on parent, child-order, canon, source-reference, policy, relation-kind, or digest mismatch. It does not inspect an actual UCNS payload path. |
| `tools/check_contract_graph.py` | IMPLEMENTED-CONTRACT | Reconciles source `CONTRACTS` and test `CHECKS` without imports and reports planted graph defects. |
| `tools/generate_msdmd.py` | IMPLEMENTED-CONTRACT | Generates the committed product metadata graph through the pinned skill-lib collector and excludes vendored skill declarations. |
| Package and wheel gates | IMPLEMENTED-CONTRACT | Installed public surface, metadata, typing marker, all packaged fixtures, catalog and application identity, Phi policy, and optional actual-UCNS integration work as declared. |

## Cross-domain and empirical status

| Claim family | Status | Boundary |
|---|---|---|
| Applying METAPAT terms to a particular scientific, organizational, psychological, or AI domain | CROSS-DOMAIN-HYPOTHESIS unless separately demonstrated | Catalog or application-module addressability does not make the application root, theorem, measurement, or empirical result. |
| A catalog module correctly reproduces the exact current source statement and declared status | IMPLEMENTED-CONTRACT | This establishes addressability and provenance only, not external truth. |
| A catalog `derived-from` edge correctly reproduces a `THEORIES.md` declaration | IMPLEMENTED-CONTRACT | This records declared semantic ancestry, not formal proof of the derivation. |
| Quantum-magnetism catalog bindings and source-current fixture | IMPLEMENTED-CONTRACT | Establish exact provenance and evidence limits only; physics validity remains a CROSS-DOMAIN-HYPOTHESIS. |
| Quantum-magnetism physical interpretation and predictive adequacy | CROSS-DOMAIN-HYPOTHESIS / EMPIRICAL-FRONTIER | Requires precise scale and boundary definitions, explicit physical-variable mapping, distinguishing predictions, and experimental or computational comparison. |
| Explicitly authorized ordered children are simultaneous constitutive components of one semantic parent | IMPLEMENTED-CONTRACT as a METAPAT declaration | The authorization records declared meaning and provenance; it does not establish that an actual UCNS fixture encodes the topology correctly. |
| Binding a `UCNSForkAuthorization` to exact UCNS parent identity, payload path, ordered child hashes, and encoded topology | EMPIRICAL-FRONTIER / hmmm | Requires a downstream topology-binding schema and fail-closed linter. Geometry cannot supply missing semantic child identities by itself. |
| Mapping METAPAT statements into UCNS payload or tag semantics outside an explicit constitutive authorization | EMPIRICAL-FRONTIER / hmmm | Current adapter remains external provenance with unit payloads. No broader payload or tag meaning is ratified. |
| EDCM measurements corresponding to METAPAT semantic labels | EMPIRICAL-FRONTIER | Labels constrain interpretation; they are not measured values. |
| Claims that contract tests validate the ontology externally | RETRACTED_OR_SUPERSEDED | Tests protect encoded contracts only. |
| Claims that catalog membership promotes a statement's claim status | RETRACTED_OR_SUPERSEDED | Catalog modules retain declared status; addressability transfers no status. |
| Claims that application binding validates a domain claim | RETRACTED_OR_SUPERSEDED | Binding establishes identity, provenance, and evidence boundaries only. |
| Claims that UCNS theorem status proves METAPAT ontology | RETRACTED_OR_SUPERSEDED | Proof-status transfer is forbidden. |

## Superseded architecture statements

| Former surface | Status | Replacement |
|---|---|---|
| Single flow `UCNS -> METAPAT -> EDCM` | RETRACTED_OR_SUPERSEDED | Separate authority, runtime-data, and proof-status flows in `metapat.flow_plan`. |
| METAPAT-native `UCNSObject`, normalization, carrier calculation, and composition | RETRACTED_OR_SUPERSEDED | Optional adapter to the actual `ucns` package; no second algebra. |
| `call:` fields inside source `CONTRACTS` | RETRACTED_OR_SUPERSEDED | Test-owned `CHECKS` entries with `proves:` and `self::` resolution. |
| Importable-constants-only canon digest | RETRACTED_OR_SUPERSEDED | Identity schema `2.0.0` binds the complete canon-file manifest alongside importable constants. |
| Root spine classified as a `simplex` by constructor convenience | RETRACTED_OR_SUPERSEDED | Schema `1.2.0` classifies the root spine as a neutral `canon-module`; simplex claims require their own source authority. |
| Postulates implicitly sharing theorem or root status | RETRACTED_OR_SUPERSEDED | `WORKING-POSTULATE` explicitly preserves revisability and non-root status. |
| Whole documents required as the only machine-addressable semantic surface | RETRACTED_OR_SUPERSEDED | Catalog v2 supplies stable module IDs, exact source resolution, claim status, and deterministic identity without replacing canon files. |
| Free-form application labels sufficient for downstream use | RETRACTED_OR_SUPERSEDED | Application schema `1.0.0` requires exact catalog module identities, digests, statuses, source statements, and explicit evidence boundaries. |
| “theorem validation helpers” wording | RETRACTED_OR_SUPERSEDED | Deterministic canon contract checks with explicit non-validation boundaries. |
| All payload, tag, and external-provenance semantics described as wholly unresolved | RETRACTED_OR_SUPERSEDED | Default adapter mapping is external provenance; explicit canon-bound `constitutive-simultaneous` authorization is ratified; topology binding and broader semantic mappings remain unresolved. |

## Usage

When adding or changing a public claim:

1. cite the exact source statement or executable surface;
2. assign one status from this ledger;
3. state what evidence would change that status;
4. update affected catalog or application declarations, fixtures, code metadata, documentation, tests, generated msdmd, and canon manifest as applicable;
5. preserve unresolved constraints as `hmmm`.

## hmmm

Catalog v2 can name current doctrine and declared ancestry without guessing. The first application vertical slice demonstrates that catalog reuse preserves the quantum-magnetism note's cross-domain status rather than laundering it into canon, proof, measurement, or UCNS topology. Physics evidence remains unresolved and external.
