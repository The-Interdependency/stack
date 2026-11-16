"""AHBG read-only consumer of the verified UCHC 0.1.0a2 structural field.

This is a separate native contract from the historical English input
candidate: its wheel and 711 MB full-corpus field have different identities.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from .uchc import UchcConsumerError, _canonical

DEFAULT_STRUCTURAL_LOCK = Path(__file__).with_name("UCHC_STRUCTURAL.json")
SCHEMA = "interdependency.ahbg.uchc-structural-evidence/1"


class UchcStructuralError(UchcConsumerError):
    """Structural artifact, operation or replay refused."""


@dataclass(frozen=True)
class UchcStructuralSettings:
    field_dir: Path
    lock: Path = DEFAULT_STRUCTURAL_LOCK
    require_complete: bool = False
    max_text_bytes: int | None = None


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


class UchcStructuralSession:
    def __init__(self, settings: UchcStructuralSettings):
        if not isinstance(settings, UchcStructuralSettings):
            raise UchcStructuralError("structural settings type mismatch")
        if type(settings.require_complete) is not bool:
            raise UchcStructuralError("require_complete must be boolean")
        if settings.max_text_bytes is not None and (
            type(settings.max_text_bytes) is not int or settings.max_text_bytes <= 0
        ):
            raise UchcStructuralError("max_text_bytes must be positive or None")
        self.settings = settings
        self._field: Any = None
        self._provenance: dict[str, Any] = {}

    def __enter__(self) -> "UchcStructuralSession":
        if self._field is not None:
            raise UchcStructuralError("structural field already open")
        try:
            raw = self.settings.lock.read_bytes()
            lock = json.loads(raw)
            if type(lock) is not dict or lock.get("profile") != "english.structural/1":
                raise UchcStructuralError("not a verified English structural lock")
            if lock.get("complete_corpus") is not True or lock.get("authority_transfer") is not False:
                raise UchcStructuralError("partial or authority-promoting structural lock refused")
            # Common installed wheel verifier remains the existing Stack
            # UCHC verifier; no second RECORD/hash implementation is invented.
            from research.zfae.uchc_input import verify_install
            installed = verify_install(
                lock, expected_schema="interdependency.ahbg.uchc-structural-lock/1"
            )
            database = self.settings.field_dir / "construct.db"
            physical = _file_sha256(database)
            if physical != lock["database_sha256"]:
                raise UchcStructuralError("structural database byte identity mismatch")
            from english_gonol.structural_query import StructuralField
            field = StructuralField(self.settings.field_dir)
            self._field = field
            manifest = field.manifest
            if (
                not field.complete_corpus
                or manifest.get("receipt_sha256") != lock["logical_receipt"]
                or manifest.get("metadata", {}).get("implementation_sha256")
                    != lock["implementation_sha256"]
                or manifest.get("schema") != "english-gonol.structural-construct"
                or manifest.get("metadata", {}).get("profile", {}).get("profile")
                    != lock["profile"]
            ):
                raise UchcStructuralError("structural field/profile receipt mismatch")
            self._provenance = {
                "schema": "interdependency.ahbg.uchc-structural-provenance/1",
                "lock_sha256": sha256(raw).hexdigest(),
                "source_repository": lock["source_repository"],
                "source_commit": lock["source_commit"],
                "package_version": installed["package_version"],
                "wheel_sha256": installed["wheel_sha256"],
                "verified_installed_files": installed["verified_files"],
                "database_sha256": physical,
                "logical_receipt": manifest["receipt_sha256"],
                "implementation_sha256": manifest["metadata"]["implementation_sha256"],
                "profile": lock["profile"],
                "authority_transfer": False,
                "neural_inference": False,
                "standing": "full-corpus extracted structural candidate, local geometry only",
            }
            return self
        except Exception as exc:
            self.close()
            if isinstance(exc, UchcStructuralError):
                raise
            raise UchcStructuralError(f"structural artifact refused: {exc}") from exc

    def __exit__(self, *_args: object) -> None:
        self.close()

    def close(self) -> None:
        if self._field is not None:
            self._field.close()
            self._field = None

    def _require_open(self) -> Any:
        if self._field is None:
            raise UchcStructuralError("structural session closed")
        return self._field

    @property
    def provenance(self) -> dict[str, Any]:
        self._require_open()
        return json.loads(_canonical(self._provenance))

    @property
    def capabilities(self) -> dict[str, str]:
        self._require_open()
        return {
            "english.structural_construct": "AVAILABLE",
            "english.word": "AVAILABLE",
            "english.definition": "AVAILABLE",
            "english.replay": "AVAILABLE",
            "english.ordered_text_composition": "AVAILABLE",
            "english.sentence_composition": "AVAILABLE",
            "ucns.global_displacement": "UNIMPLEMENTED",
            "english.ordinal": "NOT_IN_PINNED_ARTIFACT",
            "semantic.sense_selection": "UNIMPLEMENTED",
        }

    def require_capability(self, operation: str) -> None:
        state = self.capabilities.get(operation, "UNKNOWN_OPERATION")
        if state != "AVAILABLE":
            raise UchcStructuralError(f"{operation!r} refused: {state}")

    def construct(self, text: str, *,
                  boundary_decisions: dict[str, Any] | None = None) -> dict[str, Any]:
        field = self._require_open()
        if type(text) is not str:
            raise UchcStructuralError("structural text must be str")
        if self.settings.max_text_bytes is not None and (
            len(text.encode("utf-8")) > self.settings.max_text_bytes
        ):
            raise UchcStructuralError("structural input exceeds configured byte limit")
        try:
            graph = field.construct(text, boundary_decisions=boundary_decisions)
            if graph.get("source") != text or field.replay(graph) != graph:
                raise UchcStructuralError("structural source/replay differs")
            if self.settings.require_complete and (
                graph.get("refusals") or graph.get("logical_state") != "closed"
            ):
                raise UchcStructuralError("structural admission incomplete")
            return graph
        except (ValueError, TypeError, UnicodeError) as exc:
            raise UchcStructuralError(f"structural construction refused: {exc}") from exc

    def replay(self, graph: dict[str, Any]) -> dict[str, Any]:
        return self._require_open().replay(graph)

    def word(self, surface: str) -> dict[str, Any]:
        return self._require_open().word(surface)

    def definition(self, identity: int) -> dict[str, Any]:
        return self._require_open().definition(identity)

    def compose(self, graph: dict[str, Any], *, relation: str) -> dict[str, Any]:
        self._require_open()
        if relation not in {"ordered-text", "sentence"}:
            raise UchcStructuralError(f"unlicensed composition {relation!r}")
        return self._field.compose(graph, relation=relation)

    def annotate_messages(self, messages: list[Mapping[str, Any]], *,
                          source_prefix: str) -> tuple[dict[str, Any], ...]:
        self._require_open()
        if type(source_prefix) is not str or not source_prefix:
            raise UchcStructuralError("source_prefix must be nonempty text")
        result = []
        for ordinal, message in enumerate(messages):
            if not isinstance(message, Mapping):
                raise UchcStructuralError("AHBG message must be an object")
            if "text" not in message:
                continue
            graph = self.construct(message["text"])
            result.append({
                "schema": SCHEMA,
                "source_id": f"{source_prefix}:message:{ordinal}",
                "message_ordinal": ordinal,
                "admission": "COMPLETE" if (
                    graph.get("logical_state") == "closed" and not graph.get("refusals")
                ) else "PARTIAL",
                "frame": graph,
                "frame_sha256": sha256(_canonical(graph)).hexdigest(),
            })
        return tuple(result)
