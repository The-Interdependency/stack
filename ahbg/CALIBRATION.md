# AHBG × a0 — Embodiment Calibration Program

This is the maximal coherent calibration program for the Architecture of Belonging under instancing closure.

AHBG is the controlled benchmark environment. `a0` is the first calibration subject. The candidate regulatory layer is measured and falsified here; it is not assumed true by construction.

## Independent build + reciprocal check rule

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

Each builder has two distinct obligations:

1. **build** its own a0 + AHBG realization independently;
2. **check both of the other realizations** after all three builds are frozen.

No builder validates its own implementation for comparative evidence. The calibration therefore produces six directional peer checks:

```text
Grok     -> Codex
Grok     -> DeepSeek
Codex    -> Grok
Codex    -> DeepSeek
DeepSeek -> Grok
DeepSeek -> Codex
```

Each builder works only inside its own directory. Do not patch a sibling implementation. Shared source doctrine, frozen scenarios, schemas, and evaluation criteria may be read from `stack/ahbg/`; implementation code may not be copied between the three builds during the calibration epoch.

A checker may read a sibling's frozen source, manifests, events, replay artifacts, and normalized outputs, but may not modify them. Findings are written only inside the checker's own workspace.

The purpose of triplicate construction is independent realization, not majority vote. The purpose of reciprocal checking is independent attack, not consensus manufacture. Agreement is replication evidence. Disagreement is a diagnostic surface and remains `hmmm` until resolved by source authority or experiment.

## Build target

Each workspace must build:

1. an `a0` realization capable of being instantiated with explicit lineage, boundary, perspective, history, permission state, uncertainty, action, consequence, and resource telemetry;
2. an AHBG realization capable of presenting controlled worlds, executing repeated turns, recording all admissible state transitions, and replaying the run deterministically;
3. a read-only checker capable of evaluating each of the other two frozen implementations against the common calibration contract.

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

## Reciprocal calibration checks

The evaluation contract is common and frozen; the checkers are independent.

Each builder must run the full check suite against **both sibling builds and not its own**.

Each directional check must verify:

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

A checker reports failures to the owning workspace but does not silently repair that build during sealed evaluation.

If both independent checkers of one build reach the same result, record the agreement. If they disagree, preserve both findings and mark the disputed boundary `hmmm`; do not resolve it by vote.

## Cross-build comparison

Each builder must emit the same normalized implementation result surface so the three implementations can be compared without sharing their internal code.

Required implementation outputs:

```text
BUILD_MANIFEST.json
RUN_MANIFEST.json
EVENTS.jsonl
CALIBRATION_RESULT.json
CALIBRATION_REPORT.md
```

Each builder must additionally emit read-only review artifacts for both siblings, for example:

```text
reviews/
├── <sibling-a>/
│   ├── CHECK_RESULT.json
│   └── CHECK_REPORT.md
└── <sibling-b>/
    ├── CHECK_RESULT.json
    └── CHECK_REPORT.md
```

Every build result and every peer check must identify exact source commits, implementation workspace, checker workspace, scenario corpus identity, seed set, provider relation, fitted parameters, controls, and evidence standing.

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

This layer closes only when:

- Grok, Codex, and DeepSeek each have an independently built a0 + AHBG pair;
- all three execute the same sealed calibration corpus;
- each builder checks the other two without modifying them;
- all **six directional peer checks** complete or terminate in an explicit `BLOCKED`/`UNRESOLVED` state;
- every build has two external check reports;
- disagreements between checkers remain visible rather than being averaged away;
- the final comparison publishes which regulatory components survived, failed, remain unresolved, or were blocked.

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

Read `../CALIBRATION.md`, resolve current source identities and skill-lib instructions, record them in the workspace build manifest, and build only inside that workspace.

After all three implementations are frozen, remain in your own workspace and run your checker against the other two read-only. Store review outputs under your own `reviews/` directory. Never patch a sibling as part of checking it.

Before expensive runs, preflight compute, memory, disk, network, provider quotas, and execution durability. Once a healthy sealed run begins, allow it to reach its natural terminal condition unless a real external limit or failure stops it.

## hmmm

The exact cost functional, resource projection, empirical thresholds, coupling-plasticity law, and final calibration corpus size remain open until measured. Reciprocal checking intentionally leaves one useful discomfort: three independent builders can still share the same wrong assumption if it entered through the common frozen protocol.