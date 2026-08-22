# METAPAT application modules

## Purpose

Application modules bind domain-specific uses of METAPAT to exact catalog modules without amending canon or transferring claim status.

A `MetapatApplicationModule` carries:

- application identity and version;
- application claim status;
- named domains and selected scales;
- exact source document references and statements;
- exact catalog version and digest;
- ordered catalog bindings;
- domain statements and shared question-form;
- what transfers and what does not;
- working question;
- evidence boundary and requirements;
- unresolved `hmmm`;
- explicit false status-transfer and validation fields;
- deterministic application digest.

## Catalog bindings

Each `ApplicationCatalogBinding` binds:

```text
catalog module id
catalog module digest
catalog module claim status
application role
application statement
binding digest
```

A binding states how an application uses a module. It does not change the module, inherit its status, prove the application, or establish UCNS topology.

Catalog validation requires exact agreement on:

- catalog version;
- catalog digest;
- every module ID;
- every module digest;
- every module claim status.

A catalog rotation therefore invalidates stale application fixtures rather than silently relabeling them.

## Evidence firewall

Application modules currently permit only:

```text
CROSS-DOMAIN-HYPOTHESIS
EMPIRICAL-FRONTIER
```

Every application module requires:

```text
root_impact = none
metapat_validity_claim = false
domain_validity_claim = false
measurement_validity_claim = false
ucns_theorem_status_transfer = false
ucns_topology_claim = false
```

The schema records a bounded application hypothesis and its provenance. It does not supply external evidence.

## Source integrity

Application source references use:

```text
path/to/document.md#heading-slug::statement-N
```

`assert_application_sources_match()` fails if:

- the source document is absent;
- a declared heading is absent;
- an exact identity, binding, mapping, transfer, evidence, or `hmmm` statement drifts;
- a reference points to a different source document.

The source Markdown remains the human-readable application surface. The fixture is a strict machine-readable identity-bearing representation.

## First vertical slice

The first implementation is:

```text
metapat.application.quantum_magnetism
```

It binds twelve exact catalog modules while preserving:

- `CROSS-DOMAIN-HYPOTHESIS` status;
- root impact `none`;
- nuclear, atomic, crystalline, and magnetic-domain scale distinctions;
- physics evidence as the governing domain evidence;
- Theory 10 as explicitly excluded;
- unresolved “field-space” meaning as `hmmm`.

Package usage:

```python
from pathlib import Path
import metapat

catalog = metapat.canonical_semantic_catalog()
application = metapat.quantum_magnetism_application_module(catalog)

metapat.validate_application_against_catalog(application, catalog)
metapat.assert_application_sources_match(Path("."), application)
print(application.application_digest)
```

Packaged fixture:

```text
metapat/fixtures/quantum-magnetism-application-v2.json
```

## Regeneration

```bash
python tools/generate_application_fixtures.py
python tools/generate_application_fixtures.py --check
python tools/generate_msdmd.py --check
python tools/check_contract_graph.py
python -m pytest -q tests/test_application.py tests/test_quantum_magnetism.py
```

Generated application fixtures must not be edited by hand.

## hmmm

The application schema preserves declared domain evidence requirements but does not execute physical simulations, derive Hamiltonians, collect measurements, or decide whether the mapping predicts anything beyond established physics. Those remain the evidence required to advance the application beyond a cross-domain hypothesis.
