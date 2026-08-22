# Preregistration: molecular geometry from element gonols

- Status: **CROSS-DOMAIN-HYPOTHESIS / provisional research candidate**
- Owner of record: `The-Interdependency/stack` → `research/epac/`
- Constructor: `edcm.gonol` from the pinned EDCM snapshot
- Comparison policy is frozen **before** construction. Known molecular-shape
  labels are sealed and may be opened only by the comparison step.

## Domain claims

| Surface form | Term id | Claiming domain | Claimed sense | Excluded |
|---|---|---|---|---|
| element gonol | `epac.periodic.element_gonol` | epac candidate | closed gonol of one periodic-table element carrying Z, ground-state electron configuration, and typical main-group valence | molecular shape, bond angle, hybridization |
| valence arity | `epac.periodic.typical_valence` | epac candidate | main-group hydride valence from the periodic table (group-derived) | VSEPR domain count as a shape rule |
| affixiation | `metapat.affixiation_harmonics.affixiation` | METAPAT | identity-preserving higher-order relation | UCNS topology selection |
| UCNS coupling | `ucns.native-mobius-root-loop` | UCNS | established 360° frame flip / 720° restore | invented 3-space arrangement |
| molecular gonol | `epac.molecular.affixiated_whole` | epac candidate | closed recursive gonol of element-gonol participants | known chemistry shape names |
| predicted geometry | `epac.molecular.construction_invariants` | epac candidate | atom count, center valence, slot occupancy, Möbius frame sequence | sealed comparison labels |

Collision check: physics/chemistry own empirical molecular shapes. This candidate
does not claim those senses during construction. Resolution: **clear** (separate
scopes) until comparison.

## Frozen pipeline

```text
element gonols
  -> valence arity
  -> affixiation
  -> UCNS coupling geometry (native Möbius only)
  -> molecular gonol
  -> construction invariants
  -> (only then) compare to sealed known chemistry
```

## Inputs allowed in construction

- atomic number Z, default isotope A, proton and neutron counts
- every electron: n, l, m_l, m_s, shell, subshell
- hydrogenic angular identity Y_l^m, radial node count n-l-1
- Slater atomic Z_eff and hydrogenic Rydberg energy -Z_eff²/n²
- unpaired valence electrons from Hund filling
- atomic s→p promotion in the same n when more unpaired sites are required
- caller-supplied stoichiometric formula (element counts only)

## Inputs forbidden in construction

- bond angles
- VSEPR shape names
- hybridization labels used as shape
- any sealed comparison filename contents

## UCNS coupling candidate

Only the implemented Möbius root loop is applied:

```text
(t, ε) ~ (t + n, (-1)^n ε)
t = 0, 1, 2
```

Public Gonol positions, when supplied, are identity coordinates. Position
operations remain `hmmm`. No spherical equal-spacing rule is added.

## Molecules in this run

`H2`, `H2O`, `NH3`, `CH4`, `CO2`

## Comparison policy (frozen)

Opened only after molecular gonols exist:

1. Construction source and receipts must not contain the sealed shape labels.
2. Record construction invariants per formula.
3. Open `data/sealed_known_molecular_geometry.json`.
4. Ask whether UCNS coupling invariants distinguish formulas that chemistry
   distinguishes by shape.
5. Compare three signatures: UCNS Möbius coupling; atomic unpaired (l, m_l)
   plus ligand shell content; and a matched-information control of formula
   symbols only.

## Terminal standings for the hmmm question

The question: does gonol geometry predict molecular shape, or merely reproduce
information already present in the inputs?

- `SURVIVED` as prediction — only if UCNS coupling invariants distinguish
  sealed shape classes after subtracting the matched-information control.
- `FALSIFIED` as prediction — if those invariants are identical across sealed
  shape classes, or if distinguishing power is already present in
  valence+stoichiometry.
- `UNRESOLVED` — if the readout is incomplete.
- None of these standings select canon.

## hmmm

- Public Gonol function operations beyond carrier identity
- whether a later UCNS 3-space coupling exists that is not VSEPR imported
- expansion of the element table beyond Z=1–18
- epac still has no canonical source repository
