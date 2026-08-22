# stack

"This is how it comes together."

`The-Interdependency/stack` is the consolidated, provenance-bearing research stack for the
organization's core work. The named repositories are retained as archive provenance: their
identities, source commits, boundaries, and licenses explain where each stack participant
came from. After a participant is archived into `stack`, stack-level research may continue
here without deleting that provenance.

Repository-level Public Gonol admission is a promotion artifact. It happens after a body
of research is ready to close, not before construction starts.

## Layout

```text
stack/
├── skill-lib/               # full snapshot of The-Interdependency/skill-lib
├── research/
│   ├── metapat/              # full snapshot — semantic authority (Meta Energy Theory)
│   ├── ucns/                 # full snapshot — geometry and mathematical representation
│   ├── edcm/                 # full snapshot — measurement and text-gonol construction
│   ├── epac/                 # stack-owned provisional energy particle affixiation coupling research
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

- **Start at [`STACK_MANIFEST.md`](STACK_MANIFEST.md).** It records archived source
  identities, stack ownership, authority boundaries, snapshot paths, and license status.
- **Read and continue research in place.** `research/<repo>/` contains archived source
  material plus any stack-owned research deltas accepted after archival.
- **Preserve provenance.** Do not delete named repository identities just because their
  active research has moved into `stack`; those names are the replay trail.
- **Do not require Public Gonols up front.** Construct candidate research first. Close and
  promote a participant's Public Gonol only after the research has an admissible boundary.
- **`libs/` is reserved, not implemented.** Its scaffolds mark where consolidated library
  surfaces will live; nothing in this repo depends on them yet.
- **`backend/` and `frontend/cli/` are empty scaffolds** reserved for stack-level
  application work.

## Archiving A Participant

From a clean checkout of the source repository at the desired commit:

```bash
git -C <checkout> archive <commit> | tar -x -C research/<name>/
```

Then update `STACK_MANIFEST.md` and `stack-manifest.json`, recompute the work-graph digest,
and commit with the archived source commit SHAs in the message. After archival, stack-owned
research changes belong in this repository unless a participant is deliberately split back
out into its own active repo.

## Verification

```bash
python3 tools/check_stack_manifest.py
```

Stack CI runs this same root manifest gate plus `git diff --check`.

## hmmm

- Repo-level Public Gonol closure and promotion receipts are downstream of research.
- Whether `libs/` should eventually contain package-only sources, built artifacts, or full
  vendored copies remains an open stack-integration decision.
- The exact shape of `backend/` and `frontend/cli/` is not yet declared.
- `research/epac/` is stack-owned provisional research until it is closed, promoted, or
  deliberately split into a separate archived participant.
