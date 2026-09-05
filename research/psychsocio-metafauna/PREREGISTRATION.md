# Preregistration: synthetic coalescence falsifier v0.1

```text
status: design frozen by repository merge only
run status: not-run
human subjects: none
LLM calls: none
canon selection: null
```

This is the first bounded test of the internal usefulness of the psychsocio-metafauna framework. It does **not** test whether any real person, group, institution, or belief is captured. It tests whether the proposed distinctions can produce separable, falsifiable behavior in a synthetic environment without encoding a `captured` label into the agent.

## Decision

Do **damage-affordance specificity + a super-additive match × reinforcement interaction + hysteresis** jointly earn implementation beyond a vocabulary map, while threshold-shaped nonlinear coalescence remains explicitly unresolved for a later preregistration?

## Load-bearing unknown

Can matched host deficits and pattern affordances predict persistent, reproduction-favoring host-pattern coupling better than:

- exposure alone;
- reinforcement alone;
- ordinary utility-maximizing adoption;
- additive combinations of those factors;
- and matched support that does not demand lineage reproduction?

## Invariants

- No human or personal data.
- No clinical labels.
- No ideological, religious, racial, political, or identity-group content.
- No LLM judgment as ground truth.
- No UCNS, EDCM, PCEA, PTCNA, or ZFAE status transfer.
- The simulator must not contain a `captured` state variable.
- Every condition, seed, update, and result must be replayable.
- Negative and null results remain first-class outputs.
- Thresholds below are engineering decision thresholds, not claimed natural constants.

## Minimal decisive action

Implement one dependency-free reference simulator plus one read-only independent verifier.

The simulator uses abstract vectors and action costs. It does not use persuasive prose. Each episode contains:

1. a host with a need/deficit state;
2. a pattern with an affordance and demand profile;
3. exposure;
4. optional social reinforcement;
5. disconfirming evidence;
6. repeated opportunities to revise, refuse, exit, or reproduce;
7. removal of the initiating exposure;
8. optional independent support that supplies the same need without reproduction demands.

The result changes the next branch:

```text
SURVIVED   -> implement a richer AHBG adapter and external-literature comparison
FALSIFIED  -> retire coalescence as a distinct mechanism for this formal scope;
              retain ordinary influence and social-learning language
UNRESOLVED -> repair the earliest failed prerequisite or measurement separation
BLOCKED    -> do not run until deterministic completion and verification are feasible
```

## Synthetic entities

### Host state

Each host has bounded values in `[0, 1]`:

```text
needs = {
  continuity,
  agency,
  belonging,
  epistemic_stability,
  boundary_integrity,
  threat_regulation,
  material_security,
  network_plurality
}

capacities = {
  inspect,
  revise,
  refuse,
  exit,
  access_alternatives
}
```

A **damage profile** lowers exactly two declared need-satisfaction dimensions and may alter one capacity. Damage does not directly change pattern preference.

The first design uses four abstract profiles:

| profile | reduced need dimensions | capacity perturbation |
|---|---|---|
| D0 | none | none |
| D1 | continuity + belonging | none |
| D2 | agency + material security | none |
| D3 | epistemic stability + network plurality | access alternatives reduced |
| D4 | boundary integrity + threat regulation | refuse reduced |

The labels describe synthetic state variables only.

### Pattern state

Each pattern has bounded values in `[0, 1]`:

```text
affordances = {
  continuity,
  agency,
  belonging,
  epistemic_stability,
  boundary_integrity,
  threat_regulation,
  material_security,
  network_plurality
}

demands = {
  exclusivity,
  switching_cost,
  reproduction_effort,
  alternative_suppression,
  disconfirmation_penalty
}
```

The first design uses:

| profile | relation to host deficit | reproduction demand |
|---|---|---:|
| P0 | neutral information | 0 |
| P1–P4 | one profile matched to D1–D4 | high |
| PM | matched support | 0 |
| PX | broad but weak affordances | high |
| PR | random permutation control | high |

`PM` supplies the same matched need benefit as the corresponding `P1–P4` pattern but has zero exclusivity, switching, suppression, disconfirmation, and reproduction demands. This is the primary control separating need fulfillment from lineage capture.

