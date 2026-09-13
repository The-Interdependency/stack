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
│   ├── ptcna/               # current PTCNA research + BASE.json
│   ├── epac/                # historical forge evidence; active implementation is independent
│   ├── psychsocio-metafauna/ # proposed pattern-lineage, coalescence, accountability research
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
After upstream merge, refresh `libs/ucns/`; update `research/ucns/BASE.json` only
after separately verifying the research rebase.

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
Psychsocio metafauna and From Photons to the Macroverse remain stack-local
pre-graduation research. EPAC has an independently published MPL-2.0 `v0.1.0`
release and has passed public Stack reconsumption. Its Python forge copy is retired;
`research/epac/` preserves historical evidence. EPAC is graduated: implementation and public-contract authority belong to the
independent repository, as recorded in
[`integration/epac/authority-transition.json`](integration/epac/authority-transition.json).

```bash
python3 integration/epac/reconsume.py \
  integration/epac/release-lock.json /tmp/epac-public-consumption python3.12
```

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
- Actual VM PostgreSQL/service-account/storage state and the independent backup device
  remain deployment observations until inspected on the VM.
- A GitHub-hosted executor remains optional and unimplemented; VM-local execution is the
  resilience baseline.
- Organization aggregate and website-projection derivation specs are not yet registered.
- The root `skill-lib/` snapshot was refreshed on 2026-09-13. Runtime doctrine and
  generator identities are recorded separately in `backend/fresh-making-provenance.json`;
  existing generated collections need verification under the changed generator identity.
