# UCNS

<p align="center">
  <img src="docs/ucns-geometry-repository.svg" alt="UCNS — Geometry Repository" width="100%">
</p>

UCNS is a geometry repository.

Its active scope is limited to constructions that directly represent or test geometry:

- the exact 157-position Public Gonol carrier;
- the directed lifted carrier and its 360° visible / 720° complete return;
- exact framed Möbius motion;
- Möbius vesica and Seed-of-Life constructions and certificates;
- candidate exact finite modular-action orbit and circle geometry;
- candidate exact visible-circle continuum wave / gonal boundary traces;
- prime-indexed ribbon, link, interval, Milnor, Alexander, and related topological geometry;
- numerical machinery used to certify those constructions.

Everything semantic is outside this repository's active domain: lexical corpora, definitions, morphology, NLP parsing, function-name semantics, EDCM measurement profiles, PTCNA state, evaluator laboratories, and cross-stack adapters.

The poster above is a display certificate of those constructions. It is not an interpretation layer.

## Public Gonol

The Public Gonol is the exact ordered 157-position carrier in `src/ucns/public_gonol.py`. Every glyph is a Public Gonol function position. UCNS does not divide glyphs into letters, punctuation, digits, or symbols for construction.

A function's geometric operation is not inferred from Unicode names or dictionary definitions. Where an operation is not geometrically established, it remains `hmmm`.

## Möbius root loop

`src/ucns/direct_mobius.py` implements the exact framed quotient

```text
(t, ε) ~ (t + n, (-1)^n ε)
```

One visible turn preserves phase and reverses the local frame. Two visible turns restore the complete state.

## Modular orbit geometry candidate

`src/ucns/modular_orbit.py` implements a candidate finite modular multiplication representation

```text
T_{a,m}(x) = a*x mod m
```

over a caller-declared canonical residue carrier. The carrier must be nonempty, closed under the action, and bijective under that action, so the result is an exact disjoint cycle decomposition rather than a transient functional graph.

The executable arithmetic is exact within the declared model. The representation remains candidate-scoped until its own falsifier/replay/ratification path selects stronger UCNS standing. Executability alone is not ratification.

The candidate records only geometry: canonical residues, exact action edges, cycle periods, and exact normalized circle positions `r/m` turns. Display aliases and downstream meanings stay with renderers and consumers.

For the mod-9 digit carrier used in common circular diagrams:

```python
from ucns import build_modular_orbit_geometry

g = build_modular_orbit_geometry(9, 2, range(1, 9))
assert g.orbits == ((1, 2, 4, 8, 7, 5), (3, 6))
assert g.periods == (6, 2)
```

The core uses residues `0..m-1`; a renderer may choose to display residue `0` as `9` in a mod-9 digit diagram without changing the UCNS record.

## Continuum wave → gonal boundary trace candidate

`src/ucns/gonal_boundary_trace.py` supplies the candidate exact visible-boundary bridge.

On a circle of radius `R`, the continuum scalar wave equation is

```text
u_tt = (c^2/R^2) u_θθ.
```

Periodic spatial modes have integer harmonic number `n`. On an `m`-gonal visible boundary, residue `r` sits at exactly `r/m` turns and harmonic `n` has exact phase

```text
(n*r mod m)/m.
```

For positive integer continuum covering degree `d`, the matched spacetime covering

```text
(θ, t) -> (dθ, dt)
```

preserves the wave equation. Its finite gonal trace is

```text
r -> d*r mod m.
```

If `a = d mod m`, this is exactly the finite modular action `r -> a*r mod m`.

The finite trace forgets the continuum degree: `d`, `d+m`, `d+2m`, ... all produce the same residue action while multiplying the continuum harmonic and time scale differently. Therefore the continuum covering degree is an explicit input; UCNS does not infer it from the modular multiplier.

```python
from ucns import (
    build_circle_wave_mode_trace,
    build_modular_orbit_geometry,
    pullback_circle_wave_trace,
)

geometry = build_modular_orbit_geometry(9, 2, range(1, 9))
source = build_circle_wave_mode_trace(9, 1, range(1, 9))

covering_2 = pullback_circle_wave_trace(source, geometry, 2)
covering_11 = pullback_circle_wave_trace(source, geometry, 11)

assert covering_2.action == covering_11.action == geometry.action
assert covering_2.target.harmonic == 2
assert covering_11.target.harmonic == 11
assert covering_2.time_scale == 2
assert covering_11.time_scale == 11
```

So the candidate witnesses an exact finite boundary relation between modular multiplication and a continuum wave-equation covering. The equation does **not** select a privileged continuum lift, modulus, carrier, or physical meaning, and the representation itself is not yet ratified as selected UCNS geometry.

