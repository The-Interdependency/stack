# Three-Phase Nested Electromagnetic Pipe System

## Application identity

Status: **EMPIRICAL-FRONTIER / engineering application**  
Domain: electromagnetics, power electronics, magnetic materials, thermal engineering, spacecraft systems  
Root impact: **none**

This application preserves a bounded device geometry and experimental program. METAPAT determines the question, distinction, boundary, tensor, gradient, transformation, registration, and optimization structure. It does not replace electromagnetic simulation, power-electronics design, insulation qualification, alloy characterization, thermal analysis, or experiment.

## Canon correction

|∆|The natural control object is one three-phase vector per handedness per radial layer.|∆|

The system is not eighteen unrelated currents and the internal alloy objects are not bearings.

## Current geometry

Three-meter coaxial assembly for space use:

- outer iron pipe: 3 inches across;
- three radial copper-winding layers;
- iron pipe between each winding layer;
- hollow central region containing mobile ceramic-coated magnetic attractors;
- all pipes and conductors ceramic-coated;
- copper remains solid during normal operation;
- ceramic winding channels contain molten copper only during catastrophic overheating.

From outside inward:

```text
outer iron pipe
→ outer winding layer
→ middle iron pipe
→ middle winding layer
→ inner iron pipe
→ inner winding layer
→ mobile alloy-attractor region
```

## Windings

Each radial layer contains:

- three clockwise phase windings;
- three widdershins phase windings.

Therefore:

- 3 radial layers;
- 2 handednesses per layer;
- 3 phases per handedness;
- 18 phase circuits total;
- naturally organized as |∆|six three-phase systems|∆|.

| Layer | Wire | Turns per inch | Clockwise phases | Widdershins phases |
|---|---:|---:|---:|---:|
| outer | 12 AWG | 6 | 3 | 3 |
| middle | 16 AWG | 12 | 3 | 3 |
| inner | 20 AWG | 18 | 3 | 3 |

Each phase circuit can operate with:

- alternating current;
- direct-current bias;
- reversed polarity;
- independently controlled amplitude and phase;
- nominal 0–250+ volt drive.

The drives should be current-controlled. Voltage is compliance, not the magnetic command variable.

## Three-phase behavior

Each handedness/layer pair is one three-phase vector system.

Possible relationships:

- same phase order: reinforcing/coupled fields;
- reversed phase order: counter-rotating or counter-traveling field;
- equal opposing systems: standing or pulsating field;
- unequal opposing systems: dominant rotation plus adjustable drag/phase structure;
- direct-current bias plus alternating three-phase field: attraction/location control plus eddy-current excitation.

Three-phase currents require physical phase displacement.

Possible geometries:

- circumferential displacement → rotation;
- axial displacement → translation;
- helical displacement → simultaneous rotation and translation.

## Mobile internal elements

The internal objects are |∆|not bearings|∆|.

They are ceramic-coated magnetic eddy-current attractors intended to alter:

- shielding amplitude;
- magnetic phase delay;
- field gradients;
- settling behavior;
- local permeability;
- local eddy-current losses;
- field-history response.

They may move, cluster, chain, redistribute, rotate, or occupy field maxima.

Ceramic coating:

- electrically isolates each attractor;
- prevents large conductive networks;
- prevents welding/contact faults;
- does not prevent magnetization;
- does not prevent internal eddy currents;
- does not prevent magnetic clustering.

The attractors should eventually be constrained by cells, tracks, pockets, or controlled free-volume geometry if repeatability is required.

## Candidate alloy

Desired alloy family:

```text
Fe + Co + Ni = 75 atomic percent
Cr = 15 atomic percent
Mn = 10 atomic percent
```

Initial METAPAT anchor candidate:

```text
Fe42.5 Co22.5 Ni10 Cr15 Mn10 atomic percent
```

Alternative composition-search candidates:

| Candidate | Fe | Co | Ni | Cr | Mn | Basis |
|---|---:|---:|---:|---:|---:|---|
| A | 42.5 | 22.5 | 10 | 15 | 10 | atomic percent |
| B | 37.5 | 22.5 | 15 | 15 | 10 | atomic percent |
| C | 32.5 | 17.5 | 25 | 15 | 10 | atomic percent |
| D | 45 | 15 | 15 | 15 | 10 | atomic percent |
| E | 35 | 30 | 10 | 15 | 10 | atomic percent |

