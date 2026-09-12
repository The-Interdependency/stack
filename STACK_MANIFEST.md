# STACK_MANIFEST.md

Provenance and authority-boundary record for `The-Interdependency/stack`.

- Source snapshot UTC: `2026-08-22T10:19:43Z` (initial participant snapshot)
- Layout migration UTC: `2026-08-30T02:58:49Z`
- PCEA canonical refresh UTC: `2026-08-31T07:49:28Z` at `91ffa8c7249dfb810ca64a0bbc500481c0bd12a9`
- EPAC extraction reconciliation UTC: `2026-09-05` at `d8868858b2e455381ce670797bdbe47189bdc496`
- English Gonol separation reconciliation UTC: `2026-09-12` at `030022948fb7c749961ae65743a4448c4bb6cbbe`
- Stack-manifest schema: `the-interdependency.stack-manifest` version `1.1.0`
- Work-graph digest (SHA-256 over canonical `repositories` + `research_participants` + `boundaries` JSON):
  `9ab3b3f75a32f5f73b5df68419148181fc632593babe4ec6adf4269d4f35badb`
- Machine-readable copy: [`stack-manifest.json`](stack-manifest.json)

## Directory contract

For an established repository participating in stack:

```text
libs/<repo>/       = exact imported canonical repository view at the manifest commit
research/<repo>/   = mutable stack-local research bound to an explicit source identity
```

`libs/` does not gain authority by containing a copy. The owning repository remains
canonical. `research/` does not gain canon status by producing a useful result.

A research workspace normally shares the imported `libs/<repo>/` pin. If it intentionally
uses a different exact source commit, that source identity must be represented explicitly
in `research_participants`; it does not silently refresh or replace the `libs/` pin.

A Python `src/` directory inside `libs/<repo>/` retains the normal package-layout
meaning used by that repository.

## Participants

| Repository | Exact source commit | Source branch | Authority | Stack relation |
|---|---|---|---|---|
| `The-Interdependency/skill-lib` | `fb3b53a7629f7f03ecf255167d52c13abef1a979` | main | organization-wide build and evidence doctrine | operational snapshot at `skill-lib/` |
| `The-Interdependency/metapat` | `34d954aa1e2092e615b03a180500f6b6977f501e` | main | semantic authority (Meta Energy Theory) | canon view `libs/metapat/`; research `research/metapat/` |
| `The-Interdependency/ucns` | `828c0b8bbcfc267efb5701da714191c1f73a81ff` | main | geometry and mathematical representation | canon view `libs/ucns/`; research `research/ucns/` |
| `The-Interdependency/edcm` | `7951ca32ba0f2494dc68ff9b7f6a80151918a56d` | main | measurement and evaluation of text-domain outputs | canon view `libs/edcm/`; measurement research `research/edcm/`; English Gonol construction is separate at `research/english-gonol/` |
| `The-Interdependency/pcea` | `91ffa8c7249dfb810ca64a0bbc500481c0bd12a9` | main | prime circle encryption algorithm | canon view `libs/pcea/`; research `research/pcea/` |
| `The-Interdependency/ptcna` | `97abdd1bbda61a68e0aac8595a32a3cb0ce73487` | main | prime tensor circled neural architecture | canon view `libs/ptcna/`; research `research/ptcna/` |
| `The-Interdependency/epac` | `d8868858b2e455381ce670797bdbe47189bdc496` | main | independent extracted candidate repository; implementation/public-contract authority transition incomplete | extracted repo exists; forge candidate remains `research/epac/` until release/reconsumption; `libs/epac/` remains unpopulated |

## Research-Only Composition Participants

These records bind stack-local research inputs without refreshing `libs/`,
changing canonical repository pins, or presenting the research package as a
release identity.

