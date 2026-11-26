# ratios: loc_comments=69:6 imports_exports=5:3 calls_definitions=31:3
# === CHECKS ===
# id: check_ucns_source_tree_rejects_historical_overlay
#   proves: ucns_package_matches_pinned_source
#   call: self::test_gate_rejects_each_audited_fault
# === END CHECKS ===
"""Replay the Stack import history and challenge the package gate in a temporary clone."""

import hashlib
import json
import subprocess
from pathlib import Path

from tools import check_stack_consistency as consistency


ROOT = Path(__file__).resolve().parents[4]
SOURCE = "libs/ucns/src/ucns"
RECEIPT = ROOT / "research/ucns/receipts/ahbg-standing-wave-provenance-v1.json"


def git(root, *args):
    return subprocess.check_output(["git", "-C", root, *args])


def test_historical_imports_and_clean_package_identity():
    record = json.loads(RECEIPT.read_bytes())
    history = record["stack_history"]
    parent = history["pre_overlay_commit"]
    overlay = history["overlay_commit"]
    assert git(ROOT, "rev-parse", f"{overlay}^").decode().strip() == parent
    tree = git(ROOT, "rev-parse", f"{parent}:{SOURCE}").decode().strip()
    assert tree == record["upstream"]["package_git_tree"]
    manifest = json.loads(git(ROOT, "show", f"{parent}:stack-manifest.json"))
    producer = next(r for r in manifest["repositories"] if r["repository"] == record["upstream"]["repository"])
    assert producer["commit"] == record["upstream"]["commit"]

    old = {row["module"]: row for row in record["historical_imports"]}
    clean = {row["module"]: row for row in record["corrected_imports"]}
    assert len(old) == len(record["historical_imports"]) == 9
    assert len(clean) == len(record["corrected_imports"]) == 7
    assert old.keys() - clean.keys() == {"ucns.mobius_standing_wave", "ucns.mobius_band_standing_wave"}
    assert clean.keys() <= old.keys()
    for name, row in old.items():
        path = row["path"]
        data = git(ROOT, "show", f"{overlay}:{path}")
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
        assert consistency.git_blob_sha(data) == row["git_blob"]
        if name in clean:
            assert path == "libs/ucns/" + clean[name]["upstream_path"]
            source = git(ROOT, "show", f"{parent}:{path}")
            assert hashlib.sha256(source).hexdigest() == clean[name]["sha256"]
            assert row["origin"] == ("stack_modified_facade" if name == "ucns" else "upstream")
            assert (data != source) == (name == "ucns")
        else:
            assert git(ROOT, "ls-tree", parent, "--", path) == b""
            assert row["origin"] == "stack_candidate"
            assert (ROOT / row["research_path"]).is_file()


def test_gate_rejects_each_audited_fault(tmp_path, monkeypatch):
    record = json.loads(RECEIPT.read_bytes())
    source = record["upstream"]
    repositories = {source["repository"]: source}
    history = record["stack_history"]
    git(ROOT, "clone", "--quiet", "--shared", "--no-checkout", str(ROOT), str(tmp_path))
    git(tmp_path, "checkout", history["pre_overlay_commit"], "--", SOURCE)
    monkeypatch.setattr(consistency, "ROOT", tmp_path)
    findings = []
    consistency.check_ucns_package(repositories, findings)
    assert findings == []

    for row in record["historical_imports"]:
        if row["origin"] == "upstream":
            continue
        path = tmp_path / row["path"]
        original = path.read_bytes() if path.exists() else None
        path.write_bytes(git(ROOT, "show", f"{history['overlay_commit']}:{row['path']}"))
        findings = []
        consistency.check_ucns_package(repositories, findings)
        assert len(findings) == 1 and path.name in findings[0], findings
        if original is None:
            path.unlink()
        else:
            path.write_bytes(original)
    findings = []
    consistency.check_ucns_package(repositories, findings)
    assert findings == []
# ratios: loc_comments=69:6 imports_exports=5:3 calls_definitions=31:3
