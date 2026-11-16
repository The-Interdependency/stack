# Native attachment target stabilizer v0

Standing: **Stack-local explicit-assumption geometry experiment**.

Receipt SHA-256: `6133673d732eff5ce00c2abfa2e29de86034c6aef501e9920f4b0107ab200d0f`.

## Exact result

| Target | Stabilizer order | Deck swap | Reflection | Verdict |
|---|---:|---|---|---|
| `visible-phase-basepoint` | 4 | True | True | `FALSIFIED` |
| `c2-invariant-two-lift-fiber` | 4 | True | True | `FALSIFIED` |
| `single-complete-framed-lift` | 2 | False | True | `FALSIFIED` |
| `single-lift-with-directed-local-germ` | 1 | False | False | `SURVIVED_LOCALLY` |

The visible phase target and its full two-lift fiber are the same complete-state subset with the same stabilizer. A single lift removes the deck swap but retains reflection. Adding one directed local germ makes the target rigid within the declared signed-turn isometry group.

## First remaining irreducible assumption

**geometry-owned oriented incidence**: one intrinsic UCNS relation must attach Structural Null or Public Gonol origin to a complete native Mobius state and distinguish one local displacement germ

## Next experiment

**public-origin to native-germ incidence sieve**. an exact carrier-owned incidence must select one directed germ with trivial signed-turn-isometry stabilizer and replay independently of source order, frame defaults, covering-degree choice, hashes, or PCEA expectations

## Security boundary

PCEA cryptographic security remains `FALSIFIED`. The general UCNS trapdoor lift remains `UNRESOLVED`; its smallest fourth-power candidate remains `FALSIFIED`.

hmmm: the directed germ is the smallest locally sufficient refinement tested here, but current geometry still does not select one.
