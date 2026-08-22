# stack

"This is how it comes together."

`The-Interdependency/stack` is the consolidated, provenance-bearing aggregation of the
organization's core repositories. It is an integration surface, not a source of truth:
each `research/` snapshot is pinned to an exact source commit, and canonical edits still
happen in the individual repositories.

## Layout

```text
stack/
├── skill-lib/               # full snapshot of The-Interdependency/skill-lib
├── research/
│   ├── metapat/              # full snapshot — semantic authority (Meta Energy Theory)
│   ├── ucns/                 # full snapshot — geometry and mathematical representation
│   ├── edcm/                 # full snapshot — measurement and text-gonol construction
│   ├── epac/                 # placeholder — energy particle affixiation coupling (no source yet)
│   ├── pcea/                 # full snapshot — prime circle encryption algorithm
│   └── ptcna/                # full snapshot — prime tensor circled neural architecture
├── libs/                     # empty scaffolds reserved for consolidated library surfaces
│   ├── skill-lib/
│   ├── metapat/
│   ├── ucns/
│   ├── edcm/
│   ├── epac/
│   ├── pcea/
│   └── ptcna/
├── backend/                  # empty scaffold
├── frontend/
│   └── cli/                  # empty scaffold
├── STACK_MANIFEST.md         # human-readable provenance record
└── stack-manifest.json       # machine-readable stack manifest (schema 1.0.0)
```

## Usage guidance

- **Start at [`STACK_MANIFEST.md`](STACK_MANIFEST.md).** It pins the exact source commit,
  branch, authority, snapshot path, and license status of every participant.
- **Read research sources in place.** `research/<repo>/` contains that repository's full
  tracked tree at the pinned commit (README, AGENTS/CLAUDE, source, tests, and docs).
- **Do not edit `research/` snapshots as doctrine.** Edit the canonical repository first,
  then refresh this aggregation with the procedure in `STACK_MANIFEST.md`.
- **`libs/` is reserved, not implemented.** Its scaffolds mark where consolidated library
  surfaces will live; nothing in this repo depends on them yet.
- **`backend/` and `frontend/cli/` are empty scaffolds** reserved for stack-level
  application work.

## Replaying a snapshot

From a clean checkout of the source repository at the desired commit:

```bash
git -C <checkout> archive <commit> | tar -x -C research/<name>/
```

Then update `STACK_MANIFEST.md` and `stack-manifest.json`, recompute the work-graph digest,
and commit with the new source commit SHAs in the message.

## hmmm

- Whether `libs/` should eventually contain package-only sources, built artifacts, or full
  vendored copies remains an open stack-integration decision.
- The exact shape of `backend/` and `frontend/cli/` is not yet declared.
- `research/epac/` is a placeholder until an energy particle affixiation coupling source
  repository exists.
