# ratios: loc_comments=81:81 imports_exports=17:3 calls_definitions=83:3
# === CHECKS ===
# id: check_distribution_replay_source_integrity
#   proves: ucns_distributions_replay_installed_code, ucns_distribution_evidence_binds_all_files
#   call: self::test_replay_source_changes_fail_closed
#   requires: python3, pytest
#   timeout: 10
#   mutates: temporary_path
#   cleanup: pytest temporary_path
#
# id: check_distribution_replay_installed_inventory
#   proves: ucns_distributions_replay_installed_code, ucns_distribution_evidence_binds_all_files
#   call: self::test_installed_distribution_inventory
#   requires: python3, pytest, uv
#   timeout: 30
#   mutates: temporary_path
#   cleanup: pytest temporary_path
#
# id: check_distribution_replay_source_install
#   proves: ucns_distributions_replay_installed_code, ucns_distribution_evidence_binds_all_files
#   call: self::test_sdist_installer_metadata_is_recorded
#   requires: python3, pytest, uv, build
#   timeout: 60
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===
"""Usage: pytest tests/test_distribution_replay.py. Exercise real installed files."""
import base64
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest

from tools._distribution_evidence import source_snapshot, verify_snapshot
from tools.verify_skill_lib_contracts import audit_repository


def test_replay_source_changes_fail_closed(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    for name in ("test_case.py", "helper.sh", "evidence.json", "extensionless"):
        (source / name).write_text("original")
    script = Path(__file__).resolve().parents[1] / "tools/replay_distributions.sh"
    for optimize in ("1", "2"):
        rejected = subprocess.run(["bash", str(script)], env=dict(os.environ, PYTHONOPTIMIZE=optimize), capture_output=True, text=True)
        assert rejected.returncode == 2 and "optimized Python mode" in rejected.stderr
    binary = tmp_path / "bin"
    binary.mkdir()
    fake_uv = binary / "uv"
    fake_uv.write_text("#!/bin/sh\nprintf '%s\\n' 'uv 0.11.17'\n")
    fake_uv.chmod(0o755)
    rejected = subprocess.run(["bash", str(script)], env=dict(os.environ, PYTHONOPTIMIZE="0", PATH=str(binary) + os.pathsep + os.environ["PATH"]), capture_output=True, text=True)
    assert rejected.returncode == 2 and "unsupported uv" in rejected.stderr
    baseline = source_snapshot(source)
    verify_snapshot(source, baseline)
    for name in baseline:
        path = source / name
        path.write_text("mutated")
        with pytest.raises(ValueError, match="archived source changed"):
            verify_snapshot(source, baseline)
        path.write_text("original")
    (source / "added").write_text("extra")
    with pytest.raises(ValueError, match="archived source changed"):
        verify_snapshot(source, baseline)
    (source / "added").unlink()
    (source / "link").symlink_to(source / "evidence.json")
    with pytest.raises(ValueError, match="symlink"):
        verify_snapshot(source, baseline)
    # A behavior-bearing shell contract must enter the no-exec graph.
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools/replay.sh").write_text("# === CONTRACTS ===\n# id: shell_unwitnessed\n#   given: replay inputs\n#   then: replay evidence\n# === END CONTRACTS ===\nexit 0\n")
    ok, gaps = audit_repository(tmp_path)
    assert not ok and any("shell_unwitnessed" in gap for gap in gaps), gaps


def test_installed_distribution_inventory(tmp_path):
    wheel = tmp_path / "ucns-0-py3-none-any.whl"
    info = "ucns-0.dist-info/"
    files = {"ucns/__init__.py": b"VALUE = 1\n", info + "METADATA": b"Metadata-Version: 2.1\nName: ucns\nVersion: 0\n", info + "WHEEL": b"Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n"}
    record = io.StringIO()
    writer = csv.writer(record)
    for name, payload in files.items():
        writer.writerow((name, "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).rstrip(b"=").decode(), len(payload)))
    writer.writerow((info + "RECORD", "", ""))
    files[info + "RECORD"] = record.getvalue().encode()
    with zipfile.ZipFile(wheel, "w") as archive:
        for name, payload in files.items():
            archive.writestr(name, payload)
    environment = tmp_path / "environment"
    subprocess.run(["uv", "venv", "--python", sys.executable, str(environment)], check=True, capture_output=True)
    python = environment / "bin/python"
    uri = wheel.as_uri() + "#sha256=" + hashlib.sha256(wheel.read_bytes()).hexdigest()
    subprocess.run(["uv", "pip", "install", "--python", str(python), "--no-deps", "ucns @ " + uri], check=True, capture_output=True)
    from tools import _distribution_evidence
    helper = str(Path(_distribution_evidence.__file__).resolve())
    script = """
import importlib.util, json, pathlib, sys
spec = importlib.util.spec_from_file_location('evidence', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
wheel = pathlib.Path(sys.argv[2])
report = module.installed_inventory(wheel, wheel)
print(json.dumps(report))
"""
    clean = {name: value for name, value in os.environ.items() if name not in {"PYTHONPATH", "PYTHONHOME", "UCNS_BOUND_SOURCE_ROOT"}}
    command = [str(python), "-c", script, helper, str(wheel)]
    initial = subprocess.run(command, env=clean, capture_output=True, text=True)
    assert initial.returncode == 0, initial.stderr
    report = json.loads(initial.stdout)
    assert info + "METADATA" in report["files_sha256"] and info + "direct_url.json" in report["installer_metadata"]
    site = next(environment.glob("lib/python*/site-packages"))
    for name in (info + "METADATA", info + "RECORD", info + "direct_url.json", "ucns/__init__.py"):
        path = site / name
        original = path.read_bytes()
        path.write_bytes(original + b"altered")
        assert subprocess.run(command, env=clean, capture_output=True).returncode != 0, name
        path.write_bytes(original)
    for name in (info + "unexpected", "ucns/unrecorded.txt"):
        path = site / name
        path.write_text("extra")
        assert subprocess.run(command, env=clean, capture_output=True).returncode != 0, name
        path.unlink()
    (site / (info + "METADATA")).unlink()
    assert subprocess.run(command, env=clean, capture_output=True).returncode != 0


def test_sdist_installer_metadata_is_recorded(tmp_path):
    source = tmp_path / "project"
    (source / "src/ucns").mkdir(parents=True)
    (source / "src/ucns/__init__.py").write_text("VALUE = 1\n")
    (source / "pyproject.toml").write_text('[build-system]\nrequires=["setuptools==84.0.0", "wheel==0.48.0"]\nbuild-backend="setuptools.build_meta"\n[project]\nname="ucns"\nversion="0"\n[tool.setuptools.packages.find]\nwhere=["src"]\n')
    dist = tmp_path / "dist"
    built = subprocess.run([sys.executable, "-m", "build", "--no-isolation", "--outdir", str(dist), str(source)], capture_output=True, text=True)
    assert built.returncode == 0, built.stdout + built.stderr
    wheel = next(dist.glob("*.whl"))
    artifact = next(dist.glob("*.tar.gz"))
    environment = tmp_path / "environment"
    subprocess.run(["uv", "venv", "--python", sys.executable, str(environment)], check=True, capture_output=True)
    python = environment / "bin/python"
    dependencies = tmp_path / "dependencies.txt"
    project = Path(__file__).resolve().parents[1]
    subprocess.run(["uv", "export", "--project", str(project), "--locked", "--extra", "test", "--extra", "build", "--no-emit-project", "--no-dev", "--format", "requirements.txt", "--output-file", str(dependencies)], check=True, capture_output=True)
    subprocess.run(["uv", "pip", "sync", "--python", str(python), "--require-hashes", str(dependencies)], check=True, capture_output=True)
    uri = artifact.as_uri() + "#sha256=" + hashlib.sha256(artifact.read_bytes()).hexdigest()
    result = subprocess.run(["uv", "pip", "install", "--python", str(python), "--no-deps", "--no-build-isolation", "ucns @ " + uri], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    from tools import _distribution_evidence
    script = """
import importlib.util, json, pathlib, sys
spec = importlib.util.spec_from_file_location('evidence', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(json.dumps(module.installed_inventory(pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]))))
"""
    clean = {name: value for name, value in os.environ.items() if name not in {"PYTHONPATH", "PYTHONHOME", "UCNS_BOUND_SOURCE_ROOT"}}
    command = [str(python), "-c", script, str(Path(_distribution_evidence.__file__).resolve()), str(wheel), str(artifact)]
    result = subprocess.run(command, env=clean, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    inventory = json.loads(result.stdout)
    name, = [name for name in inventory["installer_metadata"] if name.endswith("/uv_build.json")]
    assert json.loads(inventory["installer_metadata"][name]) == {}
    path = next(environment.glob("lib/python*/site-packages")) / name
    path.write_text('{"unexpected": true}')
    assert subprocess.run(command, env=clean, capture_output=True).returncode != 0
# ratios: loc_comments=81:81 imports_exports=17:3 calls_definitions=83:3
