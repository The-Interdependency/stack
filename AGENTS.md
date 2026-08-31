# stack agent guide

This checkout is a working branch of `The-Interdependency/stack`, the
provenance-bearing aggregation of the organization's core repositories.

## Authority

- `research/` snapshots are pinned evidence. Canonical edits happen in the
  source repositories first.
- `STACK_MANIFEST.md` and `stack-manifest.json` own stack-level provenance.
- `libs/`, `backend/`, and `frontend/cli/` are reserved scaffolds until explicit
  stack-level contracts promote them.

## Boundaries

- Do not edit `research/` snapshots as doctrine or silently update source
  commits.
- Do not transfer authority, proof, or license status between participant
  repositories.
- For behavior-bearing build changes, use the applicable instructions from the
  canonical `skill-lib` checkout or vendored skills if they are added later.
- Generated local state, caches, and build outputs must not be committed.

## Checks

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m unittest discover -s ahbg/deepseek/a0/tests -p 'test*.py'
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m unittest discover -s ahbg/deepseek/ahbg/tests -p 'test*.py'
```

This branch does not currently carry the root-infra stack manifest check tools;
do not claim `tools/check_stack_manifest.py` or `tools/check_msdmd_paths.py`
verification here unless those tools are added with a compatible manifest.

## hmmm

- The final shape of consolidated libraries, backend, frontend CLI, and EPAC
  source remains unresolved.
- Stack manifest verification tooling is present in the `agent/stack-root-infra`
  worktree, not this AHBG worktree.
