# ratios: loc_comments=170:53 imports_exports=14:12 calls_definitions=83:17
"""Negative controls for the qualification gate; run with pytest."""
# === CHECKS ===
# id: check_test_compare_rejects_self_consistent_incomplete_inventory
#   proves: language_qualification_complete_inventory
#   call: self::test_compare_rejects_self_consistent_incomplete_inventory
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary files and SQLite
#   cleanup: pytest_tmp_path and connection context
# id: check_test_compare_accepts_complete_manifest_fixture
#   proves: language_qualification_manifest_integrity
#   call: self::test_compare_accepts_complete_manifest_fixture
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary files and SQLite
#   cleanup: pytest_tmp_path and connection context
# id: check_test_compare_rejects_rebound_invalid_manifest
#   proves: language_qualification_manifest_integrity
#   call: self::test_compare_rejects_rebound_invalid_manifest
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary files and SQLite
#   cleanup: pytest_tmp_path and connection context
# id: check_test_compare_rejects_minimal_constructed_manifest
#   proves: language_qualification_manifest_integrity
#   call: self::test_compare_rejects_minimal_constructed_manifest
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary files and SQLite
#   cleanup: pytest_tmp_path and connection context
# id: check_test_compare_checks_each_manifest_receipt
#   proves: language_qualification_manifest_integrity
#   call: self::test_compare_checks_each_manifest_receipt
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary files and SQLite
#   cleanup: pytest_tmp_path and connection context
# id: check_test_tab_oracle_counts_formfeed_as_one_column
#   proves: language_qualification_tab_witness
#   call: self::test_tab_oracle_counts_formfeed_as_one_column
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary files and SQLite
#   cleanup: pytest_tmp_path and connection context
# id: check_python_encoding_admission
#   proves: language_qualification_complete_inventory
#   call: self::test_compare_binds_actual_encoding_admission
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary files
#   cleanup: pytest_tmp_path
# === END CHECKS ===
import importlib.util
import gzip
import json
from hashlib import sha256
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("language_qualification", Path(__file__).parents[1] / "qualify_python_gonols.py")
qualification = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qualification)


def test_all_preupgrade_projection_misses_have_native_glyphs(tmp_path):
    import os
    import sqlite3
    import sys
    sys.path.insert(0, str(qualification.ROOT / "research/python-gonol"))
    from python_gonol import affixiate_python_source, verify_construct

    history = qualification.ROOT / "docs/evidence/python-gonol-20260919/python-outcomes.jsonl.gz"
    rows = [json.loads(line) for line in gzip.decompress(history.read_bytes()).splitlines()]
    flags = [row["manifest"]["not_on_pinned_carrier"] for row in rows
             if row["outcome"] == "CONSTRUCTED" and row["manifest"]["not_on_pinned_carrier"]]
    scalars = sorted({ch for flag in flags for ch in flag})
    assert (len(flags), len(scalars)) == (113, 290)
    native = os.environ["UCNS_SOURCE_ROOT"]
    text = "".join(scalars)
    result = affixiate_python_source(text, state_dir=tmp_path, source_id="archived-scalars", ucns_source_root=native)
    with sqlite3.connect(tmp_path / "construct.db") as db:
        qualification.check_source_rows(db, text.encode(), "utf-8")
        assert db.execute("SELECT count(*) FROM occurrences o JOIN characters c ON c.id=o.character_id "
                          "WHERE c.public_position IS NULL").fetchone() == (len(scalars),)
    assert verify_construct(tmp_path, native) == result.receipt_sha256


@pytest.mark.parametrize("body", ["", "<testcase><skipped/></testcase>", "<testcase><failure/></testcase>", "<testcase><error/></testcase>"])
def test_test_gate_rejects_incomplete_evidence(tmp_path, body):
    path = tmp_path / "outcome.xml"
    path.write_text("<testsuites><testsuite>" + body + "</testsuite></testsuites>")
    with pytest.raises(ValueError):
        qualification.check_tests([path])


def test_test_gate_accepts_passed_cases(tmp_path):
    path = tmp_path / "outcome.xml"
    path.write_text('<testsuites><testsuite tests="1" skipped="0" failures="0" errors="0"><testcase name="passed"/></testsuite></testsuites>')
    qualification.check_tests([path])
