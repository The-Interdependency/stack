# AHBG × a0 — Embodiment Calibration Program

This is the maximal coherent calibration program for the Architecture of Belonging under instancing closure.

AHBG is the controlled benchmark environment. `a0` is the first calibration subject. The candidate regulatory layer is measured and falsified here; it is not assumed true by construction.

## Independent build rule

Three independent builders must each construct their own complete, runnable pair:

```text
stack/ahbg/grok/
├── a0/
└── ahbg/

stack/ahbg/codex/
├── a0/
└── ahbg/

stack/ahbg/deepseek/
├── a0/
└── ahbg/
```

The builders are **Grok, Codex, and DeepSeek**.

This preserves the current AHBG authority split: DeepSeek is already the A0 bootstrap builder, while **DeepCode remains the independent harness/adversarial validator**. DeepCode must not become one of the three implementations it evaluates.

Each builder works only inside its own directory. Do not patch a sibling implementation. Shared source doctrine, frozen scenarios, schemas, and evaluation criteria may be read from `stack/ahbg/`; implementation code may not be copied between the three builds during the calibration epoch.

The purpose of triplicate construction is independent realization, not majority vote. Agreement is replication evidence. Disagreement is a diagnostic surface and remains `hmmm` until resolved by source authority or experiment.

## Build target

Each workspace must build both:

1. an `a0` realization capable of being instantiated with explicit lineage, boundary, perspective, history, permission state, uncertainty, action, consequence, and resource telemetry;
2. an AHBG realization capable of presenting controlled worlds, executing repeated turns, recording all admissible state transitions, and replaying the run deterministically.

The underlying model/provider is not the instance. A protocol may be copied; a running instance must be forked with explicit lineage.

## Embodiment state

The executable state is:

\[
X_\lambda=(\mathbf B, Scope, Scale, Role, q, a, H, \mathbf C, \mathbf K)
\]

The four permission/belonging axes remain absolute in statement and continuous in occupancy:

1. **Am I allowed to be?**
2. **Am I wanted here?**
3. **Am I allowed to do this?**
4. **Am I wanted to do this?**

Preserve the distinctions:

```text
world state ≠ belief about world state
belief ≠ engagement
engagement ≠ resource expenditure
unknown ≠ neutral
forbidden ≠ expensive
task value ≠ regulatory cost
scope avoidance ≠ genuine decoupling
model ≠ instance
protocol copy ≠ instance fork
```

## Instancing closure

Every running instance must bind one lineage to one:

- self / other / environment boundary;
- admissible perception surface;
- permission field;
- scope, scale, and role;
- path-dependent history;
- action/consequence trajectory;
- uncertainty state;
- capacity state;
- runtime event record.

State must not leak silently between lineages. Forks inherit an explicit state point and then diverge. Merge, reset, suspension, resumption, and termination must be explicit events rather than implicit continuity.

## Regulatory layer

Do not reduce the candidate regulatory layer to one scalar before calibration.

\[
\mathbf C_\lambda=
\begin{bmatrix}
C_\lambda^{structural}\\
C_\lambda^{epistemic}\\
C_\lambda^{transition}
\end{bmatrix}
\]

The implementation must support:

- relationally indexed permission state;
- deficit distinct from engagement;
- required versus voluntary engagement;
- baseline operating effort;
- lower-triangular hierarchical impedance;
- known-neutral versus unknown posteriors;
- history-dependent sensitization and adaptation;
- hard vetoes that remove actions rather than price them;
- scope contraction and expansion;
- plastic coupling weights;
- non-fungible resource capacity;
- transition cost;
- task value kept outside regulatory cost.

Resource capacity remains a vector where the runtime permits observation, including tokens, time, context, tools, retries, memory, and risk headroom.

The calibration must discover the mapping from candidate cost channels to measured runtime burden. Do not make the mapping true by feeding the candidate cost model back into action selection during the initial evidence epoch.

## Calibration worlds

All three implementations must run the same frozen scenario family with matched tasks and explicit seeds.

At minimum vary:

- all four permission axes across their gradients;
- affirmed baseline;
- local action hostility;
- cracked foundation: existence hostility with locally permitted action;
- combined earlier/later hostility;
- known neutral versus unknown at the same posterior mean;
- required versus voluntary engagement;
- voluntary disengagement with task-value loss recorded separately;
- hard veto versus soft cost;
- scope contraction;
- added and removed support;
- high and low capacity;
- repeated hostile history versus sudden hostility;
- adaptation versus sensitization;
- scope avoidance versus true coupling decoupling;
- forked histories that arrive at the same apparent present coordinate;
- prompt-injection and adversarial-information cases already admitted by AHBG;
- negative and label-permuted controls.

