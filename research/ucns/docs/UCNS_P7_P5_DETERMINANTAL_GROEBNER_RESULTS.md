# P7/P5 complete rational-Laurent determinantal ideals

**Status:** completed preregistered rational-Laurent computation certificates

**Protocol identity:** `7841af162698efb823db79b70ef7b99a5ac53d27e2bbb318f97f36aecae515b4`

## Result

Complete compound-family computation succeeded, independent exact Buchberger
replay returned the same canonical reduced lex bases, and every frozen direct
full-minor audit pair agreed exactly. Each audited minor was recomputed through
SymPy's fraction-field LU path and a separately implemented fraction-field
Gaussian path, then compared with the compound identity.

| case | all subset pairs | nonzero products | audit pairs | nonzero audited | normalized generators | reduced basis |
|---|---:|---:|---:|---:|---:|---:|
| P7 `E_1` | 1,444 | 1,444 | 111 | 111 | 7 | 7 |
| P5 `E_3` | 665,856 | 98,310 | 71 | 24 | 207 | 3 |

P7 basis SHA-256 is
`c3bdb9b27f20191320e85360063113ed7e250996830ca4a4fd2ca8f11637127d`.
P5 basis SHA-256 is
`5e20f2539229070c12261d70cd6f1ba202ddeee04c7105e4bea1945253b79711`.
The P7 direct-audit result SHA-256 is
`da18dcd07ea84d4bdbd5ebe5d59280f0e4290e7a50079107c3ebfb0a2dc399ec`.
The P5 direct-audit result SHA-256 is
`b351bbdea8428bf3f26f550acb4f38198b363fddd62c55e05dc9d68f9d1eb1ae`.

The P5 reduced basis depends only on `t_R1,t_R2,t_R3` and is

```text
(t_R1 - 1)(t_R2 - 1)
(t_R2 - 1)^2
(t_R2 - 1)(t_R3 - 1)
```

in the frozen variable order. P7 retains a seven-element, substantially larger
multivariable basis recorded coefficient-for-coefficient in its receipt.

The successful P7 run completed in 1,895.65 seconds, including 1,547.82
seconds for its audit. The successful P5 run completed in 2,651.56 seconds,
including 4.19 seconds for its audit. Earlier P7 attempts are retained as
failure evidence: a single-process audit was abandoned near the wall boundary,
and the original two-worker Bareiss schedule exhausted the 7,200-second bound.
Neither failure produced a success receipt or observed an exact mismatch. The
successful retry changed only the deterministic execution backend, not the
frozen selector set or equality criteria.

## Boundary

These are complete reduced bases after scalar extension to `QQ` and
localization at component variables. The current result does not establish an
integral-Laurent strong
basis or integer torsion. It does not select a phase law, classify ambient
isotopy, force a prime, define a spectral object, support a zeta correspondence,
or escalate theorem status.

Length-four Milnor invariants and finite nilpotent quotients remain an independent
research route. Any phase-co-winner separator still requires preregistration.
