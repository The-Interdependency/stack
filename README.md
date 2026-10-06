# stack

"This is how it comes together."

`The-Interdependency/stack` is the organization's composition forge. Pinned views of
canonical repositories are brought together here so stack-local research can test
relations among them and, when warranted, form new projects such as EPAC and AHBG.

Canonical authority does **not** transfer into stack when a repository is imported.
For repositories with an independent authority:

- `libs/<repo>/` is the read-only, manifest-pinned canonical repository view.
- `research/<repo>/` is stack-local current research against that pinned base.
- accepted changes to an existing project route back to its owning repository;
- a genuinely new composed project remains stack-local until it earns an independent
  repository and release lifecycle.

## Layout

```text
stack/
├── skill-lib/               # operational pinned snapshot of org build/evidence doctrine
├── .agents/skills/          # repo-local consumed skills; stack-update guards structural changes
├── libs/                    # manifest-pinned canonical repository views; do not edit
│   ├── metapat/
│   ├── ucns/
│   ├── edcm/
│   ├── pcea/
│   ├── ptcna/
│   └── skill-lib/           # reserved; root skill-lib/ remains the operational special case
├── research/                # stack-local work; never source authority by location
│   ├── metapat/             # current METAPAT research + BASE.json
│   ├── ucns/                # current UCNS research + BASE.json
│   ├── english-gonol/       # English lexical/gonol construction; distinct from EDCM
│   ├── python-gonol/        # Python 3.12 source affixiation from characters upward
│   ├── edcm/                # current EDCM measurement research + BASE.json
│   ├── pcea/                # current PCEA research + BASE.json
│   ├── urpcs/               # RETIRED: substituted GPT-produced codec; historical evidence only
│   ├── weave/               # full gonol/private-key/thread/corpus/interleave research
│   ├── ptcna/               # current PTCNA research + BASE.json
│   ├── zfae/                # inference construction research and gonol input parser
│   ├── a0-municipality/     # municipal application handoff and composition research
│   ├── epac/                # historical forge evidence; active implementation is independent
│   ├── epac-derived-carrier/ # active Stack audit consuming exact EPAC source
│   ├── psfr/                 # Psychosocial Fauna Research: lineages, agency displacement, coalescence
│   └── from-photons-to-macroverse/ # audited consciousness-first candidate research
├── integration/epac/        # immutable EPAC release lock and consumer verification
├── ahbg/                    # emerging composed benchmark/game workspace
├── backend/                 # PostgreSQL-backed durable fresh-making control plane
├── frontend/
│   └── cli/                 # human control/status surface for backend
├── tools/
│   └── check_stack_consistency.py # deterministic authority/provenance drift gate
├── STACK_MANIFEST.md        # human-readable provenance and boundary record
└── stack-manifest.json      # machine-readable work graph
```

`src/` inside an imported repository keeps its normal Python meaning: it is that
repository's package-source layout. It does not mean "canonical source" for stack.

## Usage guidance

### Read canon

Start at [`STACK_MANIFEST.md`](STACK_MANIFEST.md), then read the pinned repository in
`libs/<repo>/`. Those trees are exact imported views of the source commits recorded by
the manifest. Do not make canonical edits there.

### Do current research

Work in `research/<repo>/`. Each established project workspace has a `BASE.json` that
binds the research to an exact owning repository, commit, and `libs/` path.

```bash
cat research/ucns/BASE.json
```

If the result changes UCNS itself, prepare the change for `The-Interdependency/ucns`.
After upstream merge, refresh `libs/ucns/` and update `research/ucns/BASE.json`.

English Gonol Construction is a separated stack-local component at
`research/english-gonol/`. UCNS owns its consumed geometry. English Gonol owns the
English text-domain construction candidate. EDCM may evaluate those outputs but does
not define the construction.

Python Gonol Construction is a separate stack-local component at
`research/python-gonol/`. It admits every exact Python source occurrence as a character
gonol, closes the occurrence's applicable character-definition gonols, then affixiates
lexical forms, delimiters, grammar constructions, and the module from already-closed
participants. METAPAT owns affixiation semantics; UCNS owns optional consumed geometry;
Python Gonol owns Python source construction. Tokens and AST nodes are recognition
witnesses, never gonol substitutes.

EPAC-derived carrier research is a separate stack-local audit at
`research/epac-derived-carrier/`. It consumes exact EPAC source bytes without
restoring implementation code to the sealed historical `research/epac/` path.
EPAC retains implementation and public-contract authority; Stack owns only the
local carrier audit and its bounded receipts.

URPCS at `research/urpcs/` is **retired historical evidence**. The implemented
recursive-pairing/authenticated-codec profile diverged from Erin Spencer's intended
multi-arity interleaving construction during GPT-assisted implementation. The reason
for the substitution is unresolved. Its tests and receipts apply only to that
substituted codec and must not be used to validate or falsify the intended URPCS design.

The replacement research path is `research/weave/`. It owns the full intended encryption construction: hyperspace/gonol plaintext representation, private-gonol recovery, multiple reconstruction-dependent threads, thread-associated corpus/material, multi-arity bit interleaving, and the eventual asymmetric public/private relation. The interleave is one layer, not the project identity. The workspace deliberately contains no URPCS implementation dependency and makes no security claim.

