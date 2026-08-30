# STACK_MANIFEST.md

Provenance and authority-boundary record for `The-Interdependency/stack`.

- Source snapshot UTC: `2026-08-22T10:19:43Z` (source commits unchanged by this layout migration)
- Layout migration UTC: `2026-08-30T02:52Z`
- Stack-manifest schema: `the-interdependency.stack-manifest` version `1.0.0`
- Work-graph digest (SHA-256 over canonical `repositories` + `boundaries` JSON):
  `0760abd60f089266405aa589063a7533f485761e2bd25faa44f2eac64fb89f7d`
- Machine-readable copy: [`stack-manifest.json`](stack-manifest.json)

## Directory contract

For an established repository participating in stack:

```text
libs/<repo>/       = exact imported canonical repository view at the manifest commit
research/<repo>/   = mutable stack-local research based on that imported view
```

`libs/` does not gain authority by containing a copy. The owning repository remains
canonical. `research/` does not gain canon status by producing a useful result.

A Python `src/` directory inside `libs/<repo>/` retains the normal package-layout
meaning used by that repository.

## Participants

| Repository | Exact source commit | Source branch | Authority | Stack relation |
|---|---|---|---|---|
| `The-Interdependency/skill-lib` | `fb3b53a7629f7f03ecf255167d52c13abef1a979` | main | organization-wide build and evidence doctrine | operational snapshot at `skill-lib/` |
| `The-Interdependency/metapat` | `34d954aa1e2092e615b03a180500f6b6977f501e` | main | semantic authority (Meta Energy Theory) | canon view `libs/metapat/`; research `research/metapat/` |
| `The-Interdependency/ucns` | `1975fe70cf4e0826a8020c2da3047569e277af64` | main | geometry and mathematical representation | canon view `libs/ucns/`; research `research/ucns/` |
| `The-Interdependency/edcm` | `7951ca32ba0f2494dc68ff9b7f6a80151918a56d` | main | measurement and text-gonol construction | canon view `libs/edcm/`; research `research/edcm/` |
| `The-Interdependency/pcea` | `4d2c581448b97bfb71da92b35487e74e6e3bcedc` | main | prime circle encryption algorithm | canon view `libs/pcea/`; research `research/pcea/` |
| `The-Interdependency/ptcna` | `97abdd1bbda61a68e0aac8595a32a3cb0ce73487` | main | prime tensor circled neural architecture | canon view `libs/ptcna/`; research `research/ptcna/` |
| `The-Interdependency/epac` | `hmmm` | — | stack-local emerging research; no independent source repository exists yet | active candidate `research/epac/`; `libs/epac/` unpopulated |

The imported `libs/` trees are the complete tracked working trees of their source
repositories at the pinned commits, produced from Git trees / `git archive` contents.
VCS metadata, virtualenvs, caches, and untracked files are excluded.

## Research base records

Each established `research/<repo>/` workspace carries a `BASE.json` with:

- owning repository;
- exact source commit;
- matching `libs/<repo>/` canon path;
- authority owner;
- standing `stack-local-research`.

Use that record before interpreting or extending work in the workspace.

## License status at pinned commits

| Repository | License file |
|---|---|
| skill-lib | MPL-2.0 (`LICENSE`) |
| metapat | MPL-2.0 (`LICENSE`) |
| ucns | none at `1975fe7` — `hmmm` |
| edcm | MPL-2.0 (`LICENSE`) |
| pcea | present (`LICENSE`) |
| ptcna | present (`LICENSE`) |
| epac | no independent repository/license yet |

## Non-transfer boundaries

- `authority_transfer: false` — imported canonical views do not gain authority over their owners.
- `proof_status_transfer: false` — no proof/theorem status transfers through stack composition.
- `measurement_status_transfer: false` — no measurement/empirical validity transfers.
- `semantic_mapping: external-provenance` — canonical meaning remains owned by source repositories.
- `research/` is explicitly noncanonical stack-local work.
- `libs/` is read-only by contract and is refreshed only from an owning repository at an exact commit.

## Refresh procedure

For each pinned repository, from a clean checkout at the desired commit:

```bash
rm -rf libs/<name>/*
git -C <checkout> archive <commit> | tar -x -C libs/<name>/
```

Then update this file, `stack-manifest.json`, and `research/<name>/BASE.json`; recompute
the work-graph digest; and commit with the new source commit SHA.

Do not edit `libs/<name>/` to create a canonical change. Route the change to the owning
repository, merge it there, then refresh the pinned view.

## Graduation boundary

A project born in stack (currently EPAC; AHBG follows its own workspace) may eventually
become an independent repository. Graduation is not accomplished by copying its research
tree into `libs/`. First create the owning repository and preserve provenance; after the
new repository becomes authoritative and a commit is pinned, populate its `libs/<name>/`
view from that authority.

## hmmm

- UCNS has no LICENSE file at pinned commit `1975fe7`; licensing terms need resolution at source.
- EPAC has no independent source repository or populated canonical `libs/epac/` view yet.
- `skill-lib/` remains a special operational snapshot at stack root rather than following the
  ordinary `libs/` + `research/` pair.
