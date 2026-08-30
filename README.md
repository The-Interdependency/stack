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
│   └── epac/                # emerging composed project; no independent repo yet
├── ahbg/                    # emerging composed benchmark/game workspace
├── backend/                 # stack-level application scaffold
├── frontend/
│   └── cli/                 # stack-level application scaffold
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

EPAC is currently in this pre-graduation state.

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
- proof, measurement, and semantic standing do not transfer merely because projects are
  composed in stack.

## hmmm

- `skill-lib/` remains a special operational root snapshot instead of using the same
  `libs/` + `research/` pair.
- The exact graduation automation from stack-local project to independent repo + package
  is not yet implemented.
- The exact long-term shape of `backend/` and `frontend/cli/` remains undeclared.
