# EPAC artifact consumption

These commands verify EPAC's public interfaces from an installed wheel. They do
not establish empirical validity or change the 14 retained FALSIFIED results, including the original four.
The independent repository's license and distribution rights must be resolved
before a candidate qualifies for stable publication.

## Accepted release

EPAC v0.1.0 has graduated. The independent repository owns EPAC implementation
and public contracts; Stack consumes its immutable public artifacts.
[`authority-transition.json`](authority-transition.json) binds the before/after
work graphs, public release, all six 209-test installs, pre-publication and public
Stack checks, source retirement and explicit non-transfer boundaries.

The source archive retains the qualification-time graduation record. The
subsequent lifecycle receipt records the completed event without rewriting the
immutable release bytes.

## Before publication

Build a clean, licensed candidate in the owning EPAC repository with
`tools/build_release.py`, then run its complete wheel and source-install replay.
Retain the wheel, source archive, release manifest, and SHA256SUMS unchanged.

Use a new environment outside stack, install the candidate's hash-locked upstream
dependencies, and install that exact wheel without editable or checkout paths.
Run the stack integration gate from an external working directory:

```bash
/path/to/clean-venv/bin/python /path/to/stack/integration/epac/verify_release.py \
  /path/to/candidate/interdependency_epac-0.1.0-py3-none-any.whl \
  /path/to/evidence/stack-candidate.json --phase candidate
```

The gate checks installed payload hashes and import origins, exact UCNS source
provenance, Public Gonol construction/replay, all nine declared molecules, helium
replay, and all 14 FALSIFIED standings. Its receipt binds the wheel and verifier
hashes plus the clean stack commit and tree. Candidate bytes, installed payloads,
verifier bytes, and the stack source must remain unchanged through execution.
A failure requires a repaired candidate and new verification before
stable publication.

## Public reconsumption

Use a clean Git checkout with `uv==0.11.18` on PATH. Run the launcher with
Python 3.12 (or a patched interpreter providing `tarfile.data_filter`); the
selected package runtime is a separate argument. The launcher clears inherited
Python import paths and user-site imports for its child environments.

After publishing those verified bytes, record a release lock with:

- `release_tag` and exact `source_commit`;
- `upstream`, binding the UCNS repository and exact commit with `authority_transfer: false`;
- `assets`, mapping each filename to its public GitHub release URL and SHA-256;
- `phase`, first `reconsumed`, then `graduated` only after retiring the forge copy.

The public asset set contains the wheel, source archive, `release-manifest.json`,
and `SHA256SUMS`. The lock is repository-owned acceptance evidence once its public
bytes have been independently verified. The current `release-lock.json` binds the selected public assets and upstream.
The checker compares it with the current EPAC manifest entry, and the launcher
compares its UCNS pin with the producer's hash-bound source lock before install.

The graduation event remains separately bound to the archived
`evidence/graduation-release-lock.json` and byte-exact before/after manifest
snapshots, including their source commit and Git blob identities. Its qualification
and consumer receipts describe the original v0.1.0 transition. Later participant
graph changes or accepted EPAC release updates do not rewrite that history;
current public-consumer CI must pass at the new Stack source before accepting a
new pin. The structural checker verifies local identities, not producer signatures
or current public availability.

```bash
python3 integration/epac/reconsume.py \
  integration/epac/release-lock.json /tmp/epac-public-consumption python3.12
```

The output directory must be new and outside stack. The command downloads and
hash-verifies the public assets, checks their source identity, installs locked
dependencies and the public wheel in a clean environment, and reruns integration.
It does not edit the source or authority records.

After successful public reconsumption, remove the versioned Python implementation
and tests from `research/epac/`, preserving historical evidence and provenance.
Replace the forge-local CI import path with this release consumer. The graduated
gate additionally requires that no Python implementation remains in that research
path. Commit the verified lock, before/after graph identities, and scoped
implementation/public-contract transition receipt with that retirement.

## Dependency and rollback boundaries

EPAC's release binds its own exact UCNS dependency. This does not update the
root `libs/ucns/` snapshot or unrelated research pins. Stack consumes EPAC as a
release artifact; a `libs/epac/` source mirror is not required for execution.

If public downloads or integration fail, stop the transition and preserve its
unpassed gate. Before graduation the existing forge authority remains in place.
After graduation, a rollback selects a previously accepted immutable release lock
and reruns integration. The first release has no earlier accepted release: retain
the evidence and repair through the independent repository. Do not silently
restore the historical forge copy as an authoritative implementation.

Generated environments and operational receipt projections stay outside the
repository. Only explicitly accepted release locks and transition evidence belong
in the versioned integration record.
