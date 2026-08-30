# backend — durable fresh-making orchestration

`backend/` is the stack-level orchestration plane. It exists because derived artifacts
must remain inspectable and recoverable when a hosted executor such as GitHub Actions
is delayed, unavailable, or unreliable.

The first production vertical slice is MSDMD fresh-making.

## Contract

```text
current exact identities
  -> persisted derivation spec
  -> deterministic freshness key
  -> durable executor-independent job
  -> leased attempt
  -> executor candidate
  -> independent rerender verification
  -> atomic publication
  -> accepted receipt
  -> replayable freshness decision
```

Freshness means **provably consistent with declared current inputs**, not recently
rebuilt. Timestamps and executor choice are audit metadata and do not enter the
freshness key.

Operational state defaults to `.stack/state/` and is intentionally untracked:

```text
.stack/state/jobs.sqlite3   # fresh_jobs, fresh_attempts, accepted receipts
.stack/state/specs/         # persisted derivation specifications
.stack/state/receipts/      # accepted fresh-making receipts
```

The earlier prototype `jobs` table, if present in an existing SQLite file, is left
untouched. New semantics use `fresh_*` tables rather than silently reinterpreting old
rows.

## Reliability boundaries

- Logical job identity is `kind + target + desired freshness key`; executor choice is
  attempt metadata, so retrying through another executor does not create a different
  logical job.
- Active attempts are leased. Expired leases retain their attempt evidence and return
  the logical job to `queued` for recovery.
- A successful executor exit does not establish freshness. MSDMD is rerendered into a
  second isolated candidate and compared byte-for-byte before publication.
- The accepted output is replaced only after verification. Failed or nondeterministic
  candidates do not overwrite the last accepted artifact.
- Repository authority remains with the owning repository. The backend coordinates a
  derivation; it does not become authority for repository-owned metadata.

## Usage guidance

From the stack repository root:

```bash
# Register current identities and make one repo's MSDMD collection fresh.
python -m frontend.cli.stackctl fresh make-msdmd ucns --root ../ucns

# Re-evaluate a registered target and do nothing when it is already proven fresh.
python -m frontend.cli.stackctl fresh make msdmd:ucns

# Verify current freshness evidence.
python -m frontend.cli.stackctl fresh status msdmd:ucns

# Explain spec, desired/accepted keys, active attempt, and hmmm.
python -m frontend.cli.stackctl fresh explain msdmd:ucns

# Inspect durable history and recover abandoned leases.
python -m frontend.cli.stackctl fresh jobs
python -m frontend.cli.stackctl fresh recover
```

Use `--queue-only` with `fresh make-msdmd` when another worker will execute the job.
Use `--source-sha <40-hex>` only when the target root cannot resolve its own Git HEAD.

Run the local verification suite:

```bash
python -W error::ResourceWarning -m unittest backend.tests.test_orchestrator
```

The suite covers no-op idempotency, source and generator invalidation, tamper detection,
false-green rejection, expired-lease recovery, moved identities before execution,
minimal affected closure, executor-independent job identity, and receipt replay.

## hmmm

- VM executor adapter and its credential/capability boundary.
- GitHub Actions executor as an optional worker, never the durable state owner.
- Organization-level derivation specs connecting repo MSDMD collections to aggregate and
  website projections; the generic affected-closure engine is implemented, but only the
  repo MSDMD adapter is wired today.
- Persistent daemon/service; the current slice is intentionally operator-driven.
- The root `skill-lib/` snapshot predates the newly merged `fresh-making` skill and needs
  an exact full-snapshot refresh before stack can claim that newer skill-lib commit as its
  pinned local doctrine identity.
