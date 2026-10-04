"""Construct EDCM metric words as English hyperspace origin sets.

Usage: load_metric_origin_specs(), then build_metric_origin_set(state_dir, id,
construct_receipt=...). Only EDCM semantic-definition words enter the origin.
Declared/implemented measurement rules stay outside the semantic construction.
"""

# === MODULE_BUILD ===
# id: english_edcm_metric_origin_sets_v0
#   module_name: english_gonol.edcm_metric_origins
#   module_kind: constructor
#   summary: constructs ordered English hyperspace origin sets from EDCM-owned semantic metric descriptions
#   owner: Stack English Gonol Construction
#   public_surface: MetricOriginSet, OriginComponent, load_metric_origin_specs, build_metric_origin_set
#   internal_surface: exact-run admission and deterministic receipt
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/english-gonol/tests/test_edcm_metric_origins.py
#   rollout: stack-local research candidate
#   rollback: remove module fixture and tests; EDCM source specs remain unchanged
#   requires: english_gonol_language_hyperspace, edcm metric-origin spec fixture
#   since: 2026-10-03
#   unresolved: O and L source semantics conflict; full-corpus closure requires the generated construct.db
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: metric_origin_words_define_instrument_not_evidence
#   given: an EDCM metric origin set is constructed
#   then: it contains only source-owned semantic construction and no observation or metric value
#   class: boundary_contract
#
# id: metric_origin_preserves_order_identity_provenance
#   given: a resolved metric description is admitted by the English construct
#   then: exact ordered word and whitespace-glyph axes plus producer and construct identities survive in the receipt
#   class: correctness
#
# id: metric_origin_unresolved_fails_open_as_hmmm_not_closed
#   given: the EDCM source spec is hmmm
#   then: no semantic components are constructed and closed is false
#   class: safety
# === END CONTRACTS ===

from __future__ import annotations
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import sqlite3

from .full_construct_run import _definition_runs
from .hyperspace_construct import glyph_inventory, promote_glyph, promote_word

SCHEMA = "english-gonol.edcm-metric-origin-set"
VERSION = "0.1.0"
FIXTURE = Path(__file__).resolve().parents[1] / "EDCM_METRIC_ORIGINS_SOURCE.json"

def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")

@dataclass(frozen=True, slots=True)
class OriginComponent:
    ordinal: int
    kind: str
    surface: str
    axis_origin: str
    axis_index: int | None
    identity: str

@dataclass(frozen=True, slots=True)
class MetricOriginSet:
    metric_id: str
    producer_repository: str
    producer_commit: str
    construct_receipt: str
    source_text: str
    components: tuple[OriginComponent, ...]
    closed: bool
    unresolved: tuple[str, ...]
    receipt_sha256: str

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": SCHEMA, "version": VERSION,
            "metric_id": self.metric_id,
            "producer_repository": self.producer_repository,
            "producer_commit": self.producer_commit,
            "construct_receipt": self.construct_receipt,
            "source_text": self.source_text,
            "components": [asdict(x) for x in self.components],
            "closed": self.closed,
            "unresolved": list(self.unresolved),
            "receipt_sha256": self.receipt_sha256,
        }

def load_metric_origin_specs(path: Path = FIXTURE) -> dict[str, object]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema") != "edcm.metric-origin-spec-fixture" or data.get("version") != "0.2.0":
        raise ValueError("unsupported EDCM metric-origin fixture")
    return data

def _receipt(payload: dict[str, object]) -> str:
    return sha256(_canonical(payload)).hexdigest()

def build_metric_origin_set(
    state_dir: Path,
    metric_id: str,
    *,
    construct_receipt: str,
    fixture_path: Path = FIXTURE,
) -> MetricOriginSet:
    source = load_metric_origin_specs(fixture_path)
    specs = source["specs"]
    if metric_id not in specs:
        raise KeyError(f"unknown metric origin {metric_id!r}")
    spec = specs[metric_id]
    text = " ".join((*spec["surface_terms"], spec["semantic_definition"]))
    unresolved = tuple(spec.get("unresolved", ()))
    common = {
        "metric_id": metric_id,
        "producer_repository": source["producer_repository"],
        "producer_commit": source["producer_commit"],
        "construct_receipt": construct_receipt,
        "source_text": text,
    }
    if spec["standing"] != "resolved":
        payload = {**common, "components": [], "closed": False, "unresolved": list(unresolved)}
        return MetricOriginSet(**common, components=(), closed=False, unresolved=unresolved,
                               receipt_sha256=_receipt(payload))

    db_path = Path(state_dir) / "construct.db"
    if not db_path.exists():
        raise ValueError(f"construct.db not found under {state_dir}")
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        inventory = glyph_inventory(db)
        components = []
        for ordinal, (kind, surface, _start, _end) in enumerate(_definition_runs(text)):
            if kind == "word":
                row = db.execute("SELECT id FROM words WHERE surface = ?", (surface,)).fetchone()
                if row is None:
                    raise ValueError(f"metric {metric_id}: unadmitted word surface {surface!r}")
                word, axis = promote_word(db, row[0])
                components.append(OriginComponent(
                    ordinal, "word", surface, "O_W", axis, f"word:{word.word_id}"
                ))
            else:
                glyph, axis = promote_glyph(db, inventory, surface)
                components.append(OriginComponent(
                    ordinal, "glyph", surface, "O_G", axis, f"glyph:{glyph.identity}"
                ))
    finally:
        db.close()

    payload = {**common, "components": [asdict(x) for x in components],
               "closed": True, "unresolved": list(unresolved)}
    return MetricOriginSet(
        **common,
        components=tuple(components),
        closed=True,
        unresolved=unresolved,
        receipt_sha256=_receipt(payload),
    )

__all__ = ["SCHEMA","VERSION","OriginComponent","MetricOriginSet",
           "load_metric_origin_specs","build_metric_origin_set"]
