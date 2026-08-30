# frontend/cli — fresh-making operator surface

This directory is the deliberately thin human control surface for `backend/`.
Durable state and acceptance live in PostgreSQL; execution and verification live in
backend adapters; repository authority remains outside both.

## Usage guidance

With `STACK_DATABASE_URL` configured:

```bash
python -m frontend.cli.stackctl db migrate

python -m frontend.cli.stackctl fresh make-msdmd ucns \
  --root /srv/stack-repos/ucns \
  --source-sha <40-hex-commit>

python -m frontend.cli.stackctl fresh status msdmd:ucns
python -m frontend.cli.stackctl fresh explain msdmd:ucns
python -m frontend.cli.stackctl fresh make msdmd:ucns
python -m frontend.cli.stackctl fresh jobs --target msdmd:ucns
python -m frontend.cli.stackctl fresh recover
python -m frontend.cli.stackctl fresh affected msdmd:ucns
```

Queue for the VM worker:

```bash
python -m frontend.cli.stackctl fresh make-msdmd ucns \
  --root /srv/stack-repos/ucns \
  --source-sha <40-hex-commit> \
  --queue-only

python -m frontend.cli.stackctl worker once
python -m frontend.cli.stackctl worker run
```

The old `stackctl msdmd ...` namespace is removed. MSDMD is one derivation adapter
under `fresh`, not a parallel orchestration surface.

## Boundaries

- `--database-url` / `STACK_DATABASE_URL` must name PostgreSQL; SQLite is not a
  production fallback.
- production roots are constrained by `STACK_REPO_ROOT` and `STACK_ALLOWED_REPOS`.
- executor selection is attempt metadata, not logical job identity.
- `fresh status` verifies current identities, accepted receipt, output digest, and the
  derivation-specific verifier; it does not equate “recent” with fresh.
- the CLI does not commit, push, merge, or acquire repository authority.
- JSON receipt files are inspection projections; PostgreSQL `target_acceptance` is the
  acceptance authority.

## hmmm

The GitHub-hosted executor adapter is not implemented. VM-local execution is the
independent resilience baseline.