| Workspace | Participant | Exact commit | Relation | Canonical release |
|---|---|---|---|---|
| `research/english-gonol/` | `The-Interdependency/stack` | `030022948fb7c749961ae65743a4448c4bb6cbbe` | stack-local English lexical/gonol construction separated from EDCM; consumes UCNS geometry; EDCM may evaluate outputs but does not define construction | no |
| `research/ucns/` | `The-Interdependency/ucns` | `1975fe70cf4e0826a8020c2da3047569e277af64` | explicit source base for integrated stack-local UCNS research; does not refresh or replace the manifest-pinned `libs/ucns` canonical view | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/stack` | `77ef8c7fb0ff75a524181655ee9f9641372768f7` | target composition forge baseline at audit start | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/skill-lib` | `61eb3b14db440e6ee9b7bf8de3b646dbfd00fb32` | audit, domain-claim, work-graph, and hmmm doctrine | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/metapat` | `d6699e21b11c8f8394998efc34a468e2d6efc8b0` | domain-restraint authority; root impact none | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/ucns` | `ef98748309913588fb13f389f809d5ef6cb5fec3` | candidate exact visible-circle continuum/gonal trace; no ratification or meaning transfer | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/edcm` | `eb5f200d48a8c4ffa7b943238407fbdac4934946` | adjacent measurement discipline only; no validation claim | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/pcea` | `834987cb0c1fea5f62d6ea08e5c5bb878c312646` | adjacent runtime/security work; no ontology transfer | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/epac` | `d8868858b2e455381ce670797bdbe47189bdc496` | adjacent internal research; no external physics transfer | no |

The imported `libs/` trees are the complete tracked working trees of their source
repositories at the pinned commits, produced from Git trees / `git archive` contents.
VCS metadata, virtualenvs, caches, and untracked files are excluded.

## Research base records

Each established `research/<repo>/` workspace carries a `BASE.json` with:

- owning/source repository;
- exact source commit;
- canon path when one exists;
- authority owner;
- standing `stack-local-research`.

When `BASE.json.source_commit` differs from the repository's manifest-pinned `libs/`
commit, the workspace must carry an explicit matching `research_participants` identity.
That record preserves the newer/different research input without pretending `libs/` was
refreshed. `research/ucns/` currently uses this form: its exact source base is UCNS
`1975fe70cf4e0826a8020c2da3047569e277af64`, while `libs/ucns/` remains pinned at
`828c0b8bbcfc267efb5701da714191c1f73a81ff`.

A newly separated stack-local component may instead preserve the repository it was
extracted from as provenance while declaring a distinct `project` and stack-local
authority. Such a component must also appear in the stack research-participant graph;
its source repository must stop claiming the separated responsibility at stack level.

EPAC is currently an extraction-transition exception: the independent repository exists,
but authority transfer is not complete, so the forge candidate remains in `research/epac/`
and no `libs/epac/` canonical import is created yet.

## License status at pinned commits

| Repository | License file |
|---|---|
| skill-lib | MPL-2.0 (`LICENSE`) |
| metapat | MPL-2.0 (`LICENSE`) |
| ucns | none at `828c0b8` — `hmmm` |
| edcm | MPL-2.0 (`LICENSE`) |
| pcea | present (`LICENSE`) |
| ptcna | present (`LICENSE`) |
| epac | independent repository exists; no `LICENSE` yet — `hmmm` |

## Non-transfer boundaries

- `authority_transfer: false` — imported or extracted views do not gain authority merely by location.
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

Then update this file, `stack-manifest.json`, and the matching
`research/<name>/BASE.json`; recompute the work-graph digest; and commit with the new
source commit SHA. Structural ownership/relation changes must additionally follow the
`stack-update` skill and pass `python tools/check_stack_consistency.py`.

Do not edit `libs/<name>/` to create a canonical change. Route the change to the owning
repository, merge it there, then refresh the pinned view.

## Graduation boundary

EPAC now has an independent extracted repository, but extraction is not graduation.
Do not populate `libs/epac/`, replace the forge candidate, or assert implementation/public-contract
authority transfer until EPAC completes its clean build/install, license/distribution,
immutable release, downstream stack reconsumption, and authority-transition receipt gates.

English Gonol Construction is earlier in that lifecycle: it is a distinct stack-local
research component, not EDCM and not an independent canonical release.

## hmmm

- UCNS has no `LICENSE` file at pinned commit `828c0b8`.
- EPAC clean install, license, stable release, downstream reconsumption, and authority-transition receipt remain incomplete; `libs/epac/` stays unpopulated until graduation.
- English Gonol Construction remains stack-local research; independent repository/release authority has not been established.
- `skill-lib/` remains a special operational snapshot at stack root rather than following the ordinary `libs/` + `research/` pair.