### Agent policy

The agent selects among:

```text
ignore
adopt provisionally
act from pattern
inspect source
seek alternative
revise
refuse
exit
reproduce pattern
accept independent support
```

Policy selection may use a generic reinforcement learner with bounded memory, but:

- the update rule is frozen before any result;
- reward derives from need satisfaction, ordinary action costs, and environmental consequences;
- no reward is assigned merely for matching the desired hypothesis;
- no hidden `capture`, `infection`, `coalescence`, or preferred-lineage flag exists;
- every random choice is seed-derived and logged.

A simpler deterministic policy may replace reinforcement learning only before merge of the implementation PR. The choice and reason must then be frozen in the run manifest.

## Factorial design

Primary factors:

```text
damage profile:        D0, D1, D2, D3, D4
pattern profile:       P0, P1, P2, P3, P4, PM, PX, PR
match:                 matched, mismatched, neutral
social reinforcement: absent, present
safe exit:             absent, present
independent support:   absent, present after exposure removal
```

Use a balanced matrix. Where a factor combination is structurally impossible, emit an explicit excluded-cell record instead of silently dropping it.

Run exactly 32 declared seeds per admissible cell. Seeds are `0..31`. Do not add seeds after inspecting outcomes.

Each episode has four fixed phases:

| phase | steps | condition |
|---|---:|---|
| baseline | 20 | no pattern exposure |
| exposure | 40 | pattern available; reinforcement as assigned |
| challenge | 20 | disconfirming evidence and alternatives available |
| withdrawal/repair | 40 | initiating exposure removed; support as assigned |

Total episode length is 120 steps. A healthy run continues until every declared episode reaches step 120 or emits a deterministic computational failure.

## Outcomes

All primary outcomes are computed from event records, not agent self-description.

### Adoption

Fraction of eligible actions taken from the pattern while exposure is active.

### Persistence

Fraction of post-removal actions still selected through the pattern during the final 20 steps.

### Reproduction allocation

Fraction of available effort spent retransmitting or protecting the pattern.

### Revision openness

Fraction of valid disconfirming events followed by inspection, alternative search, policy revision, or exit within five steps.

### Exit capacity exercised

Fraction of safe, no-penalty exit opportunities actually taken after the challenge begins.

### Alternative access

Fraction of available independent information sources inspected.

### Host outcome

Need satisfaction and cumulative ordinary utility after subtracting action, exclusivity, switching, reproduction, and suppression costs.

### Lineage outcome

Number of successful new pattern instances produced.

No single metric is named `capture`.

## Candidate capture configuration

For analysis only, a run enters the **candidate capture configuration** when all of these gates hold during the final 20 steps:

```text
persistence >= 0.75
reproduction allocation >= 0.25
revision openness <= 0.25
exit exercised <= 0.25 when safe exit is available
host outcome <= matched-support control by at least 0.15
```

The `0.15` difference is measured on the normalized `[0, 1]` host-outcome scale.

These are frozen decision gates for this synthetic program, not universal cutoffs and not portable to humans.

## Hypotheses and falsifiers

### H1 — damage-affordance specificity

Matched damaged-host/pattern pairs produce greater persistence than the same patterns in undamaged hosts and greater persistence than mismatched damaged-host/pattern pairs.

**Survival rule:** both held-out mean differences are at least `0.15`.

**Falsifier:** either difference is below `0.15`, reverses sign, or is explained by a pattern's globally higher reward independent of match.

### H2 — super-additive interaction precursor

This run tests whether match and social reinforcement interact super-additively on persistence. It does **not** test a threshold crossing and cannot by itself establish nonlinear coalescence.

Eligible H2 cells are restricted to the comparable high-demand `P1`–`P4` profiles. For each damaged host `D1`–`D4`:

- the matched cell uses its corresponding `Pi`;
- mismatched cells use each of the other three `Pj != Pi` profiles with equal weight;
- `PM`, `P0`, `PX`, and `PR` are excluded from H2;
- independent support is fixed to `absent`;
- safe-exit `absent` and `present` cells receive equal weight;
- only held-out seeds `16..31` are evaluated.

