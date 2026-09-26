# STACK_MANIFEST.md

Provenance and authority-boundary record for `The-Interdependency/stack`.

- Source snapshot UTC: `2026-08-22T10:19:43Z` (initial participant snapshot)
- Layout migration UTC: `2026-08-30T02:58:49Z`
- PCEA canonical refresh UTC: `2026-08-31T07:49:28Z` at `91ffa8c7249dfb810ca64a0bbc500481c0bd12a9`
- EPAC graduation UTC: `2026-09-12`; immutable `v0.1.0`, public reconsumption and scoped implementation/public-contract transition accepted.
- EPAC extraction reconciliation UTC: `2026-09-05` at `d8868858b2e455381ce670797bdbe47189bdc496`
- English Gonol separation reconciliation UTC: `2026-09-12` at `030022948fb7c749961ae65743a4448c4bb6cbbe`
- English Gonol definition-topology repair UTC: `2026-09-13` at `c1900403b540835bdefa9a1274038b2f806be897`
- English Gonol full-construct v2 verification UTC: `2026-09-14` at `99b3598b02a6e683b3c84184d8ea443b12fc0e1a`
- Python Gonol construction baseline UTC: `2026-09-12` at `0e8384bbb60e4c2189016a212bdd0030d04aed7d`
- EPAC-derived carrier workspace separation UTC: `2026-09-18` at `545e135e2efbbcf29f033ab5530ac4876a68b718`
- URPCS v1 workspace integration UTC: `2026-09-20` from Stack baseline `a428a41a38a8b30bacb7025a4d54070b228a8089`
- English four-view complete-corpus audit UTC: `2026-09-22`, exact view source `1f9a35eb355296fc88d09784c7a3e2e95511ca31`; all 164,864 words, native and independent agreement.
- Stack-manifest schema: `the-interdependency.stack-manifest` version `1.1.0`
- Work-graph digest (SHA-256 over canonical `repositories` + `research_participants` + `boundaries` JSON):
  `7faa844d63c0e6d30727f3310f82c3ebc57193324b05f6c7979ed1fb90e7ef17`
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
| `The-Interdependency/epac` | `949cb1cb304927942966c9fb396caf6227120e7f` | v0.1.0 | independent implementation and public-contract authority for EPAC | immutable release artifact consumer at integration/epac/; historical forge evidence at research/epac/; libs/epac/ remains unpopulated |

## Research-Only Composition Participants

These records bind stack-local research inputs without refreshing `libs/`,
changing canonical repository pins, or presenting the research package as a
release identity.

