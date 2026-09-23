# ratios: loc_comments=149:40 imports_exports=12:7 calls_definitions=82:9
"""Behavioral witnesses against the real pinned glyph producers.

Set ZFAE_UCNS_SOURCE to the exact downloaded public_gonol.py, then run:
python -m unittest discover -s research/zfae/tests -v
"""

from dataclasses import replace
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gonol_parser import GonolAdmissionError, load_parser
import input_probe
import gonol_probe

# === CHECKS ===
# id: zfae_gonol_source_and_carrier_witness
#   proves: zfae_gonol_parser_consumes_producers
#   call: self::test_producer_and_carrier_identity
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: zfae_gonol_order_and_recovery_witness
#   proves: zfae_gonol_parser_preserves_occurrences
#   call: self::test_occurrence_order_and_recovery
#   mutates: none
#   cleanup: none
# id: zfae_gonol_collision_witness
#   proves: zfae_gonol_parser_preserves_occurrences
#   call: self::test_prior_collisions_are_preserved
#   mutates: none
#   cleanup: none
# id: zfae_gonol_admission_boundary_witness
#   proves: zfae_gonol_parser_reports_missing_admission
#   call: self::test_invalid_and_unsupported_sources
#   mutates: none
#   cleanup: none
# id: zfae_gonol_serialization_witness
#   proves: zfae_gonol_parser_replays_construction
#   call: self::test_native_gonols_and_serialized_tampering
#   mutates: none
#   cleanup: none
# id: zfae_gonol_probe_scope_witness
#   proves: zfae_gonol_probe_exhausts_profile
#   call: self::test_gonol_probe_complete_scope
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def _parser():
    return load_parser(Path(os.environ["ZFAE_UCNS_SOURCE"]))


def _rejects(call, error=ValueError):
    with unittest.TestCase().assertRaises(error):
        call()


def test_producer_and_carrier_identity():
    parser = _parser()
    glyphs = tuple(parser.inventory.values())
    assert len(glyphs) == 165
    assert all(type(g).__name__ == "GlyphGonol" for g in glyphs)
    from english_gonol.hyperspace_construct import GlyphGonol
    assert all(type(g) is GlyphGonol for g in glyphs)
    carrier = sorted((g for g in glyphs if g.carrier_position is not None),
                     key=lambda g: g.carrier_position)
    assert len(carrier) == 157
    assert [g.carrier_position for g in carrier] == list(range(157))
    assert carrier[0].identity == " " and carrier[80].identity == "a"
    # Extra scalar axes are not invented Public Gonol positions.
    assert parser.inventory["é"].carrier_position is None
    assert parser.inventory["é"].axis_index >= 157
    assert parser.inventory["é"].construction_kind == "encoded-name"
    assert "U+00E9" in "".join(parser.inventory["é"].construction_parts)
    assert parser.inventory["\t"].construction_kind == "encoded-codepoint"
    with tempfile.TemporaryDirectory() as tmp:
        marker = Path(tmp) / "executed"
        altered = Path(tmp) / "public_gonol.py"
        altered.write_text(f"open({str(marker)!r}, 'w').write('bad')\n")
        _rejects(lambda: load_parser(altered), GonolAdmissionError)
        assert not marker.exists()
    producer = sys.modules["english_gonol.hyperspace_construct"]
    producer.glyph_inventory = lambda db: {}
    assert len(_parser().inventory) == 165
    _rejects(lambda: parser.inventory.__setitem__("x", glyphs[0]), AttributeError)


def test_occurrence_order_and_recovery():
    parser = _parser()
    profile = json.loads((input_probe.HERE / "GONOL_PARSER.json").read_text())
    # Complete declared inventory plus source-position and normalization controls.
    texts = [case["text"] for case in profile["cases"] if case["admitted"]]
    texts.append("".join(parser.inventory))
    for text in texts:
        parsed = parser.parse_text(text, source_id="fixture:recovery")
        assert parsed.admitted and len(parsed.occurrences) == len(text)
        assert parsed.recover_text() == text
        assert parser.parse_utf8(text.encode("utf-8"), source_id=parsed.source_id) == parsed
        assert parser.parse_gonols(parsed.require_gonols(), source_id=parsed.source_id) == parsed
        assert parser.replay(json.loads(json.dumps(parsed.to_dict()))) == parsed
        encoded = text.encode("utf-8")
        for ordinal, occurrence in enumerate(parsed.occurrences):
            assert occurrence.ordinal == ordinal
            assert occurrence.gonol is parser.inventory[text[ordinal]]
            assert encoded[occurrence.utf8_start:occurrence.utf8_end].decode("utf-8") == text[ordinal]
    repeated = parser.parse_text("AaAαα\r\n", source_id="fixture:repeat")
    assert repeated.occurrences[0].gonol is repeated.occurrences[2].gonol
    assert repeated.occurrences[3].gonol is repeated.occurrences[4].gonol
    assert repeated.occurrences[0] != repeated.occurrences[2]
    assert repeated.occurrences[0].gonol != repeated.occurrences[1].gonol
    assert [o.scalar for o in repeated.occurrences[-2:]] == ["\r", "\n"]
    precomposed = parser.parse_text("é", source_id="fixture:normalization")
    decomposed = parser.parse_text("e\u0301", source_id="fixture:normalization")
    assert precomposed != decomposed