```bash
cat research/weave/SPECIFICATION.md
cat research/weave/BASE.json
```

### Change stack structure

Any change that alters a participant, pin, authority, relation, research workspace,
extraction/graduation standing, `BASE.json`, or architecture projection must load the
`stack-update` skill and finish as one coherent stack transaction.

Run the deterministic gate before and after the mutation:

```bash
python tools/check_stack_consistency.py
```

A structural change is not complete merely because moved code or local tests pass. The
machine manifest, human manifest, affected base records, architecture description, and
work-graph digest must agree before merge.

### Compose something new

New cross-project work may be born in stack. It does not inherit the authority of its
inputs. While it is still stack research, keep its standing explicit. When it becomes
coherent enough to graduate, create its independent repository, preserve provenance,
package/release it, then let stack consume the released project rather than a hidden
stack-local implementation.

English Gonol Construction is currently a distinct stack-local research component,
separated from EDCM but not independently graduated.
Python Gonol Construction is likewise stack-local and ungraduated; its Python 3.12
constructor is an implemented candidate, not stack or language canon.
URPCS is retired; its retained vectors and replay evidence establish behavior only
of the substituted historical codec. No URPCS claim may be inferred from them.
Weave is new stack-local research and remains specification-first; no
confidentiality or production-security standing is implied by its placement.
PSFR and From Photons to the Macroverse remain stack-local
pre-graduation research. EPAC has an independently published MPL-2.0 `v0.1.0`
release and has passed public Stack reconsumption. Its Python forge copy is retired;
`research/epac/` preserves historical evidence. EPAC is graduated: implementation and public-contract authority belong to the
independent repository, as recorded in
[`integration/epac/authority-transition.json`](integration/epac/authority-transition.json).

```bash
python3 integration/epac/reconsume.py \
  integration/epac/release-lock.json /tmp/epac-public-consumption python3.12
```

### English four-view full-corpus evidence

The English construction's [complete four-view audit](research/english-gonol/docs/hyperspace-views-full-v1.md)
records historical execution of all 164,864 admitted words and compares every native record with an independent
reconstruction. All fifteen nonempty view combinations and three complete renumbering
controls are recorded. The synthesis has 137,013 distinct values; view 4 is derivable
from view 2 or view 3, while each of views 1, 2, and 3 adds distinctions. Numeric addresses
remain useful provenance/memory metadata; distinctness alone does not select geometry
or establish inference quality. The frozen protocol binds Stack `1f9a35e`, UCNS
`1cf10c2`, and separately pinned skill-lib doctrine `abd259b` without changing `libs/`.
### ZFAE construction research

Read [research/zfae/README.md](research/zfae/README.md) for the gonol input parser, source identities,
the construction sequence, the first executable input-distinction experiment,
and the remaining UCNS/PTCNA and UCHC prerequisites. This is Stack research;
conceptual, producer and runtime authority remain with their owners.

### a0 Municipality composition research

[research/a0-municipality/](research/a0-municipality/README.md) holds the complete
v1.1 municipal application handoff, its source receipt and exact research inputs.
It preserves the four workflows, the Oakland/Berkeley homeless union stewardship
model, tax-funded remuneration and UCNS/UCHC native construction requirements.
Stack owns composition research; a0 owns runtime implementation. This is
specification-first work, with the fifth workflow reserved and operational proof
still outstanding. Read the workspace README for current producer standing, then
HANDOFF.md for the full build and acceptance contract.

### Make derived artifacts fresh without depending on hosted CI

`backend/` implements the durable `fresh-making` control plane. PostgreSQL on the VM is
the single production state authority for derivation specs, desired freshness keys,
logical jobs, attempts/leases, receipts, acceptance, dependency edges, and `hmmm`.
Repositories retain source/canon/artifact authority.

Freshness is identity-based, not time-based. MSDMD regeneration is the first adapter:

```bash
python -m frontend.cli.stackctl fresh make-msdmd ucns \
  --root /srv/stack-repos/ucns \
  --source-sha <40-hex-commit>

python -m frontend.cli.stackctl fresh status msdmd:ucns
python -m frontend.cli.stackctl fresh explain msdmd:ucns
python -m frontend.cli.stackctl fresh recover
```

The VM worker uses leases and `FOR UPDATE SKIP LOCKED`; the MSDMD adapter independently
rerenders output before publication. GitHub Actions may later become an executor, but it
cannot become durable state or acceptance authority.

The old `stackctl msdmd ...` namespace is removed rather than maintained as a second
orchestration architecture.

See [`backend/README.md`](backend/README.md) for the state/verification/backup contract
and [`frontend/cli/README.md`](frontend/cli/README.md) for operator commands.

## Refreshing a canonical view

From a clean checkout of the owning repository at the desired commit:

```bash
rm -rf libs/<name>/*
git -C <checkout> archive <commit> | tar -x -C libs/<name>/
```

