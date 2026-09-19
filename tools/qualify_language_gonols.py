# ratios: loc_comments=179:23 imports_exports=18:10 calls_definitions=110:10
"""Replay the declared language construction profiles without executing corpus code.

Usage: python tools/qualify_language_gonols.py --help
Run python-pass twice in separate processes, then compare their output JSONL.
Source and producer checkouts stay read-only; temporary constructs are removed
after each file. Receipts retain every admission outcome and unresolved scalar.
"""
# === MODULE_BUILD ===
# id: language_gonol_qualification
#   module_name: qualify_language_gonols
#   module_kind: instrument
#   summary: checks full source coverage, independent replay, exact identities and actual test outcomes
#   owner: Stack language construction research
#   public_surface: python-pass, compare, english-compare, check-tests commands
#   internal_surface: source inventory, independent address/tab witnesses, canonical receipts
#   auth_boundary: read-only source and authority checkouts
#   storage_boundary: explicit output directory and automatically removed temporary constructs
#   network_boundary: none
#   user_data_boundary: supplied public corpus only
#   admin_only: false
#   tests: complete protocol in docs/language-gonol-qualification.md; negative comparison and skipped-XML probes
#   rollout: explicit qualification command; check-tests also runs in language CI
#   rollback: remove qualification calls and preserve existing evidence history
# === END MODULE_BUILD ===

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import tokenize
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CPYTHON = "2abcf904b8dac8c999d2b3aac76681abb333798a"
UCNS_PYTHON = "62e08ee1cf3b5d7b6e48c927b1047509e6328b5c"
OEWN = "dc343f2683279ecbb13fab4e2fd778d7b162d287"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def inventory(root, prefix):
    entries = git(root, "ls-tree", "-rz", "HEAD", "--", prefix).split(b"\0")
    records = []
    for entry in entries:
        if not entry:
            continue
        meta, raw_path = entry.split(b"\t", 1)
        mode, kind, blob = meta.decode().split()
        path = raw_path.decode()
        if not path.endswith(".py"):
            continue
        require(kind == "blob" and mode in {"100644", "100755"}, "non-file source")
        local = root / path
        require(local.is_file() and not local.is_symlink(), "source absent or symlink")
        raw = local.read_bytes()
        import hashlib
        observed = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        require(observed == blob, "source differs from committed blob: " + path)
        records.append({"path": path, "git_blob": blob, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})
    require(bool(records), "empty declared corpus")
    return sorted(records, key=lambda record: record["path"])


def check_source_rows(db, raw, encoding):
    source = raw.decode(encoding)
    require(db.execute("SELECT data FROM source_bytes").fetchall() == [(raw,)], "raw source mismatch")
    rows = db.execute("SELECT ordinal, scalar, line, column FROM occurrences ORDER BY ordinal").fetchall()
    require("".join(row[1] for row in rows) == source, "decoded source mismatch")
    offsets = {}
    for line, match in enumerate(re.finditer(r"[^\r\n]*(?:\r\n|\r|\n|$)", source), 1):
        for column, offset in enumerate(range(match.start(), match.end()), 1):
            offsets[offset] = (line, column, match.start())
    require(len(rows) == len(source) == len(offsets), "source coverage mismatch")
    for ordinal, scalar, line, column in rows:
        require(offsets[ordinal][:2] == (line, column), "physical source address mismatch")
    controls = db.execute("SELECT o.ordinal, c.spaces_to_next_stop FROM controls c JOIN occurrences o ON o.id=c.occurrence_id WHERE o.scalar=char(9)").fetchall()
    require(len(controls) == source.count("\t"), "tab coverage mismatch")
    for ordinal, width in controls:
        prefix = source[offsets[ordinal][2]:ordinal].rsplit("\f", 1)[-1]
        expected = len((prefix + "\t").expandtabs(8)) - len(prefix.expandtabs(8))
        require(width == expected, "tab expansion mismatch")


