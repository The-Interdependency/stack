# stack

"This is how it comes together."

`The-Interdependency/stack` is the consolidated, provenance-bearing research stack for the
organization's core work. Named repository identities are retained as archive provenance:
their pinned commits, tree identities, authority boundaries, and license status explain
where each stack participant came from.

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

- **Start at [`STACK_MANIFEST.md`](STACK_MANIFEST.md).** It pins each archived source
  commit, tree identity, authority, stack path, and license status.
- **Read research sources in place.** Archived participant paths contain their tracked
  source tree at the pinned commit (README, AGENTS/CLAUDE, source, tests, and docs).
- **Preserve provenance.** Do not delete named repository identities just because active
  research has moved into `stack`; those names are the replay trail.
- **`libs/` is reserved, not implemented.** Its scaffolds mark where consolidated library
  surfaces will live; nothing in this repo depends on them yet.
- **`backend/` and `frontend/cli/` are empty scaffolds** reserved for stack-level
  application work.

## Replaying An Archive

From a clean checkout of the source repository at the desired commit:

```bash
git -C <checkout> archive <commit> | tar -x -C research/<name>/
```

Then update `STACK_MANIFEST.md` and `stack-manifest.json`, recompute the tree identities
and work-graph digest, and commit with the archived source commit SHAs in the message.

## Verification

```bash
python3 tools/check_stack_manifest.py
```

The verifier checks the machine manifest schema, digest, archived tree identities,
declared paths, non-transfer boundaries, and generated artifact hygiene.

## License

See [`LICENSE_STATUS.md`](LICENSE_STATUS.md). The stack contains archived participant
trees with mixed license states; no repository-wide stack license is selected by that
status file.

## hmmm

- Whether `libs/` should eventually contain package-only sources, built artifacts, or full
  vendored copies remains an open stack-integration decision.
- The exact shape of `backend/` and `frontend/cli/` is not yet declared.
- `research/epac/` is a placeholder until an energy particle affixiation coupling source
  repository exists.
- Repo-level Public Gonol closure and promotion receipts are downstream of research.