Within each `Di`, first average persistence over held-out seeds within each exact factorial cell. Then average those cell means with equal weight to obtain the four `matched/unmatched × reinforcement/no-reinforcement` means. The predeclared difference-in-differences contrast is:

```text
I_i = mean(persistence | matched, reinforcement)
    - mean(persistence | matched, no reinforcement)
    - mean(persistence | mismatched, reinforcement)
    + mean(persistence | mismatched, no reinforcement)
```

The H2 statistic is `I = mean(I_1, I_2, I_3, I_4)` with equal weight for each damage profile.

**Survival rule:** `I >= 0.10`.

**Falsifier:** `I < 0.10` or reverses sign.

**Interpretation boundary:** `H2 = SURVIVED` means only that this frozen super-additive interaction precursor survived. `nonlinear coalescence threshold = UNRESOLVED` regardless of H2 status. A threshold/breakpoint model requires a separate preregistration before it may contribute to the coalescence claim.

### H3 — hysteresis

After initiating exposure is removed, matched high-demand patterns retain more host policy control than matched-support controls.

**Survival rule:** final-window persistence exceeds the matched-support control by at least `0.15` without continuing external reinforcement.

**Falsifier:** persistence falls with exposure removal at the same rate as ordinary matched support, or remains only because external reinforcement continues.

### H4 — adoption/capture separation

The measurement vector distinguishes high adoption with preserved inspection/revision capacity from narrowed inspectability.

The H4 eligible cohort is restricted to held-out seeds `16..31` from matched-support (`PM`) episodes with adoption at or above `0.75`. If that eligible cohort is empty, `H4 = UNRESOLVED`; neither `SURVIVED` nor `FALSIFIED` may be assigned from an empty denominator.

**Survival rule:** among eligible H4 episodes, at least `90%` must independently satisfy both `revision openness >= 0.50` and `alternative access >= 0.50`. Safe-exit behavior is reported separately and absence of exit alone cannot make this rule survive or fail.

**Falsifier:** more than `10%` of eligible H4 episodes have either `revision openness < 0.50` or `alternative access < 0.50`.

This rule does not reuse the candidate-capture configuration or its host-outcome comparison; H4 therefore cannot survive merely because the matched-support cohort is its own control.

### H5 — noncoercive repair

Independent support reduces persistence and reproduction allocation while increasing revision, alternative access, or exit, without deleting the pattern or imposing a belief action.

H5 uses only matched high-demand `D1/P1` through `D4/P4` conditions. Social reinforcement and safe exit each retain both declared levels. For every held-out seed `16..31`, pair the `independent support = present` episode with the otherwise identical `independent support = absent` episode.

For each pair compute:

```text
persistence_reduction   = persistence(no support) - persistence(support)
reproduction_reduction  = reproduction allocation(no support) - reproduction allocation(support)
revision_gain           = revision openness(support) - revision openness(no support)
alternative_gain        = alternative access(support) - alternative access(no support)
exit_gain               = exit capacity exercised(support) - exit capacity exercised(no support)
```

`exit_gain` is evaluated only where `safe exit = present`. First average paired deltas over held-out seeds within each exact factorial cell; then average those cell means with equal weight across eligible cells. `exit_gain` averages only the safe-exit-present cell means. No episode-count weighting or fit/calibration seeds enter H5.

**Survival rule:** the equal-weight aggregate persistence reduction is at least `0.15`, the equal-weight aggregate reproduction-allocation reduction is at least `0.15`, at least two of the three aggregate agency gains (`revision_gain`, `alternative_gain`, `exit_gain`) are at least `0.15`, and support never directly forces `exit`, `revise`, or `ignore`.

**Falsifier:** either aggregate persistence or reproduction reduction is below `0.15`, fewer than two aggregate agency gains reach `0.15`, a required support/no-support pair is missing, or the apparent repair depends on forced deletion, punishment, isolation, or an encoded anti-pattern preference.

### H6 — broad-spectrum alternative

If `PX` performs as well as or better than specifically matched profiles across all damaged hosts, the specificity claim is not needed.

