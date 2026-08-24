# EPAC constraint ledger

Status: **provisional candidate**. Not org canon. Resolved means the constructor
now obeys the listed rule. Unresolved remains `hmmm`.

## Constraints that stand

| Id | Constraint | Standing |
|---|---|---|
| C1 | `epac.public_gonol`, not `edcm.gonol` | resolved |
| C2 | `(z,x) ≠ (x,z)` | resolved |
| C3 | overlap is not a proof of `(x,y,z)` | resolved |
| C4 | degree is required | resolved |
| C5 | 3-structure = oriented couplings + charge state + degree | resolved at each scale that has a 3 |
| C6 | representing a 3 takes 4 quaternion components; scalar is Möbius ε | resolved where a local 3 exists |
| C7 | Hamilton product is not a coupling proof | resolved (forbidden rule) |
| C8 | letters/abbreviations are not physics axes | resolved |
| C9 | protons and neutrons are precursor gonols of the nucleus | resolved |
| C10 | electrons couple to the closed nucleus; nucleons stay inside it | resolved |
| C11 | closed gonols are atomic at the next scale; promotion is allowed | resolved |
| C12 | molecular attachment consumes closed unpaired valence electrons, not `atomic_of` | resolved |
| C13 | atomic s→p promotion is an atomic excited gonol, not VSEPR | resolved |
| C14 | H₂ is a single binary and is not a 3 | resolved |
| C15 | sealed chemistry shapes stay out of construction | resolved |
| C16 | nothing bigger than atoms is an *input* to element construction | resolved |

## Contradictions

### X1 — molecular hub

- C5/C6 and “every instance has `(z, x_i)` / `(z, y_j)`” require **one hub** with degree ≥ 2 to make a molecular 3.
- “Valence electrons are arity coupled” was implemented as disjoint `(center_electron, ligand_electron)` pairs, each hub degree 1, so **no molecular 3**.

**Resolution:** two declared relations, not one inferred from the other.

1. **3-structure:** hub `z` is the closed center atom; instances are ligand unpaired valence electrons: `(center, ligand_e_i)`.
2. **Bond:** unpaired valence electrons are arity-coupled to each other: `(center_e_i, ligand_e_i)`.

Water: `deg(O#2)=2` on `(O#2, H0_e)` and `(O#2, H1_e)`; quaternion `(ε, 8, −1, −1)`. Bonds remain the two electron–electron couplings. Not `(x,y,z)`.

### X2 — “do not reopen electrons” vs “electrons make molecules”

**Resolution:** promote already-closed unpaired valence electron gonols as molecular *instances*. Do not flatten nucleons or core electrons into molecular axes.

### X3 — consume atomic 3-structure vs formula-count geometry

**Resolution:** composition still names which atoms. Attachment sites and charges come from closed gonols. Molecular 3 uses the closed center as hub and ligand valence electrons as instances.

### X4 — internucleon `(every proton, every neutron)` vs no all-pairs authority

**Unresolved / hmmm.** Bipartite `(proton, neutron)` is a declared nuclear candidate, not p–p or n–n fill, and not a selected nuclear force. Multiple proton hubs at nuclear scale is the same *shape* of question as X1 and is not closed here.

## Usage

After changing couplings, replay:

```bash
cd research/epac
PYTHONPATH=".:../ucns/src" python3 -m unittest discover -s tests -q
```
