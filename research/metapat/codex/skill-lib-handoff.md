# Codex Handoff: Make `skill-lib/meta` consume METAPAT

## Target repositories

- Source canon: `The-Interdependency/METAPAT`
- Consumer skill: `The-Interdependency/skill-lib`, directory `meta/`

## Mission

Alter `The-Interdependency/skill-lib` so the `meta` skill consumes METAPAT as upstream canon instead of acting as the primary home of Energy Theory.

`skill-lib/meta` remains useful as an agent skill. It should load and enforce METAPAT doctrine, not redefine it.

## Hard constraints

1. Do not create a new `energy-theory/` skill inside `skill-lib`.
2. Do not let `skill-lib` own Meta Energy Theory root canon.
3. Do not import consciousness, psychology, phenomenology, physics, linguistics, computation, EDCMBONE, FLAR, UCNS, a0, or a0p as root ontology.
4. Do not use `medium` as root definition of simplex. The current root phrase is: `A simplex is a bounded state-bearing object.`
5. Do not define time as consciousness, observer, story, or registration. Current canon: `Time is sequential tensor alteration.`
6. Do not define registration as parent of time. Registration preserves, expresses, or transmits sequential tensor alteration.
7. Preserve `hmmm` as unresolved marker, not decoration.

## Canon source to reference

Use METAPAT files as the source of truth:

- `README.md`
- `CHAPTER_ZERO.md`
- `AXIOMS.md`
- `POSTULATES.md`
- `THEOREMS.md`
- `GLOSSARY.md`
- `DOMAIN_RESTRAINT.md`
- `examples/`
- `tests/`

## Current skill-lib drift to correct

`skill-lib/meta/SKILL.md` currently frames the root around older terms such as:

```text
Distinction
Relation
Coupled Emergence
Ordered Transformation
```

That is now superseded by METAPAT Chapter Zero.

Update the `meta` skill to use this root spine:

```text
Legible difference is distinction.
Distinction defines boundaries.
Boundaries define simplex.
Boundary is simplex of distinction.
Simplex holds or modifies energy in a state of being.
```

And this primitive extension:

```text
Tensor is primitive simultaneous arrangement of energy-states.
Energy-state held is scalar.
Energy-state motioned is vector.
Energy-state vectors alter energy-state scalars.
Time is sequential tensor alteration.
Registration is the capacity of a simplex to preserve, express, or transmit sequential tensor alteration.
Observer is a simplex performing registration.
Consciousness is one possible observer-mode.
Story is conscious registration of time.
A question is a bounded unresolved energy-state.
```

## Required file changes in `skill-lib`

### 1. `meta/SKILL.md`

Rewrite to make `meta` a METAPAT consumer skill.

Required behavior:

- Load when asked to define, preserve, extend, test, or apply Meta Energy Theory.
- Treat `The-Interdependency/METAPAT` as canonical upstream.
- Enforce root/tool/domain separation.
- Enforce mind-agnostic language.
- Enforce boundary-as-simplex and tensor-primitive doctrine.
- Enforce question-finder framing: Energy Theory answers `What questions do I ask?`
- Route examples/tests back to METAPAT when they are ontology-level.

Suggested description field:

```yaml
description: Meta Energy Theory consumer skill. Load when defining, preserving, extending, testing, or applying METAPAT doctrine; when checking Energy Theory root/tool/domain separation; when evaluating tensor, simplex, boundary, relation, gradient dynamics, registration, time, question, or object-instantiation claims; or when ensuring domain examples do not capture the root.
```

### 2. `meta/AXIOMS.md`

Replace old root core with a compact mirror of `METAPAT/AXIOMS.md`.

Header should state:

```text
This file is a skill-lib mirror. Canonical upstream is The-Interdependency/METAPAT.
```

### 3. `meta/LAW_FAMILIES.md`

Keep as derived law-family / resonance layer.

Do not place root axioms here.

Retain useful law-family lines only as derived:

```text
Gradient dynamics select vector direction through tensor arrangement, simplex relations, and boundary-simplex states.
Energy-state vectors alter energy-state scalars.
```

The older line may remain as a resonance only if demoted:

```text
Gradient permits flow; architecture determines flow.
```

Mark it as a domain-shaped resonance, not root.

### 4. `meta/OVERLAP_GRID.md`

Update overlap grid to include METAPAT status categories:

- root axiom
- primitive extension
- derived theorem
- postulate
- explicationary tool
- domain example
- hmmm

Include rows for:

- physics/waves: scalar/vector as standing/propagating wave explicationary tool;
- computation: registration via log/state persistence;
- linguistics: question as bounded unresolved energy-state;
- cognition: gestalt as cognitive registration, not root;
- physical object: cup as boundary-simplex + space-within simplex tensor.

### 5. `meta/LOAD_BEARING_LINES.md`

Add METAPAT guardrails:

```text
Do not collapse time into consciousness.
Do not collapse registration into consciousness.
Do not collapse observer into mind.
Do not collapse gestalt into object-instantiation.
Do not collapse domain tools into root terms.
Do not collapse tensor into a late map of relations.
Do not collapse boundary into decorative edge.
```

### 6. `README.md`

Update the `meta/` row so it states that `skill-lib/meta` consumes METAPAT and enforces root/tool/domain separation.

Do not add a second Energy Theory skill row.

### 7. `skills.json`

Update the `meta` description to match the new upstream relation.

Do not change `kind`; keep it procedural.

### 8. Generated and sync files

After updates, run skill-lib maintenance checks and update generated files if needed:

```bash
python tools/check_skill_lib_drift.py
python tools/check_skill_compliance.py
python -m unittest discover -s tests
python -m llms.build --root . --out llms.txt --apply
python -m llms.build --root . --out llms.txt --check
```

If `AGENTS.md`, `CLAUDE.md`, `ORG_DISTRIBUTION.md`, or `llms.txt` drift because of the `meta` description change, update them consistently.

## Acceptance criteria

- `skill-lib/meta` clearly names `The-Interdependency/METAPAT` as canonical upstream.
- No local file in `skill-lib/meta` contradicts METAPAT Chapter Zero.
- The old four-root core is removed or explicitly marked superseded.
- Time is defined as sequential tensor alteration.
- Registration is defined as preserving, expressing, or transmitting sequential tensor alteration.
- Consciousness appears only as one observer-mode, not root.
- Gestalt appears only as cognitive registration of object-whole, not source of physical object-instantiation.
- `README.md` and `skills.json` stay consistent.
- Skill-lib tests/checks pass, or remaining failures are documented with `hmmm` and exact command output.

## Suggested branch and commit

```text
branch: codex/metapat-meta-upstream
commit: update meta skill to consume METAPAT canon
```

## Suggested PR title

```text
meta: consume METAPAT as upstream Energy Theory canon
```

## Suggested PR body

```markdown
## Summary
- Reframes `meta` as a METAPAT consumer skill rather than local root owner.
- Mirrors current METAPAT Chapter Zero root/primitive extension into `meta/AXIOMS.md`.
- Updates derived law-family, overlap, and load-bearing guardrails for tensor primitive, boundary-as-simplex, registration, and mind-agnostic observer language.
- Updates README/skills.json descriptions.

## Canon source
- The-Interdependency/METAPAT

## Tests
- [ ] `python tools/check_skill_lib_drift.py`
- [ ] `python tools/check_skill_compliance.py`
- [ ] `python -m unittest discover -s tests`
- [ ] `python -m llms.build --root . --out llms.txt --check`

## Hmmm
- Note any unresolved local skill-lib wording that cannot yet be fully aligned with METAPAT without broader skill inventory changes.
```
