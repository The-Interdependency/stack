# ratios: loc_comments=238:42 imports_exports=19:12 calls_definitions=139:12
"""Replay the declared Python construction profile without executing corpus code.

Usage: python tools/qualify_python_gonols.py --help
Run python-pass twice in separate processes, then compare their output JSONL.
Source and producer checkouts stay read-only; temporary constructs are removed
after each file. Receipts retain every admission outcome and unresolved scalar.
"""
# === MODULE_BUILD ===
# id: language_gonol_qualification
#   module_name: qualify_python_gonols
#   module_kind: instrument
#   summary: checks full source coverage, independent replay, exact identities and actual test outcomes
#   owner: Stack language construction research
#   public_surface: python-pass, compare, check-tests commands
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
# === CONTRACTS ===
# id: language_qualification_complete_inventory
#   given: two supplied CPython qualification receipts
#   when: compare evaluates their source coverage
#   then: both match the frozen complete pinned Lib/test inventory
# id: language_qualification_manifest_integrity
#   given: a CONSTRUCTED outcome
#   when: compare evaluates the embedded manifest
#   then: schema, provenance, source identity, counts and canonical receipt agree
# id: language_qualification_tab_witness
#   given: source containing form-feed and tab characters
#   when: independent source rows are checked
#   then: widths agree with Python expandtabs on the physical line
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing
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
# Independently frozen from CPython's complete pinned Lib/test tree; the caller
# cannot redefine "complete" by supplying a smaller self-consistent inventory.
CPYTHON_INVENTORY = (1052, 20732440, "1dd99a2c8e27e10c669dfd46a29b2e0107da15279f18aac94eb5453052bb41e1")
# Frozen encoding-admission outcomes for those exact source bytes. All other
# files in the bound inventory must carry a complete constructed manifest.
CPYTHON_ENCODING_REJECTIONS = {
    "Lib/test/tokenizedata/bad_coding.py": "ffd93515dbe0bc61779aafb3cdf11e4c32d229e120139bfc38d3ea54b95a76e3",
    "Lib/test/tokenizedata/bad_coding2.py": "8cf248d2b943c380e0f50a3b80293de6d739f8a6a7ebfc182d81ee7663e04aa1",
    "Lib/test/tokenizedata/badsyntax_pep3120.py": "8d39a6286aca58ab1a43ffd9f84e0758243334f579c6a7e3c082cf55a96a9f6d",
}


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
        prefix = source[offsets[ordinal][2]:ordinal]
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
              "cpython": CPYTHON, "ucns": UCNS_PYTHON, "python": "3.12.14", "sqlite_runtime": sqlite3.sqlite_version,
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
                    with closing(sqlite3.connect(f"file:{state / 'construct.db'}?mode=ro", uri=True)) as db:
                        db.execute("PRAGMA temp_store=MEMORY")
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


def distinct_outputs(a, b, files):
    require(a.resolve() != b.resolve(), "two distinct execution directories required")
    for name in files:
        require(not (a / name).samefile(b / name), "aliased evidence file: " + name)


