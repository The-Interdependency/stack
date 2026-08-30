# stack agent guide

This repository is `The-Interdependency/stack`, the organization's composition forge:
canonical projects are pinned here, stack-local research can combine them, and emergent
projects may later graduate into their own repositories.

## Authority and topology

- `libs/<repo>/` is the manifest-pinned canonical repository view. Treat it as read-only
  inside stack; canonical edits happen in the owning repository.
- `research/<repo>/` is current stack-local research against an exact pinned base. It is
  not canon merely because it is in stack.
- root-level emerging projects such as `ahbg/` may be close to external repo-hood; root
  placement does not transfer authority from their inputs.
- `STACK_MANIFEST.md` and `stack-manifest.json` own stack-level participant provenance.
- `backend/` is the durable stack orchestration/fresh-making control plane.
- `frontend/cli/` is the replaceable human/operator surface for that backend.
- `skill-lib/` is the currently pinned operational skill snapshot; exact newer doctrine
  may be bound separately only when its provenance and non-transfer boundary are explicit.

## Fresh-making boundary

PostgreSQL on the VM is the single production state authority for derivation specs,
freshness keys, logical jobs, attempts/leases, receipts, target acceptance, dependency
edges, and `hmmm`. It is **not** authority for repository source, canon, generated
artifact meaning, theorem status, measurement validity, or publication standing.

```text
fresh != recent
fresh == exact current identities + matching accepted receipt + output digest + verifier
```

MSDMD collection regeneration is the first derivation adapter. The old `stackctl msdmd`
namespace is deprecated and removed; use `stackctl fresh ...`.

## Boundaries

- Do not edit `libs/` as doctrine or silently update pinned source commits.
- Do not transfer semantic, proof, empirical, certification, measurement, or license
  status between participant repositories.
- Do not call generated output fresh from timestamps, executor success, or GitHub Actions
  status alone.
- GitHub Actions may become an executor but must not become durable state or acceptance
  authority.
- Generated local state, caches, candidates, backups, and receipt projections must not be
  committed unless the artifact is explicitly repository-owned evidence.
- For behavior-bearing build changes, resolve and follow applicable `skill-lib` doctrine;
  `backend/fresh-making-provenance.json` binds the current runtime's exact fresh-making
  doctrine identity.

## Checks

Fresh-making/backend checks that can run without PostgreSQL:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -W error::ResourceWarning -m unittest \
  backend.tests.test_orchestrator \
  backend.tests.test_worker_postgres \
  backend.tests.test_publication_rollback
python3 -m compileall -q backend frontend
bash -n backend/ops/backup_postgres.sh backend/ops/restore_test.sh
```

PostgreSQL integration checks require an explicitly disposable database. A skipped
integration check is `hmmm`, not a pass.

AHBG/Grok has its own local suites under `ahbg/grok/`; run those when touching that
workspace. Do not claim root manifest-check tooling that is not present in this branch.

## hmmm

- Concrete VM PostgreSQL/auth/service-account/storage and backup-mount acceptance remains
  unobserved until checked on the VM.
- Organization aggregate and website-projection derivation specs are not yet registered.
- The complete root `skill-lib/` snapshot refresh remains separate because the current
  provenance-bound fresh-making doctrine is newer than the local generator snapshot.
- Project graduation automation remains unimplemented.
