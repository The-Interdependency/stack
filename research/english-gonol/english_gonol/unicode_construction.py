# ratios: loc_comments=57:41 imports_exports=8:6 calls_definitions=25:8
# === MODULE_BUILD ===
# id: uchc_unicode_bit_radius_consumer
#   module_name: unicode_construction
#   module_kind: adapter
#   summary: UCHC scalar and text entrypoint consuming exact UCNS 16-bit-radius big-endian gonols
#   owner: Erin Spencer
#   public_surface: construct_glyph, construct_text, encode_text, decode_text, authority, main
#   auth_boundary: exact caller-supplied UCNS source bytes are verified before execution; integrity is not authentication
#   storage_boundary: reads one explicit native source file; constructed objects remain caller-owned
#   network_boundary: none
#   user_data_boundary: caller text remains local
#   admin_only: false
#   tests: unicode_tests/test_unicode_construction.py
#   rollout: forward Unicode entrypoint; historical corpus receipts retain exact producers
#   rollback: revert this entrypoint and its pin as one change
#   requires: unicode_gonol_geometry
#   unresolved: higher-scale affixiation and closed-word bearings; corpus migration and UCHC package extraction
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: uchc_unicode_native_width
#   given: exact Unicode text and the pinned native source
#   then: all glyphs are native UCNS objects with bit radius 16, bit diameter 32 and big-endian scalar bytes; exact UTF-8 anatomy is retained
# id: uchc_unicode_lossless_transport
#   given: arbitrary admitted scalar sequences including nulls, repeated scalars and supplementary-plane scalars
#   then: big-endian transport and recovery preserve all source occurrences and reject invalid widths or scalar values
# id: uchc_unicode_native_integrity
#   given: missing or changed native source bytes
#   then: fail before executing that source rather than guessing geometry or accepting an ambient installation
# === END CONTRACTS ===
"""UCHC's forward 16 b rad / 32-bit big-endian scalar entrypoint.

GPT generated; context, prompt Erin Spencer.

Usage::

    python -m english_gonol.unicode_construction 'Aë𐍈' --ucns-source-root /path/to/ucns

UCNS owns every returned gonol, bearing, bit representation and frame. This
adapter admits exact scalar text without normalizing or splitting it. A text
frame preserves its constituents; it does not supply closed-word bearings or
complete the separate corpus migration. No network access occurs at runtime.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import sys
from types import ModuleType

UCNS_COMMIT = "0600a23e27af83d06157ee6ca66644dbff613d2a"
UCNS_SOURCE = "src/ucns/unicode_gonol.py"
UCNS_SOURCE_SHA256 = "302cdb12a1314b21a54a84e4263ec7da498b27c3ec3d82758e2b726a90e2252a"
PROFILE = "uchc.unicode-bit-radius/1"


@lru_cache(maxsize=1)
def _load_native(source: bytes) -> ModuleType:
    # Execute the bytes already verified, never reread a mutable source path.
    name = "_uchc_unicode_native_" + UCNS_SOURCE_SHA256
    module = ModuleType(name)
    module.__file__ = UCNS_SOURCE
    sys.modules[name] = module  # Required by stdlib dataclass annotation lookup.
    try:
        exec(compile(source, UCNS_SOURCE, "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def _native(ucns_source_root):
    source = (Path(ucns_source_root) / UCNS_SOURCE).read_bytes()
    if sha256(source).hexdigest() != UCNS_SOURCE_SHA256:
        raise ValueError("UCNS_UNICODE_PRODUCER_DRIFT")
    return _load_native(source)


def authority():
    return {"repository": "The-Interdependency/ucns", "commit": UCNS_COMMIT,
            "source": UCNS_SOURCE, "source_sha256": UCNS_SOURCE_SHA256}


def construct_glyph(character, *, ucns_source_root):
    return _native(ucns_source_root).unicode_glyph_gonol(character)


def construct_text(text, *, ucns_source_root, placement_radius=1):
    return _native(ucns_source_root).build_unicode_scalar_frame(text, radius=placement_radius)


def encode_text(text, *, ucns_source_root):
    """Four big-endian bytes per scalar, no inserted byte-order marker."""
    return construct_text(text, ucns_source_root=ucns_source_root).utf32_be


def decode_text(data, *, ucns_source_root):
    """Recover complete diameters, retaining zero bytes and source U+FEFF."""
    native = _native(ucns_source_root)
    if not isinstance(data, bytes):
        raise TypeError("encoded text must be immutable bytes")
    width = native.GONOL_BIT_DIAMETER // 8
    if not data or len(data) % width:
        raise ValueError("encoded text must contain complete four-byte gonol diameters")
    return "".join(native.UnicodeGlyphGonol.from_utf32_be(data[i:i + width]).character
                   for i in range(0, len(data), width))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text")
    parser.add_argument("--ucns-source-root", required=True)
    args = parser.parse_args(argv)
    frame = construct_text(args.text, ucns_source_root=args.ucns_source_root)
    print(json.dumps({"profile": PROFILE, "geometry_authority": authority(),
                      "frame": frame.record()}, ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
# ratios: loc_comments=57:41 imports_exports=8:6 calls_definitions=25:8
