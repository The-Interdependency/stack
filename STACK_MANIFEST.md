# STACK_MANIFEST.md

Provenance and archive identity record for the consolidated research stack in
`The-Interdependency/stack`.

- Snapshot UTC: `2026-08-22T10:19:43Z`
- Stack-manifest schema: `the-interdependency.stack-manifest` version `1.0.0`
- Work-graph digest (SHA-256 over canonical `repositories` + `boundaries` JSON):
  `4756dcd6147b3ebea473689fbd1a1b9f749cf5c886f839967de8c90aee305256`
- Machine-readable copy: [`stack-manifest.json`](stack-manifest.json)

## Participants

| Repository | Archived source commit | Source branch | Authority | Snapshot path | Source tree | Snapshot SHA-256 |
|---|---|---|---|---|---|---|
| `The-Interdependency/skill-lib` | `fb3b53a7629f7f03ecf255167d52c13abef1a979` | main | organization-wide build and evidence doctrine | `skill-lib/` | `859a9f4cddea0937579f0fb48a36bce4c1a19c99` | `a1a89697b9722b1e3897e83b0ff465adb7e0832a9068080c0ef429b0edcf27a9` |
| `The-Interdependency/metapat` | `34d954aa1e2092e615b03a180500f6b6977f501e` | main | semantic authority (Meta Energy Theory) | `research/metapat/` | `9d83b8bb393a7420062c5049cfa2baa572336ace` | `bc91150d10edba747a779e29da4428c1a5eab7dc7a5ee8a0ae40c6a5118581ae` |
| `The-Interdependency/ucns` | `1975fe70cf4e0826a8020c2da3047569e277af64` | main | geometry and mathematical representation | `research/ucns/` | `06c2fe6cf2e148d610808c6f00f4a26e85f43d62` | `a6fa5a674950b1847738c48e57c7df2e8727c8951db16b698318fe2ca9611d65` |
| `The-Interdependency/edcm` | `7951ca32ba0f2494dc68ff9b7f6a80151918a56d` | main | measurement and text-gonol construction | `research/edcm/` | `92e7fd2040a6d8b162636083739e1927cac8326b` | `61426c7d592b2376cce03bff12e8fbb07a857ccddcd1fe411ff4b00d2cec3afa` |
| `The-Interdependency/pcea` | `4d2c581448b97bfb71da92b35487e74e6e3bcedc` | main | prime circle encryption algorithm | `research/pcea/` | `521b26b36692ca91baa73ef65d5314efbc7c9cba` | `173b5f8c27eeb54744f0cf9ddd406afa5f7a7a533ad8e4bf649c490dcb908f63` |
| `The-Interdependency/ptcna` | `97abdd1bbda61a68e0aac8595a32a3cb0ce73487` | main | prime tensor circled neural architecture | `research/ptcna/` | `0820e25698b8fdefa41da635a5d5dc43b230b396` | `1610b6d24391989472476ae2f38dd5574f31a4af3efb454d9ce458fd28d750a1` |
| `The-Interdependency/epac` | `hmmm` | — | placeholder scaffold for energy particle affixiation coupling; no source repository exists yet | `research/epac/` | `hmmm` | `hmmm` |

Each archived source-tree participant is the complete tracked working tree of its source
repository at the pinned commit, produced with `git archive HEAD`. VCS data, virtualenvs,
caches, and untracked files are excluded by construction. Source tree identities and
snapshot SHA-256 digests are verified by `tools/check_stack_manifest.py`.

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

The root stack license boundary is recorded in `LICENSE_STATUS.md`.

## Non-transfer boundaries

- `authority_transfer: false` — archived source trees do not transfer theorem, measurement,
  or promotion status merely by being archived into stack.
- `proof_status_transfer: false` — no proof/theorem status transfers into this aggregation.
- `measurement_status_transfer: false` — no measurement/empirical validity transfers.
- `semantic_mapping: archive-provenance` — named repository identities are retained as the
  replay trail for stack participants.
- `archive_provenance_required: true` — archived source identity must remain explicit.
- `public_gonol_timing: after-research-closure` — participant Public Gonol closure is a
  downstream promotion artifact, not a prerequisite for construction.

## Archive procedure

For each pinned repository, from a clean checkout at the desired commit:

```bash
git -C <checkout> archive <commit> | tar -x -C research/<name>/
```

Then update this file and `stack-manifest.json`, recompute the source tree identities,
snapshot SHA-256 digests, and work-graph digest, and commit with a message citing the
archived source commit SHAs.

## Verification

Run:

```bash
python3 tools/check_stack_manifest.py
```

The verifier checks manifest schema, work-graph digest, archived tree identities,
declared paths, non-transfer boundaries, and generated artifact hygiene.

## hmmm

- ucns has no LICENSE file at snapshot commit `1975fe7`; its licensing terms need to be
  resolved at the source repository.
- epac has no source repository yet; its placeholder carries no doctrine until one exists.
- Repo-level Public Gonol closure receipts are downstream of research.
- `libs/`, `backend/`, and `frontend/cli/` are intentional empty scaffolds reserved for
  later stack integration work.