Then update `STACK_MANIFEST.md`, `stack-manifest.json`, and the matching
`research/<name>/BASE.json`; recompute the work-graph digest; and commit with the exact
source commit in the message. Run `python tools/check_stack_consistency.py` before
merge.

## Licensing

Stack's own original code is licensed under the Mozilla Public License 2.0
(SPDX: `MPL-2.0`). The full text is in [`LICENSE`](LICENSE). At present that covers
`backend/`, `frontend/`, `integration/`, `tools/` and the root-level stack files.
Pinned and vendored components keep their own licenses:

| Path | License | Notes |
|---|---|---|
| `libs/edcm/` | MPL-2.0 | `libs/edcm/LICENSE`, pinned from The-Interdependency/edcm |
| `libs/metapat/` | MPL-2.0 | `libs/metapat/LICENSE`, pinned from The-Interdependency/metapat |
| `libs/pcea/` | MIT | `libs/pcea/LICENSE` (Copyright (c) 2026 Erin Patrick Spencer) |
| `libs/ptcna/` | MPL-2.0 | `libs/ptcna/LICENSE`, pinned from The-Interdependency/ptcna |
| `libs/ucns/` | `hmmm`: no `LICENSE` at pinned commit `828c0b8` | Upstream ucns carries MPL-2.0 again from 2026-09-11; a refresh of this pin would bring it in |
| `skill-lib/` | MPL-2.0, plus Apache-2.0 imports | `skill-lib/LICENSE` (MPL-2.0). The Apache-2.0 skills imported from anthropics/knowledge-work-plugins (`sql-queries/`, `statistical-analysis/`, `explore-data/`, `validate-data/`, and `data-visualization/SKILL.md` only) are listed in `skill-lib/ATTRIBUTION.md`. The other files in `skill-lib/data-visualization/` are original to skill-lib under MPL-2.0. The Apache-2.0 text is in [`skill-lib/LICENSES/Apache-2.0.txt`](skill-lib/LICENSES/Apache-2.0.txt) |

The whole `skill-lib/` snapshot, including
[`skill-lib/LICENSES/Apache-2.0.txt`](skill-lib/LICENSES/Apache-2.0.txt) and
`skill-lib/ATTRIBUTION.md`, is an exact copy of The-Interdependency/skill-lib
`1b1a947`. The doctrine and MSDMD generator pin is that same commit (see
`stack-manifest.json` and `backend/fresh-making-provenance.json`). The root
[`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt) is the same text.

`hmmm` (not yet decided): the license status of `ahbg/`, `research/`, `media/` and
`docs/`. Files there that are modified copies of an MPL-2.0 or MIT component stay
under that component's license. Nothing else in these paths is licensed yet.

Usage: when you copy code out of stack, take the license of the path it came from
in the table above. For MPL-2.0 files, keep the license notice and publish your
modifications to those files under MPL-2.0. For the Apache-2.0 skills, keep
`skill-lib/ATTRIBUTION.md` and include `skill-lib/LICENSES/Apache-2.0.txt`. This section is
a licensing map, not legal advice.

## Boundaries

- `libs/` is a pinned view, not a transfer of authority.
- `research/` is mutable stack-local work, not doctrine by location.
- moving work from `research/` to `libs/` is not a promotion mechanism; `libs/` is
  populated only from an owning canonical repository at an exact commit.
- proof, measurement, semantic, empirical, and certification standing do not transfer
  merely because projects are composed in stack.
- backend may coordinate an owning repository but does not acquire that repository's
  authority.
- PostgreSQL owns orchestration/freshness evidence, not repository artifacts or canon.
- executor success alone cannot establish freshness; the declared verifier and accepted
  receipt must agree with exact current identities.
- hosted CI may execute work, but durable state and acceptance must survive its absence.
- a database backup is complete only when its independently mounted mirror is verified;
  a second same-disk directory is not redundancy.

## hmmm

- `skill-lib/` remains a special operational root snapshot instead of using the same
  `libs/` + `research/` pair.
- The exact graduation automation from stack-local project to independent repo + package
  is not yet implemented.
- English Gonol Construction has distinct stack-local authority but has not yet gained an
  independent repository/release authority boundary.
- Python Gonol Construction has distinct stack-local authority but has not yet gained an
  independent repository/release authority boundary; UCNS affixiation geometry remains unresolved.
- URPCS is retired because the implemented GPT-produced codec diverged from the
  intended specification. Cause of the substitution remains `hmmm`; retained evidence
  applies only to the substituted implementation.
- Actual VM PostgreSQL/service-account/storage state and the independent backup device
  remain deployment observations until inspected on the VM.
- A GitHub-hosted executor remains optional and unimplemented; VM-local execution is the
  resilience baseline.
- Organization aggregate and website-projection derivation specs are not yet registered.

URPCS provenance boundary: the immutable public intended-design transcript identity
and detailed design attribution remain unresolved; see
[`SOURCE_RECEIPT.json`](research/urpcs/SOURCE_RECEIPT.json).

Weave native public/private key derivation and source of asymmetry remain
unresolved. Provenance metadata is not an implementation of that missing law.
