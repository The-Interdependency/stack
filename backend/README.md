# backend — durable stack orchestration

`backend/` is the stack-level orchestration plane. It exists because repository
automation must remain inspectable and recoverable when a hosted executor such as
GitHub Actions is delayed, unavailable, or unreliable.

The first vertical slice is MSDMD regeneration.

## Contract

```text
request
  -> durable SQLite job
  -> exact source + generator identities
  -> selected executor
  -> repo-local generation
  -> artifact verification
  -> SHA-256 receipt
  -> explicit retry / hmmm
```

GitHub Actions is not the job database and is not required by this slice. The
implemented executor is `local`; VM and GitHub-hosted executors remain `hmmm`
until they implement the same job contract.

Repository authority stays with the target repository. `backend/` coordinates a
regeneration against an explicit checkout and a pinned skill-lib collector; it
does not become metadata authority.

Operational state defaults to `.stack/state/jobs.sqlite3` and is intentionally
untracked.

## Usage Guidance

From the stack repository root:

```bash
python -m frontend.cli.stackctl msdmd refresh ucns --root ../ucns
python -m frontend.cli.stackctl msdmd status
python -m frontend.cli.stackctl msdmd explain <job-id>
python -m frontend.cli.stackctl msdmd retry <job-id>
```

Queue without executing:

```bash
python -m frontend.cli.stackctl msdmd refresh ucns --root ../ucns --queue-only
python -m frontend.cli.stackctl msdmd run <job-id>
```

Run the verification suite:

```bash
python -m unittest backend.tests.test_orchestrator
```

## hmmm

- VM executor and credential boundary.
- GitHub Actions executor as an optional worker, never the durable state owner.
- Organization-level affected-repository discovery and dependency ordering.
- Persistent service/daemon; the first slice is intentionally operator-driven.
