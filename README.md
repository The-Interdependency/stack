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
├── libs/                    # manifest-pinned canonical repository views; do not edit
│   ├── metapat/
│   ├── ucns/
│   ├── edcm/
│   ├── pcea/
│   ├── ptcna/
│   ├── epac/                # canon slot unpopulated until EPAC graduates
│   └── skill-lib/           # reserved; root skill-lib/ remains the operational special case
├── research/                # stack-local work; never source authority by location
│   ├── metapat/             # current METAPAT research + BASE.json
│   ├── ucns/                # current UCNS research + BASE.json
│   ├── edcm/                # current EDCM research + BASE.json
│   ├── pcea/                # current PCEA research + BASE.json
│   ├── ptcna/               # current PTCNA research + BASE.json
│   ├── epac/                # emerging composed project; no independent repo yet
│   └── psychsocio-metafauna/ # proposed pattern-lineage, coalescence, accountability research
├── ahbg/                    # emerging composed benchmark/game workspace
├── backend/                 # PostgreSQL-backed durable fresh-making control plane
├── frontend/
│   └── cli/                 # human control/status surface for backend
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

### Compose something new

New cross-project work may be born in stack. It does not inherit the authority of its
inputs. While it is still stack research, keep its standing explicit. When it becomes
coherent enough to graduate, create its independent repository, preserve provenance,
package/release it, then let stack consume the released project rather than a hidden
stack-local implementation.

EPAC and psychsocio metafauna are currently in this pre-graduation state.

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
source commit in the message.

## Boundaries

- `libs/` is a pinned view, not a transfer of authority.
- `research/` is mutable stack-local work, not doctrine by location.
- moving work from `research/` to `libs/` is not a promotion mechanism; `libs/` is
  populated only from an owning canonical repository at an exact commit.
- proof, measurement, semantic, empirical, and certification standing do not transfer
  merely because projects are composed in stack.
- `backend/` may coordinate an owning repository but does not acquire that repository's
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
- Actual VM PostgreSQL/service-account/storage state and the independent backup device
  remain deployment observations until inspected on the VM.
- A GitHub-hosted executor remains optional and unimplemented; VM-local execution is the
  resilience baseline.
- Organization aggregate and website-projection derivation specs are not yet registered.
- The root `skill-lib/` snapshot predates the merged `fresh-making` skill; the runtime
  pins that doctrine separately in `backend/fresh-making-provenance.json` because a full
  snapshot refresh would also import unrelated doctrine changes.