The full derivation and nonclaims are in `docs/modular-orbit-wave-trace.md`.

This trace is exact on the visible 360° boundary. It is **not yet** the complete native Möbius state; the frame-bearing lift required for 720° local return remains `hmmm`.

## Geometry modules

The active package also retains the Möbius vesica/seed family and the `prime_*` topological geometry family. Generated geometry certificates remain evidence; semantic receipts do not.

## Usage

```python
from fractions import Fraction
from ucns import public_gonol_function, native_mobius_state

w = public_gonol_function("w")
s0 = native_mobius_state(Fraction(0))
s360 = s0.advance(1)
s720 = s0.advance(2)

assert s360.visible_key == s0.visible_key
assert s360.complete_key != s0.complete_key
assert s720 == s0
```

## Build

```bash
python -m pip install uv==0.11.18
uv lock --check
uv sync --locked --python python --extra test --extra build
.venv/bin/python tools/verify_skill_lib_contracts.py .
env -u PYTHONPATH -u PYTHONHOME -u PYTEST_ADDOPTS -u PYTEST_PLUGINS \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python - <<'PY'
from pathlib import Path
from tools._boundary_pytest import run_suite
raise SystemExit(run_suite(["tests", "-c", "pyproject.toml", "--noconftest", "--strict-config"], Path.cwd()))
PY
.venv/bin/python -m build
.venv/bin/python -m twine check dist/*
.venv/bin/python tools/verify_distributions.py . dist
```

The independent interval checks also require system MPFR (for example,
`libmpfr6` on Ubuntu). Verification dependencies are locked; the isolated build
backend is pinned in `[build-system].requires`. Use a clean `dist` directory.

The wheel supplies the geometry package. Repository-context research replay and
the full tests require the source archive or checkout: run from its root, where
the archived preregistrations, generated evidence, and vendored parser live.
The distribution gate checks these inputs byte-for-byte; it does not recertify
their mathematical claims. It also binds wheel filename tags, dependencies, and flags to
`pyproject.toml`, verifies every RECORD digest, and requires the exact generated
sdist configuration. Both source PKG-INFO records and generated egg-info
dependency and file lists must agree with that same source configuration. Directory
entries are validated too; duplicate names and file/directory collisions fail.

Exact modular and trace records require immutable tuples with non-Boolean integer
residues; prefer the public builders. MPFR rational constructors accept only
integers or `Fraction`, and NaN cannot participate in interval ordering.

To replay both exact distribution files after the archive gate, with no editable
installation or source-path dependency:

```bash
bash tools/replay_distributions.sh . dist /tmp/ucns-replay python3.12
```

The output directory must be new and outside this checkout. The script exports
hash-locked dependencies, installs the wheel and sdist into separate clean
venvs, and runs all geometry tests against each installed package. Its receipt
records artifact hashes, Python versions, loaded package paths, test counts,
and zero skipped checks. It also binds a selected exact-input receipt executed
from the archived source, whose UCNS hashes must match both installed artifacts.
CI repeats this on Python 3.10, 3.11, and 3.12 against the exact PR head. Each
job retains its wheel, source archive, dependency export, test reports, selected
receipt, and replay receipt in `ucns-evidence-<python-version>`. The accompanying
`source.json` binds the Git commit/tree and runtimes. Download those bundles
from the workflow run and verify their artifact/receipt hashes and source maps
before accepting the chain; a successful Actions job alone is not acceptance.
The source archive includes this replay script and the exact build-tool pins.
The no-exec graph also reconciles both exact vendored reference parsers, with
local Python and TypeScript numeric-field/no-execution witnesses. The complete
repository evidence suite requires Node 24.15.0 for that TypeScript check; UCNS
library use remains Python-only. Parser ownership remains in skill-lib.
Unused skill helper tools remain canonical dependency material.

Receipt inventories hash every file under the bound `src`, `tools`, `tests`,
`docs`, `generated`, `.agents/skills`, and `.github/workflows` directories,
excluding `__pycache__`, plus the runner's declared root inputs. Text, binary,
and extensionless fixtures are included. Symlinks in bound inputs are unsupported
and fail before execution. Source archives retain the complete
package, test, tool, documentation, generated-evidence, skill, and CI trees;
the distribution gate rejects missing or altered inputs. Declared test-function
bindings must be unique. Test-helper modules receive the same collection-surface
audit, and the observer compares the actual test function code with its declared
source before and after the call. An imported replacement cannot stand in for
the original witness. Bound Python imports compile the inventoried source, and
pytest runs use fresh bytecode-cache locations; pre-existing caches cannot replace
those source imports. Snapshot failures during execution become explicit ERROR
outcomes, retain mutation evidence, and produce a not-passed receipt.

