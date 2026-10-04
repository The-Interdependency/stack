"""Construct EDCM metric descriptions as English hyperspace origin sets.

Only EDCM-owned construction terms enter the semantic origin. Measurement rules
and observed evidence stay outside it. Resolved origins require the exact pinned
English v2 construct receipt; unresolved EDCM semantics remain unclosed hmmm.
"""

# === MODULE_BUILD ===
# id: english_edcm_metric_origin_sets_v0
#   module_name: english_gonol.edcm_metric_origins
#   module_kind: constructor
#   summary: constructs ordered English hyperspace origin sets from EDCM-owned exact construction terms
#   owner: Stack English Gonol Construction
#   public_surface: MetricOriginSet, OriginComponent, load_metric_origin_specs, build_metric_origin_set
#   internal_surface: verified construct identity, exact-run admission, deterministic receipt
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/english-gonol/tests/test_edcm_metric_origins.py
#   rollout: stack-local research candidate
#   rollback: remove module fixture and tests; EDCM source specs remain unchanged
#   requires: english_gonol_language_hyperspace, english_gonol_full_construct, edcm metric-origin spec fixture
#   since: 2026-10-03
#   unresolved: O and L source semantics conflict; lawful observed-state projection to these origins remains hmmm
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: metric_origin_words_define_instrument_not_evidence
#   given: an EDCM metric origin set is constructed
#   then: it contains only source-owned semantic construction and no observation or metric value
#   class: boundary_contract
#
# id: metric_origin_preserves_order_identity_provenance
#   given: a resolved metric description is admitted by the verified English construct
#   then: exact ordered word and whitespace-glyph axes plus producer and verified construct identities survive in the receipt
#   class: correctness
#
# id: metric_origin_unresolved_fails_open_as_hmmm_not_closed
#   given: the EDCM source spec is hmmm
#   then: no semantic components are constructed and closed is false
#   class: safety
#
# id: metric_origin_receipt_binds_schema
#   given: any metric-origin record is emitted
#   then: receipt identity covers schema version and every serialized field except the receipt itself
#   class: identity_contract
#
# id: metric_origin_terms_admitted_by_pinned_corpus
#   given: resolved EDCM construction terms are compared with the exact pinned OEWN 2025 source
#   then: every term is an exact admitted word surface before an origin is licensed
#   class: provenance_contract
# === END CONTRACTS ===

from __future__ import annotations
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import sqlite3

from .full_construct_run import _assert_schema_boundary, _definition_runs, _logical_receipt
from .hyperspace_construct import (
    V2_MANIFEST_RECEIPT,
    glyph_inventory,
    promote_glyph,
    promote_word,
)

SCHEMA = "english-gonol.edcm-metric-origin-set"
VERSION = "0.2.0"
FIXTURE = Path(__file__).resolve().parents[1] / "EDCM_METRIC_ORIGINS_SOURCE.json"


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False,
        separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


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

    def _payload(self) -> dict[str, object]:
        return {
            "schema": SCHEMA,
            "version": VERSION,
            "metric_id": self.metric_id,
            "producer_repository": self.producer_repository,
            "producer_commit": self.producer_commit,
            "construct_receipt": self.construct_receipt,
            "source_text": self.source_text,
            "components": [asdict(x) for x in self.components],
            "closed": self.closed,
            "unresolved": list(self.unresolved),
        }

    def to_dict(self) -> dict[str, object]:
        return {**self._payload(), "receipt_sha256": self.receipt_sha256}


def load_metric_origin_specs(path: Path = FIXTURE) -> dict[str, object]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if (
        data.get("schema") != "edcm.metric-origin-spec-fixture"
        or data.get("version") != "0.3.0"
    ):
        raise ValueError("unsupported EDCM metric-origin fixture")
    return data


def _emit(
    common: dict[str, object],
    *,
    components: tuple[OriginComponent, ...],
    closed: bool,
    unresolved: tuple[str, ...],
) -> MetricOriginSet:
    payload = {
        "schema": SCHEMA,
        "version": VERSION,
        **common,
        "components": [asdict(x) for x in components],
        "closed": closed,
        "unresolved": list(unresolved),
    }
    receipt = sha256(_canonical(payload)).hexdigest()
    return MetricOriginSet(
        **common,
        components=components,
        closed=closed,
        unresolved=unresolved,
        receipt_sha256=receipt,
    )


def build_metric_origin_set(
    state_dir: Path,
    metric_id: str,
    *,
    fixture_path: Path = FIXTURE,
) -> MetricOriginSet:
    source = load_metric_origin_specs(fixture_path)
    specs = source["specs"]
    if metric_id not in specs:
        raise KeyError(f"unknown metric origin {metric_id!r}")
    spec = specs[metric_id]
    unresolved = tuple(spec.get("unresolved", ()))
    terms = tuple(spec.get("construction_terms", ()))
    source_text = " ".join(terms)

    if spec["standing"] != "resolved":
        common = {
            "metric_id": metric_id,
            "producer_repository": source["producer_repository"],
            "producer_commit": source["producer_commit"],
            "construct_receipt": "hmmm",
            "source_text": source_text,
        }
        return _emit(common, components=(), closed=False, unresolved=unresolved)

    if not terms or any(not isinstance(term, str) or not term for term in terms):
        raise ValueError(f"metric {metric_id}: resolved origin requires exact construction terms")

    db_path = Path(state_dir) / "construct.db"
    if not db_path.exists():
        raise ValueError(f"construct.db not found under {state_dir}")
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        _assert_schema_boundary(db)
        observed_receipt = _logical_receipt(db)
        if observed_receipt != V2_MANIFEST_RECEIPT:
            raise ValueError(
                f"metric {metric_id}: construct receipt mismatch; "
                f"expected {V2_MANIFEST_RECEIPT}, got {observed_receipt}"
            )
        inventory = glyph_inventory(db)
        components: list[OriginComponent] = []
        for ordinal, (kind, surface, _start, _end) in enumerate(_definition_runs(source_text)):
            if kind == "word":
                row = db.execute(
                    "SELECT id FROM words WHERE surface = ?", (surface,)
                ).fetchone()
                if row is None:
                    raise ValueError(
                        f"metric {metric_id}: unadmitted exact word surface {surface!r}"
                    )
                word, axis = promote_word(db, row[0])
                components.append(
                    OriginComponent(
                        ordinal, "word", surface, "O_W", axis, f"word:{word.word_id}"
                    )
                )
            else:
                glyph, axis = promote_glyph(db, inventory, surface)
                components.append(
                    OriginComponent(
                        ordinal, "glyph", surface, "O_G", axis, f"glyph:{glyph.identity}"
                    )
                )
    finally:
        db.close()

    common = {
        "metric_id": metric_id,
        "producer_repository": source["producer_repository"],
        "producer_commit": source["producer_commit"],
        "construct_receipt": observed_receipt,
        "source_text": source_text,
    }
    return _emit(
        common,
        components=tuple(components),
        closed=True,
        unresolved=unresolved,
    )


__all__ = [
    "SCHEMA",
    "VERSION",
    "OriginComponent",
    "MetricOriginSet",
    "load_metric_origin_specs",
    "build_metric_origin_set",
]
