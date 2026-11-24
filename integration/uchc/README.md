# Released UCHC in Stack

## What this establishes

Stack installs the hash-locked UCHC `0.2.0a3` release for its English input and
structural readers. The [ZFAE input lock](../../research/zfae/UCHC_INPUT.json)
and [AHBG structural lock](../../ahbg/integration/UCHC_STRUCTURAL.json) pin
the same wheel and each corpus's own database and logical receipt.

## Usage guidance

Download the exact wheel into a clean Python 3.12 environment:

```bash
python3 -m venv .uchc-env
.uchc-env/bin/python -m pip download --no-deps --require-hashes -r integration/uchc/halving-requirements.txt -d dist
.uchc-env/bin/python -m pip install --no-index --no-deps dist/uchc-0.2.0a3-py3-none-any.whl
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

The `uchc-input.yml` workflow installs the locked release wheel, tests the
consumer in an isolated environment, rebuilds the complete
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

To roll back, restore the preceding input and structural locks and their
matching workflows and graph projections together. The source-owned UCNS
neural-audit prerequisite and PTCNA propagation, learning and readout are
recorded in the ZFAE research workspace.

## 0.1.0 graduation candidate

`candidate-0.1.0.json` records the historical extracted package and its exact
wheel. Select it with `UCHC_INPUT_LOCK` when replaying that candidate. The
released consumer reproduces the pinned v2 corpus using Python 3.12.14 and
SQLite 3.45.1.


## Ordinal radius-halving

UCHC supplies the ordinal disc construction and its full additive resultant.
The [release receipt](epicycle-release.json) identifies the verified wheel.
Its URL and SHA-256 are locked in `halving-requirements.txt`. With its pinned UCNS geometry
installed, run `uchc-halving bull` or `uchc-halving --sequence bull bull`.
Stack keeps its 16 b rad experiment in `research/english-gonol`; its earlier
ordinal evidence stays at its recorded source revisions.

```sh
python -m pip download --no-deps --require-hashes -r integration/uchc/halving-requirements.txt -d dist
python -m pip install --no-deps 'ucns @ git+https://github.com/The-Interdependency/ucns.git@1edfa593ae9d8c9ad394b5462638bcc717f99fbd' dist/uchc-0.2.0a3-py3-none-any.whl
python -I integration/uchc/verify_halving.py dist/uchc-0.2.0a3-py3-none-any.whl /path/to/encoding-ucns
```

The encoding checkout is UCNS `300877066436a03d046b8951772c1e2aed2c5166`.
The verifier replays a sentence made of two closed words and checks its
ordinal radii, placed endpoint, and full additive vector. It also verifies
Stack's four-byte ASCII result. To roll back, restore the
[0.2.0a2 consumer revision](https://github.com/The-Interdependency/stack/tree/8ed854544d8f0983d7385adc5ad1cb3f14376145/integration/uchc).
