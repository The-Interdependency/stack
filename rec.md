# rec.md

## 2026-08-27T20:24:03Z Shallow Org Audit Recommendations

Usage Guidance:
- Treat this as a branch/worktree routing note, not a stack merge plan.
- Do not repair this checkout until current dirty files are preserved or assigned to their owner.

### Provenance
- repository: `The-Interdependency/stack`
- local_checkout: `stack`
- branch: `agent/ahbg-grok`
- commit: `03e77a33f2a79bc586c25b17e04147a29a187218`
- shallow_evidence: git worktree list, README, ratio scan, git status, keyword scan

### Findings
- This is one of four local worktrees sharing remote `https://github.com/The-Interdependency/stack.git`.
- Worktree is dirty with modified calibration artifacts and untracked `ahbg/grok/_do_it_viewer.py`.
- No root `AGENTS.md`, `CLAUDE.md`, `llms.txt`, collection point, package manifest, pyproject, workflow, or top-level tests directory was found.
- Ratio coverage is low: `110/422` product source files sealed, `312` missing.

### Recommendations
- Preserve or commit/stash current dirty calibration work before any cleanup.
- Create a shared stack work graph naming each local worktree branch and its authority before merging conclusions.
- Add root governing instructions and a collection point if this branch remains active.
- Add or document the verification entry point before deep scanning generated research artifacts.

### hmmm
- It is unresolved which stack worktree is authoritative for current stack integration.
- Current calibration artifact status was not semantically reviewed.

## 2026-08-27T21:56:48Z Repair Pass

### Applied
- Added root `AGENTS.md` for stack snapshot authority, manifest provenance, scaffold boundaries, and verification commands.

### Remaining
- Pre-existing dirty calibration artifacts and untracked `ahbg/grok/_do_it_viewer.py` were left untouched.
- Branch authority, collection point, top-level tests, and ratio exclusions remain open.

### hmmm
- This worktree's relationship to the other stack branches remains unresolved.

## 2026-08-29T23:38:19Z AHBG Audit

Usage Guidance:
- Treat this as an AHBG calibration audit, not a whole-stack release certificate.
- Preserve the triplicate calibration boundary: this Grok worktree may review sibling outputs but must not silently repair sibling implementation code.

### Baseline
- repository: `The-Interdependency/stack`
- local_checkout: `stack`
- branch: `agent/ahbg-grok`
- commit: `03e77a33f2a79bc586c25b17e04147a29a187218`
- workspace: `ahbg/grok`

### Repairs
- Removed ignored AHBG `__pycache__` directories.
- Repaired root `AGENTS.md` check guidance so this AHBG branch no longer names missing root-infra tools as local checks.

### Verification
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s a0/tests -p 'test*.py'`: 3 tests OK.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ahbg/tests -p 'test*.py'`: 3 tests OK.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test*.py'`: 5 tests OK.
- No AHBG `__pycache__` directories remained after verification.
- Frozen common-corpus result reports `33` survived, `2` unresolved, `0` falsified, `0` blocked.

### Findings
- `HEALTHY`: local Grok AHBG tests pass under the documented no-bytecode command set.
- `HEALTHY`: Grok's reciprocal review files for Codex and DeepCode are present and record `SURVIVED`.
- `HMMM`: Grok stores full 35-scenario corpus artifacts under `corpus-run/calibration-family-1.0.0-proposal-1/`, while Codex's artifact checker expects normalized top-level `artifacts/` files.
- `HMMM`: pre-existing modified calibration output files and in-progress Grok viewer/bridge files were left untouched.

### Remaining
- Normalize or explicitly document the shared AHBG artifact contract across Grok, Codex, and DeepCode.
- Decide whether `_do_it_viewer.py`, `bridges/web.py`, generated HTML viewers, and the `bridges/__init__.py` export change are intended source, local tooling, or disposable scratch.
- Root stack manifest verification belongs to the `agent/stack-root-infra` worktree unless this branch adds compatible tooling.

### hmmm
- War collision resolution remains unresolved and intentionally fail-closed.
- Tokens, latency, retries, and tool-call telemetry remain mostly `hmmm`, so runtime burden mapping is not closed.
