# ratios: loc_comments=65:1 imports_exports=8:2 calls_definitions=38:3
"""Print replay evidence for 'corpus FMT_GIT_CHECKOUT' or 'unicode' (all valid scalars)."""
import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import subprocess

from cpp_gonol import construct, replay
from cpp_gonol.source import PROFILE, UCNS_COMMIT

FMT = "40626af88bd7df9a5fb80be7b25ac85b122d6c21"
EXTENSIONS = {".cc", ".cpp", ".cxx", ".c++", ".cppm", ".h", ".hh", ".hpp", ".hxx", ".ipp", ".inl"}


def corpus(root):
    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args])

    rows = []
    listing = git("ls-tree", "-r", "-z", FMT).split(b"\0")
    for entry in filter(None, listing):
        metadata, path = entry.split(b"\t", 1)
        path = path.decode("utf-8")
        if PurePosixPath(path).suffix not in EXTENSIONS:
            continue
        _, kind, blob = metadata.decode("ascii").split()
        if kind != "blob":
            raise ValueError(f"unexpected non-blob corpus object: {path}")
        raw = git("cat-file", "blob", blob)
        record = construct(raw, source_id=path)
        if replay(record, original=raw) != raw:
            raise ValueError(f"source replay differs: {path}")
        rows.append({"path": path, "blob": blob, "bytes": len(raw), "occurrences": len(record["occurrences"]),
                     "source_sha256": record["source_sha256"], "receipt": record["receipt"]})
    if not rows:
        raise ValueError("C++ qualification corpus is empty")
    return {"repository": "fmtlib/fmt", "commit": FMT, "extensions": sorted(EXTENSIONS),
            "files": len(rows), "bytes": sum(r["bytes"] for r in rows),
            "occurrences": sum(r["occurrences"] for r in rows), "outcomes": rows}


def unicode_range():
    ordered = sha256()
    seen = projected = 0
    for start in range(0, 0x110000, 4096):
        text = "".join(chr(i) for i in range(start, start + 4096) if not 0xD800 <= i <= 0xDFFF)
        original = text.encode("utf-8")
        record = construct(original, source_id=f"unicode/{start:06x}")
        replay(record, original=original)
        if record["occurrences"] != list(map(ord, text)):
            raise ValueError("physical occurrence order differs")
        for char in text:
            row = record["glyphs"][str(ord(char))]
            be = bytes.fromhex(row["utf32be"])
            turn = Fraction((ord(char) - 32) % 0x110000, 0x110000)
            if (be != char.encode("utf-32-be") or bytes.fromhex(row["utf8"]) != char.encode()
                    or row["turn"] != [turn.numerator, turn.denominator]):
                raise ValueError(f"incorrect native glyph at U+{ord(char):04X}")
            ordered.update(be)
            seen += 1
            projected += row["public_position"] is not None
    if (seen, projected) != (1112064, 157):
        raise ValueError("Unicode coverage differs")
    return {"scalars": seen, "public_positions": projected, "utf32be_sha256": ordered.hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("corpus").add_argument("root", type=Path)
    actions.add_parser("unicode")
    options = parser.parse_args()
    result = corpus(options.root) if options.action == "corpus" else unicode_range()
    print(json.dumps({"profile": PROFILE, "ucns": UCNS_COMMIT, **result}, indent=2, sort_keys=True))
# ratios: loc_comments=65:1 imports_exports=8:2 calls_definitions=38:3
