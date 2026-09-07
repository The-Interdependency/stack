#!/usr/bin/env python3
"""Validate and assemble the audited paper's ordered Markdown fragments."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
MANIFEST = PROJECT / "paper" / "manifest.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def assemble() -> bytes:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    parts: list[bytes] = []
    for item in manifest["fragments"]:
        path = PROJECT / item["path"]
        data = path.read_bytes()
        observed = sha256(data)
        if observed != item["sha256"]:
            raise SystemExit(
                f"fragment drift: {item['path']}: expected {item['sha256']}, observed {observed}"
            )
        blob = git_blob_sha1(data)
        expected_blob = item.get("git_blob_sha1")
        if expected_blob is None:
            raise SystemExit(f"fragment missing git blob identity: {item['path']}")
        if blob != expected_blob:
            raise SystemExit(
                f"fragment blob drift: {item['path']}: expected {expected_blob}, observed {blob}"
            )
        parts.append(data)
    paper = b"".join(parts)
    observed = sha256(paper)
    expected = manifest["assembled_sha256"]
    if observed != expected:
        raise SystemExit(f"assembled paper drift: expected {expected}, observed {observed}")
    return paper


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="destination Markdown path")
    args = parser.parse_args()
    paper = assemble()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(paper)
    print(f"wrote {args.output} ({len(paper)} bytes, sha256={sha256(paper)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
