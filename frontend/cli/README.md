# frontend/cli — stack operator surface

This directory is the deliberately thin human control surface for `backend/`.
Durable state lives in PostgreSQL; execution and verification live in the
backend.

## Usage guidance

With `STACK_DATABASE_URL` configured:

```bash
python -m frontend.cli.stackctl db migrate
python -m frontend.cli.stackctl msdmd refresh ucns --root /srv/stack-repos/ucns
python -m frontend.cli.stackctl msdmd status
python -m frontend.cli.stackctl msdmd explain <job-id>
python -m frontend.cli.stackctl msdmd retry <job-id>
python -m frontend.cli.stackctl worker once
```

The systemd service invokes:

```bash
python -m frontend.cli.stackctl worker run
```

Do not add orchestration state, repository authority, generated metadata, or
database schema logic here. This surface should remain replaceable.

## Boundaries

- `--database-url` / `STACK_DATABASE_URL` must name PostgreSQL; SQLite is not a
  fallback.
- production target roots are constrained by `STACK_REPO_ROOT` and
  `STACK_ALLOWED_REPOS`.
- the CLI does not commit, push, merge, or acquire repository authority.
