# === CHECKS ===
# id: every_python_source_occurrence_closes_first_check
#   proves: every_python_source_occurrence_closes_first
#   call: self::test_letter_floor_preserves_identity_order_multiplicity_and_provenance
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: python_lexical_forms_affixiate_letters_check
#   proves: python_lexical_forms_affixiate_letters
#   call: self::test_lexical_floor_is_an_exact_partition_of_closed_letters
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: python_constructions_affixiate_closed_gonols_check
#   proves: python_constructions_affixiate_closed_gonols, python_gonol_parent_references_closed_children
#   call: self::test_larger_constructions_reference_prior_closed_gonols_and_own_relations
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: python_affixiation_is_lossless_and_replayable_check
#   proves: python_affixiation_is_lossless_and_replayable, python_gonol_receipt_is_canonical_json
#   call: self::test_receipt_roundtrip_reconstructs_exact_source_and_replays
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: unresolved_python_source_remains_hmmm_check
#   proves: unresolved_python_source_remains_hmmm
#   call: self::test_missing_parenthesis_preserves_lower_closures_and_records_hmmm
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: parser_objects_never_become_gonols_check
#   proves: parser_objects_never_become_gonols
#   call: self::test_receipt_contains_source_relations_not_parser_objects
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: python_gonol_geometry_binding_fails_closed_check
#   proves: python_gonol_geometry_binding_fails_closed
#   call: self::test_exact_ucns_carrier_is_observed_and_drift_fails_closed
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from collections import Counter
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

from python_gonol import (
    PythonAffixiationReceipt,
    PythonGonolConstructionError,
    affixiate_python_bytes,
    affixiate_python_source,
    reconstruct_source,
    replay_python_affixiation,
)


def _letters(receipt: PythonAffixiationReceipt):
    return tuple(gonol for gonol in receipt.gonols if gonol.scale == "letter")


def test_letter_floor_preserves_identity_order_multiplicity_and_provenance() -> None:
    source = "π = (a + a)\n# a\n"
    receipt = affixiate_python_source(source, source_id="fixture/repeated.py")
    letters = _letters(receipt)
    assert len(letters) == len(source)
    assert [item.span.start for item in letters] == list(range(len(source)))
    assert len({item.address for item in letters}) == len(source)
    assert len({item.gonol_id for item in letters}) == len(source)
    repeated = [item for item in letters if dict(item.relation.properties)["unicode_scalar"] == "a"]
    assert len(repeated) == 3
    assert len({item.address for item in repeated}) == 3
    assert all(("source_id", "fixture/repeated.py") in item.provenance for item in letters)


def test_lexical_floor_is_an_exact_partition_of_closed_letters() -> None:
    source = "value  = f'{name!r:>{width}}'  # keep both spaces\n"
    receipt = affixiate_python_source(source, source_id="fixture/lexical.py")
    lexical = [gonol for gonol in receipt.gonols if gonol.scale == "lexical-form"]
    counts = Counter(member.address for gonol in lexical for member in gonol.relation.members)
    assert counts == Counter(item.address for item in _letters(receipt))
    earlier = {gonol.gonol_id: index for index, gonol in enumerate(receipt.gonols)}
    for gonol in lexical:
        assert gonol.relation.members
        assert all(receipt.gonols[earlier[member.gonol_id]].scale == "letter" for member in gonol.relation.members)
    kinds = {gonol.relation.kind for gonol in lexical}
    assert "python.lexical.FSTRING_START" in kinds
    assert "python.lexical.COMMENT" in kinds
    assert "python.lexical.INTERTOKEN" in kinds


def test_larger_constructions_reference_prior_closed_gonols_and_own_relations() -> None:
    source = "answer = (((left + right)))\n"
    receipt = affixiate_python_source(source, source_id="fixture/nesting.py")
    position = {gonol.gonol_id: index for index, gonol in enumerate(receipt.gonols)}
    delimiters = [gonol for gonol in receipt.gonols if gonol.scale == "delimiter-construction"]
    assert len(delimiters) == 3
    assert all(gonol.relation.kind == "python.delimiter.parentheses" for gonol in delimiters)
    assert receipt.gonols[-1].scale == "module"
    assert receipt.gonols[-1].relation.kind == "python.grammar.Module"
    assert any(gonol.relation.kind == "python.grammar.BinOp" for gonol in receipt.gonols)
    for parent_index, gonol in enumerate(receipt.gonols):
        for member in gonol.relation.members:
            assert position[member.gonol_id] < parent_index
            assert receipt.gonols[position[member.gonol_id]].address == member.address


