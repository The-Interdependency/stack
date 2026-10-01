# Native attachment target stabilizer audit v0

Date: 2026-09-19. Standing: **Stack-local explicit-assumption geometry experiment**.

This audit resumes from the old origin-attachment STOP. It does not promote a
UCNS origin attachment. It asks a narrower question: what is the smallest
native target structure that would make a local attachment rigid if geometry
selected it?

## Exact sources

| Source | Identity | Use |
|---|---|---|
| Stack PR #42 | `57e3f047c092a6df5435ed4f502347664513a0ff` | research base |
| Stack agent-guidance base | `7419712f5bfa0813b9d2e8f28743aa44dad6f30c` | parent commit and governing repository instructions |
| Stack rooted-closure follow-on | `ef9dfee02f67231e08d49cc44159bfee501aef28` | predecessor constructor and successor gate |
| UCNS authority | `d8f0c505e6f5132e9711de0e7c24e4718e77e51a` | current native Möbius and visible-boundary standing |
| PCEA authority | `1595842abd1a5b443c6a601a2afe935b60c4adf7` | current stable runtime |
| METAPAT authority | `e4165b0cac9eca41daef9c2f941881028ca55d48` | semantic/domain boundary |
| skill-lib authority | `dd5027d99516831c0dcb83a176a67140d3819b66` | evidence and option-selection workflow |
| PCEA crypto audit | `0b49672862a30cec0a0ee24e39a34241c9626f27` | separate security falsification |
| unpublished trapdoor audit base | `82dc5e39f1e0c3f162138c2e7b642814df14dd98` plus receipt/source hashes in the JSON receipt | separate trapdoor standing |

The local VM also contained separate unpublished working heads for METAPAT
`e3111d9bf34eae17255af96d2e4f6c072ef16dc4` and skill-lib
`22c2c5702d14fb4b0faeb717777ecab2665770a1`. They were consulted as local
working evidence, not substituted for the published work-graph authorities.
METAPAT's local affixiation application confirms that an ordered parameter may
be spatial or orientational without becoming time. Here the parameter is exact
turn displacement.

The receipt binds the current UCNS source hashes. In particular, current UCNS
canon still calls the visible-to-complete-state lift unresolved, and the
current gonal trace explicitly stops at the visible 360-degree boundary. The
unpublished PCEA boundary bridge likewise reports no canonical derivation
functor. Current PCEA differs from the crypto-audited runtime only in metadata
and test witnesses, so no repaired security behavior was found.

## Rechecking the old blocker

The frozen basepoint audit modeled unframed visible states as `Q/Z` and proved
that exact translations act simply transitively. That result is valid, but its
scope is only an unframed point selector. It did not compare the full two-lift
fiber, one complete lift, or a directed germ.

A dynamic replay of that historical module now stops on its own terminology
drift detector because later UCNS commits introduced two matching certificate
phrases. That is inherited source drift, not a counterexample to its frozen
proof. This audit binds the frozen predecessor receipt by digest and rebuilds
the larger complete-state calculation independently.

The complete native state can be represented exactly as

```text
X = Q/2Z.
```

Visible projection and the deck involution are

```text
pi([x]_2) = [x]_1,
delta([x]_2) = [x+1]_2.
```

This representation was cross-checked against the pinned
`NativeMobiusState.advance`: one turn preserves visible phase and exchanges
frames; two turns restores complete state; exact inverse motion restores the
starting state.

Because direction is the field under test, the relevant symmetry group cannot
presuppose oriented signed-displacement preservation. The audit uses the exact
group of turn isometries that preserves displacement up to one global sign

```text
x -> s*x + c  (mod 2),  s in {-1,+1}, c in Q/2Z,
d -> s*d.
```

The `s=-1` elements are exact direction-reversing reflections.

## Frozen candidate assumptions

The target coordinate `0` is an explicit control, not an intrinsic choice.
No observed gonol cardinality occurs in the constructor.

| Candidate target | Exact stabilizer | Order | Result |
|---|---|---:|---|
| visible phase `[0]_1` | `tau_0, tau_1, rho_0, rho_1` | 4 | `FALSIFIED` as sufficient for direction |
| unordered fiber `{[0]_2,[1]_2}` | `tau_0, tau_1, rho_0, rho_1` | 4 | `FALSIFIED` as additional information |
| complete lift `[0]_2` | `tau_0, rho_0` | 2 | `FALSIFIED` as sufficient for direction |
| complete lift plus positive local germ | `tau_0` | 1 | `SURVIVED_LOCALLY` as an explicit constructor |

