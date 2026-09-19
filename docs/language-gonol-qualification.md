# Language construction qualification

Status: execution pending. This protocol qualifies the current English v2
corpus construction and Python source/control construction. Geometry,
language understanding, runtime equivalence, and canon promotion remain hmmm.

## Frozen scope and evidence

- Stack starting source: `bcaba85900716e5209150a504660fa2ca5158299`.
- Minimum repair: `14b6063` (tabs, physical source addresses, density rendering).
- English: every file admitted by the existing OEWN 2025 loader, from
  `globalwordnet/english-wordnet@dc343f2683279ecbb13fab4e2fd778d7b162d287`.
- English UCNS authority: `4f863ad37096b7baab8f62820ad5cb937b62a3a7`.
- Historical lexical test authority: `d7c6f51304ed6c32d48badf63132bea6de8af497`.
- Python UCNS authority: `62e08ee1cf3b5d7b6e48c927b1047509e6328b5c`.
- Python corpus: every tracked `.py` file beneath CPython `Lib/test/` at the
  `v3.12.14` commit `2abcf904b8dac8c999d2b3aac76681abb333798a`. Exact source inventory is frozen before the run.
  Files that violate the existing encoding admission rule remain explicit
  rejection evidence with original byte hashes. Invalid syntax and off-carrier
  Unicode remain represented, with their existing witness flags and hmmm.

## Acceptance

1. Run every existing English and Python workspace test with exact dependencies;
   require actual call outcomes, zero skips, zero failures, and nonempty suites.
2. Rebuild all admitted English input twice in separate processes and empty
   output directories. Verify SQLite integrity, logical replay, complete counts,
   unchanged source inventories, and identical logical receipts/manifests.
3. Enumerate the complete Python corpus before construction. Each eligible file
   must have two independent process builds, exact source recovery, replay,
   matching canonical database content and manifest, and an explicit outcome.
4. Check tab widths and physical addresses against independent source-based
   witnesses. Verify provenance and constitutive control data, and reject
   targeted changes to identity, order, source, relation and receipt fields.
5. Generated databases remain local execution state. Commit compact provenance,
   outcome and digest receipts; do not substitute a sample for the declared scope.

## Resource preflight and stopping

Observed available resources before execution: 26 GiB free disk, 21.5 GiB RAM,
Python 3.12.14. The recorded English run needs about 293 MiB output and 280 MiB
RSS; two serial builds fit. Python file pairs are verified and removed one pair
at a time, keeping compact per-file evidence. Preflight the largest input and
storage estimate before starting. These are local persistent processes; no
arbitrary scientific wall-clock cutoff is imposed. Stop on completion or a
recorded computational/admission failure; retain failures and all hmmm.

## Usage and next steps

Run the workspace tests from their own directories. Supply
`ENGLISH_GONOL_UCNS_ROOT` for the exact historical lexical producer and
`UCNS_SOURCE_ROOT` for the Python producer. The full construction/replay runner
and final receipt will be linked here after implementation and execution.

Passing this protocol qualifies its explicit construction profiles only.
UCNS retains geometry authority; Stack retains active construction ownership;
EDCM retains measurement authority. Independent repository graduation is outside
this qualification.

## CPython provenance correction

The former `2d7d957248038635334b62b27f650220213d8e5d` pin cannot be fetched
from the declared upstream (`not our ref`). The annotated `v3.12.14` tag
`4b65faa0b452113bf130086fb1519be6d9cd9b06` resolves to
`2abcf904b8dac8c999d2b3aac76681abb333798a`. BASE and the Python work graph
now use that observed source identity; the graph digest is recomputed.
No language profile or geometry authority changes. The root Stack manifest
contains no CPython pin and its authority projection remains applicable.
