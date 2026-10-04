# Provisional domain claim — system-set trajectory

```yaml
surface_form: system-set
term_id: english-gonol.system-set
claiming_domain: Stack English Gonol Construction research
claimed_sense: a higher-order semantic construction represented by an ordered relation-bearing trajectory whose component identities and provenance remain recoverable
scope: research/english-gonol trajectory construction and downstream comparison handoff
claim_type: provisional
authority_source: operator-directed system-set convergence work, 2026-10-03
status: provisional
included_uses:
  - ordered semantic trajectories constructed from English Gonol identities
  - a candidate higher-order object whose structural recurrence may later be tested
excluded_uses:
  - UCNS structural equivalence judgment
  - METAPAT recurrence adjudication
  - EDCM measurement or validation
neighboring_terms:
  - semantic trajectory
  - tensor
  - structural recurrence
known_collisions:
  - ordinary-language uses of system and set
effective_version: system-set-trajectory-v0
supersedes: none
unresolved:
  - exact closure criterion by which a trajectory earns higher-order system-set identity
  - UCHC graduation and authority transfer
```

Usage: this claim licenses the provisional schema handle inside the Stack forge.
It does not make system-set a METAPAT primitive and does not authorize UCNS or
UCHC to infer semantic identity from matching labels or paths.

`SemanticStep.relation_id` is an opaque source relation reference under the
`english-gonol.system-set-trajectory` schema. It records a declared relation in
the English input; it does not evaluate that relation. The labels `equivalence`,
`analogy`, and `recurrence` may occur in source material and must remain
recoverable without becoming UCNS/METAPAT judgments. No value of `relation_id`
authorizes a downstream classification. Consumers require independent comparison
evidence and the owning adjudicator for those outcomes.

Usage: pass ordered sequences for steps, provenance IDs, and unresolved reasons.
The constructor freezes them to tuples. Scalar text, sets, mappings, and other
non-sequence containers fail closed instead of choosing an order or silently
discarding multiplicity.
