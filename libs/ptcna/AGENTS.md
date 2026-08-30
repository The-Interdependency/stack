# PTCNA agent guide

PTCNA is one four-layer architecture:

```text
neural -> circle -> seed -> core
```

Authority and invariants:

- `ptcna.neural` is the only differentiable layer and the only owner of
  back-propagation.
- Circle, seed, and core objects are non-differentiating auditing and timing
  tensors. They may carry neural payloads opaquely; carrying a payload does not
  transfer gradient ownership.
- Every circle, seed, and core is itself a tensor. Composition counts are
  variable.
- Fiqs gate internal core propagation according to Fickian field motion. That
  is timing, not gradient descent.
- UCNS integration is active only for the exact pinned `157x7x7x53` candidate
  receipt. Other shapes remain suspended. Do not activate archived surfaces
  such as `a0_safe`, `UCNSObject`, or `factor_search`.
- EDCM measurement authority belongs to `The-Interdependency/edcm`. PTCNA may
  consume an explicitly injected measurement provider; it must not maintain a
  shadow EDCM implementation.

## Construction and evaluation boundary

- Build the selected PTCNA architecture faithfully. Curiosity may select the
  object of inquiry; neither upstream validation nor a simpler baseline grants
  permission to construct it.
- Build and maintain a dependable simpler fallback behind an explicit interface.
  The fallback preserves useful operation if PTCNA fails; it must not silently
  replace, redefine, or be reported as PTCNA.
- "Does it work?" is the critical falsifiability question. Freeze the
  representative workload, comparator, exact metrics and aggregation,
  thresholds, resource bounds, stopping rules, and failure propagation before
  inspecting outcomes. This freeze governs the verdict, not construction.
- Build non-receipted PTCNA prime and ring structures under local provenance.
  Only the exact receipt-covered state may carry UCNS candidate provenance.
- Record terminal status before repair: `FALSIFIED`, `SURVIVED — not proved`,
  or `UNRESOLVED`. A simpler recovery method may supply the fallback; it does
  not invalidate the architecture that selected the discovery path.

Before changing code, load the applicable repo-local skills under
`.agents/skills/`. All new or materially revised modules need self-declared
`MODULE_BUILD`, `CONTRACTS`, and actual runtime `BOUNDARIES` metadata when the
corresponding skill applies. Tests own `CHECKS` evidence. Unknowns remain
`hmmm`.

## Usage

Install and verify:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python scripts/check_contracts.py
python .agents/skills/ratios/ratios_check.py --root ptcna --strict
PYTHONPATH=.agents/skills python .agents/skills/msdmd/collect.py \
  --root . --repo ptcna --out /tmp/ptcna_msdmd.ts
cmp /tmp/ptcna_msdmd.ts ptcna_msdmd.ts
```

Build and inspect the release:

```bash
python -m build
python -m twine check dist/*
python -m pip install --force-reinstall dist/ptcna-*.whl
python -c "import ptcna; print(ptcna.__version__)"
```

Do not publish from a dirty tree or before the repository tests, metadata
collection check, ratios gate, wheel smoke test, and downstream
`interdependent-lib` compatibility check all pass.

## hmmm

- Continuous seven-fold geometry is not established by the candidate receipt.
- Training and timing behavior across the complete four-layer seam remains
  unfalsified under sustained load.
