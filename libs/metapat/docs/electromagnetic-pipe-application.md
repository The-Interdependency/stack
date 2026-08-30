# Three-phase electromagnetic-pipe application record

## Purpose

`metapat.electromagnetic_pipe` preserves the current three-phase nested electromagnetic-pipe handoff as two linked surfaces:

1. an `EMPIRICAL-FRONTIER` `MetapatApplicationModule` bound to exact semantic-catalog identities;
2. a strict `ElectromagneticPipeDesign` record carrying the load-bearing engineering topology and unresolved experiment program.

Neither surface validates device performance.

## Control identity

```text
radial layers: 3
handednesses per layer: 2
phases per handedness: 3
phase circuits: 18
three-phase systems: 6
```

The natural control object is one three-phase vector per handedness per radial layer. The eighteen physical phase circuits remain separately measurable and isolatable, but they are not modeled as eighteen unrelated magnetic commands.

## Typed design surfaces

`WindingLayerSpec` preserves:

- radial order;
- wire gauge;
- turns per inch;
- three clockwise phases;
- three widdershins phases;
- two three-phase systems per radial layer.

`AlloyCandidate` preserves atomic-percent composition and rejects candidates that do not satisfy:

```text
Fe + Co + Ni = 75
Cr = 15
Mn = 10
total = 100
```

`ElectromagneticPipeDesign` preserves:

- three-meter assembly length;
- three-inch outer-pipe diameter;
- three iron pipes and three winding layers;
- current-command and voltage-compliance roles;
- drive modes and unresolved spatial phase geometry;
- ceramic-coated magnetic eddy-current attractors, explicitly not bearings;
- measurement requirements;
- normal-operation constraints;
- extreme-fault objectives;
- high-voltage and vacuum-insulation requirements;
- protection-distance status;
- twelve immediate next-work items;
- five alloy-search candidates;
- all unresolved `hmmm` boundaries.

## Evidence firewall

The following fields are required to remain false:

```text
electromagnetic_validity_claim
alloy_validity_claim
insulation_validity_claim
fault_containment_validity_claim
spacecraft_safety_validity_claim
```

The nested application record separately keeps METAPAT validity, domain validity, measurement validity, UCNS theorem transfer, and UCNS topology claims false.

Fault statements are objectives to test. Ceramic containment, molten-copper isolation, absence of conductive spray, and absence of spacecraft fire are not represented as demonstrated outcomes.

## Release surface

METAPAT `0.7.0` exports the canon-v2-bound pipe application and design records through the top-level `metapat` package.

Human source:

```text
docs/applications/three-phase-electromagnetic-pipe.md
```

Packaged deterministic fixture:

```text
src/metapat/fixtures/three-phase-electromagnetic-pipe-v2.json
```

Generation and verification:

```bash
python tools/generate_application_fixtures.py
python tools/generate_application_fixtures.py --check
python tools/generate_msdmd.py --check
python -m unittest tests.test_electromagnetic_pipe
python -m pytest -q tests/test_electromagnetic_pipe.py tests/test_packaging.py
```

The clean-wheel smoke test verifies version `0.7.0`, the top-level constructors, the exact packaged fixture, the 18-circuit / six-system topology, catalog binding, and design digest without requiring UCNS.

## Short-section prototype gate

The first physical build should be a short instrumented section rather than the full three-meter assembly. It should register, at minimum:

- all phase currents and voltages;
- local field magnitude and phase;
- attractor distribution and mechanical motion;
- winding, pipe, ceramic, and attractor temperatures;
- hysteresis, settling, leakage, and insulation behavior;
- end leakage and return-path effects.

The prototype does not authorize extrapolation to full-length operation until the six coupled three-phase systems, moving boundaries, thermal behavior, and vacuum high-voltage behavior are reconciled against measurement.

## hmmm

The strict record prevents unresolved engineering values from disappearing, but it cannot supply them. Frequency, phase current, voltage interpretation, target field, shielding attenuation, desired phase shift, attractor geometry, temperatures, protection distance, alloy microstructure, and heat treatment remain living experimental work.
