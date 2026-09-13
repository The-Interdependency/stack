"""Focused regressions for Stack #39's post-merge Python Gonol findings."""

from dataclasses import replace

import pytest

from python_gonol import (
    PythonGonolConstructionError,
    affixiate_python_source,
    replay_python_affixiation,
    reconstruct_source,
)
from python_gonol import _recognition


def test_hmmm_root_cannot_be_relabelled_as_success() -> None:
    receipt = affixiate_python_source("call(1\n", source_id="fixture/unclosed.py")
    assert receipt.standing == "hmmm"
    relabelled = replace(
        receipt,
        standing="implemented-candidate",
        receipt_digest=_recognition._receipt_digest(
            replace(receipt, standing="implemented-candidate", receipt_digest="")
        ),
    )
    with pytest.raises(PythonGonolConstructionError, match="compiler-valid module"):
        replay_python_affixiation(relabelled)


def test_exact_cpython_patch_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    import sys

    monkeypatch.setattr(sys, "version_info", (3, 12, 13))
    with pytest.raises(PythonGonolConstructionError, match="CPython 3.12.14"):
        affixiate_python_source("value = 1\n", source_id="fixture/version.py")


@pytest.mark.parametrize(
    "source",
    (
        "return 1\n",
        "await value\n",
        "value = 1\nfrom __future__ import annotations\n",
    ),
)
def test_compiler_invalid_file_inputs_remain_hmmm(source: str) -> None:
    receipt = affixiate_python_source(source, source_id="fixture/compiler-invalid.py")
    assert receipt.standing == "hmmm"
    assert any(item.startswith("compiler:") for item in receipt.hmmm)
    assert reconstruct_source(receipt) == source
    replay_python_affixiation(receipt)


def test_classic_mac_line_boundaries_preserve_exact_source() -> None:
    source = "first = 1\rsecond = first + 1\r"
    receipt = affixiate_python_source(source, source_id="fixture/classic-mac.py")
    assert receipt.standing == "implemented-candidate"
    assert reconstruct_source(receipt) == source
    replay_python_affixiation(receipt)
    second_line_s = next(
        item for item in receipt.gonols
        if item.scale == "character" and item.span.start == source.index("second")
    )
    assert second_line_s.span.start_line == 2


def test_deep_valid_ast_is_traversed_without_python_recursion() -> None:
    source = "value = " + ("-" * 1600) + "1\n"
    receipt = affixiate_python_source(source, source_id="fixture/deep.py")
    assert receipt.standing == "implemented-candidate"
    assert reconstruct_source(receipt) == source
    replay_python_affixiation(receipt)
