# STACK_MANIFEST.md

Provenance and lifecycle record for the consolidated research stack in
`The-Interdependency/stack`.

- Snapshot UTC: `2026-08-22T12:20:36Z`
- Stack-manifest schema: `the-interdependency.stack-manifest` version `1.0.0`
- Work-graph digest (SHA-256 over canonical `repositories` + `boundaries` JSON):
  `5cb76f4cea491b2c50ac009477c6df13482ede47f826e29e75f8f56a102cfabf`
- Machine-readable copy: [`stack-manifest.json`](stack-manifest.json)

## Participants

| Repository | Archived source commit | Source branch | Authority | Stack path |
|---|---|---|---|---|
| `The-Interdependency/skill-lib` | `fb3b53a7629f7f03ecf255167d52c13abef1a979` | main | organization-wide build and evidence doctrine | `skill-lib/` |
| `The-Interdependency/metapat` | `34d954aa1e2092e615b03a180500f6b6977f501e` | main | semantic authority (Meta Energy Theory) | `research/metapat/` |
| `The-Interdependency/ucns` | `1975fe70cf4e0826a8020c2da3047569e277af64` | main | geometry and mathematical representation | `research/ucns/` |
| `The-Interdependency/edcm` | `7951ca32ba0f2494dc68ff9b7f6a80151918a56d` | main | measurement and text-gonol construction | `research/edcm/` |
| `The-Interdependency/pcea` | `4d2c581448b97bfb71da92b35487e74e6e3bcedc` | main | prime circle encryption algorithm | `research/pcea/` |
| `The-Interdependency/ptcna` | `97abdd1bbda61a68e0aac8595a32a3cb0ce73487` | main | prime tensor circled neural architecture | `research/ptcna/` |
| `The-Interdependency/epac` | `hmmm` | stack-owned | provisional energy particle affixiation coupling research; no external source archive yet | `research/epac/` |

For participants with an archived source commit, the stack path began as the complete tracked
working tree of its source repository at that commit, produced with `git archive HEAD`. VCS
data, virtualenvs, caches, and untracked files are excluded by construction. Stack-owned
research deltas may then continue in this repository while the archived source identity is
retained for replay and provenance.

## License status at snapshot commits

| Repository | License file |
|---|---|
| skill-lib | MPL-2.0 (`LICENSE`) |
| metapat | MPL-2.0 (`LICENSE`) |
| ucns | none at `1975fe7` — `hmmm` |
| edcm | MPL-2.0 (`LICENSE`) |
| pcea | present (`LICENSE`) |
| ptcna | present (`LICENSE`) |
| epac | stack-owned provisional research — root stack licensing unresolved |

## Non-transfer boundaries

- `authority_transfer: false` — archived repositories do not transfer theorem, measurement,
  or promotion status merely by being archived into stack.
- `proof_status_transfer: false` — no proof/theorem status transfers into this aggregation.
- `measurement_status_transfer: false` — no measurement/empirical validity transfers.
- `semantic_mapping: stack-research-with-archive-provenance` — stack is the working research
  surface while archived repository identities remain visible.
- `archive_provenance_required: true` — named repositories are kept because provenance matters.
- `public_gonol_timing: after-research-closure` — each participant's Public Gonol is closed
  after research reaches an admissible boundary, not before construction.

## Archive procedure

For each pinned repository, from a clean checkout at the desired commit:

```bash
git -C <checkout> archive <commit> | tar -x -C research/<name>/
```

Then update this file and `stack-manifest.json`, recompute the work-graph digest, and
commit with a message citing the archived source commit SHAs. After archival, stack-owned
research may continue here unless the participant is deliberately split back out.

## Verification

Run the root verifier after manifest or lifecycle edits:

```bash
python3 tools/check_stack_manifest.py
```

The verifier checks the machine manifest schema, declared paths, archive-status fields,
non-transfer boundaries, and digest agreement with this file.

## hmmm

- ucns has no LICENSE file at snapshot commit `1975fe7`; its licensing terms need to be
  resolved at the source repository.
- epac has no external source archive yet; its current material is stack-owned provisional
  research and remains candidate status until closure.
- Repo-level Public Gonol closure receipts are not present yet; they occur after research,
  before promotion.
- `libs/`, `backend/`, and `frontend/cli/` are intentional empty scaffolds reserved for
  later stack integration work.