| Workspace | Participant | Exact commit | Relation | Canonical release |
|---|---|---|---|---|
| `research/epac/` | `The-Interdependency/stack` | `0e8384bbb60e4c2189016a212bdd0030d04aed7d` | historical forge evidence; active implementation consumed from the independent EPAC release | no |
| `research/epac-derived-carrier/` | `The-Interdependency/stack` | `545e135e2efbbcf29f033ab5530ac4876a68b718` | active stack-local carrier audit consuming exact EPAC source; no EPAC implementation/public-contract or scientific standing transfer | no |
| `research/urpcs/` | `The-Interdependency/stack` | `a428a41a38a8b30bacb7025a4d54070b228a8089` | stack-local authenticated recursive pairing codec research with byte-exact reference vectors; no confidentiality, PCEA compatibility, or UCNS-gonol identity transfer | no |
| `research/english-gonol/` | `The-Interdependency/stack` | `99b3598b02a6e683b3c84184d8ea443b12fc0e1a` | stack-local English lexical/gonol construction separated from EDCM; full pinned-corpus v2 build/replay survived; consumes UCNS geometry; EDCM may evaluate outputs but does not define construction | no |
| `research/python-gonol/` | `The-Interdependency/stack` | `0e8384bbb60e4c2189016a212bdd0030d04aed7d` | stack-local bottom-up Python 3.12 source gonol construction; applies METAPAT affixiation semantics, consumes optional UCNS geometry, and transfers no language authority to UCNS or EDCM | no |
| `research/ucns/` | `The-Interdependency/ucns` | `1975fe70cf4e0826a8020c2da3047569e277af64` | explicit source base for integrated stack-local UCNS research; does not refresh or replace the manifest-pinned `libs/ucns` canonical view | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/stack` | `77ef8c7fb0ff75a524181655ee9f9641372768f7` | target composition forge baseline at audit start | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/skill-lib` | `61eb3b14db440e6ee9b7bf8de3b646dbfd00fb32` | audit, domain-claim, work-graph, and hmmm doctrine | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/metapat` | `d6699e21b11c8f8394998efc34a468e2d6efc8b0` | domain-restraint authority; root impact none | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/ucns` | `ef98748309913588fb13f389f809d5ef6cb5fec3` | candidate exact visible-circle continuum/gonal trace; no ratification or meaning transfer | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/edcm` | `eb5f200d48a8c4ffa7b943238407fbdac4934946` | adjacent measurement discipline only; no validation claim | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/pcea` | `834987cb0c1fea5f62d6ea08e5c5bb878c312646` | adjacent runtime/security work; no ontology transfer | no |
| `research/from-photons-to-macroverse/` | `The-Interdependency/epac` | `d8868858b2e455381ce670797bdbe47189bdc496` | adjacent internal research; no external physics transfer | no |
| `research/english-gonol/` | `The-Interdependency/stack` | `1f9a35eb355296fc88d09784c7a3e2e95511ca31` | complete four-view audit source; existing candidate formulas remain unchanged | no |
| `research/english-gonol/` | `The-Interdependency/ucns` | `1cf10c2df2541a332a77f2ed3feda0c6bef4abcc` | exact eight-file motion dependency closure consumed for every word; no broader geometry selection | no |
| `research/english-gonol/` | `The-Interdependency/skill-lib` | `abd259b4722901317e4388d774a20d6819d959c2` | full-corpus comparison discipline; address utility distinguished from downstream inference usefulness | no |
| `research/zfae/` | `The-Interdependency/stack` | `d713cc5f901d74deb902a191837ef5657dbaba94` | research baseline; no new canonical runtime | no |
| `research/zfae/` | `The-Interdependency/zfae` | `95fd37ef0e1775643399c8a9e8292190abf05c04` | construction questions and source-bound carrier observation | no |
| `research/zfae/` | `The-Interdependency/ptcna` | `a06a049cd8722adaad32dbc9c36d9c87b0204236` | current intended-construction gate; historical scaffold is not intended architecture | no |
| `research/zfae/` | `The-Interdependency/a0` | `f4faf5c50dd5bc55e377279a0e403e088bcdced8` | producer-state and Zeta evaluation source inspection; no runtime mutation | no |
| `research/zfae/` | `The-Interdependency/a0-betatest` | `5d51d70a0ae6044d1386d72bd0cada9d48887f77` | exact heuristic parser comparison source; not equivalent to a0 | no |
| `research/zfae/` | `The-Interdependency/uchc` | `118b48802b20509afa556cf3ce68cee915628af0` | extracted construct and pending release/reconsumption boundary | no |
| `research/zfae/` | `The-Interdependency/metapat` | `e4165b0cac9eca41daef9c2f941881028ca55d48` | current domain-restraint consultation; root impact none | no |
| `research/zfae/` | `The-Interdependency/skill-lib` | `abd259b4722901317e4388d774a20d6819d959c2` | current research, source, structural-update and metadata rules; no snapshot refresh | no |
| `research/zfae/` | `The-Interdependency/ucns` | `4086ab82399c4d142b0eacfbc09e0a69ed151aa5` | exact Public Gonol carrier consumed by the Stack glyph producer for the finite parser profile; no function semantics inferred | no |

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

