# PR #94 — containment and checkpoint repair

GPT generated; context, prompt Erin Spencer.

This repairs two reproducible integrity defects at reviewed head
`bd54c789cf5df1910dbb57a22cce6c7754b47e54`, against base
`9de81c67b271df09c1d9ba5422660c96fe8af7ac`. The exact measured counts and source
digests are in [REVIEW_REPAIR.json](REVIEW_REPAIR.json). Original RESULTS.json and
CHECKS.json remain historical observations; this record does not replace them.

## Findings and repairs

| Finding | Classification / owner | Repair and independent witness |
| --- | --- | --- |
| [Private directory escapes](https://github.com/The-Interdependency/stack/pull/94#discussion_r4420365794) | DEFECT / v2 artifact orchestration | Resolve checkout and private paths before checking containment; use the resolved path. Check private children, generation, packaging, grading, exports and harness receipt destinations. Synthetic tests attempt direct, parent-component and symlink disclosure, including every release level. |
| [Orphaned ciphertext becomes FAILED](https://github.com/The-Interdependency/stack/pull/94#discussion_r4420365802) | DEFECT / v2 checkpoint orchestration | Recompute from the unchanged frozen row, compare complete existing ciphertext bytes, and verify recovery in a fresh receiver process before reconstructing a receipt. Conflicting evidence is retained and rejected without a replacement/FAILED receipt. |
| Hosted workflow failures | EXTERNAL / GitHub account execution availability | Both job annotations explicitly report a billing-related account lock that prevented startup. No test-step result exists. No workflow syntax or algorithm cause is inferred. |

Checkpoint files now publish complete bytes atomically and without replacement.
Interruption before publication cannot leave a valid-looking partial JSON receipt;
interruption between ciphertext and receipt remains resumable. Existing failed or
malformed receipts stay available for inspection. Repeated completed generation
checks the receipts and retains the existing consistent report; conflicting report
counts are rejected. Use one generator per archive in operator-owned directories.
This is not a filesystem sandbox against a hostile process changing ancestors.

The repair adds only artifact/checkpoint controls, their regressions and a CI step.
The matrix, operation adapters, original algorithms, source locks, prediction
commitment, staged clue contents, all 1,841 identities and the public archive bytes
are unchanged. Per-case answers, corpora, schedule mappings and grading receipts
remain outside Git. Public records contain aggregate validation only.

## Verification and evidence limits

- Four focused tests executed against the exact pre-repair build/release modules
  failed as expected: 25 failing subcases, zero test errors. These reproduce
  containment, attempted public export, missing-receipt recovery and conflicting
  evidence behavior. The failures are defects, not attacker-recovery results.
- The repaired synthetic suite passes 16 tests, including an interruption injected
  between wire and receipt publication, interruption during atomic publication,
  receiver refusal, receipt conflicts, unsafe IDs and redirected private children.
- A separate replay starts from the original private plan and all original wire
  files, with no receipts. It reconstructs all 1,841 receipts through recomputation
  and fresh receiver checks. An independent filesystem comparison checks every
  ciphertext byte, inode and modification time against the pre-run snapshot.
- The existing 176-test Weave suite passes with zero errors, failures or skips and
  an unchanged-source receipt. The 11-test v2 harness passes, including 602 typed
  schedule refusals, all 12,887 case/level clue projections, 28 exports and four
  standalone level-six receivers. The full-Weave gate still exits 2 as required.
- Stack consistency, portfolio validation/ancestry, municipal handoff integrity
  and all 42 ratio fields pass. A shallow checkout initially lacked a historical
  Git object; fetching full history satisfied the existing gate without changing it.
- One interim 176-test run passed its test methods but was correctly rejected by
  its source-stability guard because a regression file was edited during that run.
  That result is excluded; the final unchanged-source run supplies acceptance.

These are authorized recovery and harness-integrity checks, not cryptanalytic
attacks, an independent cryptographic implementation, or a full-system security
assessment. **No v2 attacker-recovery trial was run.** Asymmetric key generation,
authentication, replay resistance and private-state binding remain incomplete.

## Hosted evidence

At the reviewed head, [stack-consistency run 41001095046](https://github.com/The-Interdependency/stack/actions/runs/41001095046)
has job `123885412475`; [Weave run 41001095045](https://github.com/The-Interdependency/stack/actions/runs/41001095045)
has job `123885412696`. Both have no steps and log retrieval returns 404/BlobNotFound.
The authoritative check annotations, fetched separately, state:

> The job was not started because your account is locked due to a billing issue.

The additional Ubuntu migration notice is not a diagnosed cause. The new workflow
step runs synthetic integrity regressions with the exact pinned UCNS source; it
requires no private operator archive. Local results do not turn blocked hosted jobs
green. Review and merge remain separate states; this repair does not bypass gates.

## Usage and replay

From the full Stack checkout, supply the two hash-locked UCNS files as described in
README.md, then run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/weave/recovery-challenges/v2/test_regressions.py
PYTHONDONTWRITEBYTECODE=1 WEAVE_SOURCES="$PWD/sources" python3 research/weave/test.py \
  --receipt /absolute/outside-checkout/weave-suite.json
python3 research/weave/recovery-challenges/v2/test_harness.py \
  --private /absolute/original-operator \
  --receipt /absolute/outside-checkout/new-harness.json --require-full-weave
python3 tools/check_stack_consistency.py
python3 skill-lib/ratios/ratios_check.py --root research/weave/recovery-challenges/v2 --strict
```

The harness must pass its 11 methods and return 2 for incomplete full-Weave
coverage. Choose a new receipt filename; existing evidence is not overwritten.
To exercise every missing checkpoint, make a new private copy of only the original
`private.json` and `ciphertexts/`, add an empty `receipts/` directory, and run
`build.py generate --private /absolute/replay --workers 4`. Do not run `freeze`:
that creates a different experiment. Retain a pre-run byte/inode/mtime snapshot,
then compare all wires and the public prediction commitment after completion.
Do not call `package` over the existing frozen public archive.

Rollback is a revert of the repair commit alone: it leaves frozen data unchanged
but reopens both defects. Do not resume publication through a reverted harness.

## hmmm

The GitHub billing lock requires account-owner resolution before hosted validation
can execute. Current-head review and merge admission remain external gates. No
attacker success, confidentiality, asymmetry or commercial-strength claim follows
from this repair. The original operator bundle retains its historical tool source;
use this repaired checkout with that bundle's unchanged private data.
