"""Element gonols for Z=1-18 from atomic structure only.

Usage guidance
--------------
This candidate closes one gonol per periodic-table element using the pinned
``edcm.gonol`` constructor. Carried options are Z, configuration, and typical
valence. Do not load the sealed comparison file from this module.

    from epac_periodic import construct_element_gonol, construct_periodic_table

    carbon = construct_element_gonol("C")
    table = construct_periodic_table()
    assert "C" in table
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from edcm.gonol import ClosedGonol, GonolReceipt, construct_gonol, replay_gonol


ROOT = Path(__file__).resolve().parent
TABLE_PATH = ROOT / "data" / "periodic_table_z1_18.json"
RELATION = "epac.periodic.element"
SCALE = "word"


def load_atomic_table() -> tuple[dict[str, Mapping[str, Any]], ...]:
    payload = json.loads(TABLE_PATH.read_text(encoding="utf-8"))
    elements = tuple(payload["elements"])
    if len(elements) != 18:
        raise RuntimeError("periodic table candidate requires Z=1-18")
    return elements


def _geometry_authority() -> Any:
    from ucns import public_gonol

    return public_gonol


def construct_element_gonol(symbol: str, *, occurrence: int = 0) -> GonolReceipt:
    """Close one element gonol from the frozen atomic-structure table."""

    record = None
    for element in load_atomic_table():
        if element["symbol"] == symbol:
            record = element
            break
    if record is None:
        raise ValueError(f"no atomic-structure record for symbol {symbol!r}")
    carried = (
        ("Z", str(record["Z"])),
        ("period", str(record["period"])),
        ("group", str(record["group"])),
        ("electron-configuration", str(record["electron_configuration"])),
        ("valence-electrons", str(record["valence_electrons"])),
        ("typical-valence", str(record["typical_valence"])),
    )
    return construct_gonol(
        scale=SCALE,
        source=symbol,
        source_id=f"epac.periodic:{symbol}#{occurrence}",
        relation=None,
        carried_options=carried,
        geometry_authority=_geometry_authority(),
        occurrence=occurrence,
    )


def construct_periodic_table() -> dict[str, GonolReceipt]:
    """Close element gonols for every Z=1-18 record."""

    table: dict[str, GonolReceipt] = {}
    for element in load_atomic_table():
        symbol = str(element["symbol"])
        table[symbol] = construct_element_gonol(symbol)
    return table


def replay_element_gonol(receipt: GonolReceipt) -> GonolReceipt:
    return replay_gonol(receipt=receipt)


def typical_valence_of(gonol: ClosedGonol) -> int:
    for key, value in gonol.carried_options:
        if key == "typical-valence":
            return int(value)
    raise KeyError("typical-valence is missing from element gonol")


def symbol_of(gonol: ClosedGonol) -> str:
    if gonol.source_units:
        return "".join(gonol.source_units)
    raise KeyError("element gonol has no symbol source units")