For a source-bound, selected-check receipt:

```bash
.venv/bin/python tools/run_skill_lib_boundaries.py . \
  --check check_boundary_runner_nonactivation --receipt /tmp/ucns-receipt.json
```

Receipt schema 2.1 rejects skips, expected failures, both forms of XPASS, absent
reports, and source changes during execution (including write-and-restore
through external hardlinks).
Receipt execution requires Linux inotify and readable procfs process identities;
unavailable instrumentation is an error before check execution. Descendant discovery
uses the task-children interface when available and otherwise reads procfs parent IDs.
Potential test definitions inside module or class control flow fail the declaration
audit closed; executable witnesses use direct module-level definitions.
The graph requires explicit `testpaths = ["tests"]` and
`collect_imported_tests = false`, with pytest 9.1 or later, and supports default pytest
file/class/function naming. Unrecognized configuration keys fail closed.
Repository-root helper imports outside the declared source layout fail the audit.
The complete-suite gate also requires every statically declared top-level test to
execute, so hiding a failing witness during collection cannot leave a passing gate.
Both full and selected execution also reconcile every collected pytest item,
including separate parameter invocations, against its actual call outcome.
Conftest files and local plugin registration are
outside this bounded collection contract. Changed settings, alternative pytest configuration
files, and collection-changing `addopts` fail closed. Root `pyproject.toml` is
parsed without executing tests; Python 3.10 uses the declared `tomli` test dependency.
Nested pytest configuration is rejected, and selected execution explicitly uses
the audited root config with conftest loading disabled. Collection-time execution
is limited to declarations, literal data, pytest decorators with literal arguments,
and read-only `Path(__file__)` source constants. Callable decorator options and
string skip/xfail conditions are unsupported. Compound annotations require
`from __future__ import annotations`. Indirect namespace mutation and unresolved calls, decorators,
or namespace protocols fail closed; setup work belongs in fixtures or checks.
Module/class pytest marks and pytest/xunit hooks are unsupported implicit execution. Class
data bindings must be literal values; imported descriptors, unresolved bases, nested classes, and compound class
namespace construction fail closed. Fixture helpers remain supported, including
test-prefixed helper names, but fixture-decorated functions cannot resolve CHECKS.
Imported or destructured `__test__` bindings are unresolved collection opt-outs and fail closed.
Class and base names must have unambiguous bindings; later rebinding cannot
stand in for the class used during construction.
CI runs the complete suite through the outcome observer: collection skips/errors,
runtime skips, xfail, XPASS, and empty execution fail the suite gate.
Source observation starts before capability probing. Executable Node version
probes use the same descendant supervisor as checks; a timeout or leaked child
cannot satisfy the capability. Source archives require owner-readable/writable
files and owner-readable/writable/searchable directories, without special mode bits.
Explicit archive directories must belong to the hierarchy of allowed files.
Receipt output must be outside the bound source tree and is written by atomic
replacement so an output hardlink cannot modify a bound input.
Checks import the bound checkout with ambient pytest plugins disabled and
PYTHONPATH replaced. An inherited startup hook makes ordinary Python descendants
prefer bound packages over their working directory. A separate supervisor uses Linux
child subreaping to terminate remaining descendants before observation ends;
leaked background work prevents acceptance. Timeout cleanup is outside the
pytest process, so replacing its signal handler cannot bypass descendant cleanup. Origin receipts observe the selected
pytest process. Explicit isolated/no-site interpreters and replaced child
environments do not inherit the import protocol. The observer instruments trusted
checks; it is not a sandbox for hostile test code. A `passed` receipt covers only its selected
checks; it does not select geometry, ratify candidates, or establish freshness.

`hmmm`: ratification of the modular-orbit / continuum-boundary-trace candidates, the complete higher-dimensional UCNS construction, the exact visible-circle wave-trace lift into the native Möbius carrier, any law selecting one continuum covering lift from a finite modular congruence class, and the exact geometric operation of every Public Gonol function position remain unresolved. Unresolved geometry stays unresolved; semantic machinery is not used to fill it.

Distribution replays hash the complete extracted tree before and after each full suite, reject persistent source changes, and retain the full source map. Each installed distribution inventory covers package files, dist-info payloads, and validated uv installer metadata/RECORD; imports remain separately witnessed. Check downloaded archives from their directory with `sha256sum -c ../replay/archives.sha256`. These checks establish execution provenance, not scientific ratification.

Standalone replay requires uv 0.11.18. It verifies the bootstrap version, synchronizes the verification environment from the hash-locked export, uses that environment’s uv for later installation, and retains both executable identities. Fixture source builds consume the same locked dependency export. Optimized Python mode is rejected before evidence can be produced.
