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
| C12 | molecular attachment consumes published bonding surfaces, not `atomic_of` | resolved |
| C13 | atomic s→p promotion is an atomic excited gonol, not VSEPR | resolved |
| C14 | H₂ is a single binary and is not a 3 | resolved |
| C15 | sealed chemistry shapes stay out of construction | resolved |
| C16 | nothing bigger than atoms is an *input* to element construction | resolved |
| C17 | occupancy-2 `(n,l,m_l)` electrons pair inside the atom as `(e_ms+1, e_ms-1)` | resolved |
| C18 | bonding surfaces are leftover unpaired valence `(nucleus, e_i)` after pairing | resolved |
| C19 | carbon is the primary research atom; exactly one C instance is the molecular hub | resolved |

## Contradictions

### X1 — molecular hub

- C5/C6 and “every instance has `(z, x_i)` / `(z, y_j)`” require **one hub** with degree ≥ 2 to make a molecular 3.
- “Valence electrons are arity coupled” was implemented as disjoint `(center_electron, ligand_electron)` pairs, each hub degree 1, so **no molecular 3**.

**Resolution:** two declared relations, not one inferred from the other.

1. **3-structure:** hub `z` is the closed center atom; instances are ligand electrons of matched bonding surfaces: `(center, ligand_e_i)`.
2. **Bond:** matched bonding-surface electrons are arity-coupled: `(center_e_i, ligand_e_i)`.

Water: `deg(O#2)=2` on `(O#2, H0_e)` and `(O#2, H1_e)`; quaternion `(ε, 8, −1, −1)`. Bonds remain the two electron–electron couplings. Not `(x,y,z)`.

### X2 — “do not reopen electrons” vs “electrons make molecules”

**Resolution:** promote already-closed unpaired valence electron gonols as molecular *instances*. Do not flatten nucleons or core electrons into molecular axes.

### X3 — consume atomic 3-structure vs formula-count geometry

**Resolution:** composition still names which atoms. Attachment sites are the leftover unpaired valence `(nucleus, e_i)` published as bonding surfaces. Molecular 3 uses the closed center as hub and the ligand electrons of matched surfaces as instances.

### X5 — pairing vs nucleus–electron 3-structure

- C5/C6 already make `(nucleus, e_i)` the atomic 3.
- Occupancy-2 pairing is a second declared relation `(e_ms+1, e_ms-1)`, not a proof of `(nucleus, e_i, e_j)`.

**Resolution:** two declared atomic relations, same shape as X1. Pairing does not install a ternary. Leftover unpaired valence incidences remain the bonding surfaces.

### X4 — internucleon `(every proton, every neutron)` vs no all-pairs authority

**Unresolved / hmmm.** Bipartite `(proton, neutron)` is a declared nuclear candidate, not p–p or n–n fill, and not a selected nuclear force. Multiple proton hubs at nuclear scale is the same *shape* of question as X1 and is not closed here.

### X6 — carbon hub vs stoichiometric singleton

**Resolution:** this candidate freezes carbon as the primary research atom. Exactly one carbon instance is the hub. Without carbon, the unique singleton remains the hub. Multiple carbons, ions, and group fragments stay outside the declared run.

## Usage

After changing couplings, replay:

```bash
cd research/epac
PYTHONPATH=".:../ucns/src" python3 -m unittest discover -s tests -q
```
