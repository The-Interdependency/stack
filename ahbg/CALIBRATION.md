# AHBG × a0 — Embodiment Calibration Program

This is the maximal coherent calibration program for the Architecture of Belonging under instancing closure.

AHBG is the controlled benchmark environment. `a0` is the first calibration subject. The candidate regulatory layer is measured and falsified here; it is not assumed true by construction.

## Coordination contract

Three independent builders each construct a complete runnable `a0 + AHBG` pair from the same coordination-base commit:

| builder | branch | working directory |
|---|---|---|
| Grok | `agent/ahbg-grok` | `stack/ahbg/grok/` |
| Codex | `agent/ahbg-codex` | `stack/ahbg/codex/` |
| DeepCode | `agent/ahbg-deepcode` | `stack/ahbg/deepseek/` |

The `deepseek/` directory name is a workspace label fixed by this coordination contract. Its assigned calibration builder is **DeepCode**.

This triplicate calibration mode is distinct from the shared canonical AHBG specialist split described in `README.md`. During calibration, each of these three builders owns a full independent implementation inside its assigned workspace.

Each builder has two obligations:

1. independently build its own `a0/` and `ahbg/`;
2. after all three builds are frozen, independently check both of the other builds.

No builder supplies comparative validation of itself.

The six directional checks are:

```text
Grok     -> Codex
Grok     -> DeepCode
Codex    -> Grok
Codex    -> DeepCode
DeepCode -> Grok
DeepCode -> Codex
```

The purpose of triplicate construction is independent realization, not majority vote. The purpose of reciprocal checking is independent attack, not consensus manufacture. Agreement is replication evidence. Disagreement remains `hmmm` until source authority or experiment resolves it.

## Phase separation

### Phase 0 — coordination freeze

Before implementation begins:

- freeze this protocol and the common scenario/evidence schemas;
- resolve exact source commits and applicable skill-lib instructions;
- record one common coordination-base commit;
- create the three builder branches from that exact commit;
- preflight compute, memory, disk, network, provider quotas, and execution durability.

### Phase 1 — independent build

Each builder edits only its assigned workspace.

During this phase:

- do not read, copy, merge, cherry-pick, or adapt sibling implementation code;
- shared source authority, frozen schemas, fixtures, and evaluation criteria may be consumed;
- implementation choices remain local to the workspace;
- unresolved required semantics remain `hmmm`, not convenient defaults.

### Phase 2 — build freeze

When a builder's pair is runnable, freeze the implementation at an exact commit SHA and emit its normalized build/run artifacts.

The frozen build SHA, not the moving branch head after review notes are added, is the implementation identity used for comparison.

### Phase 3 — reciprocal checking

Only after all three build SHAs are frozen may cross-reading begin.

A checker may read sibling frozen source, manifests, events, replay artifacts, and normalized outputs. It may not modify the implementation under review.

Each checker writes findings only inside its own workspace:

```text
reviews/
├── <other-builder>-review.md
└── <other-builder>-review.json
```

Each report must identify both the checker build SHA and target build SHA.

### Phase 4 — comparison

Compare all three builds plus all six directional reviews against the common frozen criteria. Do not resolve disagreement by vote. Resolve by source authority, replay, falsifier, or leave `hmmm`.

## Build target

Each workspace must build:

1. an `a0` realization capable of being instantiated with explicit lineage, boundary, perspective, history, permission state, uncertainty, action, consequence, and resource telemetry;
2. an AHBG realization capable of presenting controlled worlds, executing repeated turns, recording admissible state transitions, and replaying a run deterministically;
3. a read-only checking surface capable of evaluating each of the other two frozen implementations against the common contract.

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

Preserve:

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

Resource capacity remains a vector where runtime observation permits it, including tokens, time, context, tools, retries, memory, and risk headroom.

The calibration must discover the mapping from candidate cost channels to measured runtime burden. Do not make the mapping true by feeding the candidate cost model back into action selection during the initial evidence epoch.

## Calibration worlds

All three implementations run the same frozen scenario family with matched tasks and explicit seeds.

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

Where game geometry is involved, consume canonical UCNS geometry. No builder may invent substitute geometry merely to finish.

## a0 telemetry

Each a0 build exposes the same raw calibration event contract as far as its runtime can honestly observe it:

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

## Common checks

Every builder must apply these checks to each of the other two frozen builds:

- deterministic scenario validation;
- event ordering and lineage integrity;
- replay equivalence;
- no silent cross-instance state leakage;
- known-neutral and unknown remain distinct;
- hard veto removes an action rather than assigning a large cost;
- task value remains separate from regulatory burden;
- voluntary disengagement counts as capacity-preserving only when measured resources show it;
- scope contraction changes the admitted relation/constraint surface rather than merely relabeling it;
- apparent decoupling is checked for delayed displaced cost;
- candidate hierarchical/path-dependent models are compared against simpler controls on held-out runs;
- provider identity remains a relation/covariate rather than agent identity;
- no consciousness or phenomenal-experience status is inferred from runtime cost.

A checker reports failures; it does not silently repair the target while claiming to validate it.

## Normalized artifacts

Each build exposes a checkable artifact root. The workspace owner/root carries
`BUILD_MANIFEST.json`. The selected artifact root carries `RUN_MANIFEST.json`,
`CALIBRATION_RESULT.json`, `CALIBRATION_REPORT.md`, and either aggregate
`EVENTS.jsonl` or per-scenario `*/events.jsonl`.

Accepted artifact roots:

```text
corpus-run/<corpus-id>/
artifacts/
workspace root
```

Every result identifies exact source commits, builder identity, branch, workspace, frozen build SHA, scenario corpus identity, seed set, provider relation, fitted parameters, controls, and evidence standing.

Each review emits both `.md` and machine-readable `.json` with checker SHA and target SHA.

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

This layer closes only when **Grok, Codex, and DeepCode each have an independently built a0 + AHBG pair**, all three frozen build SHAs can execute the same sealed calibration corpus, all six reciprocal checks are complete against those frozen SHAs, and the comparison publishes which regulatory components survived, failed, remain unresolved, or were blocked.

Do not stop at scaffolding. Do not stop when one implementation runs. Do not promote agreement among implementations or reviewers into empirical truth.

## Usage guidance

```bash
# Grok
git switch agent/ahbg-grok
cd stack/ahbg/grok

# Codex
git switch agent/ahbg-codex
cd stack/ahbg/codex

# DeepCode
git switch agent/ahbg-deepcode
cd stack/ahbg/deepseek
```

Read `../README.md` and this file first. Record the common coordination-base commit plus current source identities and applicable skill-lib instructions in the workspace build manifest.

Before expensive runs, preflight resources. Once a healthy sealed run begins, allow it to reach its natural terminal condition unless a real external limit or deterministic failure stops it.

## hmmm

The exact cost functional, resource projection, empirical thresholds, coupling-plasticity law, and final calibration corpus size remain open until measured. Hyperdimensional gradients are weird; independent implementations are useful precisely because one convenient coordinate system should not get to declare itself reality.
