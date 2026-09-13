#!/usr/bin/env bash
# === MODULE_BUILD ===
# id: ucns_distribution_replay
#   module_name: replay_distributions
#   module_kind: instrument
#   summary: runs the complete geometry suite against clean wheel and sdist installations
#   owner: Erin Spencer
#   public_surface: bash tools/replay_distributions.sh ROOT DIST OUTPUT PYTHON
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: write
#   storage_notes: new caller-selected output directory and uv cache
#   network_boundary: external
#   network_notes: locked Python build/test dependencies
#   user_data_boundary: none
#   admin_only: false
#   tests: full geometry suite under both installed artifacts
#   rollout: CI on Python 3.10, 3.11, and 3.12
#   rollback: remove the replay CI step
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: ucns_distributions_replay_installed_code
#   given: archives match the source inputs and dependencies resolve from the lock
#   then: each artifact installs without editable source and every geometry test passes without skips while ucns resolves inside its clean environment
#   class: evidence
# === END CONTRACTS ===

# Usage: bash tools/replay_distributions.sh . dist /tmp/ucns-replay python3.12
# OUTPUT must not exist and must be outside ROOT. Receipts cover packaging and
# executed tests, never candidate ratification or historical expensive replay.
set -euo pipefail
case "${PYTHONOPTIMIZE-}" in ""|0) ;; *) echo 'optimized Python mode cannot produce replay evidence' >&2; exit 2;; esac
bootstrap_uv=$(command -v uv)
test -f "$bootstrap_uv"
bootstrap_version=$("$bootstrap_uv" --version)
uv_pattern='^uv 0[.]11[.]18( \([a-z0-9_-]+\))?$'
if [[ ! "$bootstrap_version" =~ $uv_pattern ]]; then echo "unsupported uv: $bootstrap_version" >&2; exit 2; fi
bootstrap_sha=$(sha256sum "$bootstrap_uv"); bootstrap_sha=${bootstrap_sha%% *}
repo=$(realpath "$1")
dist=$(realpath "$2")
output=$(realpath -m "$3")
runtime=${4:-python3}
case "$output/" in "$repo/"*) echo 'OUTPUT must be outside source' >&2; exit 2;; esac
test ! -e "$output"
mkdir -p "$output"
"$bootstrap_uv" export --project "$repo" --locked --extra test --extra build --no-emit-project --no-dev --format requirements.txt --output-file "$output/dependencies.txt" >/dev/null
"$bootstrap_uv" venv --python "$runtime" "$output/verification-venv"
"$bootstrap_uv" pip sync --python "$output/verification-venv/bin/python" --require-hashes "$output/dependencies.txt"
installer_uv="$output/verification-venv/bin/uv"
installer_version=$("$installer_uv" --version)
if [[ ! "$installer_version" =~ $uv_pattern ]]; then echo 'locked uv version mismatch' >&2; exit 2; fi
installer_sha=$(sha256sum "$installer_uv"); installer_sha=${installer_sha%% *}
"$output/verification-venv/bin/python" "$repo/tools/verify_distributions.py" "$repo" "$dist"
(cd "$dist"; sha256sum ./*.whl ./*.tar.gz) > "$output/archives.sha256"
mkdir "$output/source"
tar -xzf "$dist"/*.tar.gz -C "$output/source"
source_root=$(find "$output/source" -mindepth 1 -maxdepth 1 -type d)
snapshot_tool="$repo/tools/_distribution_evidence.py"
"$output/verification-venv/bin/python" "$snapshot_tool" snapshot "$source_root" "$output/source-snapshot.json"
for kind in wheel sdist; do
  "$output/verification-venv/bin/python" "$snapshot_tool" verify-snapshot "$source_root" "$output/source-snapshot.json"
  environment="$output/$kind-venv"
  "$installer_uv" venv --python "$runtime" "$environment"
  "$installer_uv" pip sync --python "$environment/bin/python" --require-hashes "$output/dependencies.txt"
  if [ "$kind" = wheel ]; then artifact=("$dist"/*.whl); else artifact=("$dist"/*.tar.gz); fi
  artifact_uri=$("$output/verification-venv/bin/python" - "${artifact[0]}" <<'PYTHON'
import hashlib
from pathlib import Path
import sys
if sys.flags.optimize:
    raise SystemExit("optimized Python mode cannot produce replay evidence")
artifact = Path(sys.argv[1])
print(artifact.as_uri() + "#sha256=" + hashlib.sha256(artifact.read_bytes()).hexdigest())
PYTHON
  )
  "$installer_uv" pip install --python "$environment/bin/python" --no-deps --no-build-isolation "ucns @ $artifact_uri"
  (
    cd "$source_root"
    env -u PYTHONPATH -u PYTHONHOME -u PYTEST_ADDOPTS -u PYTEST_PLUGINS PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX="$output/$kind-bytecode" PATH="$environment/bin:$PATH" \
      "$environment/bin/python" - "$output/$kind.xml" "$output/$kind-import.json" "$dist"/*.whl "${artifact[0]}" <<'PY'
import hashlib
import json
from pathlib import Path
import sys
if sys.flags.optimize:
    raise SystemExit("optimized Python mode cannot produce replay evidence")
import xml.etree.ElementTree as ET
import ucns
from tools._boundary_pytest import run_suite
from tools._distribution_evidence import installed_inventory

installed = Path(ucns.__file__).resolve()
assert installed.is_relative_to(Path(sys.prefix)), installed
initial = installed.read_bytes()
expected = {p.relative_to(Path("src")).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in Path("src/ucns").rglob("*") if p.is_file() and "__pycache__" not in p.parts}
def installed_sources():
    entries = tuple(installed.parent.rglob("*"))
    assert not any(path.is_symlink() for path in entries), "installed package contains a symlink"
    return {"ucns/" + p.relative_to(installed.parent).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in entries if p.is_file() and "__pycache__" not in p.parts}
assert installed_sources() == expected
distribution_before = installed_inventory(Path(sys.argv[3]), Path(sys.argv[4]))
result = run_suite(["tests", "-p", "no:cacheprovider", "-c", "pyproject.toml", "--noconftest", "--strict-config", "--junitxml=" + sys.argv[1]], Path.cwd())
assert result == 0, result
assert Path(ucns.__file__).resolve() == installed
assert installed.read_bytes() == initial
assert installed_sources() == expected
assert installed_inventory(Path(sys.argv[3]), Path(sys.argv[4])) == distribution_before
origins = {name: str(Path(module.__file__).resolve()) for name, module in sys.modules.items() if (name == "ucns" or name.startswith("ucns.")) and getattr(module, "__file__", None)}
assert all(Path(path).is_relative_to(installed.parent) for path in origins.values()), origins
cases = list(ET.parse(sys.argv[1]).getroot().iter("testcase"))
assert cases and not any(c.find("skipped") is not None or c.find("failure") is not None or c.find("error") is not None for c in cases)
Path(sys.argv[2]).write_text(json.dumps({"python": sys.version, "ucns_path": str(installed), "ucns_init_sha256": hashlib.sha256(initial).hexdigest(), "installed_source_sha256": expected, "installed_distribution": distribution_before, "imported_origins": origins, "tests": len(cases), "skips": 0, "status": "passed"}, indent=2) + "\n")
PY
  )
  "$output/verification-venv/bin/python" "$snapshot_tool" verify-snapshot "$source_root" "$output/source-snapshot.json"
done
# This receipt executes the exact source archived above. Installed wheel/sdist
# execution is separately witnessed by the two complete suites and source maps.
env -u PYTHONPATH -u PYTHONHOME -u PYTEST_ADDOPTS -u PYTEST_PLUGINS PYTHONDONTWRITEBYTECODE=1 PATH="$output/verification-venv/bin:$PATH" \
  "$output/verification-venv/bin/python" "$source_root/tools/run_skill_lib_boundaries.py" "$source_root" \
  --check check_modular_orbit_fails_closed \
  --check check_gonal_boundary_trace_fails_closed_on_incompatible_geometry \
  --check check_mpfr_nan_is_not_ordered_evidence \
  --check check_mpfr_exact_rational_admission \
  --check check_boundary_runner_nonactivation --receipt "$output/exact-input-receipt.json"
(cd "$dist"; sha256sum -c "$output/archives.sha256")
"$output/verification-venv/bin/python" "$snapshot_tool" verify-snapshot "$source_root" "$output/source-snapshot.json"
"$output/verification-venv/bin/python" "$repo/tools/verify_distributions.py" "$repo" "$dist"
test "$(sha256sum "$bootstrap_uv" | cut -d ' ' -f 1)" = "$bootstrap_sha"
test "$(sha256sum "$installer_uv" | cut -d ' ' -f 1)" = "$installer_sha"
"$output/verification-venv/bin/python" - "$dist" "$output" "$bootstrap_version" "$bootstrap_sha" "$installer_version" "$installer_sha" <<'PY'
import hashlib
import json
from pathlib import Path
import sys
if sys.flags.optimize:
    raise SystemExit("optimized Python mode cannot produce replay evidence")
dist, out = map(Path, sys.argv[1:3])
boundary = json.loads((out / "exact-input-receipt.json").read_text())
assert boundary["status"] == "passed" and boundary["source_unchanged"] and boundary["snapshot_errors"] == []
for kind in ("wheel", "sdist"):
    installed = json.loads((out / (kind + "-import.json")).read_text())["installed_source_sha256"]
    assert all(boundary["source_files_sha256"]["src/" + name] == digest for name, digest in installed.items())
receipt = {"uv_identity": {"bootstrap": {"version": sys.argv[3], "sha256": sys.argv[4]}, "installer": {"version": sys.argv[5], "sha256": sys.argv[6]}}, "schema": "ucns.distribution-replay", "version": "1.0.0", "status": "passed", "artifacts_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dist.iterdir()) if p.suffix == ".whl" or p.name.endswith(".tar.gz")}, "runs": {kind: json.loads((out / (kind + "-import.json")).read_text()) for kind in ("wheel", "sdist")}, "dependency_export_sha256": hashlib.sha256((out / "dependencies.txt").read_bytes()).hexdigest(), "candidate_ratification": "none", "exact_input_receipt_sha256": hashlib.sha256((out / "exact-input-receipt.json").read_bytes()).hexdigest(), "exact_input_receipt_identity": boundary["receipt_sha256"], "full_replay_source_sha256": json.loads((out / "source-snapshot.json").read_text()), "exact_input_source_boundary": "archived source; installed artifact execution witnessed separately above"}
(out / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
print(json.dumps(receipt, indent=2))
PY
