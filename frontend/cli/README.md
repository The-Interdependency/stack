# frontend/cli — operator surface for stack orchestration

The CLI is the human control and inspection surface for `backend/`. It does not
own orchestration state or MSDMD semantics.

## Usage Guidance

From the stack repository root:

```bash
# regenerate one repository against its exact current git commit
python -m frontend.cli.stackctl msdmd refresh ucns --root ../ucns

# inspect all durable jobs
python -m frontend.cli.stackctl msdmd status

# inspect one failure, artifact identity, or unresolved boundary
python -m frontend.cli.stackctl msdmd explain <job-id>

# retry a failed/cancelled job
python -m frontend.cli.stackctl msdmd retry <job-id>
```

Use `--source-sha <40-hex>` when the checkout cannot resolve its own git HEAD.
Use `--queue-only` when another process will execute the job later.

The first executor is `local`. VM and GitHub-hosted executors are intentionally
not exposed until they satisfy the same durable job and receipt contract.

## Failure semantics

A source checkout or generator identity that moved after queueing fails closed.
A successful subprocess without the declared output artifact also fails.
Failures remain in SQLite with an explicit error and, where needed, `hmmm`.
