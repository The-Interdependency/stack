"""DeepSeek A0 diary.

The diary is A0's append-only memory surface. Entries are hash-chained so a
diary can be verified for truncation or tampering independently of the world
event log. The diary is ordinary structure: it contributes exactly the
breadth it retains, no more.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

DIARY_SCHEMA = "interdependency.ahbg.a0.diary/1.0.0"


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


@dataclass(frozen=True)
class DiaryEntry:
    seq: int
    turn: int
    text: str
    prev_digest: str

    def __post_init__(self) -> None:
        if isinstance(self.seq, bool) or not isinstance(self.seq, int) or self.seq < 0:
            raise ValueError("diary seq must be a non-negative integer")
        if isinstance(self.turn, bool) or not isinstance(self.turn, int) or self.turn < 0:
            raise ValueError("diary turn must be a non-negative integer")
        if not isinstance(self.text, str) or not self.text:
            raise ValueError("diary text must be non-empty")
        if not isinstance(self.prev_digest, str):
            raise ValueError("diary prev_digest must be a string")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": DIARY_SCHEMA,
            "seq": self.seq,
            "turn": self.turn,
            "text": self.text,
            "prev_digest": self.prev_digest,
        }

    def digest(self) -> str:
        return hashlib.sha256(canonical_json(self.to_dict()).encode("utf-8")).hexdigest()


class Diary:
    """Append-only, hash-chained diary."""

    def __init__(self) -> None:
        self._entries: list[DiaryEntry] = []
        self._head: str = ""

    @property
    def head(self) -> str:
        return self._head

    def __len__(self) -> int:
        return len(self._entries)

    def write(self, turn: int, text: str) -> DiaryEntry:
        entry = DiaryEntry(seq=len(self._entries), turn=turn, text=text, prev_digest=self._head)
        self._entries.append(entry)
        self._head = entry.digest()
        return entry

    def verify(self) -> None:
        expected = ""
        for index, entry in enumerate(self._entries):
            if entry.seq != index:
                raise ValueError(f"diary seq {entry.seq} out of order at index {index}")
            if entry.prev_digest != expected:
                raise ValueError(f"diary seq {entry.seq} breaks the hash chain")
            expected = entry.digest()
        if expected != self._head:
            raise ValueError("diary head digest does not match its chain")

    def to_jsonl(self) -> str:
        self.verify()
        return "\n".join(canonical_json(entry.to_dict()) for entry in self._entries) + (
            "\n" if self._entries else ""
        )

    @classmethod
    def from_jsonl(cls, text: str) -> "Diary":
        diary = cls()
        if not text:
            return diary
        for line in text.splitlines():
            data = json.loads(line)
            entry = DiaryEntry(
                seq=data["seq"],
                turn=data["turn"],
                text=data["text"],
                prev_digest=data["prev_digest"],
            )
            diary._entries.append(entry)
            diary._head = entry.digest()
        diary.verify()
        return diary
