# STACK_MANIFEST.md

Provenance and authority-boundary record for `The-Interdependency/stack`.

- Source snapshot UTC: `2026-08-22T10:19:43Z` (initial participant snapshot)
- Layout migration UTC: `2026-08-30T02:58:49Z`
- PCEA canonical refresh UTC: `2026-08-31T07:49:28Z` at `91ffa8c7249dfb810ca64a0bbc500481c0bd12a9`
- Canonical tool/library refresh UTC: `2026-09-13`; exact upstream commits and validation in [`docs/updates/2026-09-13-tools.md`](docs/updates/2026-09-13-tools.md).
- EPAC graduation UTC: `2026-09-12`; immutable `v0.1.0`, public reconsumption and scoped implementation/public-contract transition accepted.
- EPAC extraction reconciliation UTC: `2026-09-05` at `d8868858b2e455381ce670797bdbe47189bdc496`
- English Gonol separation reconciliation UTC: `2026-09-12` at `030022948fb7c749961ae65743a4448c4bb6cbbe`
- Python Gonol construction baseline UTC: `2026-09-12` at `0e8384bbb60e4c2189016a212bdd0030d04aed7d`
- Stack-manifest schema: `the-interdependency.stack-manifest` version `1.1.0`
- Work-graph digest (SHA-256 over canonical `repositories` + `research_participants` + `boundaries` JSON):
  `7c2721fee05a4bd961ee5e51aeb41b5581d7eb7c272c2a7b19a9e5ccc5c2bf62`
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
| `The-Interdependency/skill-lib` | `22c2c5702d14fb4b0faeb717777ecab2665770a1` | main | organization-wide build and evidence doctrine | operational snapshot at `skill-lib/` |
| `The-Interdependency/metapat` | `510e0171f4ecc6d1889e66bb66a8734c49c3b1fa` | main | semantic authority (Meta Energy Theory) | canon view `libs/metapat/`; research `research/metapat/` |
| `The-Interdependency/ucns` | `31bb761e49307b04a7c7dd7c7c2059ea35fdc089` | main | geometry and mathematical representation | canon view `libs/ucns/`; research `research/ucns/` |
| `The-Interdependency/edcm` | `ddc89a97ebbcf0a5863dad6e633b01b520e9bccf` | main | measurement and evaluation of text-domain outputs | canon view `libs/edcm/`; measurement research `research/edcm/`; English Gonol construction is separate at `research/english-gonol/` |
| `The-Interdependency/pcea` | `75d2ea68e4a4a3256b324f039cb1712d196d323d` | main | prime circle encryption algorithm | canon view `libs/pcea/`; research `research/pcea/` |
| `The-Interdependency/ptcna` | `a06a049cd8722adaad32dbc9c36d9c87b0204236` | main | prime tensor circled neural architecture | canon view `libs/ptcna/`; research `research/ptcna/` |
| `The-Interdependency/epac` | `949cb1cb304927942966c9fb396caf6227120e7f` | v0.1.0 | independent implementation and public-contract authority for EPAC | immutable release artifact consumer at integration/epac/; historical forge evidence at research/epac/; libs/epac/ remains unpopulated |

## Research-Only Composition Participants

These records bind stack-local research inputs without refreshing `libs/`,
changing canonical repository pins, or presenting the research package as a
release identity.

| Workspace | Participant | Exact commit | Relation | Canonical release |
|---|---|---|---|---|
| `research/epac/` | `The-Interdependency/stack` | `0e8384bbb60e4c2189016a212bdd0030d04aed7d` | historical forge evidence; active implementation consumed from the independent EPAC release | no |
| `research/english-gonol/` | `The-Interdependency/stack` | `030022948fb7c749961ae65743a4448c4bb6cbbe` | stack-local English lexical/gonol construction separated from EDCM; consumes UCNS geometry; EDCM may evaluate outputs but does not define construction | no |
| `research/english-gonol/` | `The-Interdependency/edcm` | `7951ca32ba0f2494dc68ff9b7f6a80151918a56d` | preserved extraction source; English construction remains Stack-local | no |
| `research/python-gonol/` | `The-Interdependency/stack` | `0e8384bbb60e4c2189016a212bdd0030d04aed7d` | stack-local bottom-up Python 3.12 source gonol construction; applies METAPAT affixiation semantics, consumes optional UCNS geometry, and transfers no language authority to UCNS or EDCM | no |
| `research/metapat/` | `The-Interdependency/metapat` | `34d954aa1e2092e615b03a180500f6b6977f501e` | preserved research source base; canonical snapshot refresh does not rebase research | no |
| `research/edcm/` | `The-Interdependency/edcm` | `7951ca32ba0f2494dc68ff9b7f6a80151918a56d` | preserved research source base; canonical snapshot refresh does not rebase research | no |
| `research/pcea/` | `The-Interdependency/pcea` | `91ffa8c7249dfb810ca64a0bbc500481c0bd12a9` | preserved research source base; canonical snapshot refresh does not rebase research | no |
| `research/ptcna/` | `The-Interdependency/ptcna` | `97abdd1bbda61a68e0aac8595a32a3cb0ce73487` | preserved research source base; canonical snapshot refresh does not rebase research | no |
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
These records preserve historical research inputs while canonical snapshots advance.
The 2026-09-13 refresh leaves all research BASE commits intact and records the
METAPAT, UCNS, EDCM, PCEA, and PTCNA source bases explicitly. `research/ucns/`
retains UCNS `1975fe70cf4e0826a8020c2da3047569e277af64`; `libs/ucns/` now pins
`31bb761e49307b04a7c7dd7c7c2059ea35fdc089`.

