# METAPAT semantic module catalog v2

## Purpose

The catalog makes current METAPAT doctrine addressable without changing canon text.

It contains exactly:

```text
1 root module
12 axiom modules
7 postulate modules
8 theorem modules
12 theory modules
40 modules total
```

Each catalog entry carries a strict `MetapatModuleEnvelope`, doctrine class, claim status, contiguous ordinal, and deterministic module digest. The complete catalog carries the METAPAT canon identity, exact declared derivation relations, and a deterministic catalog digest.

## Identity layers

These identities remain separate:

```text
canon digest
catalog digest
module-envelope provenance digest
catalog-module digest
semantic-relation digest
UCNS geometry identity
Phi authorization digest
EDCM policy and epoch identity
```

A changed statement, source reference, claim status, constraint, unresolved `hmmm`, relation, or canon identity changes the appropriate digest. Catalog identity evidence is not empirical validation or formal proof.

## Claim status

The catalog uses the claims-ledger vocabulary and adds the explicit status:

```text
WORKING-POSTULATE
```

This prevents a postulate from being flattened into either root stipulation or internal theorem. Current classification is:

- root and foundational axioms: `ROOT-STIPULATION`;
- primitive extensions: `DEFINITION`;
- postulates: `WORKING-POSTULATE`;
- theorems: `INTERNAL-DERIVATION`;
- theories 0–9 and 11: `INTERNAL-DERIVATION`;
- theory 10, Symbolic and Memetic Transfer: `CROSS-DOMAIN-HYPOTHESIS`.

Using a module does not transfer its status into an application, measurement, UCNS object, or downstream theorem.

## Relations

The bounded relation vocabulary is:

```text
defines
derived-from
constrains
organizes
applies
constitutive-simultaneous
```

Catalog v2 materializes only exact `Derived from:` declarations already present in `THEORIES.md`. It does not infer relations from similar wording, analogy, order, geometry, carrier size, or repeated terms.

`constitutive-simultaneous` is recognized by the shared vocabulary but is prohibited inside an ordinary catalog unless separately backed by an explicit canon-bound `UCNSForkAuthorization`. A theory ancestry edge is not payload containment.

## Source integrity

Every module statement has a source reference of the form:

```text
FILE.md#heading-slug::statement-N
```

Every relation records both its exact `Derived from:` statement and its section reference. `assert_catalog_sources_match(Path("."))` fails if:

- a source file is absent;
- a declared heading cannot be found;
- an exact statement is absent from its declared section;
- a relation statement drifts from the source section.

The catalog does not replace the canon-bearing Markdown files. It makes their current statements addressable and verifies that the generated representation still resolves to them.

## Package surface

```python
from pathlib import Path
import metapat

catalog = metapat.canonical_semantic_catalog()
metapat.assert_catalog_complete(catalog)
metapat.assert_catalog_sources_match(Path("."), catalog)

module = metapat.semantic_module_by_id("metapat.axiom.4.tensor", catalog)
print(module.claim_status)
print(module.envelope.source_statements)
print(catalog.catalog_digest)
```

The installed package includes:

```text
metapat/fixtures/semantic-module-catalog-v2.json
```

It must remain byte-identical to `canonical_semantic_catalog().to_json()` plus one trailing newline.

## Regeneration

```bash
python tools/generate_catalog.py
python tools/generate_catalog.py --check
python tools/generate_msdmd.py --check
python tools/check_contract_graph.py
python -m pytest -q tests/test_catalog.py tests/test_relations.py
```

The generator writes both the current root-spine envelope and catalog fixtures. Any canon or catalog identity change must update both packaged fixtures, generated msdmd evidence, claims ledger, applications, and consumer migration consequences together.

## Boundaries

The catalog establishes:

- stable semantic addresses;
- exact doctrine text and provenance;
- bounded claim status;
- declared theory ancestry;
- deterministic identity and strict serialization.

It does not establish:

- empirical truth of Meta Energy Theory;
- formal proof of internal theorems;
- EDCM metric values or validity;
- UCNS theorem-status transfer;
- application-specific meaning merely because a module name is reused;
- constitutive payload topology without explicit Phi authorization and downstream object binding.

## hmmm

The first application-module vertical slice should bind the quantum-magnetism note to exact catalog module IDs while preserving its `CROSS-DOMAIN-HYPOTHESIS` status, physical scale distinctions, evidence boundary, and unresolved meanings of “field-space.”
