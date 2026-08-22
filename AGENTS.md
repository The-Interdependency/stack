# AGENTS.md

Guidance for agents working in `The-Interdependency/stack`.

## Role

`stack` preserves archived repository provenance and provides the root surface for
cross-repository stack infrastructure. Keep named repository identities, archived source
commits, authority boundaries, and license status visible.

Public Gonol admission is downstream of research closure. Do not require a participant's
Public Gonol before construction; record closure and promotion only after the research
boundary is admissible.

## Boundaries

- Do not delete archived repository provenance.
- Do not rewrite participant research as part of root stack infrastructure.
- Keep stack-level verification, manifest, and CI changes at the repository root.
- Generated local state such as caches, build outputs, and skill usage state must not be
  committed.

Before committing root infrastructure or manifest changes, run:

```bash
python3 tools/check_stack_manifest.py
```
