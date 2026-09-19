# stack agent guide

This repository is `The-Interdependency/stack`, the organization's composition forge:
canonical projects are pinned here, stack-local research can combine them, and emergent
projects may later graduate into their own repositories.

These root instructions apply recursively to every file and workspace in Stack.
More-specific `AGENTS.md` files may add constraints for their subtree, but they
must not weaken the authority, provenance, preservation, or evidence rules below.

## Authority and topology

- `libs/<repo>/` is the manifest-pinned canonical repository view. Treat it as read-only
  inside stack; canonical edits happen in the owning repository.
- `research/<repo>/` is current stack-local research against an exact pinned base. It is
  not canon merely because it is in stack.
- `research/english-gonol/` is a distinct stack-local English lexical/gonol construction
  component. UCNS owns consumed geometry; EDCM may evaluate outputs but does not define
  the English Gonol construction.
- `research/python-gonol/` is a distinct stack-local Python source/gonol construction
  component. It owns Python source admission and bottom-up affixiation only; METAPAT owns
  affixiation semantics, UCNS owns consumed geometry, and parser objects are witnesses
  rather than gonol identities.
- `integration/epac/` consumes the hash-pinned public EPAC release.
  `research/epac/` retains historical evidence only; route implementation changes to
  `The-Interdependency/epac`. Do not restore the retired forge import path.
- root-level emerging projects such as `ahbg/` may be close to external repo-hood; root
  placement does not transfer authority from their inputs.
- `STACK_MANIFEST.md` and `stack-manifest.json` own stack-level participant provenance.
- `backend/` is the durable stack orchestration/fresh-making control plane.
- `frontend/cli/` is the replaceable human/operator surface for that backend.
- `skill-lib/` is the currently pinned operational skill snapshot; exact newer doctrine
  may be bound separately only when its provenance and non-transfer boundary are explicit.

## Structural update gate

Before adding, moving, separating, extracting, graduating, renaming, removing, or
changing the authority/relation/pin of a stack participant or research workspace, load:

```text
.agents/skills/stack-update/SKILL.md
```

Also resolve the applicable `interdependent-work-graph` doctrine and, for lifecycle
transitions, `project-incubation-graduation`. Structural changes are one transaction:
update every affected machine/human authority projection, remove superseded ownership
claims, recompute the work-graph digest, and pass:

```bash
python tools/check_stack_consistency.py
```

Do not treat moved code, passing local tests, or a new repository as sufficient evidence
that stack authority/provenance records are current.

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

Structural stack consistency:

```bash
python tools/check_stack_consistency.py
```

EPAC release integration (new output directory outside Stack):

```bash
python3 integration/epac/reconsume.py \
  integration/epac/release-lock.json /tmp/epac-public-consumption python3.12
```

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
workspace. The root stack-consistency checker verifies declared authority/provenance
coherence; it does not replace workspace behavioral tests.

## hmmm

- Concrete VM PostgreSQL/auth/service-account/storage and backup-mount acceptance remains
  unobserved until checked on the VM.
- Organization aggregate and website-projection derivation specs are not yet registered.
- English Gonol Construction has distinct stack-local authority but has not yet gained an
  independent repository/release authority boundary.
- Python Gonol Construction has distinct stack-local authority but has not yet gained an
  independent repository/release authority boundary; exact UCNS affixiation geometry is unresolved.
- The complete root `skill-lib/` snapshot refresh remains separate because the current
  provenance-bound fresh-making doctrine is newer than the local generator snapshot.
- Project graduation automation remains unimplemented.

## Universal evidence and implementation rules

- Inspect the owning source, applicable `AGENTS.md` files, and exact participant
  identities before changing behavior. Moving code, passing a local test, or a
  successful workflow does not transfer authority, proof status, or security status.
- Preserve unrelated user changes. Keep experiments in their owning research
  workspace, and route completed behavior to the owning canonical repository with
  explicit review and release evidence.
- Preserve identity, order, multiplicity, relations, recoverable constituents,
  and provenance whenever a structure is transformed. Do not replace a retained
  object with a scalar summary merely because the scalar is convenient.
- Freeze source bytes, inputs, algorithms, parameter ranges, work limits, and
  readout rules before comparing known targets. Emit deterministic receipts with
  exact commands and hashes; incomplete external computation is `UNRESOLVED`,
  not a negative control.
- Separate missing implementation, missing selection, mathematical obstruction,
  and missing evidence. A failed candidate falsifies that candidate, not every
  possible construction; a local survival remains bounded by its assumptions.
- Preserve historical receipts and negative results. If source identity changes,
  create a new receipt instead of rewriting the old result.
- Treat arithmetic patterns, primes, geometry, round-trip correctness, carrier
  size, and representation fidelity as non-cryptographic evidence unless a
  construction-specific security property is demonstrated against a stated threat
  model. Assess confidentiality, integrity, replay, rollback, forward secrecy,
  and compromise recovery separately from functional correctness.
- Do not fit observed sequences or promote supplied parameters into discovered
  selectors. Any claimed successor must expose a deterministic selector from the
  retained state, or return an explicit candidate set or unresolved result.
- Record the first remaining irreducible assumption and the smallest next
  experiment that could resolve it in the handoff and receipt.

For the detailed UCNS/PCEA constructor, arity, successor, and cryptographic
requirements, read [`research/AGENTS.md`](research/AGENTS.md) when working in
those workspaces.
