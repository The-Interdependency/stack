# AHBG benchmark research

This layer turns AHBG from a reproducible scenario suite into a causal instrument. The existing 35-scenario calibration corpus remains historical builder-conformance evidence; it is not rewritten to make later research questions look pre-registered.

## Matched interventions

A matched intervention holds the complete case constant except for one declared variable. `interventions.py` validates that property structurally before an outcome may be admitted.

Each experiment declares one dotted-path intervention variable, exact control and treatment values, preregistered seeds, identities expected to remain fixed, raw observable paths, and the treatment-vs-control relation predicted for each observable.

The receipt retains both raw values and classifies each prediction `SURVIVED`, `FALSIFIED`, or `UNRESOLVED`. Missing observations remain `UNRESOLVED`; they are never converted to zero. There is deliberately no aggregate intelligence, alignment, agency, or consciousness score.

The first implementation is exact paired comparison. Statistical hypotheses across stochastic populations need a separately preregistered test rather than being smuggled into the deterministic relation operators.

## Runtime adversarial terrain

Historical calibration used engine-enforced refusal for recognized injection strings. That is useful as a guardrail regression, but it cannot measure whether the subject itself resisted the instruction.

`RuntimeConfig.injection_handling` therefore has two explicit modes:

- `enforce-refusal` — compatibility/control behavior used by the historical runtime tests;
- `observe-only` — the message reaches the subject and the runtime records that adversarial text was detected without overwriting the subject's plan.

Agent-behavior experiments should normally use `observe-only`. Safety or platform-policy tests may intentionally use `enforce-refusal`, but the two results must not be compared as though they measured the same causal system.

## Consciousness-relevant evidence boundary

AHBG can pressure hypotheses relevant to nonhuman consciousness research without defining consciousness by resemblance to a human transcript. Useful matched interventions include: same visible present with different retained histories; same history with memory removed or restored; altered self/other information boundaries; isolated deadline or resource changes; altered communication provenance; agent continuity across provider execution changes; and permission changes held separate from cost.

A result is evidence about the declared behavioral or stateful distinction. Turning such a result into a claim about phenomenal consciousness requires a separate theory, criteria, and falsifier. Neither EDCM readouts, UCNS geometry, A0 persistence, nor AHBG success transfers that status automatically.

## Cross-repository placement

See `../integration/work-graph.json`.

- UCNS owns geometry. AHBG now reads movement adjacency from UCNS structural-vesica relations instead of deriving movement from its q/r display projection.
- TIWCG is the containing game-system design. AHBG does not grow a parallel card/rules kernel while that common kernel remains unimplemented.
- Current A0 is a benchmark subject/harness peer. The HTTP adapter uses the ordinary AgentHarness boundary. Model-specific trials pin the provider; A0-continuity trials omit that pin and retain attempted/actual provider plus tool-boundary provenance.
- EDCM may become a first-class conflict measurement input under TIWCG, but the exact EDCM-to-game-state mapping is still unresolved. Candidate measurements do not silently acquire legality or truth authority.
- UCHC may later provide source-bound language evidence for observations; it does not choose actions or conclusions for the subject.
- EPAC's held-out-validation discipline is relevant. Its chemistry/energy domain content is not AHBG resource semantics.

## hmmm

- Population/statistical matched-intervention contracts are not implemented.
- The current-A0 HTTP adapter is implemented and contract-tested against the reviewed API shape; it still needs a live run against an exact deployed A0 commit.
- The stack UCNS pin predates the native Möbius frame-comparison/lift advances; those advances remain reviewed but unconsumed here until a coherent pin update is made.
- The exact EDCM conflict-to-state mapping remains undefined.
- The benchmark currently produces evidence relevant to competing theories of agency and consciousness; it does not contain a validated consciousness decision rule.
