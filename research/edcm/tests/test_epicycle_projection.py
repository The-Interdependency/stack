# ratios: loc_comments=174:26 imports_exports=4:14 calls_definitions=71:15
"""Usage: python -m pytest -q research/edcm/tests on the locked producers."""
# === MODULE_BUILD ===
# id: stack_edcm_epicycle_projection_tests
#   module_name: test_epicycle_projection
#   module_kind: test
#   summary: exercises release identity, native reconstruction, boundary controls and frozen contrasts
#   owner: The-Interdependency/stack
#   public_surface: pytest suite
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: public fixtures
#   admin_only: false
#   tests: stack_edcm_epicycle_projection
# === END MODULE_BUILD ===
# === CHECKS ===
# id: epicycle_release_record_replay
#   contract: edcm_epicycle_native_replay
#   method: origin reconstruction and malformed packet controls
# id: epicycle_distinction_and_orthogonality
#   contract: edcm_epicycle_comparison_boundary
#   method: origin pair matrix, ordering and matched history comparisons, typed missingness
# id: epicycle_replay_receipt
#   contract: edcm_epicycle_frozen_protocol
#   method: source and digest binding plus independent CLI replay in CI
# === END CHECKS ===
from copy import deepcopy
import math

import pytest

from research.edcm import epicycle_projection as e


@pytest.fixture(scope="module")
def report():
    return e.experiment()


def test_all_declared_origins_replay(report):
    assert tuple(report["origin_specs"]) == e.AXES
    specs = e.origin_specs()
    roots = e.verify_origins(
        {axis: report["origins"][axis]["graph"] for axis in e.AXES}, specs
    )
    for axis, root in roots.items():
        assert "".join(root.recover()) == "".join(specs[axis]["terms"])
        assert len(root.participants) == len(specs[axis]["terms"])
        assert root.radius == 1
        views = e.build_views(root)
        assert len(views["additive"]) == len(views["ordinal"]) == 1
        assert len(views["paired"]) == 2
        assert set(views["paired"]).issubset(views["recursive"])


@pytest.mark.parametrize(
    "view,rank", [("additive", 2), ("ordinal", 2), ("paired", 4), ("recursive", 11)]
)
def test_origin_rank_and_nonorthogonality(report, view, rank):
    diagnostic = report["origin_analysis"][view]
    assert diagnostic["rank"] == rank
    assert diagnostic["nonzero_origins"] == 11
    assert diagnostic["orthogonality"] == "FALSIFIED"
    assert diagnostic["nonorthogonal_pairs"] == diagnostic["pair_count"] == 55
    for i, row in enumerate(diagnostic["pairs"]):
        assert row[i]["distance"] == 0
        assert row[i]["cosine"] == pytest.approx(1)
        for j, pair in enumerate(row):
            assert pair["distance"] == diagnostic["pairs"][j][i]["distance"]
            assert pair["cosine"] == pytest.approx(diagnostic["pairs"][j][i]["cosine"])


def test_exact_reversals_scale_and_zero(report):
    controls = report["controls"]
    assert set(controls["reversals"]) == set(e.AXES)
    for result in controls["reversals"].values():
        assert result["exact_additive_equal"]
        assert result["comparisons"]["additive"]["exact_equal"]
        assert (
            result["comparisons"]["ordinal"]["distance"]
            > report["comparison"]["comparison_tolerance"]
        )
    assert controls["scale"]["placement_scales_exactly"]
    assert controls["scale"]["additive_scales_exactly"]
    assert controls["cancellation"]["exact_additive_zero"]
    assert controls["cancellation"]["nonzero_placement"]
    assert controls["cancellation"]["self"]["additive"]["projection"] is None
    assert controls["cancellation"]["self"]["additive"]["cosine"] is None
    assert controls["cancellation"]["against_origin"]["additive"]["projection"] == 0
    assert (
        controls["cancellation"]["origin_against_zero"]["additive"]["projection"]
        is None
    )
    assert set(controls["refusals"].values()) == {"SURVIVED"}


def test_each_order_counterexample(report):
    protocol = e.load("EPICYCLE_PROTOCOL.json")
    by_id = {item["id"]: item for item in report["contrasts"]}
    for fixture in protocol["fixtures"]:
        if not fixture.get("same_multiset"):
            continue
        item = by_id[fixture["id"]]
        for grain in ("round", "prefix"):
            assert item["pair"][grain]["additive"]["exact_equal"]
            assert not item["pair"][grain]["ordinal"]["exact_equal"]
        for witness in item["witnesses"].values():
            assert witness["left"] != witness["right"]
            assert witness["baseline"] == "SURVIVED"
            for grain in ("round", "prefix"):
                assert (
                    witness["grains"][grain]["additive"]["distinction"] == "FALSIFIED"
                )
                for view in ("ordinal", "paired", "recursive"):
                    assert witness["grains"][grain][view]["distinction"] == "SURVIVED"


