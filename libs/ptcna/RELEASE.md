# Releasing `ptcna` to PyPI

`ptcna` ships as a pure-Python wheel + sdist. Publishing is done manually
(e.g. from Termux). This checklist is the whole procedure.

## 0. One-time: current tooling

PEP 639 license metadata (Metadata 2.4) requires **recent** build tooling. Old
`twine`/`packaging` will *false-fail* `twine check` on a perfectly valid dist,
so upgrade first:

```bash
pip install -U build twine "packaging>=24.2" "setuptools>=77"
```

(The build itself pins `setuptools>=77` via `build-system.requires`; the upgrade
above is for the *checking/uploading* side.)

## 1. Pre-flight

```bash
python -m pytest            # all tests must pass (neural layer needs numpy)
python scripts/check_contracts.py
python .agents/skills/ratios/ratios_check.py --root ptcna --strict
PYTHONPATH=.agents/skills python .agents/skills/msdmd/collect.py \
  --root . --repo ptcna --out /tmp/ptcna_msdmd.ts
cmp /tmp/ptcna_msdmd.ts ptcna_msdmd.ts
```

- Confirm `pyproject.toml` and `ptcna.__version__` both name `0.1.1`.
- Confirm `LICENSE`, `README.md` present; README "Status" line current.
- Confirm `ptcna/neural/edcm.py` is absent and the UCNS boundary remains typed
  and suspended.

## 2. Build

```bash
rm -rf dist build ptcna.egg-info
python -m build             # produces dist/ptcna-<ver>-py3-none-any.whl + .tar.gz
```

The wheel ships the four layer packages (`neural`, `circle`, `seed`, `core`);
per-layer `tests/` are excluded from the distribution.

## 3. Validate

```bash
python -m twine check dist/*
```

Expect `PASSED` for both files. If you see
`unrecognized or malformed field 'license-expression'/'license-file'`, your
local `packaging` is < 24.2 — upgrade it (step 0); the dist is fine.

## 4. Upload

```bash
# Test PyPI first (optional but recommended for a first publish):
python -m twine upload --repository testpypi dist/*
python -m pip install -i https://test.pypi.org/simple/ ptcna    # smoke check

# Real PyPI:
python -m twine upload dist/*
```

Auth: use a PyPI API token (`__token__` as username, `pypi-...` as password), or
a `~/.pypirc`. Never commit tokens.

## 5. Post-publish

- Tag the release: `git tag v0.1.1 && git push origin v0.1.1`.
- Wire the extra into the aggregator: in `interdependent-lib`, add
  `ptcna = ["ptcna>=0.1.1"]` to `[project.optional-dependencies]`, include it
  in `all`, and note it in `docs/dependency-policy.md`.

## Notes

- Pure-Python, no compiled extensions — one wheel serves all platforms.
- Runtime dependency: `numpy>=1.21` (neural layer only; circle/seed/core are
  stdlib). Installing `ptcna` pulls numpy.