@pytest.mark.parametrize("attribute,value", [("tests", "2"), ("failures", "1"), ("errors", "1"), ("skipped", "1")])
def test_junit_aggregate_must_agree(tmp_path, attribute, value):
    report = '<testsuite tests="1" skipped="0" failures="0" errors="0"><testcase name="a"/></testsuite>'
    before = 'tests="1"' if attribute == "tests" else f'{attribute}="0"'
    path = tmp_path / "results.xml"
    path.write_text(report.replace(before, f'{attribute}="{value}"'))
    with pytest.raises(ValueError):
        qualification.check_tests([path])


def test_alias_cannot_claim_two_executions(tmp_path):
    (tmp_path / "receipt.json").write_text("{}")
    with pytest.raises(ValueError, match="distinct"):
        qualification.distinct_outputs(tmp_path, tmp_path / ".", ("receipt.json",))


def test_compare_rejects_self_consistent_incomplete_inventory(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    inputs = [{"path": "x.py", "git_blob": "a" * 40, "sha256": "b" * 64, "bytes": 1}]
    outcome = {**inputs[0], "outcome": "REJECTED_ENCODING", "reason": "SyntaxError"}
    data = qualification.canonical(outcome) + b"\n"
    receipt = {"schema": "language-gonol.python-qualification", "version": 2,
               "cpython": qualification.CPYTHON, "ucns": qualification.UCNS_PYTHON,
               "python": "3.12.14", "sqlite_runtime": qualification.sqlite3.sqlite_version, "implementation_sha256": qualification.implementation_hashes(),
               "input_files": 1, "input_bytes": 1, "counts": {"rejected_encoding": 1},
               "inventory_sha256": sha256(qualification.canonical(inputs)).hexdigest(),
               "outcomes_sha256": sha256(data).hexdigest()}
    for root in (a, b):
        (root / "inventory.json").write_bytes(qualification.canonical(inputs))
        (root / "outcomes.jsonl").write_bytes(data)
        (root / "receipt.json").write_bytes(qualification.canonical(receipt))
    with pytest.raises(ValueError, match="pinned CPython inventory"):
        qualification.compare(a, b)
    for key, value in (("schema", "wrong"), ("version", 1), ("cpython", "wrong"), ("ucns", "wrong"),
                       ("python", "wrong"), ("implementation_sha256", {}), ("input_bytes", 2), ("counts", {})):
        bad = {**receipt, key: value}
        for root in (a, b):
            (root / "receipt.json").write_bytes(qualification.canonical(bad))
        with pytest.raises(ValueError):
            qualification.compare(a, b)


def _complete_pair(tmp_path, change=lambda rows: None):
    """Use the independently replayed v3 manifests as comparison fixtures."""
    evidence = qualification.ROOT / 'docs/evidence/python-gonol-20260919'
    inputs = json.loads(gzip.decompress((evidence / 'python-inventory.json.gz').read_bytes()))
    current = qualification.ROOT / 'docs/evidence/python-gonol-unicode-v3'
    rows = [json.loads(line) for line in gzip.decompress(
        (current / 'outcomes.jsonl.gz').read_bytes()).splitlines()]
    change(rows)
    data = b''.join(qualification.canonical(row) + b'\n' for row in rows)
    receipt = json.loads((current / 'receipt.json').read_text())
    receipt.update(sqlite_runtime=qualification.sqlite3.sqlite_version,
                   implementation_sha256=qualification.implementation_hashes(),
                   outcomes_sha256=sha256(data).hexdigest())
    roots = tmp_path / 'a', tmp_path / 'b'
    for root in roots:
        root.mkdir()
        (root / 'inventory.json').write_bytes(qualification.canonical(inputs))
        (root / 'outcomes.jsonl').write_bytes(data)
        (root / 'receipt.json').write_bytes(qualification.canonical(receipt))
    return roots


def test_compare_accepts_complete_manifest_fixture(tmp_path):
    qualification.compare(*_complete_pair(tmp_path))


@pytest.mark.parametrize('field,value', [
    ('schema', 'wrong'), ('version', '1.0.0'), ('version', '2.0.0'), ('ucns', {}),
    ('source_id', 'elsewhere.py'), ('source_bytes_sha256', '0' * 64),
    ('decoded_source_sha256', 'wrong'), ('construct_sha256', 'wrong'),
    ('counts', {}), ('preflight_storage_bytes', 1), ('hmmm', ''),
    ('verification', {'ast_ok': 1, 'tokenize_ok': True}),
])
def test_compare_rejects_rebound_invalid_manifest(tmp_path, field, value):
    def change(rows):
        manifest = rows[0]['manifest']
        manifest[field] = value
        manifest.pop('receipt_sha256')
        manifest['receipt_sha256'] = sha256(qualification.canonical(manifest)).hexdigest()
    with pytest.raises(ValueError, match='manifest'):
        qualification.compare(*_complete_pair(tmp_path, change))


def test_compare_rejects_minimal_constructed_manifest(tmp_path):
    def change(rows):
        rows[0]['manifest'] = {'counts': {},
                               'verification': {'ast_ok': True, 'tokenize_ok': True}}
    with pytest.raises(ValueError, match='manifest'):
        qualification.compare(*_complete_pair(tmp_path, change))


def test_compare_checks_each_manifest_receipt(tmp_path):
    def change(rows):
        rows[-1]['manifest']['receipt_sha256'] = '0' * 64
    with pytest.raises(ValueError, match='manifest receipt'):
        qualification.compare(*_complete_pair(tmp_path, change))


def test_tab_oracle_counts_formfeed_as_one_column(tmp_path):
    import os
    import sqlite3
    import sys
    sys.path.insert(0, str(qualification.ROOT / "research/python-gonol"))
    from python_gonol import affixiate_python_bytes
    raw = b'abc\f\t'
    affixiate_python_bytes(raw, source_id="oracle.py", state_dir=tmp_path,
                           ucns_source_root=os.environ["UCNS_SOURCE_ROOT"])
    with sqlite3.connect(tmp_path / "construct.db") as db:
        qualification.check_source_rows(db, raw, 'utf-8')
        db.execute('UPDATE controls SET spaces_to_next_stop=8')
        with pytest.raises(ValueError, match='tab expansion'):
            qualification.check_source_rows(db, raw, 'utf-8')
        db.execute('UPDATE controls SET spaces_to_next_stop=4')
        db.execute("UPDATE occurrences SET character_id=98 WHERE scalar='a'")
        with pytest.raises(ValueError, match='matching Unicode glyph'):
            qualification.check_source_rows(db, raw, 'utf-8')


@pytest.mark.parametrize('attack', ['all_rejected', 'valid_rejected', 'wrong_reason'])
def test_compare_binds_actual_encoding_admission(tmp_path, attack):
    def change(rows):
        if attack == 'all_rejected':
            selected = rows
        elif attack == 'valid_rejected':
            selected = [next(r for r in rows if r['outcome'] == 'CONSTRUCTED')]
        else:
            selected = [next(r for r in rows if r['outcome'] == 'REJECTED_ENCODING')]
        for row in selected:
            row.pop('manifest', None)
            row.update(outcome='REJECTED_ENCODING', reason='UnicodeDecodeError' if attack == 'wrong_reason' else 'SyntaxError')
    roots = _complete_pair(tmp_path, change)
    for root in roots:
        receipt = json.loads((root / 'receipt.json').read_text())
        rows = [json.loads(line) for line in (root / 'outcomes.jsonl').read_text().splitlines()]
        counts = qualification.Counter()
        for row in rows:
            if row['outcome'] == 'REJECTED_ENCODING':
                counts['rejected_encoding'] += 1
            else:
                counts['constructed'] += 1
                counts['scalar_occurrences'] += row['manifest']['counts']['occurrences']
                counts['tokenize_false'] += not row['manifest']['verification']['tokenize_ok']
                counts['ast_false'] += not row['manifest']['verification']['ast_ok']
        receipt['counts'] = dict(counts)
        (root / 'receipt.json').write_bytes(qualification.canonical(receipt))
    with pytest.raises(ValueError, match='encoding admission'):
        qualification.compare(*roots)
# ratios: loc_comments=170:53 imports_exports=14:12 calls_definitions=83:17