def python_pass(corpus, producer, out):
    require(sys.version_info[:3] == (3, 12, 14), "qualification requires Python 3.12.14")
    require(git(corpus, "rev-parse", "HEAD").decode().strip() == CPYTHON, "CPython pin mismatch")
    require(git(producer, "rev-parse", "HEAD").decode().strip() == UCNS_PYTHON, "UCNS pin mismatch")
    before = inventory(corpus, "Lib/test")
    require(not out.exists(), "qualification output must be new")
    out.mkdir(parents=True)
    require(shutil.disk_usage(out).free > 4 * (65536 + max(r["bytes"] for r in before) * 256), "insufficient scratch storage")
    sys.path.insert(0, str(ROOT / "research/python-gonol"))
    from python_gonol import affixiate_python_bytes, verify_construct, PythonGonolConstructionError
    implementation = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                      for p in sorted((ROOT / "research/python-gonol/python_gonol").glob("*.py"))}
    implementation[str(Path(__file__).relative_to(ROOT))] = sha256(Path(__file__).read_bytes()).hexdigest()
    header = {"schema": "language-gonol.python-qualification", "version": 1,
              "cpython": CPYTHON, "ucns": UCNS_PYTHON, "python": "3.12.14",
              "inventory_sha256": sha256(canonical(before)).hexdigest(), "input_files": len(before),
              "input_bytes": sum(r["bytes"] for r in before), "implementation_sha256": implementation}
    (out / "inventory.json").write_bytes(canonical(before) + b"\n")
    counts = Counter()
    with (out / "outcomes.jsonl").open("wb") as stream:
        for index, entry in enumerate(before):
            raw = (corpus / entry["path"]).read_bytes()
            require(sha256(raw).hexdigest() == entry["sha256"], "source changed during run")
            record = dict(entry)
            try:
                encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
                raw.decode(encoding)
            except (SyntaxError, UnicodeDecodeError, LookupError) as exc:
                with tempfile.TemporaryDirectory(prefix="rejected-", dir=out) as temporary:
                    try:
                        affixiate_python_bytes(raw, source_id=entry["path"], state_dir=Path(temporary), ucns_source_root=producer)
                    except PythonGonolConstructionError:
                        pass
                    else:
                        raise ValueError("constructor admitted oracle-rejected encoding")
                record.update(outcome="REJECTED_ENCODING", reason=type(exc).__name__)
                counts["rejected_encoding"] += 1
            else:
                with tempfile.TemporaryDirectory(prefix="construct-", dir=out) as temporary:
                    state = Path(temporary)
                    result = affixiate_python_bytes(raw, source_id=entry["path"], state_dir=state, ucns_source_root=producer)
                    with sqlite3.connect(f"file:{state / 'construct.db'}?mode=ro", uri=True) as db:
                        check_source_rows(db, raw, result.encoding)
                    require(verify_construct(state, producer) == result.receipt_sha256, "replay mismatch")
                    manifest = json.loads((state / "manifest.json").read_text())
                    record.update(outcome="CONSTRUCTED", manifest=manifest)
                    counts["constructed"] += 1
                    counts["off_carrier_files"] += bool(result.not_on_pinned_carrier)
                    counts["tokenize_false"] += not result.tokenize_ok
                    counts["ast_false"] += not result.ast_ok
            stream.write(canonical(record) + b"\n"); stream.flush()
            if (index + 1) % 100 == 0:
                print(f"qualified {index + 1}/{len(before)}", flush=True)
    require(inventory(corpus, "Lib/test") == before, "source inventory changed")
    for path, digest in implementation.items():
        require(sha256((ROOT / path).read_bytes()).hexdigest() == digest, "implementation changed during run")
    header.update(counts=dict(counts), outcomes_sha256=sha256((out / "outcomes.jsonl").read_bytes()).hexdigest(),
                  hmmm=["off-carrier glyph admission", "deeper geometry", "grammar/runtime equivalence is outside source-floor qualification"])
    require(counts["constructed"] + counts["rejected_encoding"] == len(before), "unaccounted source")
    (out / "receipt.json").write_bytes(canonical(header) + b"\n")
    print(json.dumps(header, indent=2))


def compare(a, b):
    for filename in ("receipt.json", "inventory.json", "outcomes.jsonl"):
        require((a / filename).read_bytes() == (b / filename).read_bytes(), "independent pass mismatch: " + filename)
    receipt = json.loads((a / "receipt.json").read_text())
    for root in (a, b):
        require(sha256((root / "outcomes.jsonl").read_bytes()).hexdigest() == receipt["outcomes_sha256"], "outcome digest mismatch")
        outcomes = [json.loads(line) for line in (root / "outcomes.jsonl").read_text().splitlines()]
        require(len(outcomes) == receipt["input_files"], "outcome coverage mismatch")
        inputs = json.loads((root / "inventory.json").read_text())
        require(sha256(canonical(inputs)).hexdigest() == receipt["inventory_sha256"], "inventory digest mismatch")
        require([{key: row[key] for key in ("path", "git_blob", "sha256", "bytes")} for row in outcomes] == inputs, "outcome/source inventory mismatch")
    print(json.dumps({"status": "SURVIVED", "receipt": receipt}, indent=2))


def english_compare(a, b):
    sys.path.insert(0, str(ROOT / "research/english-gonol"))
    from english_gonol.full_construct_run import verify_replay
    first, second = verify_replay(a), verify_replay(b)
    require(first == second, "English manifests differ")
    expected = json.loads((ROOT / "research/english-gonol/experiments/full-construct-v2/manifest.json").read_text())
    require(first == expected, "English build differs from frozen complete-corpus receipt")
    for root in (a, b):
        with sqlite3.connect(f"file:{root / 'construct.db'}?mode=ro", uri=True) as db:
            require(db.execute("PRAGMA integrity_check").fetchone()[0] == "ok", "SQLite integrity")
            for table, count in first["counts"].items():
                require(db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == count, "count mismatch")
    print(json.dumps({"status": "SURVIVED", "independent_builds": 2, "manifest": first}, indent=2))


def check_tests(paths):
    count = 0
    for path in paths:
        tree = ET.parse(path)
        cases = tree.findall(".//testcase")
        require(bool(cases), "empty test suite")
        require(not tree.findall(".//skipped") and not tree.findall(".//failure") and not tree.findall(".//error"), "unpassed test outcomes")
        count += len(cases)
    print(json.dumps({"passed": count, "skipped": 0, "failed": 0}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("python-pass")
    p.add_argument("corpus", type=Path); p.add_argument("producer", type=Path); p.add_argument("out", type=Path)
    for name in ("compare", "english-compare"):
        p = commands.add_parser(name); p.add_argument("a", type=Path); p.add_argument("b", type=Path)
    p = commands.add_parser("check-tests"); p.add_argument("paths", type=Path, nargs="+")
    args = parser.parse_args()
    if args.command == "python-pass":
        python_pass(args.corpus.resolve(), args.producer.resolve(), args.out.resolve())
    elif args.command == "check-tests":
        check_tests(args.paths)
    elif args.command == "compare":
        compare(args.a, args.b)
    else:
        english_compare(args.a, args.b)


if __name__ == "__main__":
    main()
# ratios: loc_comments=179:23 imports_exports=18:10 calls_definitions=110:10