def test_prior_collisions_are_preserved():
    parser = _parser()
    pairs = json.loads((input_probe.HERE / "INPUT_PROBE.json").read_text())["pairs"]
    observed = input_probe.evaluate(pairs, lambda text: parser.parse_text(
        text, source_id="fixture:shared-source-id"
    ).to_dict())
    assert observed["standing"] == "SURVIVED"
    assert observed["controls_passed"] and observed["collision_ids"] == []
    assert all(row[side]["admitted"] for row in observed["observations"]
               for side in ("left_features", "right_features"))
    # The distinction must remain in construction, even without source hashes.
    for pair in pairs:
        left = parser.parse_text(pair["left"], source_id="same").require_gonols()
        right = parser.parse_text(pair["right"], source_id="same").require_gonols()
        assert (left == right) == (pair["kind"] == "equal-control")


def test_invalid_and_unsupported_sources():
    parser = _parser()
    for text in (None, 12, ["a"], b"a"):
        _rejects(lambda: parser.parse_text(text, source_id="fixture:invalid"), TypeError)
    for text in ("\ud800", "a\udfff"):
        _rejects(lambda: parser.parse_text(text, source_id="fixture:surrogate"))
    for data in (b"\xff", b"\xed\xa0\x80", b"\xf0\x9f"):
        _rejects(lambda: parser.parse_utf8(data, source_id="fixture:invalid"), UnicodeDecodeError)
    _rejects(lambda: parser.parse_text("a", source_id=""))
    _rejects(lambda: parser.parse_utf8("a", source_id="fixture:invalid"), TypeError)
    missing = parser.parse_text("🧪a🧪", source_id="fixture:missing")
    assert not missing.admitted and missing.recover_text() == "🧪a🧪"
    assert [o.ordinal for o in missing.unadmitted] == [0, 2]
    assert [o.utf8_start for o in missing.unadmitted] == [0, 5]
    assert missing.occurrences[1].gonol is parser.inventory["a"]
    _rejects(missing.require_gonols, GonolAdmissionError)
    assert parser.replay(missing.to_dict()) == missing


def test_native_gonols_and_serialized_tampering():
    parser = _parser()
    parsed = parser.parse_gonols((parser.inventory[c] for c in "aαa"), source_id="fixture:native")
    assert parsed.recover_text() == "aαa"
    _rejects(lambda: parser.parse_gonols(["a"], source_id="fixture:foreign"))
    wrong = replace(parser.inventory["a"], axis_index=0)
    _rejects(lambda: parser.parse_gonols([wrong], source_id="fixture:mutated"))
    _rejects(lambda: parser.parse_gonols([parsed], source_id="fixture:wrapper"))
    # Separately instantiated native producer objects remain interoperable.
    native_copy = replace(parser.inventory["a"])
    assert parser.parse_gonols([native_copy], source_id="fixture:external").occurrences[0].gonol is parser.inventory["a"]
    for field in ("axis_index", "carrier_position"):
        zero = next(g for g in parser.inventory.values() if getattr(g, field) == 0)
        for value in (False, 0.0):
            wrong = replace(zero, **{field: value})
            _rejects(lambda: parser.parse_gonols([wrong], source_id="fixture:typed"))
    wrong = replace(parser.inventory["a"], construction_parts=list(parser.inventory["a"].construction_parts))
    _rejects(lambda: parser.parse_gonols([wrong], source_id="fixture:container"))
    base = parsed.to_dict()
    mutations = []
    for key, value in (("inventory_sha256", "0" * 64), ("profile_sha256", "0" * 64),
                       ("source_sha256", "0" * 64), ("admitted", 1), ("extra", "ignored?")):
        record = copy.deepcopy(base); record[key] = value; mutations.append(record)
    record = copy.deepcopy(base); record["occurrences"].pop(); mutations.append(record)
    record = copy.deepcopy(base); record["occurrences"][1]["utf8_span"] = [1, 2]; mutations.append(record)
    record = copy.deepcopy(base); record["occurrences"][1]["ordinal"] = 0; mutations.append(record)
    record = copy.deepcopy(base); record["occurrences"][1]["glyph_identity"] = "a"; mutations.append(record)
    record = copy.deepcopy(base); record["gonols"][0]["construction_parts"] = []; mutations.append(record)
    record = copy.deepcopy(base); record["gonols"][0]["carrier_position"] = 0; mutations.append(record)
    mutations.extend(({}, {"occurrences": None}, {"occurrences": [None]}))
    for record in mutations:
        _rejects(lambda: parser.replay(record), GonolAdmissionError)


def test_gonol_probe_complete_scope():
    result = gonol_probe.run(Path(os.environ["ZFAE_UCNS_SOURCE"]))
    assert result["standing"] == "SURVIVED"
    assert result["carrier_glyph_count"] == 157 and result["admitted_scalar_count"] == 165
    assert len(result["recovery_cases"]) == 17
    assert len(result["observations"]) == 9
    assert result["collision_ids"] == []
    assert sum(not c["admitted"] for c in result["recovery_cases"]) == 1


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(unittest.FunctionTestCase(fn) for fn in (
        test_producer_and_carrier_identity,
        test_occurrence_order_and_recovery,
        test_prior_collisions_are_preserved,
        test_invalid_and_unsupported_sources,
        test_native_gonols_and_serialized_tampering,
        test_gonol_probe_complete_scope,
    ))
# ratios: loc_comments=149:40 imports_exports=12:7 calls_definitions=82:9
