# METAPAT stack repair — required changes

Date: 2026-07-12
Repository: `The-Interdependency/metapat`
Audience: coding specialist AI
Status: implementation handoff

## Governing objective

Make METAPAT the canonical authority for Meta Energy Theory meanings, constraints, and claim boundaries without making it a duplicate UCNS algebra or an EDCM measurement engine.

The current declared flow `UCNS -> METAPAT -> EDCM` must be replaced by an architecture that distinguishes:

1. **authority flow** — METAPAT constrains interpretation and preserves root canon;
2. **runtime data flow** — evidence is encoded through actual UCNS geometry and measured by EDCM;
3. **proof-status flow** — no UCNS theorem status transfers into METAPAT ontology or EDCM measurement claims.

Before editing, read `AGENTS.md`, `llms.txt`, `CHAPTER_ZERO.md`, `AXIOMS.md`, `POSTULATES.md`, `THEOREMS.md`, `THEORIES.md`, `DOMAIN_RESTRAINT.md`, `UCNS_IMPLEMENTATION.md`, and the repo-local `.agents/skills/` material. Follow the pinned `The-Interdependency/skill-lib` doctrine and preserve every unresolved constraint as `hmmm` rather than silently closing it.

## Required patch order

### 1. Make the architecture statement true

Replace the single ambiguous pipeline declaration with two explicit diagrams.

Authority:

```text
METAPAT canon
    |
    +-- constrains terms, interpretation, allowed derivations, and claim status
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

Update `README.md`, `ROADMAP.md`, `src/metapat/flow_plan.py`, package metadata, and all agent-facing documentation together. Do not leave conflicting diagrams in different files.

### 2. Remove the second UCNS algebra

`src/metapat/ucns.py` currently defines a local `UCNSObject`, normalization, carrier calculation, and composition operation. That is a second algebra even though it is described as partial.

Replace it with one of these bounded designs, preferring option A:

- **A — real adapter:** import and construct objects from the actual `ucns` public package through a narrow optional adapter;
- **B — neutral bridge record:** emit a versioned immutable transport record that does not use the name `UCNSObject` and contains only the information needed for an external UCNS adapter.

Requirements:

- METAPAT base canon must remain importable without UCNS installed.
- Attempting to use the UCNS adapter without UCNS must raise a clear dependency error; never silently substitute a different algebra.
- Do not copy `multiply`, normalization, star/disk-flip, factorization, domain status, or theorem vocabulary into METAPAT.
- Preserve tags and source statements as provenance, not as UCNS mathematical payload meaning unless an explicit adapter contract says so.
- Add round-trip tests against the actual `ucns.UCNSObject` public surface.

### 3. Introduce a METAPAT claims ledger

Create `docs/claims-ledger.md` and classify every public doctrine or executable assertion using this minimum vocabulary:

```text
ROOT-STIPULATION
DEFINITION
INTERNAL-DERIVATION
IMPLEMENTED-CONTRACT
CROSS-DOMAIN-HYPOTHESIS
EMPIRICAL-FRONTIER
RETRACTED_OR_SUPERSEDED
```

The ledger must state that executable checks of definitions are contract tests, not independent empirical or formal validation of the ontology.

Reconcile the words `axiom`, `postulate`, `theorem`, `validation`, and `proof` across README, Chapter Zero, source docstrings, tests, and generated agent metadata. Preserve Erin Spencer's canon text exactly unless a canon change is separately authorized.

### 4. Rename and constrain theorem-validation helpers

`src/metapat/validation.py` currently exposes boolean helpers whose names can read as theorem verification.

Refactor the public meaning so the functions are clearly deterministic **canon contract checks**. Acceptable approaches:

- rename the module to `contracts.py` with compatibility imports from `validation.py`; or
- retain the module path but rename metadata, capability descriptions, and documentation to `canon contract checks`.

Each function must document:

- what encoded condition it checks;
- what it does not establish;
- which METAPAT statement it corresponds to;
- whether the result is definitional, derived, or empirical.

### 5. Define the METAPAT-to-EDCM boundary

Add a versioned immutable `MetapatModuleEnvelope` or equivalently named public schema. It should carry only semantic authority and provenance, not calculated EDCM measurements.

Minimum fields:

- schema id and version;
- canon version or canon digest;
- module kind such as simplex, boundary-simplex, tensor, relation, gradient, registration, time, or question;
- exact source statement references;
- bounded constraints or permitted interpretations;
- unresolved constraints;
- provenance digest.

EDCM must be able to consume this envelope without treating its labels as measured values. Add a fixture suitable for cross-repository tests.

### 6. Make package tests exercise the installed surface

Tests must import `metapat`, not `src.metapat`.

Add packaging and smoke checks that verify:

```bash
python -m build
python -m twine check dist/*
python -m venv /tmp/metapat-wheel-test
. /tmp/metapat-wheel-test/bin/activate
pip install dist/*.whl
python -c "import metapat; print(metapat.__version__)"
```

Declare the package version in one authoritative location and expose it through the public package.

If optional UCNS or EDCM integrations are declared in `pyproject.toml`, they must be real installable dependency groups or clearly named development/integration extras. Empty extras are not acceptable architecture evidence.

### 7. Add cross-repository contract fixtures

Create deterministic fixtures proving all of the following:

1. current METAPAT root canon remains byte-for-byte stable;
2. a METAPAT module envelope can be adapted into an actual UCNS object;
3. source statements and canon digest survive adaptation;
4. the adapter does not claim UCNS theorem status for METAPAT canon;
5. an EDCM consumer can read the semantic envelope while keeping semantic labels separate from measured values;
6. `hmmm` fields survive serialization and round trip.

Keep integration tests optional when sibling repositories are unavailable, but make skipped tests explicit and reported rather than silently replaced.

### 8. Reconcile agent metadata and documentation

Update all affected `MODULE_BUILD`, `DOCS`, `CAPABILITIES`, `BOUNDARIES`, `CONTRACTS`, `DEPENDENCIES`, `OWNERS`, `AGENTS.md`, and `llms.txt` surfaces.

Run the repo-local msdmd collection and skill-lib drift checks. No metadata block may continue to describe the retired local UCNS algebra as the live bridge.

## Required non-goals

Do not:

- rewrite Chapter Zero merely to make implementation easier;
- claim that deterministic contract checks empirically prove Meta Energy Theory;
- make METAPAT depend on EDCM measurement outputs for root validity;
- let UCNS terminology redefine METAPAT root terms;
- duplicate the UCNS algebra under a different class name;
- silently convert unresolved architecture into a default behavior;
- transfer Lean or UCNS proof status into METAPAT claims.

## Verification gate

The repair is not complete until all applicable checks pass from a clean checkout:

```bash
python -m unittest discover -s tests
python -m pytest -q
python -m build
python -m twine check dist/*
```

Also run the repo-local skill-lib drift checker, msdmd collector, installed-wheel smoke test, actual-UCNS adapter tests, and the shared UCNS/METAPAT/EDCM contract fixture.

## hmmm

The implementation must preserve one unresolved design question explicitly: whether METAPAT statements should be encoded as UCNS payloads, tags, or external provenance references. Do not choose payload semantics merely because the constructor permits payloads. The adapter must carry this as an explicit unresolved constraint until a semantic rule is ratified.