from __future__ import annotations

# === CHECKS ===
# id: check_msdmd_generated_current
#   proves: metapat_msdmd_generated
#   call: self::test_committed_msdmd_is_current
#   mutates: filesystem_read
#   cleanup: none
#
# id: check_msdmd_scope_bounded
#   proves: metapat_msdmd_scope_bounded
#   call: self::test_collection_excludes_vendored_skills
#   mutates: tempdir
#   cleanup: tempdir_teardown
# === END CHECKS ===

import json
from pathlib import Path

from tools.generate_msdmd import render_collection

REPO_ROOT = Path(__file__).resolve().parents[1]


def _payload(rendered: str) -> dict:
    prefix = "export default defineMsdmdCollection("
    start = rendered.index(prefix) + len(prefix)
    end = rendered.rindex(");")
    return json.loads(rendered[start:end])


def test_committed_msdmd_is_current() -> None:
    expected = render_collection(REPO_ROOT)
    actual = (REPO_ROOT / "metapat_msdmd.ts").read_text(encoding="utf-8")
    assert actual == expected


def test_collection_excludes_vendored_skills() -> None:
    collection = _payload(render_collection(REPO_ROOT))
    files = {item["file"] for item in collection["declarations"]}
    assert files
    assert all(not path.startswith(".agents/") for path in files)
    assert any(path.startswith("src/metapat/") for path in files)
    assert any(path.startswith("tests/") for path in files)
    assert any(path.startswith("tools/") for path in files)