The smallest collision is exact:

```text
visible target [0]_1
inverse-image fiber pi^-1([0]_1) = {[0]_2,[1]_2}
```

The visible target and the full fiber name the same complete-state subset and
have the same stabilizer. Treating them as two primitive observables is
`DEPRECATED`.

Selecting one lift adds one frame observable and removes the deck swap
`tau_1`. It does not choose direction: reflection `rho_0(x)=-x` fixes the
selected lift and reverses every local displacement. Adding one directed local
germ removes that final reflection. The same stabilizer orders and collision
hold for the tested nonzero rational phases `1/3`, `2/5`, and `7/11`.

## Dependency-chain audit

| Field | Why it is needed | Implementation | Selection / obstruction | Classification |
|---|---|---|---|---|
| origin attachment | transports the singular origin into a traversable carrier target | constructible for each explicit target assumption | no geometry-owned incidence; homogeneous target orbits have no equivariant selector | `UNRESOLVED` |
| direction/chirality | distinguishes the two local signed germs | directed-germ control executes | visible, fiber, and single-lift targets retain a reversing stabilizer | `UNRESOLVED` |
| rotation system | supplies cyclic successor `sigma` on incident darts | paired-germs and sign-blocks both execute | the two rotations retain earlier fields but yield different face cycles and genus | `FALSIFIED` as derivable from earlier fields |
| marked outgoing dart | converts cyclic boundary data into a based traversal | first-role control executes | source/relation order is provenance, not selected geometry | `UNRESOLVED` |
| closure | turns `alpha` and `sigma` into a declared face/attaching operation | ribbon face rule `phi=sigma after alpha` executes | no selected global attaching or torsion law; ordinary closure yields order `1` or no finite order | `UNRESOLVED` |

This separates three different failure modes. Candidate implementations exist
for every field. Intrinsic selections do not. The exact stabilizers and the
rank-two rotation collision are mathematical obstructions to deriving later
fields from the retained earlier data alone.

## Successor and security gates

The constructor bytes and target set were frozen without `157`, `2881`,
`54837698421`, or the interpolation control. No candidate derives a successor
selector, so the observed successor chain was not evaluated again. The prior
frozen paired-germs and sign-blocks candidates remain `FALSIFIED` at their first
comparison and remain stopped.

Geometric correctness and security remain separate:

- explicit directed-germ local constructor: `SURVIVED_LOCALLY`;
- intrinsic selection of that germ: `UNRESOLVED`;
- PCEA cryptographic security: `FALSIFIED` by commit `0b49672`;
- general UCNS trapdoor lift: `UNRESOLVED`;
- minimal fourth-power trapdoor candidate: `FALSIFIED`.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  research.ucns.tests.test_native_attachment_target_stabilizer -v

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/ucns/native_attachment_target_stabilizer.py \
  --write-receipts research/ucns/receipts
```

The deterministic receipts are
[`native-attachment-target-stabilizer-v0.json`](../receipts/native-attachment-target-stabilizer-v0.json)
and
[`native-attachment-target-stabilizer-v0.md`](../receipts/native-attachment-target-stabilizer-v0.md).

## First remaining irreducible assumption

**Geometry-owned oriented incidence:** one intrinsic UCNS relation must attach
Structural Null or Public Gonol origin to a complete native Möbius state and
distinguish one local displacement germ.

The directed germ is the smallest locally sufficient refinement tested in the declared signed-turn isometry group.
It is still an explicit control, not selected geometry.

## Next resolving experiment

Freeze a **Public-origin to native-germ incidence sieve** using:

1. the exact 157-position Public Gonol arrangement;
2. current visible gonal samples `r/157`;
3. the native projection `Q/2Z -> Q/Z`;
4. all lift and local-germ choices before any successor comparator is visible.

Compare the visible map, its unordered inverse-image fiber, and a complete
lift plus directed germ as the stronger control. The experiment survives only
if a carrier-owned incidence selects one directed germ with trivial signed-turn-isometry stabilizer
without source order, frame defaults, arbitrary continuum covering degree,
hashes, or PCEA expectations.

hmmm: current UCNS supplies the visible sample geometry and the complete native
cover separately. It still supplies no authority-declared incidence between
the Public Gonol origin and one oriented complete-state germ.