EPAC is consumed as an immutable release artifact through `integration/epac/`.
`research/epac/` retains historical forge evidence at its explicit Stack BASE, with
all Python implementation/test copies retired. A `libs/epac/` source mirror is not
required for artifact consumption. The completed scoped authority transition is recorded in
`integration/epac/authority-transition.json`.

Active post-graduation carrier research lives separately at
`research/epac-derived-carrier/`. Its source verifier pins exact EPAC source
bytes for audit purposes; it neither changes the accepted immutable release nor
returns EPAC implementation authority to Stack.

URPCS v1 lives separately at `research/urpcs/` as an authenticated recursive
pairing codec experiment. Its accepted Laws 1–13, reference implementation, and
byte-exact vectors establish bounded deterministic codec behavior only. The
workspace owns no PCEA compatibility or UCNS-gonol identity, and placement in
Stack supplies no confidentiality or production-security standing.

ZFAE construction research lives at `research/zfae/`. Its exact research-only
inputs are recorded above. The parser consumes the existing English GlyphGonol
producer at the Stack baseline and the separately pinned UCNS carrier. Its
finite profile preserves occurrences and refuses incomplete gonol admission.
Conceptual authority remains in ZFAE, neural
construction in PTCNA, and runtime integration in a0. The a0-betatest parser is
a separate comparison source. Current PTCNA retains its UCNS neural-audit gate;
UCHC extraction has not completed release/reconsumption. No `libs/` pin or
upstream authority changes. Usage: read `research/zfae/README.md` and replay its
source-bound input and gonol-parser probes.

## License status at pinned commits

| Repository | License file |
|---|---|
| skill-lib | MPL-2.0 (`LICENSE`) |
| metapat | MPL-2.0 (`LICENSE`) |
| ucns | none at `828c0b8` — `hmmm` |
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

EPAC has passed its licensed candidate matrix, pre-publication Stack check, immutable
publication and public Stack reconsumption. The historical implementation path is
retired. The clean retired-source consumer gate passed, and the completed scoped
authority-transition receipt records EPAC as graduated. See `integration/epac/` for the immutable
release lock and acceptance evidence. EPAC consumes exact UCNS `6eea1828a34ed8ec99879f8090ea5d48352d8c2d`;
Stack's direct `libs/ucns/` and separate research UCNS pins remain unchanged.

English Gonol Construction remains stack-local research, not EDCM and not an independent
canonical release. Its v2 full pinned-corpus construction/replay survived with compact
committed evidence; that result establishes the construction/replay only, not semantic
quality, geometry canon, or measurement validity.

Python Gonol Construction is also stack-local research. Its Python 3.12 source
constructor has no independent repository/release authority, and its successful replay
transfers no semantic, geometric, measurement, or language-canon status.

URPCS is likewise stack-local and ungraduated. The reference implementation and
fixtures are executable evidence for one bounded profile, and an independently
structured decoder reproduced its committed outputs. A confidentiality model,
durable host state, and production-security review remain open.

## hmmm

- UCNS has no `LICENSE` file at pinned commit `828c0b8`.
- English Gonol Construction remains stack-local research; independent repository/release authority and the exact UCNS displacement law have not been established.
- Python Gonol Construction remains stack-local research; independent repository/release authority and exact UCNS affixiation geometry remain unresolved.
- URPCS remains stack-local research; bounded independent decoding survived, while confidentiality, durable rollback resistance, and release authority remain unresolved.
- `skill-lib/` remains a special operational snapshot at stack root rather than following the ordinary `libs/` + `research/` pair.

## UCHC input candidate

`research/zfae/` now consumes `The-Interdependency/uchc@3d82007b88f74ded88ca913d6e85bcd6f6ff024d` through the immutable wheel lock `research/zfae/UCHC_INPUT.json`.
The prior `118b488` extraction remains the source identity of the earlier research.
This additional candidate supplies full-corpus native language input; it does not
choose PTCNA dimensions, propagate neural state or transfer domain authority.
See `integration/uchc/README.md` for isolated installation, complete-corpus
verification and rollback. Stable released-artifact consumption remains `hmmm`.