def test_receipt_roundtrip_reconstructs_exact_source_and_replays() -> None:
    raw = b"# coding: latin-1\nname = 'caf\xe9'\r\n"
    receipt = affixiate_python_bytes(raw, source_id="fixture/latin1.py")
    assert receipt.source_bytes_sha256
    assert receipt.encoding == "iso-8859-1"
    assert reconstruct_source(receipt) == "# coding: latin-1\nname = 'caf\N{LATIN SMALL LETTER E WITH ACUTE}'\r\n"
    roundtrip = PythonAffixiationReceipt.from_json(receipt.to_json())
    assert replay_python_affixiation(roundtrip).receipt_digest == receipt.receipt_digest
    assert receipt.to_json() == roundtrip.to_json()

    root = roundtrip.gonols[-1]
    tampered_root = replace(root, relation=replace(root.relation, kind="python.grammar.Expression"))
    tampered = replace(roundtrip, gonols=roundtrip.gonols[:-1] + (tampered_root,))
    with pytest.raises(PythonGonolConstructionError, match="gonol identity mismatch"):
        replay_python_affixiation(tampered)


def test_missing_parenthesis_preserves_lower_closures_and_records_hmmm(tmp_path: Path) -> None:
    source = "result = call(1, 2\n"
    receipt = affixiate_python_source(source, source_id="fixture/missing.py")
    assert receipt.standing == "hmmm"
    assert receipt.gonols[-1].relation.kind == "python.source.hmmm"
    assert reconstruct_source(receipt) == source
    assert len(_letters(receipt)) == len(source)
    assert any("unmatched opening delimiter" in item for item in receipt.hmmm)
    assert any(item.startswith("grammar:") for item in receipt.hmmm)
    replay_python_affixiation(receipt)

    source_path = tmp_path / "missing.py"
    receipt_path = tmp_path / "missing.gonol.json"
    source_path.write_text(source, encoding="utf-8")
    run = subprocess.run(
        [sys.executable, "-m", "python_gonol", str(source_path), "--out", str(receipt_path)],
        cwd=Path(__file__).resolve().parents[1],
        check=False,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 2
    assert receipt_path.is_file()
    assert "hmmm:" in run.stderr


def test_receipt_contains_source_relations_not_parser_objects() -> None:
    receipt = affixiate_python_source(
        "def f(x: int = 1) -> int:\n    return x + 1\n",
        source_id="fixture/no-substitution.py",
    )
    encoded = json.dumps(receipt.to_dict(), ensure_ascii=False)
    assert "TokenInfo" not in encoded
    assert "<_ast." not in encoded
    assert "occurrence_addresses" not in encoded
    assert all(gonol.scale in {"letter", "lexical-form", "delimiter-construction", "python-construction", "module"} for gonol in receipt.gonols)
    assert all(type(gonol).__module__ == "python_gonol.model" for gonol in receipt.gonols)
    replay_python_affixiation(receipt)


def test_exact_ucns_carrier_is_observed_and_drift_fails_closed() -> None:
    path = Path(__file__).resolve().parents[3] / "libs" / "ucns" / "src" / "ucns" / "public_gonol.py"
    spec = importlib.util.spec_from_file_location("pinned_ucns_public_gonol", path)
    assert spec is not None and spec.loader is not None
    authority = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = authority
    try:
        spec.loader.exec_module(authority)
    finally:
        sys.modules.pop(spec.name, None)

    receipt = affixiate_python_source(
        "a + 1",
        source_id="fixture/ucns.py",
        geometry_authority=authority,
    )
    for letter in _letters(receipt):
        properties = dict(letter.relation.properties)
        assert properties["public_gonol_position"].isdigit()
        assert properties["public_gonol_function"] == "hmmm"
    assert "UCNS Public Gonol geometry authority was not supplied" not in receipt.hmmm
    replay_python_affixiation(receipt)

    drifted = {
        "PUBLIC_GONOL_157": authority.PUBLIC_GONOL_157,
        "PUBLIC_GONOL_SHA256": "0" * 64,
    }
    with pytest.raises(PythonGonolConstructionError, match="digest"):
        affixiate_python_source(
            "a",
            source_id="fixture/drift.py",
            geometry_authority=drifted,
        )