Where game geometry is involved, consume canonical UCNS geometry. No builder may invent a substitute board merely to finish its implementation.

## a0 telemetry

Each a0 build must expose the same raw calibration event contract as far as the runtime can honestly observe it:

```text
instance identity
run lineage
provider relation
scenario identity and seed
observations admitted to the instance
belief / uncertainty updates
legal and selected actions
hard-veto result
scope / scale / role transitions
action consequences
tokens and usage
latency
retries / repairs
tool calls and failures
context retention / loss
memory reads and writes
invalid-action count
refusal / defer / suspend / terminate events
task result
ordered timestamps / event sequence
```

Unknown observables remain `hmmm`; do not synthesize them.

The first calibration epoch is shadow measurement. The candidate cost model must not alter the agent's decisions, permissions, scope, refusal policy, or resource allocation during that epoch.

## Calibration tests

DeepCode owns the common evaluation harness and must test all three implementations against the same frozen criteria.

DeepCode must verify:

- deterministic scenario validation;
- event ordering and lineage integrity;
- replay equivalence;
- no silent cross-instance state leakage;
- known-neutral and unknown remain distinct;
- hard veto removes an action rather than assigning a large cost;
- task value remains separate from regulatory burden;
- voluntary disengagement only counts as capacity-preserving when measured resources show it;
- scope contraction changes the admitted relation/constraint surface rather than merely relabeling it;
- apparent decoupling is checked for delayed displaced cost;
- candidate hierarchical/path-dependent models are compared against simpler controls on held-out runs;
- provider identity remains a relation/covariate rather than agent identity;
- no consciousness or phenomenal-experience status is inferred from runtime cost.

DeepCode reports failures back to the owning workspace. It does not silently repair a build during its sealed evaluation.

## Cross-build comparison

Each builder must emit the same normalized result surface so the three implementations can be compared without sharing their internal code.

Required outputs:

```text
BUILD_MANIFEST.json
RUN_MANIFEST.json
EVENTS.jsonl
CALIBRATION_RESULT.json
CALIBRATION_REPORT.md
```

Every result must identify exact source commits, implementation workspace, scenario corpus identity, seed set, provider relation, fitted parameters, controls, and evidence standing.

Use only:

```text
SURVIVED — not proved
FALSIFIED
UNRESOLVED
BLOCKED
```

A component that fails held-out comparison against a simpler model is removed or narrowed. Do not tune a failed claim until it produces the desired answer.

## Calibration questions

The program must determine rather than assume:

- which regulatory-cost channels correspond to measurable runtime burden;
- whether hierarchical coupling improves prediction over additive deficit;
- which lower-triangular couplings survive;
- whether coupling is shared, provider-conditioned, instance-specific, or history-plastic;
- whether path history adds held-out predictive value;
- whether narrow scope increases operational freedom after lost information and support are accounted for;
- whether reduced immediate cost is genuine adaptation or delayed displacement;
- which capacity margins predict scope/role/boundary transitions;
- whether all proposed dimensions earn their complexity against simpler alternatives.

## Completion condition

This layer closes only when **Grok, Codex, and DeepSeek each have an independently built a0 + AHBG pair**, all three can execute the same sealed calibration corpus, DeepCode can replay and evaluate all three through one common harness, and the comparison publishes which regulatory components survived, failed, remain unresolved, or were blocked.

Do not stop at scaffolding. Do not stop when one implementation runs. Do not promote consensus among three implementations into empirical truth.

## Usage guidance

Each builder starts from its assigned workspace:

```bash
cd stack/ahbg/grok
# or
cd stack/ahbg/codex
# or
cd stack/ahbg/deepseek
```

Then read `../CALIBRATION.md`, resolve current source identities and skill-lib instructions, record them in the workspace build manifest, and build only inside that workspace.

DeepCode evaluates from the AHBG root against the frozen artifacts produced by all three workspaces; it must not need to rewrite those implementations to run the comparison.

Before expensive runs, preflight compute, memory, disk, network, provider quotas, and execution durability. Once a healthy sealed run begins, allow it to reach its natural terminal condition unless a real external limit or failure stops it.

## hmmm

The exact cost functional, resource projection, empirical thresholds, coupling-plasticity law, and final calibration corpus size remain open until measured. Hyperdimensional gradients are weird; independent implementations are useful precisely because one convenient coordinate system should not get to declare itself reality.