# AGENTS.md

Guidance for agents working in `The-Interdependency/stack`.

## Stack role

`stack` is the active research stack. Named repositories are retained as archive
provenance: keep their identities, pinned commits, authority boundaries, and license
status visible even when active work moves into this repository.

Repo-level Public Gonol admission is downstream of research. Do not require a
participant's Public Gonol before construction; record closure and promotion only after
the research boundary is admissible.

## Editing boundaries

- Do not delete archived repository provenance.
- Do not edit participant research directories unless the task is explicitly scoped to
  that participant.
- Keep root stack lifecycle, manifest, CI, and verification changes outside participant
  research directories when possible.
- Before committing, run the stack manifest gate:

```bash
python3 tools/check_stack_manifest.py
```

## hmmm

- `research/epac/` is active provisional research with no external source archive yet.
- Root stack licensing is not fully settled because archived participants have mixed
  license states.