def test_history_counterexample(report):
    historical_axes = set()
    for item in report["contrasts"]:
        if item["id"] not in {"same-round-different-history", "stored-tension-history"}:
            continue
        left, right = item["left"]["rounds"][-1], item["right"]["rounds"][-1]
        assert left["graphs"]["round"] == right["graphs"]["round"]
        assert left["graphs"]["prefix"] != right["graphs"]["prefix"]
        for axis, witness in item["witnesses"].items():
            historical_axes.add(axis)
            assert witness["baseline"] == "SURVIVED"
            for view in e.VIEWS:
                assert item["pair"]["round"][view]["exact_equal"]
                assert witness["grains"]["round"][view]["distinction"] == "FALSIFIED"
                assert witness["grains"]["prefix"][view]["distinction"] == "SURVIVED"
    assert historical_axes == {"F", "D", "L", "P", "kappa"}


def test_formatting_and_measurement_separation(report):
    item = next(x for x in report["contrasts"] if x["id"] == "formatting-control")
    assert item["formatting_control"]["source_differs"]
    assert item["formatting_control"]["unchanged_axes"] == list(e.AXES)
    assert item["formatting_control"]["baseline"] == "SURVIVED"
    assert all(not term["exact_equal"] for term in item["pair"]["prefix"].values())


def test_all_readouts_exercised_and_calibration_not_established(report):
    summary = e.summarize(report)
    assert set(summary["coverage"].values()) == {"SURVIVED"}
    for grain in ("round", "prefix"):
        for view in e.VIEWS:
            for statistic in ("distance", "projection", "cosine"):
                outcomes = summary["outcomes"][grain][view][statistic]
                assert outcomes["FALSIFIED"] > 0
                assert outcomes["UNRESOLVED"] >= 1
    assert summary["outcomes"]["prefix"]["recursive"]["distinction"]["SURVIVED"] == 11


def test_absence_is_not_exact_zero_and_numeric_ties_remain_unresolved():
    present = {((), "additive"): e.Coordinate([], 0j)}
    pair = e.compare_fields(present, {})
    assert pair["distance"] == 0
    assert pair["support"] == {"shared": 0, "left_only": 1, "right_only": 0}
    assert not pair["exact_equal"]
    assert e.distinction(pair, 1e-12) == "UNRESOLVED"
    assert e.monotonic(0.5, 0.5, 1, "projection", 1e-12, False, False) == "UNRESOLVED"
    assert e.monotonic(0.5, 0.5, 1, "projection", 1e-12, False, True) == "FALSIFIED"


def test_native_v2_both_vectors_and_source_required(report):
    spec = report["origin_specs"]["R"]
    packet = report["origins"]["R"]["graph"]
    text = "".join(spec["terms"])
    for vector in ("placement_endpoint", "additive_resultant"):
        changed = deepcopy(packet)
        changed["vectors"][vector] = []
        with pytest.raises(ValueError):
            e.validate_record(changed, expected_text=text)
    changed = deepcopy(packet)
    changed["record_version"] = 1
    with pytest.raises(ValueError):
        e.validate_record(changed, expected_text=text)
    with pytest.raises(ValueError):
        e.validate_record(packet, expected_text=text, expected_source="wrong-source")
    with pytest.raises(ValueError):
        e.validate_record(packet, expected_text=text, expected_terms=[text])
    with pytest.raises(ValueError):
        e.validate_record(packet, expected_text=text, radius=2)


def test_release_lock_refuses_changed_pin(monkeypatch):
    load = e.load

    def altered(name):
        result = load(name)
        if name == "BASE.json":
            result["epicycle_projection"]["uchc_wheel_sha256"] = "0" * 64
        return result

    monkeypatch.setattr(e, "load", altered)
    with pytest.raises(ValueError, match="wheel projection differs"):
        e.verify_producers()


def test_observe_new_raw_rounds_without_unicode_normalization():
    source = ["A: café.\nB: cafe\u0301.", "A: Please state it.\nB: not now."]
    report = e.observe_rounds(source)
    assert report["axis_order"] == list(e.AXES)
    assert report["standing"] == "Stack-local candidate research"
    assert report["observation"]["raw"] == "\n".join(source)
    assert len(report["observation"]["rounds"]) == 2
    for i, raw_round in enumerate(source):
        record = report["observation"]["rounds"][i]
        assert record["raw_text"] == raw_round
        e.validate_record(record["graphs"]["round"], expected_text=raw_round)
        e.validate_record(
            record["graphs"]["prefix"], expected_text="\n".join(source[: i + 1])
        )
        assert set(record["metrics"]) == set(e.AXES)
        assert all(math.isfinite(value) for value in record["metrics"].values())
    assert report["receipt_sha256"] == e.digest(
        {k: v for k, v in report.items() if k != "receipt_sha256"}
    )


def test_explicit_round_boundaries_are_required():
    with pytest.raises(ValueError):
        e.observation([], {}, {})
    with pytest.raises(ValueError):
        e.observation(["A: said.\nB: answered.\nA: repeated.\nB: replied."], {}, {})


def test_receipt_digest_binds_entire_experiment(report):
    payload = {k: v for k, v in report.items() if k != "receipt_sha256"}
    assert e.digest(payload) == report["receipt_sha256"]

# ratios: loc_comments=174:26 imports_exports=4:14 calls_definitions=71:15