The ideal alloy cannot be selected from elemental properties alone. It depends on:

- phase structure;
- grain structure;
- heat treatment;
- conductivity;
- complex permeability;
- saturation;
- coercivity;
- Curie temperature;
- operating temperature;
- alternating-current frequency;
- attractor size;
- desired phase shift;
- acceptable heating.

## Catalog bindings

| Catalog module | Application role | Bounded application statement |
|---|---|---|
| `metapat.axiom.0.root_untouchable` | domain-restraint | METAPAT organizes the question and does not replace electromagnetic, materials, thermal, insulation, or spacecraft evidence. |
| `metapat.axiom.1.legible_difference` | distinction | Every phase circuit, handedness, radial layer, iron pipe, ceramic boundary, attractor, gap, and field state remains separately legible. |
| `metapat.axiom.2.boundary` | boundary-simplex | Ceramic shells, iron pipes, gaps, winding geometry, end geometry, and attractor constraints alter passage, delay, filtering, phase, direction, and transformation. |
| `metapat.axiom.4.tensor` | control-tensor | The simultaneous arrangement contains six three-phase vectors, direct-current biases, frequency, current limits, voltage compliance, winding handedness, radial layer, attractor positions, alloy state, temperature, magnetic history, and mechanical gaps. |
| `metapat.axiom.5.energy_state` | energy-state | Phase-current, magnetic-field, magnetization, motion, eddy-current, and thermal conditions are distinct energy-state surfaces. |
| `metapat.axiom.6.relation` | relation | Layer, handedness, phase order, spatial displacement, pipe geometry, attractor position, and material state configure which transformations are possible. |
| `metapat.axiom.7.gradient` | gradient | Readable differences include field amplitude, field phase, position, temperature, magnetization, force, leakage, and shielding response. |
| `metapat.axiom.8.transformation` | feedback-transformation | Current changes field; field changes attractor magnetization and motion; attractor redistribution changes the boundary and therefore the next field cycle. |
| `metapat.axiom.9.time` | sequential-field-state | Alternating phase progression, settling, hysteresis, magnetic history, and fault evolution are sequential tensor alterations. |
| `metapat.axiom.10.registration` | instrumentation | Registration measures electrical, magnetic, thermal, mechanical, distribution, hysteresis, settling, and leakage states. |
| `metapat.axiom.11.question` | unresolved-design-state | Frequency, current, target field, shielding, phase shift, attractor geometry, temperature, and protection distance remain bounded unresolved states. |
| `metapat.postulate.2.explicationary_use` | engineering-restraint | METAPAT vocabulary clarifies the device but does not replace Maxwell-field simulation, circuit models, materials measurements, or qualification tests. |
| `metapat.postulate.6.validation_by_boundary_change` | boundary-test | A claimed boundary effect must be tested by changing boundary state while holding declared source and target conditions as constant as practicable. |
| `metapat.theorem.1.boundary_earns_its_keep` | boundary-evidence | Ceramic, iron, gap, end-return, and attractor boundaries earn model force only when their controlled change alters measured direction, delay, filtering, propagation, shielding, or transformation. |
| `metapat.theory.2.boundary_mediated_transformation` | boundary-mediated-transformation | Mobile attractor redistribution is treated as a changing boundary state that may alter shielding amplitude, phase delay, loss, and force gradients. |
| `metapat.theory.5.relational_gradient_selection` | force-selection | Direction and motion are asked through the full relation among phase order, winding displacement, pipe state, attractor state, and magnetic gradient rather than field difference alone. |
| `metapat.theory.6.time_as_sequential_tensor_alteration` | cycle-history | Phase progression, hysteresis, settling, and thermal accumulation are distinct sequential alterations rather than mere timestamps. |
| `metapat.theory.7.registration_and_observer_roles` | sensor-registration | Sensors and logs earn observer role only by preserving, expressing, or transmitting the relevant sequence. |
| `metapat.theory.8.questions_as_bounded_unresolved_energy_state` | optimization-question | Each unresolved operating bound is retained as a named question rather than silently guessed into the design. |
| `metapat.theory.11.cross_domain_question_forms` | cross-domain-question-form | Electromagnetics, power electronics, magnetic materials, thermal behavior, mechanics, insulation, and spacecraft integration may share a question-form without becoming one domain. |

