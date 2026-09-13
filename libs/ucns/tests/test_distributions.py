# ratios: loc_comments=137:10 imports_exports=9:1 calls_definitions=50:2
# === CHECKS ===
# id: check_distribution_replay_inputs
#   proves: distributions_retain_exact_replay_inputs
#   call: self::test_distribution_replay_inputs_fail_closed
#   requires: python3, pytest
#   timeout: 10
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

"""Build small archive fixtures; missing evidence must fail independently of Twine."""

import base64
import csv
import hashlib
import io
from pathlib import Path
import tarfile
import zipfile

import pytest
from tools import verify_distributions as audit




def _archives(root, sdist, wheel, *, omit="", altered="", extra="", sdist_extra="", wheel_omit="", wheel_altered="", metadata_extra="", wheel_flags="true", record_mode="", sdist_directory="", wheel_directory="", sdist_root="ucns-0", sdist_mode=None, directory_mode=0o755, directory_payload=b""):
    core_metadata = "Metadata-Version: 2.4\nName: ucns\nVersion: 0\nSummary: Fixture\nAuthor: Test\nRequires-Python: >=3.10\nDescription-Content-Type: text/markdown\nLicense: fixture\nLicense-File: LICENSE\nDynamic: license-file\n"
    with tarfile.open(sdist, "w:gz") as archive:
        files = {**audit.expected_files(root), "setup.cfg": audit.GENERATED_SETUP_CFG,
                 "PKG-INFO": (core_metadata + "\nfixture\n").encode(),
                 "src/ucns.egg-info/PKG-INFO": (core_metadata + "\nfixture\n").encode(),
                 "src/ucns.egg-info/top_level.txt": b"ucns\n",
                 "src/ucns.egg-info/dependency_links.txt": b"\n",
                 "src/ucns.egg-info/requires.txt": b"",
                 "src/ucns.egg-info/SOURCES.txt": b""}
        if sdist_extra:
            files[sdist_extra] = b"unexpected"
        files["src/ucns.egg-info/SOURCES.txt"] = ("\n".join(sorted(files.keys() - {"PKG-INFO", "setup.cfg"})) + "\n").encode()
        for name, data in files.items():
            if name == omit:
                continue
            if name == altered:
                data += b"drift"
            member = tarfile.TarInfo(f"{sdist_root}/{name}")
            member.size = len(data)
            if name == "pyproject.toml" and sdist_mode is not None:
                member.mode = sdist_mode
            archive.addfile(member, io.BytesIO(data))
        if sdist_directory:
            member = tarfile.TarInfo(f"{sdist_root}/{sdist_directory}")
            member.type = tarfile.DIRTYPE
            member.mode = directory_mode
            member.size = len(directory_payload)
            archive.addfile(member, io.BytesIO(directory_payload))
    with zipfile.ZipFile(wheel, "w") as archive:
        files = {}
        for name, data in audit.expected_files(root).items():
            if name.startswith("src/ucns/"):
                files[name.removeprefix("src/")] = data
        metadata = {
            "METADATA": (core_metadata + metadata_extra + "\nfixture\n").encode(),
            "WHEEL": f"Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: {wheel_flags}\nTag: py3-none-any\n".encode(),
            "licenses/LICENSE": (root / "LICENSE").read_bytes(),
        }
        for name, data in metadata.items():
            if name != wheel_omit:
                files[f"ucns-0.dist-info/{name}"] = data + (b"drift" if name == wheel_altered else b"")
        if extra:
            files[extra] = b"unexpected"
        record = io.StringIO()
        writer = csv.writer(record)
        for name, data in files.items():
            digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
            writer.writerow((name, "sha256=" + digest, len(data)))
        writer.writerow(("ucns-0.dist-info/RECORD", "", ""))
        if wheel_omit != "RECORD":
            files["ucns-0.dist-info/RECORD"] = b"" if record_mode == "empty" else record.getvalue().encode()
        if record_mode == "wrong-hash":
            files["ucns/__init__.py"] += b"changed after recording"
        for name, data in files.items():
            archive.writestr(name, data)
        if wheel_directory:
            archive.writestr(wheel_directory.rstrip("/") + "/", directory_payload)