A newly separated stack-local component may instead preserve the repository it was
extracted from as provenance while declaring a distinct `project` and stack-local
authority. Such a component must also appear in the stack research-participant graph;
its source repository must stop claiming the separated responsibility at stack level.

EPAC is consumed as an immutable release artifact through `integration/epac/`.
`research/epac/` retains historical forge evidence at its explicit Stack BASE, with
all Python implementation/test copies retired. A `libs/epac/` source mirror is not
required for artifact consumption. The completed scoped authority transition is recorded in
`integration/epac/authority-transition.json`.

## License status at pinned commits

| Repository | License file |
|---|---|
| skill-lib | MPL-2.0 (`LICENSE`) |
| metapat | MPL-2.0 (`LICENSE`) |
| ucns | MPL-2.0 (`LICENSE`) at the refreshed commit; historical snapshots retain their original license status |
| edcm | MPL-2.0 (`LICENSE`) |
| pcea | present (`LICENSE`) |
| ptcna | present (`LICENSE`) |
| epac | MPL-2.0 (`LICENSE`); owner weak-copyleft instruction recorded in the release source |

## Non-transfer boundaries

- `authority_transfer: false` — imported or extracted views do not gain authority merely by location.
- `proof_status_transfer: false` — no proof/theorem status transfers through stack composition.
- `measurement_status_transfer: false` — no measurement/empirical validity transfers.
- `semantic_mapping: external-provenance` — canonical meaning remains owned by source repositories.
- `research/` is explicitly noncanonical stack-local work.
- `libs/` is read-only by contract and is refreshed only from an owning repository at an exact commit.

## Refresh procedure

Resolve the exact owning repository commit first. Replace the complete imported
Git tree, including tracked dotfiles and executable modes, and remove obsolete
files. See the [2026-09-13 refresh record](docs/updates/2026-09-13-tools.md) for
source identities and a reproducible Git-tree verification command.

Update both manifests and recompute the work-graph digest. A canonical snapshot
refresh does not by itself rebase research: retain the historical `BASE.json`
and add a matching `research_participants` record when it differs from the new
canonical pin. Change a research base only as part of a separately verified rebase.

Follow `.agents/skills/stack-update/SKILL.md` and run:

```bash
python3 tools/check_stack_consistency.py
```

Canonical source edits belong in the owning repository before importing its tree.

## Graduation boundary

EPAC has passed its licensed candidate matrix, pre-publication Stack check, immutable
publication and public Stack reconsumption. The historical implementation path is
retired. The clean retired-source consumer gate passed, and the completed scoped
authority-transition receipt records EPAC as graduated. See `integration/epac/` for the immutable
release lock and acceptance evidence. EPAC consumes exact UCNS `6eea1828a34ed8ec99879f8090ea5d48352d8c2d`;
That release-specific UCNS identity is independent of Stack's refreshed `libs/ucns/`
and preserved research UCNS base.

English Gonol Construction is earlier in that lifecycle: it is a distinct stack-local
research component, not EDCM and not an independent canonical release.

Python Gonol Construction is also stack-local research. Its Python 3.12 source
constructor has no independent repository/release authority, and its successful replay
transfers no semantic, geometric, measurement, or language-canon status.

## hmmm

- EDCM docs/GONOL_LANGUAGE_BOUNDARY.md at the refreshed source still claims language-construction ownership; Stack retains its declared English/Python construction authority and records this upstream documentation discrepancy without rewriting the imported source.

- English Gonol Construction remains stack-local research; independent repository/release authority has not been established.
- Python Gonol Construction remains stack-local research; independent repository/release authority and exact UCNS affixiation geometry remain unresolved.
- `skill-lib/` remains a special operational snapshot at stack root rather than following the ordinary `libs/` + `research/` pair.