## METAPAT application

The device is modeled as a boundary-mediated energy-state system.

**Distinction:** each phase circuit, pipe, ceramic layer, attractor, gap, and field state must remain separately legible.

**Boundary-simplex:** ceramic shells, iron pipes, gaps, winding geometry, and attractor constraints alter passage, delay, filtering, phase, direction, and transformation.

**Tensor:** the simultaneous arrangement of six three-phase vectors, direct-current biases, frequency, voltage/current limits, winding handedness, radial layer, attractor positions, alloy state, temperature, magnetic history, and mechanical gaps.

**Gradient:** readable differences in field amplitude, phase, position, temperature, and magnetization.

**Transformation:** current changes produce field changes; field changes produce attractor movement and internal eddy currents; attractor redistribution alters the field boundary and therefore changes the next field cycle.

## Feedback chain

```text
current tensor
→ magnetic gradient
→ attractor magnetization and movement
→ altered boundary state
→ changed shielding amplitude and phase
→ changed force gradient
```

## Registration

Registration must measure:

- phase current and voltage;
- field magnitude;
- field phase;
- attractor distribution;
- temperature;
- hysteresis;
- settling time;
- leakage field;
- mechanical motion.

## Fault philosophy

Normal operation:

- copper remains solid;
- iron remains below magnetic degradation temperatures;
- ceramic provides insulation and containment;
- six three-phase systems remain independently isolatable.

Extreme fault:

- current controller limits or disconnects;
- fuse isolates the failed phase;
- locally molten copper remains inside its ceramic winding channel;
- no conductive spray, welded rotor, inter-turn short, or spacecraft fire occurs;
- failed copper resolidifies as an isolated circuit.

These are required fault objectives, not established outcomes.

## High-voltage requirements

For 0–250+ volts per phase:

- account for circuit-to-circuit differential voltage;
- account for inductive overshoot;
- use void-free ceramic encapsulation;
- use sealed ceramic-to-metal feedthroughs;
- avoid sharp terminals;
- provide clamping or energy recovery;
- test partial discharge under vacuum and intermediate pressure;
- monitor insulation leakage;
- isolate each phase independently.

## Protection-distance status

No fixed protection distance is established yet.

It depends on:

- central field strength;
- allowable external field;
- frequency;
- pipe geometry;
- end closure;
- attractor state;
- alloy permeability;
- saturation;
- phase configuration.

Open-end leakage dominates a long cylindrical system. End geometry and magnetic return paths will determine the final exclusion zone.

## Immediate next work

1. Define whether phase geometry is circumferential, axial, or helical.
2. Define voltage as peak, RMS, or DC-link value.
3. Bound operating frequency range.
4. Bound maximum phase current.
5. Define target field amplitude.
6. Define required shielding attenuation and phase shift.
7. Define attractor size and allowed motion.
8. Define operating and fault temperatures.
9. Simulate the six coupled three-phase systems.
10. Produce and characterize alloy coupons across the Fe–Co–Ni composition simplex.
11. Measure complex permeability, saturation, coercivity, resistivity, heating, and phase response.
12. Build a short instrumented section before attempting the full three-meter system.

## Evidence boundary

The geometry and control topology are specified as an engineering proposal. Claimed magnetic, shielding, phase-delay, fault-containment, thermal, high-voltage, mechanical, and materials performance remain answerable to electromagnetic simulation, circuit analysis, coupon characterization, vacuum insulation testing, thermal testing, fault testing, and instrumented prototypes.

No fixed protection distance, ideal alloy, operating frequency, maximum phase current, target field, shielding attenuation, phase shift, attractor dimension, or thermal limit is established by this application record.

## hmmm

The geometry is conceptually bounded, but frequency, current, target field, desired phase shift, attractor dimensions, and thermal limits remain unresolved. Until those are registered, “ideal alloy” remains a composition-search problem rather than a single truthful formula.
