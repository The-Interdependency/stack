# STACK_MANIFEST.md

Provenance record for the consolidated snapshots in `The-Interdependency/stack`.

- Snapshot UTC: `2026-08-22T10:19:43Z`
- Stack-manifest schema: `the-interdependency.stack-manifest` version `1.0.0`
- Work-graph digest (SHA-256 over canonical `repositories` + `boundaries` JSON):
  `f7a56ead99174598fd37e044f25c88b5dd47f53f9e4836c41620781bc3e6494a`
- Machine-readable copy: [`stack-manifest.json`](stack-manifest.json)

## Participants

| Repository | Exact source commit | Source branch | Authority | Snapshot path |
|---|---|---|---|---|
| `The-Interdependency/skill-lib` | `fb3b53a7629f7f03ecf255167d52c13abef1a979` | main | organization-wide build and evidence doctrine | `skill-lib/` |
| `The-Interdependency/metapat` | `34d954aa1e2092e615b03a180500f6b6977f501e` | main | semantic authority (Meta Energy Theory) | `research/metapat/` |
| `The-Interdependency/ucns` | `1975fe70cf4e0826a8020c2da3047569e277af64` | main | geometry and mathematical representation | `research/ucns/` |
| `The-Interdependency/edcm` | `7951ca32ba0f2494dc68ff9b7f6a80151918a56d` | main | measurement and text-gonol construction | `research/edcm/` |
| `The-Interdependency/pcea` | `4d2c581448b97bfb71da92b35487e74e6e3bcedc` | main | prime circle encryption algorithm | `research/pcea/` |
| `The-Interdependency/ptcna` | `97abdd1bbda61a68e0aac8595a32a3cb0ce73487` | main | prime tensor circled neural architecture | `research/ptcna/` |
| `The-Interdependency/epac` | `hmmm` | — | placeholder scaffold for energy particle affixiation coupling; no source repository exists yet | `research/epac/` |

Each `research/` snapshot is the complete tracked working tree of its source repository at
the pinned commit, produced with `git archive HEAD`. VCS data, virtualenvs, caches, and
untracked files are excluded by construction.

## License status at snapshot commits

| Repository | License file |
|---|---|
| skill-lib | MPL-2.0 (`LICENSE`) |
| metapat | MPL-2.0 (`LICENSE`) |
| ucns | none at `1975fe7` — `hmmm` |
| edcm | MPL-2.0 (`LICENSE`) |
| pcea | present (`LICENSE`) |
| ptcna | present (`LICENSE`) |
| epac | placeholder — no license yet |

## Non-transfer boundaries

- `authority_transfer: false` — snapshots do not gain authority over the source repositories.
- `proof_status_transfer: false` — no proof/theorem status transfers into this aggregation.
- `measurement_status_transfer: false` — no measurement/empirical validity transfers.
- `semantic_mapping: external-provenance` — canonical meaning remains owned by the source
  repositories; this repo only pins identities.
- `research/` snapshots are **not the source of truth**. Edit the canonical repositories
  first, then refresh this snapshot.

## Refresh procedure

For each pinned repository, from a clean checkout at the desired commit:

```bash
git -C <checkout> archive <commit> | tar -x -C research/<name>/
```

Then update this file and `stack-manifest.json`, recompute the work-graph digest, and
commit with a message citing the new source commit SHAs.

## hmmm

- ucns has no LICENSE file at snapshot commit `1975fe7`; its licensing terms need to be
  resolved at the source repository.
- epac has no source repository yet; its placeholder carries no doctrine until one exists.
- `libs/`, `backend/`, and `frontend/cli/` are intentional empty scaffolds reserved for
  later stack integration work.
