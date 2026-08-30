# METAPAT 0.6.0

## Release identity

METAPAT `0.6.0` promotes the three-phase nested electromagnetic-pipe application from a merged internal module into the public package and deterministic release surface.

This release changes no canon-bearing axiom, postulate, theorem, theory, glossary, or root text. Canon version and canon digest remain unchanged.

## Public additions

The top-level `metapat` package now exports:

- `WindingLayerSpec`;
- `AlloyCandidate`;
- `ElectromagneticPipeDesign`;
- electromagnetic-pipe schema and application constants;
- `electromagnetic_pipe_application_module()`;
- `electromagnetic_pipe_design()`;
- `electromagnetic_pipe_design_digest()`.

The release packages the exact deterministic fixture:

```text
src/metapat/fixtures/three-phase-electromagnetic-pipe-v1.json
```

The fixture is generated from the live constructor, checked for stale bytes, installed in the wheel, and compared against the installed constructor during clean-wheel smoke testing.

## Load-bearing control identity

```text
one three-phase vector per handedness per radial layer
3 radial layers × 2 handednesses × 3 phases = 18 phase circuits
3 radial layers × 2 handednesses = 6 three-phase systems
```

The mobile objects remain ceramic-coated magnetic eddy-current attractors, not bearings. Phase current remains the command variable; voltage remains compliance.

## Generated evidence

The release includes refreshed `metapat_msdmd.ts` metadata covering:

- package exports and version identity;
- electromagnetic-pipe module, documentation, capability, boundary, and contract declarations;
- application fixture generation and stale-byte checks;
- source, serialization, packaging, and installed-wheel CHECKS.

## Evidence firewall

Version `0.6.0` establishes package identity, public availability, source provenance, deterministic serialization, fixture exactness, and test coverage only.

It does not establish:

- electromagnetic performance;
- shielding attenuation or phase response;
- ideal alloy composition or heat treatment;
- insulation life or vacuum partial-discharge performance;
- fault containment or spacecraft safety;
- EDCM measurement validity;
- UCNS topology or theorem-status transfer;
- external validity of METAPAT.

The application remains `EMPIRICAL-FRONTIER`.

## Required gates

```bash
python -m unittest discover -s tests
python -m pytest -q
python tools/check_contract_graph.py
python tools/generate_catalog.py --check
python tools/generate_application_fixtures.py --check
python tools/generate_msdmd.py --check
python -m build
python -m twine check dist/*
```

The standing CI additionally requires Python 3.11, 3.12, and 3.13, actual-UCNS adapter integration, clean-wheel installation, exact fixture verification, and base import without UCNS.

## hmmm

Frequency, maximum phase current, voltage interpretation, target field, shielding attenuation, phase shift, attractor geometry, operating and fault temperatures, protection distance, alloy microstructure, and heat treatment remain unresolved experimental boundaries.
