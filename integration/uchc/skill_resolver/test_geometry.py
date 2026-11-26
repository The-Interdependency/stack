# ratios: loc_comments=61:1 imports_exports=6:1 calls_definitions=29:6
"""Run with the pinned UCHC wheel and UCHC_HALVING_UCNS_ROOT (or installed UCNS)."""

import json
import os
import unittest
from copy import deepcopy

import uchc_halving as halving

from integration.uchc.skill_resolver.geometry import (
    PROFILE, compose_bundle, decode_record, encode_record, replay_bundle,
)


class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.options = {"ucns_source_root": os.environ.get("UCHC_HALVING_UCNS_ROOT")}

    def test_exact_roundtrip_across_a_wire(self):
        record = {
            "ç": [None, True, False, 0, -7, 1.0, -0.0, "", {}, [], ["same", "same"]],
            "c\u0327": {"": "\x00😀", "s": "o", "a": "p"},
        }
        packet = encode_record(record, **self.options)
        restored = decode_record(json.loads(json.dumps(packet)), **self.options)
        assert json.dumps(restored, sort_keys=True) == json.dumps(record, sort_keys=True)
        assert encode_record(dict(reversed(record.items())), **self.options) == packet

    def test_same_additive_vector_different_ownership(self):
        a = {"groups": [["alpha"], "beta"]}
        b = {"groups": ["alpha", ["beta"]]}
        first, second = (encode_record(record, **self.options) for record in (a, b))
        assert first["vectors"]["additive_resultant"] == second["vectors"]["additive_resultant"]
        assert first["graph"]["root"] != second["graph"]["root"]
        assert decode_record(first, **self.options) == a
        assert decode_record(second, **self.options) == b

    def test_replay_rejects_tampering_and_foreign_construction(self):
        packet = encode_record({"name": "deps-build"}, **self.options)
        altered = deepcopy(packet)
        altered["graph"]["nodes"][0]["construction"]["source"] = "changed"
        with self.assertRaises(ValueError):
            decode_record(altered, **self.options)
        malformed = halving.construct_sequence(
            (halving.construct_glyph("o", **self.options),
             halving.construct_text("wrong child", source=PROFILE, **self.options)),
            source=PROFILE, **self.options,
        )
        with self.assertRaisesRegex(ValueError, "expected a skill sequence"):
            decode_record(halving.closed_record(malformed, **self.options), **self.options)

    def test_bundle_preserves_interior_ownership_direction_and_occurrences(self):
        records = [{"name": "msdmd"}, {"name": "deps-build"}]
        packets = [encode_record(record, **self.options) for record in records]
        decision = {"edges": [{"from": "deps-build", "to": "msdmd"}]}
        bundle = compose_bundle(packets, decision, **self.options)
        assert replay_bundle(bundle, **self.options) == (records, decision)
        assert {p["graph"]["root"] for p in packets} <= {
            node["receipt"] for node in bundle["graph"]["nodes"]
        }
        reversed_bundle = compose_bundle(list(reversed(packets)), decision, **self.options)
        assert bundle["vectors"]["additive_resultant"] == reversed_bundle["vectors"]["additive_resultant"]
        assert bundle["graph"]["root"] != reversed_bundle["graph"]["root"]
        assert replay_bundle(reversed_bundle, **self.options) == (list(reversed(records)), decision)
        repeated = compose_bundle([packets[0], packets[0]], decision, **self.options)
        assert replay_bundle(repeated, **self.options) == ([records[0], records[0]], decision)
        assert replay_bundle(compose_bundle([], {}, **self.options), **self.options) == ([], {})
        with self.assertRaises(ValueError):
            decode_record(bundle, **self.options)
        with self.assertRaises(ValueError):
            replay_bundle(packets[0], **self.options)
# ratios: loc_comments=61:1 imports_exports=6:1 calls_definitions=29:6