def implementation_hashes():
    paths = list((ROOT / "research/python-gonol/python_gonol").glob("*.py")) + [Path(__file__)]
    return {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def check_manifest(row):
    """Validate retained metadata; full database replay belongs to python-pass."""
    sys.path.insert(0, str(ROOT / "research/python-gonol"))
    from python_gonol import construct as producer
    manifest = row.get("manifest")
    fields = {"schema", "version", "source_id", "encoding", "source_bytes_sha256",
              "decoded_source_sha256", "ucns", "counts", "not_on_pinned_carrier",
              "verification", "preflight_storage_bytes", "hmmm", "construct_sha256",
              "receipt_sha256"}
    require(isinstance(manifest, dict) and set(manifest) == fields, "manifest fields mismatch")
    require((manifest["schema"], manifest["version"]) == (producer.SCHEMA, producer.VERSION), "manifest schema mismatch")
    require(manifest["ucns"] == {"commit": producer.UCNS_PUBLIC_GONOL_COMMIT,
            "public_gonol_module_sha256": producer.UCNS_PUBLIC_GONOL_MODULE_SHA256,
            "public_gonol_sha256": producer.PUBLIC_GONOL_SHA256}, "manifest UCNS mismatch")
    require(manifest["source_id"] == row["path"] and manifest["source_bytes_sha256"] == row["sha256"], "manifest source identity mismatch")
    for field in ("source_bytes_sha256", "decoded_source_sha256", "construct_sha256", "receipt_sha256"):
        require(isinstance(manifest[field], str) and re.fullmatch(r"[0-9a-f]{64}", manifest[field]), "manifest digest mismatch")
    require(isinstance(manifest["encoding"], str) and bool(manifest["encoding"]), "manifest encoding missing")
    counts = manifest["counts"]
    require(isinstance(counts, dict) and set(counts) == {"characters", "occurrences", "controls", "newlines"}, "manifest counts missing")
    require(all(type(n) is int and n >= 0 for n in counts.values()), "manifest counts invalid")
    require(counts["newlines"] <= counts["controls"] <= counts["occurrences"] and counts["characters"] == 157, "manifest counts inconsistent")
    require(type(manifest["preflight_storage_bytes"]) is int and manifest["preflight_storage_bytes"] == 65536 + counts["occurrences"] * 256, "manifest preflight mismatch")
    flags = manifest["verification"]
    require(isinstance(flags, dict) and set(flags) == {"tokenize_ok", "ast_ok"} and all(type(flag) is bool for flag in flags.values()), "manifest verification invalid")
    scalars = manifest["not_on_pinned_carrier"]
    require(isinstance(scalars, list) and all(isinstance(c, str) and len(c) == 1 and not 0xD800 <= ord(c) <= 0xDFFF for c in scalars), "manifest off-carrier scalars invalid")
    require(scalars == sorted(set(scalars)), "manifest off-carrier scalars not canonical")
    require(isinstance(manifest["hmmm"], str) and bool(manifest["hmmm"]), "manifest unresolved constraints missing")
    payload = {key: value for key, value in manifest.items() if key != "receipt_sha256"}
    require(sha256(canonical(payload)).hexdigest() == manifest["receipt_sha256"], "manifest receipt mismatch")
    return manifest


def compare(a, b):
    distinct_outputs(a, b, ("receipt.json", "inventory.json", "outcomes.jsonl"))
    for filename in ("receipt.json", "inventory.json", "outcomes.jsonl"):
        require((a / filename).read_bytes() == (b / filename).read_bytes(), "independent pass mismatch: " + filename)
    receipt = json.loads((a / "receipt.json").read_text())
    require(receipt.get("schema") == "language-gonol.python-qualification" and receipt.get("version") == 1, "qualification schema mismatch")
    require((receipt.get("cpython"), receipt.get("ucns"), receipt.get("python")) == (CPYTHON, UCNS_PYTHON, "3.12.14"), "qualification provenance mismatch")
    require(receipt.get("sqlite_runtime") == sqlite3.sqlite_version, "qualification SQLite runtime mismatch")
    require(receipt.get("implementation_sha256") == implementation_hashes(), "qualification implementation mismatch")
    require(tuple(receipt.get(key) for key in ("input_files", "input_bytes", "inventory_sha256")) == CPYTHON_INVENTORY, "pinned CPython inventory mismatch")
    for root in (a, b):
        require(sha256((root / "outcomes.jsonl").read_bytes()).hexdigest() == receipt["outcomes_sha256"], "outcome digest mismatch")
        outcomes = [json.loads(line) for line in (root / "outcomes.jsonl").read_text().splitlines()]
        require(len(outcomes) == receipt["input_files"], "outcome coverage mismatch")
        inputs = json.loads((root / "inventory.json").read_text())
        require(len(inputs) == receipt["input_files"] and sum(r["bytes"] for r in inputs) == receipt["input_bytes"], "source aggregate mismatch")
        counts = Counter()
        for row in outcomes:
            rejected_hash = CPYTHON_ENCODING_REJECTIONS.get(row["path"])
            require((rejected_hash is not None) == (row["outcome"] == "REJECTED_ENCODING"), "encoding admission outcome mismatch")
            if row["outcome"] == "REJECTED_ENCODING":
                require(row["sha256"] == rejected_hash and row.get("reason") == "SyntaxError", "encoding admission rejection mismatch")
                counts["rejected_encoding"] += 1
            else:
                require(row["outcome"] == "CONSTRUCTED", "unknown admission outcome")
                counts["constructed"] += 1
                manifest = check_manifest(row)
                counts["off_carrier_files"] += bool(manifest["not_on_pinned_carrier"])
                counts["tokenize_false"] += not manifest["verification"]["tokenize_ok"]
                counts["ast_false"] += not manifest["verification"]["ast_ok"]
        require(dict(counts) == receipt["counts"], "admission aggregate mismatch")
        require(sha256(canonical(inputs)).hexdigest() == receipt["inventory_sha256"], "inventory digest mismatch")
        require([{key: row[key] for key in ("path", "git_blob", "sha256", "bytes")} for row in outcomes] == inputs, "outcome/source inventory mismatch")
    print(json.dumps({"status": "SURVIVED", "receipt": receipt}, indent=2))


def check_tests(paths):
    count = 0
    for path in paths:
        tree = ET.parse(path)
        cases = tree.findall(".//testcase")
        require(bool(cases), "empty test suite")
        require(not tree.findall(".//skipped") and not tree.findall(".//failure") and not tree.findall(".//error"), "unpassed test outcomes")
        for suite in tree.getroot().iter():
            if suite.tag not in ("testsuite", "testsuites"):
                continue
            if suite.tag == "testsuite" or "tests" in suite.attrib:
                require(int(suite.attrib.get("tests", -1)) == len(list(suite.iter("testcase"))), "JUnit declared count mismatch")
            for key in ("skipped", "failures", "errors"):
                if suite.tag == "testsuite" or key in suite.attrib:
                    require(int(suite.attrib.get(key, -1)) == 0, "JUnit aggregate reports unpassed outcomes")
        count += len(cases)
    print(json.dumps({"passed": count, "skipped": 0, "failed": 0}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("python-pass")
    p.add_argument("corpus", type=Path); p.add_argument("producer", type=Path); p.add_argument("out", type=Path)
    p = commands.add_parser("compare"); p.add_argument("a", type=Path); p.add_argument("b", type=Path)
    p = commands.add_parser("check-tests"); p.add_argument("paths", type=Path, nargs="+")
    args = parser.parse_args()
    if args.command == "python-pass":
        python_pass(args.corpus.resolve(), args.producer.resolve(), args.out.resolve())
    elif args.command == "check-tests":
        check_tests(args.paths)
    elif args.command == "compare":
        compare(args.a, args.b)


if __name__ == "__main__":
    main()
# ratios: loc_comments=238:42 imports_exports=19:12 calls_definitions=139:12