def test_distribution_replay_inputs_fail_closed(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    for name in (*audit.ROOT_INPUTS, "src/ucns/__init__.py", "generated/receipt.json", "docs/preregistration.md", "tests/witness.txt", "tools/helper.sh", ".github/workflows/ci.yml", "docs/extensionless", ".agents/skills/msdmd/parsers/universal.py"):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n")
    (root / "pyproject.toml").write_text('[project]\nname="ucns"\nversion="0"\ndescription="Fixture"\nrequires-python=">=3.10"\nauthors=[{name="Test"}]\nreadme="README.md"\n')
    outside = tmp_path / "outside"
    outside.mkdir()
    link = root / "tests/linked-fixture"
    link.symlink_to(outside)
    with pytest.raises(ValueError, match="unsupported source symlink"):
        audit.expected_files(root)
    link.unlink()
    sdist, wheel = tmp_path / "ucns-0.tar.gz", tmp_path / "ucns-0-py3-none-any.whl"
    _archives(root, sdist, wheel)
    assert audit.verify_distributions(root, sdist, wheel) == []
    for options, message in (
        ({"wheel_directory": "ucns", "directory_payload": b"unaccounted"}, "nonempty archive directory"),
        ({"sdist_directory": "tests", "directory_payload": b"unaccounted"}, "nonempty archive directory"),
        ({"wheel_directory": "unexpected"}, "unexpected directory"),
        ({"sdist_directory": "unexpected"}, "unexpected directory"),
        ({"sdist_mode": 0}, "unusable sdist permissions"),
        ({"sdist_mode": 0o400}, "unusable sdist permissions"),
        ({"sdist_mode": 0o4644}, "unusable sdist permissions"),
        ({"sdist_directory": "extra", "directory_mode": 0o644}, "unusable sdist permissions"),
        ({"wheel_directory": "evil-1.dist-info"}, "exactly one .dist-info directory"),
        ({"omit": "LICENSE"}, "missing LICENSE"),
        ({"altered": "LICENSE"}, "altered LICENSE"),
        ({"wheel_omit": "licenses/LICENSE"}, "missing wheel metadata"),
        ({"wheel_altered": "licenses/LICENSE"}, "altered wheel license"),
        ({"wheel_omit": "METADATA"}, "missing wheel metadata"),
        ({"wheel_omit": "WHEEL"}, "missing wheel metadata"),
        ({"wheel_omit": "RECORD"}, "missing wheel metadata"),
        ({"sdist_extra": "setup.py"}, "unexpected payload setup.py"),
        ({"sdist_extra": "setup.cfg"}, "altered generated setup.cfg"),
        ({"sdist_extra": "PKG-INFO"}, "sdist PKG-INFO Name differs"),
        ({"sdist_extra": "src/ucns.egg-info/PKG-INFO"}, "sdist src/ucns.egg-info/PKG-INFO Name differs"),
        ({"omit": "PKG-INFO"}, "missing sdist metadata PKG-INFO"),
        ({"omit": "src/ucns.egg-info/PKG-INFO"}, "missing sdist metadata src/ucns.egg-info/PKG-INFO"),
        ({"sdist_extra": "src/ucns.egg-info/requires.txt"}, "requires.txt differs"),
        ({"altered": "src/ucns.egg-info/SOURCES.txt"}, "SOURCES.txt differs"),
        ({"omit": "setup.cfg"}, "missing generated setup.cfg"),
        ({"metadata_extra": "Requires-Dist: unexpected>=1\n"}, "Requires-Dist differs"),
        ({"wheel_flags": "false"}, "Root-Is-Purelib differs"),
        ({"record_mode": "empty"}, "RECORD missing path"),
        ({"record_mode": "wrong-hash"}, "RECORD digest or size mismatch"),
        ({"sdist_root": "other-99"}, "sdist root identity"),
        ({"sdist_directory": "pyproject.toml"}, "duplicate archive member"),
        ({"wheel_directory": "ucns/__init__.py"}, "duplicate archive member"),
        ({"sdist_directory": "../escaped"}, "unsafe archive name"),
        ({"extra": "ucns/__init__.py/inside.py"}, "file/directory archive collision"),
        ({"extra": "ucns-0.dist-info/entry_points.txt"}, "unexpected wheel metadata"),
    ):
        _archives(root, sdist, wheel, **options)
        assert any(message in problem for problem in audit.verify_distributions(root, sdist, wheel)), options
    for key, name, expected in (("omit", "tests/witness.txt", "missing"), ("altered", "docs/extensionless", "altered"), ("omit", ".github/workflows/ci.yml", "missing"), ("omit", "generated/receipt.json", "missing"), ("altered", "docs/preregistration.md", "altered"), ("extra", "ucns/lexical.py", "unexpected")):
        _archives(root, sdist, wheel, **{key: name})
        assert any(expected in problem for problem in audit.verify_distributions(root, sdist, wheel))
    _archives(root, sdist, wheel, extra="../escaped.py")
    assert any("unsafe" in problem for problem in audit.verify_distributions(root, sdist, wheel))
    _archives(root, sdist, wheel)
    renamed = wheel.with_name("ucns-0-cp310-cp310-manylinux_2_17_x86_64.whl")
    wheel.rename(renamed)
    assert any("filename identity or tags" in problem for problem in audit.verify_distributions(root, sdist, renamed))
    renamed.rename(wheel)
    with zipfile.ZipFile(wheel, "a") as archive, pytest.warns(UserWarning, match="Duplicate"):
        archive.writestr("ucns/__init__.py", b"duplicate")
    assert any("duplicate" in problem for problem in audit.verify_distributions(root, sdist, wheel))
# ratios: loc_comments=137:10 imports_exports=9:1 calls_definitions=50:2
