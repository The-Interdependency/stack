"""AHBG's source-bound consumer of the installed UCHC English construction.

Only UCHC creates native language objects. This module verifies the already
locked candidate wheel and construct, publishes exact evidence, and refuses
identity or admission failures. No game action or semantic sense is inferred.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

STACK_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOCK = STACK_ROOT / "research" / "zfae" / "UCHC_INPUT.json"
SCHEMA = "interdependency.ahbg.uchc-evidence/1"


class UchcConsumerError(ValueError):
    """UCHC dependency, provenance, input or recovery contract failed."""


@dataclass(frozen=True)
class UchcSettings:
    database: Path
    lock: Path = DEFAULT_LOCK
    require_complete: bool = False
    max_text_bytes: int | None = None


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


class UchcSession:
    """One verified corpus snapshot reused for the whole benchmark run.

    Open requires the real clean-installed UCHC wheel and complete corpus.
    The Stack ZFAE verifier is reused, not reimplemented or weakened.
    """

    def __init__(self, settings: UchcSettings):
        if not isinstance(settings, UchcSettings):
            raise UchcConsumerError("UCHC settings must be UchcSettings")
        if type(settings.require_complete) is not bool:
            raise UchcConsumerError("require_complete must be boolean")
        if settings.max_text_bytes is not None and (
            type(settings.max_text_bytes) is not int or settings.max_text_bytes <= 0
        ):
            raise UchcConsumerError("max_text_bytes must be positive or None")
        self.settings = settings
        self._corpus: Any = None
        self._lock: dict[str, Any] = {}
        self._provenance: dict[str, Any] = {}

    def __enter__(self) -> "UchcSession":
        if self._corpus is not None:
            raise UchcConsumerError("UCHC session already open")
        try:
            raw = self.settings.lock.read_bytes()
            lock = json.loads(raw)
            if not isinstance(lock, dict):
                raise UchcConsumerError("UCHC lock must be an object")
            # This import is deliberately deferred: AHBG without UCHC enabled
            # must not require an installed candidate wheel or the large corpus.
            from research.zfae.uchc_input import load_input, verify_install
            checked = verify_install(lock)
            corpus = load_input(self.settings.database, lock)
            if corpus.identity.database_sha256 != lock["database_sha256"]:
                corpus.close()
                raise UchcConsumerError("UCHC construct identity differs from lock")
            self._corpus = corpus
            self._lock = lock
            self._provenance = {
                "schema": "interdependency.ahbg.uchc-provenance/1",
                "lock_sha256": sha256(raw).hexdigest(),
                "source_repository": lock["source_repository"],
                "source_commit": lock["source_commit"],
                "package_version": checked["package_version"],
                "wheel_sha256": checked["wheel_sha256"],
                "verified_installed_files": checked["verified_files"],
                "construct": asdict(corpus.identity),
                "authority_transfer": False,
                "neural_inference": False,
                "standing": "receipt-bound input candidate, not semantic inference",
            }
            return self
        except Exception as exc:
            self.close()
            if isinstance(exc, UchcConsumerError):
                raise
            raise UchcConsumerError(f"UCHC verification/open refused: {exc}") from exc

    def __exit__(self, *_args: object) -> None:
        self.close()

    def close(self) -> None:
        if self._corpus is not None:
            self._corpus.close()
            self._corpus = None

    @property
    def provenance(self) -> dict[str, Any]:
        self._require_open()
        return json.loads(_canonical(self._provenance))

    def _require_open(self) -> Any:
        if self._corpus is None:
            raise UchcConsumerError("UCHC session is closed")
        return self._corpus

    def resolve_text(self, text: str, *, source_id: str) -> Any:
        corpus = self._require_open()
        if type(text) is not str or type(source_id) is not str or not source_id:
            raise UchcConsumerError("text must be str and source_id nonempty str")
        if self.settings.max_text_bytes is not None and (
            len(text.encode("utf-8")) > self.settings.max_text_bytes
        ):
            raise UchcConsumerError("UCHC input exceeds explicitly configured byte limit")
        try:
            frame = corpus.resolve_text(text, source_id=source_id)
            if self.settings.require_complete:
                frame.require_complete()
            if frame.recover_utf8() != text.encode("utf-8"):
                raise UchcConsumerError("UCHC source recovery mismatch")
            if corpus.replay(frame.to_bytes()) != frame:
                raise UchcConsumerError("UCHC frame replay mismatch")
            return frame
        except (ValueError, UnicodeError, TypeError) as exc:
            raise UchcConsumerError(f"UCHC input refused: {exc}") from exc

    def resolve_utf8(self, raw: bytes, *, source_id: str) -> Any:
        if type(raw) is not bytes:
            raise UchcConsumerError("UTF-8 input must be bytes")
        return self.resolve_text(raw.decode("utf-8", errors="strict"), source_id=source_id)

    def word(self, surface: str) -> Any:
        return self._require_open().word(surface)

    def definition(self, definition_id: int) -> Any:
        return self._require_open().definition(definition_id)

    def recover_definition(self, definition: Any) -> str:
        return self._require_open().recover_definition(definition)

    def replay(self, frame_bytes: bytes) -> Any:
        return self._require_open().replay(frame_bytes)

    def annotate_messages(self, messages: list[Mapping[str, Any]], *,
                          source_prefix: str) -> tuple[dict[str, Any], ...]:
        self._require_open()
        if type(source_prefix) is not str or not source_prefix:
            raise UchcConsumerError("source_prefix must be nonempty text")
        evidence = []
        for ordinal, message in enumerate(messages):
            if not isinstance(message, Mapping):
                raise UchcConsumerError("AHBG inbox entry is not an object")
            if "text" not in message:
                continue
            text = message["text"]
            if type(text) is not str:
                raise UchcConsumerError("AHBG message text is not a string")
            source_id = f"{source_prefix}:message:{ordinal}"
            frame = self.resolve_text(text, source_id=source_id)
            payload = frame.to_dict()
            evidence.append({
                "schema": SCHEMA,
                "message_ordinal": ordinal,
                "source_id": source_id,
                "admission": ("COMPLETE" if frame.glyphs_admitted and
                              frame.words_admitted else "PARTIAL"),
                "frame": payload,
                "frame_sha256": sha256(_canonical(payload)).hexdigest(),
            })
        return tuple(evidence)


def main(argv: list[str] | None = None) -> int:
    """Read-only native query CLI; exit 2 on verification/admission failure."""
    import argparse
    from dataclasses import asdict
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--max-text-bytes", type=int)
    actions = parser.add_subparsers(dest="operation", required=True)
    text_command = actions.add_parser("text")
    text_command.add_argument("text")
    text_command.add_argument("--source-id", required=True)
    word_command = actions.add_parser("word")
    word_command.add_argument("surface")
    definition_command = actions.add_parser("definition")
    definition_command.add_argument("identity", type=int)
    replay_command = actions.add_parser("replay")
    replay_command.add_argument("frame_file", type=Path)
    args = parser.parse_args(argv)
    try:
        with UchcSession(UchcSettings(
            args.database, args.lock, args.require_complete, args.max_text_bytes
        )) as session:
            if args.operation == "text":
                frame = session.resolve_text(args.text, source_id=args.source_id)
                result = frame.to_dict()
            elif args.operation == "word":
                native = session.word(args.surface)
                result = None if native is None else asdict(native)
            elif args.operation == "definition":
                native = session.definition(args.identity)
                result = {"record": asdict(native), "recovered": session.recover_definition(native)}
            else:
                frame = session.replay(args.frame_file.read_bytes())
                result = frame.to_dict()
            print(_canonical({"provenance": session.provenance, "result": result}).decode())
        return 0
    except (OSError, UnicodeError, ValueError, KeyError) as exc:
        print(_canonical({"status": "BLOCKED", "error": str(exc),
                         "hmmm": "No semantic or action inference authorized"}).decode())
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
