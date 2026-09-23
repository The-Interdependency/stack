"""Checks for the bounded URPCS-to-UCNS Möbius measurement adapter."""

# === CHECKS ===
# id: check_urpcs_projection_ucns_agreement
#   proves: urpcs_projection_matches_ucns
#   call: self::check_ucns_agreement
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_urpcs_projection_forest_and_member_laws
#   proves: urpcs_projection_matches_ucns
#   call: self::check_projection_laws
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_urpcs_projection_authentication_order
#   proves: urpcs_projection_authenticates_first
#   call: self::check_authentication_order
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_urpcs_projection_evidence_regeneration
#   proves: urpcs_projection_evidence_is_deterministic
#   call: self::check_deterministic_evidence
#   requires: python3
#   timeout: 60
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest import mock


URPCS_ROOT = Path(__file__).resolve().parents[1]
STACK_ROOT = URPCS_ROOT.parents[1]
sys.path.insert(0, str(URPCS_ROOT))

import urpcs_mobius_projection as projection  # noqa: E402
import urpcs_v1_reference as ref  # noqa: E402


UCNS_ROOT = STACK_ROOT / "libs" / "ucns"

FROZEN_HASHES = {
    "docs/urpcs-v1-spec.md": "295cd721a19475e683b1831f1a15b3c7eed521cec551d68cd031bfed4757423e",
    "urpcs_v1_reference.py": "415c22ac9f181cd079de5262bcbb5584f73f578bfb3a70f52ff721d9be8c2d3a",
    "urpcs_v1_independent.js": "907b8341ebeb6d3c972ef24692e5031cdabbe4a67affa8b6d90fed3d42c18617",
    "tests/test_independent_decoder.js": "633816370d8be0c7cdcaf5c9275d6373ae3d36d63ce71cdaaf87f146018135fe",
    "docs/URPCS-v1-independent-replay.md": "dfa430d260f38acdc05d0e750f632c920400e5c102917ae03e937136783b8c81",
    "vectors/urpcs-v1-vectors.json": "1d96299a016feed6f2e0881a5d4d21c20229714dab5eaa9338008d5282c2dfe6",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def ucns_module():
    return projection.load_ucns_direct_mobius(UCNS_ROOT)


def check_ucns_agreement() -> None:
    ucns = ucns_module()
    expected = {
        -9: (-2, 7, "positive-local-frame"),
        -8: (-1, 0, "reversed-local-frame"),
        -1: (-1, 7, "reversed-local-frame"),
        0: (0, 0, "positive-local-frame"),
        1: (0, 1, "positive-local-frame"),
        7: (0, 7, "positive-local-frame"),
        8: (1, 0, "reversed-local-frame"),
        9: (1, 1, "reversed-local-frame"),
        16: (2, 0, "positive-local-frame"),
        18: (2, 2, "positive-local-frame"),
    }
    for displacement, (quotient, remainder, frame) in expected.items():
        state = projection.euclidean_mobius_state(displacement, 8, ucns)
        require(state == {
            "S": displacement,
            "q": quotient,
            "phase": f"({remainder},8)",
            "phase_numerator": remainder,
            "phase_modulus": 8,
            "frame": frame,
        }, f"UCNS conformance disagreement at S={displacement}")


def check_projection_laws() -> None:
    sums = projection.reconstruct_path_sums(
        {b"root": b"scope", b"a": b"scope", b"b": b"scope"},
        [(b"root", b"a"), (b"a", b"b")],
        {(b"root", b"a"): 7, (b"a", b"b"): 3},
    )
    require(sums == {b"root": 0, b"a": 7, b"b": 10}, "root-to-gonol path sum mismatch")

    origin = b"origin"
    root, child = b"root", b"child"
    first, second = b"occ-a", b"occ-b"
    witness = [
        [],
        [[], [], [], [], [[root, child, ref.n_bytes(0)]]],
        [[root, child, ref.n_bytes(7)]],
        [[], True],
        [ref.n_bytes(32), (0).to_bytes(4, "big")],
    ]
    index = {
        "origins": {origin: (0, 0)},
        "gonols": {
            root: {"origin": origin, "members": [first]},
            child: {"origin": origin, "members": [first, second]},
        },
        "occurrences": {first: {}, second: {}},
    }
    result = projection.project_witness(witness, index, 0, 8, ucns_module())
    member_keys = set(result["buckets"]["member"])
    require("(7,8)|positive-local-frame" in member_keys, "member baseline state missing")
    require("(3,8)|reversed-local-frame" in member_keys, "independent member wrap missing")


def check_authentication_order() -> None:
    state = ref.vector_state(0)
    encrypted = ref.encrypt(b"\x09", state, ref.VECTOR_AD)
    with mock.patch.object(ref, "decode_witness", side_effect=AssertionError("witness parser reached")) as parser:
        with unittest.TestCase().assertRaisesRegex(ref.CodecFail, "tag verification"):
            projection.authenticated_witness(encrypted.ciphertext, state, ref.VECTOR_AD + b"!")
        parser.assert_not_called()


def check_deterministic_evidence() -> None:
    kwargs = {
        "ucns_root": UCNS_ROOT,
        "jobs": 1,
        "kmac_backend": "stdlib",
        "depths": (0,),
        "values": (b"", b"\x00", b"\xff"),
    }
    first = projection.run_measurement(**kwargs)
    second = projection.run_measurement(**kwargs)
    require(first == second, "test-subset measurement is nondeterministic")
    context = {
        "authorities": {
            "stack": {"input_commit": "test", "input_tree": "test"},
            "ucns": {
                "commit": "test",
                "native_mobius_law_id": projection.UCNS_LAW_ID,
                "native_mobius_law_version": projection.UCNS_LAW_VERSION,
            },
            "skill_lib": {"commit": "test"},
        },
        "runtime": {"test": "fixed"},
        "sources": {"test": "fixed"},
    }
    first_receipt = projection.build_receipt(measurement=first, jobs=1, **context)
    second_receipt = projection.build_receipt(measurement=second, jobs=1, **context)
    projection.verify_receipt_payload(first_receipt)
    require(
        projection._json_bytes(first_receipt) == projection._json_bytes(second_receipt),
        "test-subset receipt is nondeterministic",
    )
    first_sha = hashlib.sha256(projection._json_bytes(first_receipt)).hexdigest()
    require(
        projection.render_report(first_receipt, first_sha) == projection.render_report(second_receipt, first_sha),
        "test-subset Markdown report is nondeterministic",
    )


class URPCSMobiusProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ucns = ucns_module()

    def test_exact_ucns_agreement(self) -> None:
        check_ucns_agreement()

    def test_gonol_path_sum_and_member_wrap(self) -> None:
        check_projection_laws()

    def test_same_phase_opposite_frame_detection(self) -> None:
        positive = projection.euclidean_mobius_state(0, 8, self.ucns)
        reversed_state = projection.euclidean_mobius_state(8, 8, self.ucns)
        self.assertEqual(positive["phase"], reversed_state["phase"])
        self.assertNotEqual(positive["frame"], reversed_state["frame"])

        buckets = {
            positive["phase"] + "|" + positive["frame"]: projection._record_bytes(
                kind="gonol", case_index=0, layer=0, region=0, displacement=0, gonol_id=b"a"
            ),
            reversed_state["phase"] + "|" + reversed_state["frame"]: projection._record_bytes(
                kind="gonol", case_index=1, layer=0, region=0, displacement=8, gonol_id=b"b"
            ),
        }
        previews = {
            key: {"phase": key.split("|")[0], "frame": key.split("|")[1]}
            for key in buckets
        }
        result = projection._finalize_kind("gonol", buckets, previews, 2, 8, 1)
        self.assertEqual(result["opposite_frame_phase_buckets"], 1)
        self.assertEqual(result["records_in_opposite_frame_phase_buckets"], 2)

    def test_same_complete_state_after_two_windings(self) -> None:
        first = projection.euclidean_mobius_state(2, 8, self.ucns)
        second = projection.euclidean_mobius_state(18, 8, self.ucns)
        self.assertEqual((first["phase"], first["frame"]), (second["phase"], second["frame"]))
        self.assertNotEqual(first["q"], second["q"])

    def test_authentication_precedes_witness_parsing(self) -> None:
        check_authentication_order()

    def test_no_frame_field_in_v1_wire(self) -> None:
        built = ref.build(b"\x09", ref.vector_state(0))

        def values(value):
            if isinstance(value, list):
                for item in value:
                    yield from values(item)
            else:
                yield value

        self.assertTrue(all(isinstance(item, (bytes, bool)) for item in values(built.witness)))
        self.assertNotIn(b"frame", ref.encode_witness(built.witness).lower())

    def test_frozen_vectors_and_independent_replay_artifacts_unchanged(self) -> None:
        observed = {path: sha256_file(URPCS_ROOT / path) for path in FROZEN_HASHES}
        self.assertEqual(observed, FROZEN_HASHES)
        vectors = json.loads((URPCS_ROOT / "vectors/urpcs-v1-vectors.json").read_text(encoding="utf-8"))
        self.assertEqual([item["id"] for item in vectors["vectors"][:3]], ["empty_r0", "empty_r1", "odd_09_r0"])

    def test_deterministic_receipt_regeneration(self) -> None:
        check_deterministic_evidence()

    def test_malformed_forest_failures(self) -> None:
        scope = {b"r": b"s", b"a": b"s", b"b": b"s"}
        with self.assertRaisesRegex(projection.ProjectionError, "missing or extra displacement"):
            projection.reconstruct_path_sums(scope, [(b"r", b"a")], {})
        with self.assertRaisesRegex(projection.ProjectionError, "duplicate parent"):
            projection.reconstruct_path_sums(
                scope,
                [(b"r", b"b"), (b"a", b"b")],
                {(b"r", b"b"): 1, (b"a", b"b"): 1},
            )
        with self.assertRaisesRegex(projection.ProjectionError, "inconsistent witness reference"):
            projection.reconstruct_path_sums(
                {b"r": b"s"},
                [(b"r", b"missing")],
                {(b"r", b"missing"): 1},
            )
        with self.assertRaisesRegex(projection.ProjectionError, "malformed forest"):
            projection.reconstruct_path_sums(
                scope,
                [(b"r", b"a"), (b"a", b"r")],
                {(b"r", b"a"): 1, (b"a", b"r"): 1},
            )
        with self.assertRaisesRegex(projection.ProjectionError, "invalid modulus"):
            projection.euclidean_mobius_state(0, 0, self.ucns)

    def test_inconsistent_witness_member_reference_fails(self) -> None:
        origin, gid = b"origin", b"gonol"
        witness = [[], [[], [], [], [], []], [], [[], True], [ref.n_bytes(32), b"\0" * 4]]
        index = {
            "origins": {origin: (0, 0)},
            "gonols": {gid: {"origin": origin, "members": [b"missing"]}},
            "occurrences": {},
        }
        with self.assertRaisesRegex(projection.ProjectionError, "inconsistent witness reference"):
            projection.project_witness(witness, index, 0, 8, self.ucns)


if __name__ == "__main__":
    unittest.main()
