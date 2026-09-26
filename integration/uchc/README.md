# UCHC candidate input consumption

## What this establishes

The active Stack ZFAE research can consume a clean-installed, immutable UCHC
wheel and recover complete native language structure. The public package is
not shadowed by `research/english-gonol/`; no a0p hash-derived vector is used.
This is candidate compatibility, not stable publication or domain graduation.

The source commit and physical wheel/database hashes are pinned in
`research/zfae/UCHC_INPUT.json`. The previous UCHC baseline remains part of the
historical research records. Root work-graph projections include the new
candidate separately, preserving the old experiments and authority boundaries.

## Usage guidance

Verify the wheel SHA-256 against the lock before installing into a clean venv:

```bash
python3 -m venv .uchc-env
.uchc-env/bin/python -m pip install --no-index --no-deps /artifacts/uchc-0.1.0a1-py3-none-any.whl
.uchc-env/bin/python -I research/zfae/uchc_input.py \
  --database /artifacts/construct.db --source-id request:1 \
  --text 'alpha letter alpha'
```

The consumer verifies the installed version, pip archive digest, installed-file
RECORD digests, and actual import location, then opens a private read-only
query snapshot of the verified complete corpus. These are integrity and
reproducibility checks, not authentication of a hostile Python process.

Exit 0 means complete source admission only. Exit 2 means unknown input remains
in its exact dossier, or configuration/artifact verification failed. Neither
exit code means a neural answer was generated. No input frame changes weights,
selects a sense or manufactures coordinates.

## Acceptance

The `uchc-input.yml` workflow fetches exact sources, reproduces the locked
wheel, tests the consumer in an isolated environment, rebuilds the complete
OEWN corpus, and exhausts the reader across all words, definitions, components
and evidence rows. It also runs Stack's existing consistency gate with full
Git history; absence of that history is an environment error, never a reason
to bypass the gate. The two integration tests explicitly check artifact
mismatch refusal and native input recovery. Unit fixtures do not substitute
for exhaustive corpus acceptance.

For a local integration run after installing pytest:

```bash
UCHC_INPUT_DATABASE=/artifacts/construct.db \
  .uchc-env/bin/python -I -m pytest -q integration/uchc/tests/test_input.py
```

## Rollback and hmmm

Remove the new consumer/lock and its graph participant together to roll back;
retain earlier sealed research evidence. Do not relabel the old comparison's
hashed features as the current native language primitive.

The source-owned UCNS neural-audit prerequisite, PTCNA propagation/learning and
readout construction, held-out useful inference, stable UCHC publication,
public-artifact reconsumption and domain-authority transition remain separate
uncompleted gates. This input contract does not silently close any of them.
