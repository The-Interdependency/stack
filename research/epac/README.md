# epac — placeholder scaffold

Reserved for **energy particle affixiation coupling**.

Status: `hmmm` — no source repository exists yet. This directory carries no doctrine
until a canonical `The-Interdependency/epac` source is created and pinned in
`STACK_MANIFEST.md`.

## Current content

- [`subatomic/subatomic-affixiation-baseline.md`](subatomic/subatomic-affixiation-baseline.md) —
  provisional research candidate: hydrogen → helium baseline and the lithium/carbon
  construction form over current METAPAT affixiation semantics and UCNS carrier identity.
  Status: CROSS-DOMAIN-HYPOTHESIS / proposed. Not org canon.
- [`docs/preregistration-molecular-geometry-from-element-gonols.md`](docs/preregistration-molecular-geometry-from-element-gonols.md) —
  provisional candidate: Z=1–18 element gonols from atomic structure only, then
  affixiation of H₂, H₂O, NH₃, CH₄, CO₂ through valence arity and UCNS Möbius
  coupling. Known chemistry is sealed until after construction.

## Usage

From this directory:

```bash
PYTHONPATH=".:../edcm:../ucns/src" python3 -m unittest discover -s tests -q
```

Do not open `data/sealed_known_molecular_geometry.json` during construction.