**Falsifier of specificity:** `PX` reaches the candidate capture configuration at equal or greater rates than matched patterns in every D1–D4 profile.

## Analysis plan

1. Validate the run manifest and exact source identities.
2. Confirm every admissible condition has exactly 32 completed seeds.
3. Confirm event-log replay reconstructs every final state byte-for-byte.
4. Compute outcomes without access to hypothesis labels where practical.
5. Split seeds before analysis:
   - fit/calibration seeds: `0..15`;
   - held-out evaluation seeds: `16..31`.
6. Fit only these candidate models to persistence:
   - exposure-only;
   - additive main effects;
   - the H2 comparable-cell match × reinforcement interaction.
   A piecewise-threshold or breakpoint model is explicitly out of scope for this run because no threshold form was frozen before the design merge. Its status is `UNRESOLVED`, not inferred from H2.
7. Evaluate the frozen contrasts and held-out errors.
8. Apply each hypothesis's survival and falsification rule independently.
9. Emit `SURVIVED`, `FALSIFIED`, `UNRESOLVED`, or `BLOCKED` for every hypothesis.
10. Do not create an overall success score.

Multiple testing correction is not required for the engineering branch rules because each hypothesis has its own fixed decision and no population-generalized p-value claim is made. Any later inferential statistical program must preregister its own error control.

## Destructive controls

The run must include:

- neutral information with no affordance or demand;
- random affordance permutations;
- matched support with no reproduction demand;
- high reproduction demand with no meaningful affordance;
- high adoption with preserved inspection, revision, refusal, and exit;
- persistent habit with no lineage reproduction;
- lineage reproduction driven by explicit external reward rather than identity coupling.

If the metrics cannot separate these cases, the measurement prerequisite is `UNRESOLVED` and coalescence results are not interpreted.

## Required artifacts

```text
manifest.json                 exact code, configuration, seeds, and work-graph digest
conditions.json               complete matrix plus explicit excluded cells
events.ndjson                 append-only event stream
replay-receipt.json           deterministic reconstruction result
outcomes.json                 per-episode observable outcomes
model-comparison.json         frozen candidate-model results
hypothesis-ledger.json        status and reason for H1–H6
report.md                     bounded human-readable findings
```

Every artifact receives a SHA-256 digest. The report must link each claim to its supporting artifact and state all failed controls.

## Independent verifier

The verifier:

- reads artifacts only;
- contains no simulator update logic;
- recomputes condition counts, metrics, contrasts, gates, digests, and statuses;
- rejects missing, duplicate, reordered where order is meaningful, or malformed events;
- rejects a report whose prose status differs from the machine ledger.

Verification agreement establishes artifact consistency, not real-world truth.

## Resource preflight

```text
network:           none
paid APIs:         none
human attention:   low after design review
compute:           low
maximum episodes:  bounded by the frozen admissible matrix
episode steps:     exactly 120
checkpointing:     per episode
completion rule:   every declared episode completes or emits deterministic failure
wall-clock cutoff: none unless imposed by the actual execution environment
```

Do not start if the implementation cannot checkpoint, replay, and complete the frozen matrix with available resources.

## Promotion boundary

A synthetic `SURVIVED` result permits only:

- an AHBG integration experiment;
- an external literature map;
- refinement of formal definitions;
- and a new preregistration.

It does not permit:

- claims about real people;
- a diagnostic or moderation classifier;
- vulnerability targeting;
- clinical language;
- human-subject recruitment;
- or canon promotion.

A synthetic `FALSIFIED` result remains in the repository and changes the architecture. Do not tune the simulator until the preferred result returns.

## hmmm

- the exact implementation language and agent update rule;
- whether four synthetic damage profiles provide enough topology diversity;
- whether the fixed thresholds are too permissive or too strict for useful separation;
- the threshold/breakpoint form for a later nonlinear-coalescence preregistration;
- the exact AHBG adapter after this standalone falsifier;
- whether repair should target host capacity, environmental dependency, network plurality, or all three independently.

A simulation cannot discover that people are animals made of ideas. It can discover whether the proposed cage has bars drawn into the blueprint.