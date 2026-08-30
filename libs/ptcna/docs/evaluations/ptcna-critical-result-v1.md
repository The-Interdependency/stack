# PTCNA critical role-acquisition evaluation — result v1

Status recorded before repair:

- PTCNA meets its frozen usefulness threshold: `FALSIFIED`.
- PTCNA outperforms the simpler hashed-linear fallback: `FALSIFIED`.

The preregistered plan was merged at
`f2028004cbee65f4a0a8c113e283bd38b29d1e2c` before execution. Its semantic
digest is `67cdad3aefb3e33f6fbf3994de54e1b73a01105527bf241fce08947ed7046bbe`.
The sealed machine result is
`ptcna/data/ptcna-critical-result-v1.json`, digest
`3d73f08f3e0eeaf0f5e508aba762844c9e8d11b7146b654fd562aff425e30f13`.

## Frozen execution

- Workload: 18 balanced cases over the declared `phi` cognitive, `psi`
  self-model, and `omega` autonomy roles.
- Target: `ptcna.experimental.v1`.
- Comparator: `fallback.hashed-linear.v1`.
- Training: three epochs, reward `1.0`.
- Repetitions: five fresh target/comparator constructions.
- Aggregation: micro mean over 90 post-training case evaluations.
- Usefulness threshold: target accuracy at least `0.75`.
- Superiority threshold: target advantage over fallback at least `0.05`.
- Resource use: 270/270 training steps, 90/90 evaluations, 46.675 seconds
  under the frozen 120-second limit.
- Failure: none.

## Result

| measure | result |
|---|---:|
| PTCNA target accuracy | 0.3333333333333333 |
| hashed-linear fallback accuracy | 0.9444444444444444 |
| target advantage | -0.6111111111111112 |

An implementation-independent arithmetic replay reads only the sealed JSON and
reapplies the two frozen inequalities. It agrees with both recorded verdicts.

## Standing

This falsifies usefulness for the tested in-sample role-acquisition scope and
falsifies superiority to this matched task-interface fallback. It does not
revoke the already established construction compatibility or replace the
selected architecture with the comparator. It establishes no generalization,
continuous seven-fold geometry, EDCM measurement validity, external validity,
or production privacy result.

No workload, architecture, reward, epoch count, metric, threshold, repetition,
resource rule, backend identity, or failure rule was changed after outcome
inspection.
