# frontend/cli — operator surface for fresh-making

The CLI is the human control and inspection surface for `backend/`. It does not own
orchestration state, repository authority, or MSDMD semantics.

## Usage guidance

From the stack repository root:

```bash
# create/update the persisted derivation spec and make it fresh
python -m frontend.cli.stackctl fresh make-msdmd ucns --root ../ucns

# verify one target, or every registered target
python -m frontend.cli.stackctl fresh status msdmd:ucns
python -m frontend.cli.stackctl fresh status

# make a previously registered target fresh again
python -m frontend.cli.stackctl fresh make msdmd:ucns

# show evidence, spec, current key, and active attempt
python -m frontend.cli.stackctl fresh explain msdmd:ucns

# queue now, execute later
python -m frontend.cli.stackctl fresh make-msdmd ucns --root ../ucns --queue-only
python -m frontend.cli.stackctl fresh run <job-id>

# retry/cancel and inspect history
python -m frontend.cli.stackctl fresh retry <job-id>
python -m frontend.cli.stackctl fresh cancel <job-id>
python -m frontend.cli.stackctl fresh jobs

# return abandoned leases to queued without erasing attempt evidence
python -m frontend.cli.stackctl fresh recover

# compute the minimal dependent closure from changed registered targets
python -m frontend.cli.stackctl fresh affected msdmd:ucns
```

The old `stackctl msdmd ...` surface is removed rather than maintained as a second path.
MSDMD is now one derivation adapter under the `fresh` control plane.

The first executor is `local`. VM and GitHub-hosted executors are not exposed until
they satisfy the same lease, attempt-history, verification, and receipt contract.

## Failure semantics

A source or generator identity that moves after queueing fails closed. A successful
subprocess whose candidate cannot be reproduced by the verifier also fails. The last
accepted artifact is not replaced until verification succeeds.

Unresolved required identity or verifier evidence is `hmmm`; it is never called fresh.
