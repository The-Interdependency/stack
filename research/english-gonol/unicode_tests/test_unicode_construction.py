# === CHECKS ===
# id: uchc_unicode_ascii_width_check
#   proves: uchc_unicode_native_width
#   call: self::test_ascii_has_three_leading_zero_bytes
#   requires: python3, pytest, pinned_ucns
#   timeout: 60
#   mutates: none
#   cleanup: none
# id: uchc_unicode_scalar_transport_check
#   proves: uchc_unicode_lossless_transport
#   call: self::test_exact_scalar_transport_preserves_full_text
#   requires: python3, pytest, pinned_ucns
#   timeout: 60
#   mutates: none
#   cleanup: none
# id: uchc_unicode_invalid_transport_check
#   proves: uchc_unicode_lossless_transport
#   call: self::test_invalid_width_and_scalar_refuse
#   requires: python3, pytest, pinned_ucns
#   timeout: 60
#   mutates: none
#   cleanup: none
# id: uchc_unicode_drift_check
#   proves: uchc_unicode_native_integrity
#   call: self::test_native_source_is_verified_before_execution
#   requires: python3, pytest, pinned_ucns
#   timeout: 60
#   mutates: filesystem
#   cleanup: tmp_path
# id: uchc_unicode_cli_check
#   proves: uchc_unicode_native_width
#   call: self::test_cli_exposes_native_frame_and_producer
#   requires: python3, pytest, pinned_ucns
#   timeout: 60
#   mutates: none
#   cleanup: none
# id: uchc_unicode_graph_check
#   proves: uchc_unicode_native_integrity
#   call: self::test_work_graph_binds_native_source
#   requires: python3, pytest, pinned_ucns
#   timeout: 60
#   mutates: none
#   cleanup: none
# === END CHECKS ===
from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from english_gonol import unicode_construction as consumer


@pytest.fixture
def native_root():
    root = Path(os.environ["UCHC_UNICODE_UCNS_ROOT"])
    assert (root / consumer.UCNS_SOURCE).is_file()
    return root


def test_ascii_has_three_leading_zero_bytes(native_root):
    for value in range(128):
        glyph = consumer.construct_glyph(chr(value), ucns_source_root=native_root)
        assert (glyph.bit_radius, glyph.bit_diameter) == (16, 32)
        assert glyph.utf32_be == b"\x00\x00\x00" + bytes((value,))
        assert glyph.utf8 == bytes((value,))
        assert glyph.__class__.__module__.startswith("_uchc_unicode_native_")


def test_exact_scalar_transport_preserves_full_text(native_root):
    text = "\ufeffAë𐍈e\u0308\x00 A" * 30
    encoded = consumer.encode_text(text, ucns_source_root=native_root)
    assert encoded == text.encode("utf-32-be")
    assert len(encoded) == len(text) * 4
    assert consumer.decode_text(encoded, ucns_source_root=native_root) == text
    frame = consumer.construct_text(text, ucns_source_root=native_root,
                                    placement_radius=Fraction(7, 3))
    assert frame.recover() == text
    assert frame.utf8 == text.encode("utf-8")
    assert all(g.bit_radius == 16 for g in frame.glyphs)
    assert all(p.radius == Fraction(7, 3) for p in frame.placements)
    assert frame.glyphs[2].utf32_be == bytes.fromhex("000000EB")


@pytest.mark.parametrize("data", [b"", b"A", bytes(3), bytes(5),
                                  bytes.fromhex("0000D800"),
                                  bytes.fromhex("00110000")])
def test_invalid_width_and_scalar_refuse(native_root, data):
    with pytest.raises(ValueError):
        consumer.decode_text(data, ucns_source_root=native_root)


def test_native_source_is_verified_before_execution(tmp_path):
    path = tmp_path / consumer.UCNS_SOURCE
    path.parent.mkdir(parents=True)
    marker = tmp_path / "executed"
    path.write_text(f"from pathlib import Path\nPath({str(marker)!r}).touch()\n")
    with pytest.raises(ValueError, match="UCNS_UNICODE_PRODUCER_DRIFT"):
        consumer.construct_glyph("A", ucns_source_root=tmp_path)
    assert not marker.exists()


def test_cli_exposes_native_frame_and_producer(native_root):
    result = subprocess.run([sys.executable, "-m", "english_gonol.unicode_construction",
                             "Aë𐍈", "--ucns-source-root", str(native_root)],
                            cwd=Path(__file__).resolve().parents[1], text=True,
                            capture_output=True, check=True)
    record = json.loads(result.stdout)
    assert record["geometry_authority"] == consumer.authority()
    assert record["frame"]["utf32_be_hex"] == "00000041000000EB00010348"
    assert record["frame"]["glyph_bit_radius"] == 16


def test_work_graph_binds_native_source(native_root):
    path = Path(__file__).resolve().parents[1] / "docs/unicode-bit-radius-work-graph.json"
    graph = json.loads(path.read_text())
    payload = {key: graph[key] for key in ("repositories", "boundaries")}
    expected = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert graph["work_graph_sha256"] == expected
    native = next(p for p in graph["repositories"] if p["repository"] == "The-Interdependency/ucns")
    assert native["commit"] == consumer.UCNS_COMMIT
    assert re.fullmatch(r"[0-9a-f]{40}", native["commit"])
    assert sha256((native_root / consumer.UCNS_SOURCE).read_bytes()).hexdigest() == consumer.UCNS_SOURCE_SHA256
    workspace = Path(__file__).resolve().parents[1]
    base = json.loads((workspace / "BASE.json").read_text())
    assert base["unicode_bit_radius"]["native_commit"] == native["commit"]
    workflow = (workspace.parents[1] / ".github/workflows/uchc-unicode-bit-radius.yml").read_text()
    assert "ref: " + native["commit"] in workflow
