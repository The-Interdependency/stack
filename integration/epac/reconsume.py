"""Usage: python integration/epac/reconsume.py RELEASE_LOCK NEW_OUTPUT PYTHON.

Download hash-bound public EPAC assets, install locked dependencies and the wheel
in a new environment, and invoke the stack integration gate. The lock must have
release_tag, source_commit, assets{name:{url,sha256}}, and phase fields. No source
or authority record is changed by this command.
"""
# === MODULE_BUILD ===
# id: stack_epac_public_reconsumption
#   module_name: reconsume
#   module_kind: instrument
#   summary: downloads exact public EPAC bytes and replays stack composition in a clean environment
#   owner: The Interdependency
#   public_surface: command-line release reconsumption
#   internal_surface: main
#   auth_boundary: none
#   auth_notes: public HTTPS downloads
#   storage_boundary: write
#   storage_notes: new caller-selected output directory
#   network_boundary: external
#   network_notes: public release assets and locked Python dependencies
#   user_data_boundary: none
#   admin_only: false
#   tests: executed against the immutable EPAC release before authority transition
#   rollout: replaces forge-local EPAC workflow after successful graduation
#   rollback: retain previous artifact lock; do not restore scientific standing
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: epac_reconsumption_binds_public_bytes
#   given: a release lock with exact source and artifact hashes
#   then: downloaded assets must match the lock and release manifest before installation and public-interface verification
#   class: provenance
# === END CONTRACTS ===
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
from urllib.parse import urlsplit
from urllib.request import urlopen


def main() -> None:
    lock_path, output = (Path(argument).resolve() for argument in sys.argv[1:3])
    runtime = sys.argv[3]
    child_env = {key: value for key, value in os.environ.items()
                 if key not in {"PYTHONPATH", "PYTHONHOME", "PYTEST_ADDOPTS", "PYTEST_PLUGINS"}}
    child_env["PYTHONDONTWRITEBYTECODE"] = "1"
    child_env["PYTHONNOUSERSITE"] = "1"
    stack = Path(__file__).resolve().parents[2]
    if output.exists() or output.is_relative_to(stack):
        raise ValueError("output must be new and outside stack")
    lock = json.loads(lock_path.read_text())
    if lock["phase"] not in {"reconsumed", "graduated"}:
        raise ValueError("public reconsumption phase required")
    output.mkdir(parents=True)
    assets = lock["assets"]
    for name, identity in assets.items():
        if Path(name).name != name or name in {"", ".", ".."}:
            raise ValueError("asset must be a plain filename")
        expected_url = f'https://github.com/The-Interdependency/epac/releases/download/{lock["release_tag"]}/{name}'
        if identity["url"] != expected_url or urlsplit(expected_url).scheme != "https":
            raise ValueError("unexpected release asset URL")
        with urlopen(identity["url"], timeout=60) as response:
            payload = response.read()
        if hashlib.sha256(payload).hexdigest() != identity["sha256"]:
            raise ValueError(f"public artifact digest mismatch: {name}")
        (output / name).write_bytes(payload)
    manifest = json.loads((output / "release-manifest.json").read_text())
    if manifest["source_commit"] != lock["source_commit"]:
        raise ValueError("public source identity mismatch")
    for name, digest in manifest["artifacts_sha256"].items():
        if assets[name]["sha256"] != digest:
            raise ValueError("release manifest differs from pinned artifact identity")
    wheels, sdists = list(output.glob("*.whl")), list(output.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ValueError("exactly one wheel and source archive required")
    source = output / "source"
    source.mkdir()
    with tarfile.open(sdists[0]) as archive:
        seen = set()
        for member in archive:
            name = Path(member.name)
            if name.is_absolute() or ".." in name.parts or not (member.isfile() or member.isdir()) or member.name in seen:
                raise ValueError("unsafe source archive")
            seen.add(member.name)
        archive.extractall(source)
    roots = list(source.iterdir())
    if len(roots) != 1 or not roots[0].is_dir():
        raise ValueError("source archive root mismatch")
    source_root = roots[0]
    requirements = output / "dependencies.txt"
    subprocess.run(["uv", "export", "--project", str(source_root), "--locked", "--no-emit-project", "--no-dev", "--format", "requirements.txt", "--output-file", str(requirements)], check=True, env=child_env)
    environment = output / "venv"
    subprocess.run(["uv", "venv", "--python", runtime, str(environment)], check=True, env=child_env)
    python = str(environment / "bin/python")
    subprocess.run(["uv", "pip", "sync", "--python", python, "--require-hashes", str(requirements)], check=True, env=child_env)
    subprocess.run(["uv", "pip", "install", "--python", python, "--no-deps", str(wheels[0])], check=True, env=child_env)
    subprocess.run([python, str(stack / "integration/epac/verify_release.py"), str(wheels[0]), str(output / "consumption.json"), "--phase", lock["phase"]], check=True, cwd=output, env=child_env)
    (output / "release-lock.json").write_bytes(lock_path.read_bytes())


if __name__ == "__main__":
    main()
