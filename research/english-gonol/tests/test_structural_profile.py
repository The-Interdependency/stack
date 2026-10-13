# ratios: loc_comments=431:60 imports_exports=16:36 calls_definitions=246:43
"""Witnesses for the accepted thirteen-rule profile, including hostile records."""
from contextlib import closing
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sqlite3

import pytest

from english_gonol.language.source import LexemeRecord, SenseRecord, SynsetRecord, WordnetSnapshot
from english_gonol.structural_rules import segment, canonical
from english_gonol.structural_construct import StructuralError, build, verify, _manifest
from english_gonol.structural_query import StructuralField
from english_gonol.hyperspace_construct import glyph_inventory

# === CHECKS ===
# id: check_structural_scalar_recovery
#   proves: structural_exact_participation, structural_local_closure
#   call: self::test_exact_scalar_recovery
#   mutates: none
#   cleanup: none
# id: check_structural_atomic_repetition
#   proves: structural_shared_atomic_words, structural_atomic_recovery
#   call: self::test_repetition_and_atomic_promotion
#   mutates: filesystem
#   cleanup: pytest_tmp_path
# id: check_structural_origins
#   proves: structural_definitions_and_origins
#   call: self::test_definition_topologies_and_origins
#   mutates: filesystem
#   cleanup: pytest_tmp_path
# id: check_structural_queries
#   proves: structural_queries_do_not_admit, structural_geometry_refuses
#   call: self::test_admission_and_geometry_refusals
#   mutates: filesystem
#   cleanup: pytest_tmp_path
# id: check_structural_replay
#   proves: structural_complete_replay
#   call: self::test_complete_rebuild_and_tamper
#   mutates: filesystem
#   cleanup: pytest_tmp_path
# id: check_structural_query_snapshot
#   proves: structural_queries_keep_verified_snapshot
#   call: self::test_external_changes_cannot_replace_verified_query_rows
#   mutates: filesystem
#   cleanup: pytest_tmp_path
# id: check_structural_snapshot_cleanup
#   proves: structural_queries_keep_verified_snapshot
#   call: self::test_verified_snapshot_closes_on_initialization_failure
#   mutates: filesystem
#   cleanup: pytest_tmp_path
# id: check_structural_snapshot_lifetime
#   proves: structural_queries_keep_verified_snapshot
#   call: self::test_verified_snapshot_readonly_and_close
#   mutates: filesystem
#   cleanup: pytest_tmp_path
# id: check_structural_evidence_canonical_bytes
#   proves: structural_complete_replay
#   call: self::test_resealed_noncanonical_evidence_is_rejected
#   mutates: filesystem
#   cleanup: pytest_tmp_path
# id: check_structural_metadata_canonical_bytes
#   proves: structural_complete_replay
#   call: self::test_resealed_noncanonical_metadata_is_rejected
#   mutates: filesystem
#   cleanup: pytest_tmp_path
# id: check_structural_glyph_axis_inventory
#   proves: structural_atomic_recovery
#   call: self::test_word_glyph_axes_follow_inventory
#   mutates: filesystem
#   cleanup: pytest_tmp_path
# === END CHECKS ===


def snapshot():
    return WordnetSnapshot(
        lexemes=(LexemeRecord("geometry", "n", (), (SenseRecord("s1", "n1", ()), SenseRecord("s2", "n2", ()))),
                 LexemeRecord("ice cream", "n", (), (SenseRecord("s3", "n3", ()),)),
                 LexemeRecord("Dr.", "n", (), (SenseRecord("s4", "n4", ()),))),
        synsets=(SynsetRecord("n1", "n", ("geometry",), ("Dr. creates geometry. Dr. creates 3.14...",), ()),
                 SynsetRecord("n2", "n", ("geometry",), ("geometry  geometry\ngeometry…",), ()),
                 SynsetRecord("n3", "n", ("ice cream",), ("ice cream",), ()),
                 SynsetRecord("n4", "n", ("Dr.",), ("Dr.",), ())),
        source_tree_sha256="0" * 64, source_file_count=4)


def make(path):
    return build(snapshot(), out_dir=path, public_position=lambda c: None,
                 producer={"standing": "fixture-only"})


@pytest.fixture
def field(tmp_path):
    path = tmp_path / "field"
    make(path)
    with StructuralField(path) as field:
        yield field


def test_exact_scalar_recovery():
    for text in ("", "  ", "geometry", "Dr.", "3.14", "...", "…", "a\r\nb", "can't", "x-ray", "e\u0301", "a.b", ".."):
        parts = segment(text)
        assert "".join(p.text for p in parts) == text
        assert [(p.start, p.end) for p in parts] == [(sum(len(q.text) for q in parts[:i]), sum(len(q.text) for q in parts[:i+1])) for i in range(len(parts))]
        assert all("." not in p.text and not any(c.isspace() for c in p.text) for p in parts if p.kind == "word")
    with pytest.raises(ValueError, match="scalars"):
        segment("\ud800")


def test_repetition_and_atomic_promotion(field):
    word = field.word("geometry")
    assert len(word["glyph_axis_set"]) == 7
    assert word["occurrence_count"] == 8
    assert word["glyph_ids"][1] == word["glyph_ids"][4]
    query = field.construct("creates creates")
    first, second = query["parts"][0], query["parts"][2]
    assert first["identity"] == second["identity"]
    assert first["start"] != second["start"]
    assert first["origin"] == second["origin"] == "O_W"
    composite = field.compose(query, relation="ordered-text")
    assert composite["standing"] == "logically-closed"
    assert composite["participants"][0] == composite["participants"][2]
    assert "glyph_ids" not in composite["participants"][0]
    assert field.word("geometry") == word


def test_period_roles_and_ambiguity(field):
    query = field.construct("Dr. creates 3.14...")
    roles = [(p["start"], p["function"]["roles"]) for p in query["parts"]]
    assert roles[1][1] == ["abbreviation"]
    assert any(r == ["decimal-separator"] for _, r in roles)
    assert sum("ellipsis" in r for _, r in roles) == 3
    terminal = field.construct("Dr.")
    assert terminal["input_closed"] is True
    assert terminal["logical_state"] == "closed"
    assert terminal["closure"] == [{"part": 1, "state": "hmmm"}]
    assert field.compose(terminal, relation="sentence")["code"] == "SENTENCE_CLOSURE_UNRESOLVED"
    explicit = field.construct("Dr.", boundary_decisions={"2": {"closed": True, "source": "operator:sentence-end"}})
    assert explicit["parts"][1]["function"]["roles"] == ["abbreviation", "sentence-close"]
    assert field.compose(explicit, relation="sentence")["standing"] == "logically-closed"
    assert field.replay(json.loads(canonical(explicit))) == explicit


@pytest.mark.parametrize("decisions", [{"0": {"closed": True, "source": "x"}}, {"2": {"closed": True, "source": ""}}, {"2": {"closed": 1, "source": "x"}}, {"9": {}}, {2: {"closed": True, "source": "x"}}])
def test_bad_decisions_refuse(field, decisions):
    with pytest.raises(StructuralError):
        field.construct("Dr.", boundary_decisions=decisions)


def test_ellipsis_distinction_and_group_decision(field):
    dots = field.construct("...")
    scalar = field.construct("…")
    assert len(dots["parts"]) == 3 and len(scalar["parts"]) == 1
    assert dots["receipt_sha256"] != scalar["receipt_sha256"]
    with pytest.raises(StructuralError, match="final scalar"):
        field.construct("...", boundary_decisions={"0": {"closed": True, "source": "x"}})


def test_ellipsis_explicit_closure(field):
    q = field.construct("geometry...", boundary_decisions={"10": {"closed": True, "source": "operator:end"}})
    assert q["closure"] == [{"part": 3, "state": "closed"}]
    assert field.compose(q, relation="sentence")["standing"] == "logically-closed"


def test_spaces_open_sites_without_empty_words(field):
    query = field.construct("geometry  geometry ")
    assert [s["event"] for s in query["word_sites"]] == ["open-site", "continue-site", "open-site"]
    assert query["next_word_site_open"] is True
    assert sum(p["kind"] == "word" for p in query["parts"]) == 2
    assert not field.construct("   ")["refusals"]
    assert field.compose(field.construct(""), relation="ordered-text")["standing"] == "refused"


def test_admission_and_geometry_refusals(field):
    before = field.db.total_changes
    query = field.construct("Geometry zzzz 🦄")
    assert len(query["refusals"]) == 3
    assert query["source"] == "Geometry zzzz 🦄"
    assert query["parts"][0]["identity"] is None
    assert field.db.total_changes == before
    assert field.compose(query, relation="ordered-text")["code"] == "PARTICIPANT_ADMISSION_REQUIRED"
    known = field.construct("geometry")
    assert field.compose(known, relation="acronym-promotion")["code"] == "RELATION_NOT_REGISTERED"
    assert field.geometry(known, operation="displacement")["edges"] == []
    assert field.geometry(known, operation="displacement")["code"] == "UCNS_OPERATION_REQUIRED"


def test_definition_topologies_and_origins(field):
    ids = [r[0] for r in field.db.execute("SELECT id FROM records WHERE kind='definition' ORDER BY id")]
    first, second = [field.definition(i) for i in ids[:2]]
    assert first["origin"] == second["origin"] == {"space": "O_D", "word_id": field.words["geometry"]}
    assert second["definition_succession"]["previous"] == ids[0]
    assert first["constituent_chain"] == [[n-1, n] for n in range(1, len(first["parts"]))]
    assert len(first["constituent_direct"]) == len(first["parts"])
    compound = field.definition(ids[2])
    abbreviation = field.definition(ids[3])
    assert compound["origin"] is None and abbreviation["origin"] is None
    assert compound["origin_state"] == "hmmm:compound-lexical-origin"
    assert "ice cream" not in field.words and "Dr." not in field.words
    assert field.word("geometry")["attachment"]["attachment_point_q_w"] == field.words["geometry"]


def test_query_tamper_detected(field):
    query = field.construct("geometry geometry")
    query["parts"][2]["identity"] += 1
    with pytest.raises(StructuralError, match="replay mismatch"):
        field.replay(query)


def test_complete_rebuild_and_tamper(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    first, second = make(a), make(b)
    assert first == second
    assert (a / "construct.db").read_bytes() == (b / "construct.db").read_bytes()
    assert verify(a) == first
    with sqlite3.connect(a / "construct.db") as db:
        db.execute("UPDATE words SET surface='changed' WHERE surface='geometry'")
    with pytest.raises(StructuralError, match="receipt"):
        verify(a)


@pytest.mark.parametrize("sql", ["DELETE FROM records WHERE id=(SELECT MAX(id) FROM records)",
    "UPDATE records SET provenance='{}' WHERE kind='definition'", "UPDATE components SET function='{}' WHERE record_id=1",
    "UPDATE word_characters SET character_id=1 WHERE ordinal=1"])
def test_resealed_structural_corruption_detected(tmp_path, sql):
    root = tmp_path / "state"
    make(root)
    with sqlite3.connect(root / "construct.db") as db:
        db.execute(sql)
        db.commit()
        manifest = _manifest(db)
    (root / "manifest.json").write_bytes(canonical(manifest))
    with pytest.raises(StructuralError):
        verify(root)


def test_failed_build_publishes_no_partial_state(tmp_path):
    source = snapshot()
    bad = replace(source, synsets=())
    root = tmp_path / "bad"
    with pytest.raises(StructuralError, match="missing synset"):
        build(bad, out_dir=root, public_position=lambda c: None, producer={"standing": "fixture"})
    assert not root.exists()
    assert not list(tmp_path.glob('.structural-*'))


def reseal(root, change):
    """Adversarial helper: row receipts alone must not authorize source claims."""
    with sqlite3.connect(root / "construct.db") as db:
        change(db)
        db.commit()
        manifest = _manifest(db)
    (root / "manifest.json").write_bytes(canonical(manifest))


def test_caller_cannot_grant_complete_corpus(tmp_path):
    root = tmp_path / "state"
    with pytest.raises(StructuralError, match="exact pinned source"):
        build(snapshot(), out_dir=root, public_position=lambda c: None,
              producer={"standing": "fixture"}, complete_corpus=True)
    assert not root.exists()


@pytest.mark.parametrize("value", [1, "true", None, [], {}])
def test_completeness_requires_boolean(tmp_path, value):
    with pytest.raises(StructuralError, match="boolean"):
        build(snapshot(), out_dir=tmp_path / "state", public_position=lambda c: None,
              producer={}, complete_corpus=value)


@pytest.mark.parametrize("key,value", [
    ("authority_transfer", True), ("authority_transfer", 0),
    ("geometry_state", "executed"), ("normalization", "NFC"),
    ("definition_topologies", ["constituent-direct"]),
    ("complete_corpus", True), ("complete_corpus", 0),
    ("extra_authority", "graduated"),
])
def test_resealed_metadata_boundary_refuses(tmp_path, key, value):
    root = tmp_path / "state"
    make(root)
    reseal(root, lambda db: db.execute("INSERT OR REPLACE INTO meta VALUES(?,?)", (key, canonical(value).decode("utf-8"))))
    with pytest.raises(StructuralError):
        verify(root)


def test_resealed_pinned_source_claim_requires_all_evidence(tmp_path):
    from english_gonol.structural_construct import PINNED_SOURCE
    root = tmp_path / "state"
    make(root)
    def change(db):
        db.execute("UPDATE meta SET value=? WHERE key='source'", (canonical(PINNED_SOURCE).decode("utf-8"),))
        db.execute("UPDATE meta SET value='true' WHERE key='complete_corpus'")
    reseal(root, change)
    with pytest.raises(StructuralError, match="source evidence digest"):
        verify(root)


@pytest.mark.parametrize("kind,field,value", [
    ("lexeme", "part_of_speech", "forged"),
    ("synset", "relations", [["invented", ["n1"]]]),
    ("synset", "part_of_speech", "forged"),
])
def test_unused_included_source_evidence_cannot_be_resealed(tmp_path, kind, field, value):
    root = tmp_path / "state"
    make(root)
    def change(db):
        payload = json.loads(db.execute("SELECT payload FROM evidence WHERE kind=? AND ordinal=0", (kind,)).fetchone()[0])
        payload[field] = value
        db.execute("UPDATE evidence SET payload=? WHERE kind=? AND ordinal=0", (canonical(payload).decode("utf-8"), kind))
    reseal(root, change)
    with pytest.raises(StructuralError, match="source evidence digest"):
        verify(root)


@pytest.fixture
def punctuation_field(tmp_path):
    source = snapshot()
    source = replace(source, synsets=source.synsets + (
        SynsetRecord("punctuation", "n", ("geometry",), ('"geometry." (geometry!?) [geometry.] {geometry!} “geometry?” geometry; geometry,', "'geometry.'"), ()),))
    root = tmp_path / "punctuation"
    build(source, out_dir=root, public_position=lambda c: None, producer={"standing": "fixture"})
    with StructuralField(root) as result:
        yield result


@pytest.mark.parametrize("text", ['"geometry."', '(geometry!?)', '[geometry.]', '{geometry!}',
                                   '“geometry?”', 'geometry!?', 'geometry?!', 'geometry!!',
                                   '"geometry!?"  '])
def test_terminal_closing_punctuation_and_clusters(punctuation_field, text):
    query = punctuation_field.construct(text)
    assert not query["refusals"]
    result = punctuation_field.compose(query, relation="sentence")
    assert result["standing"] == "logically-closed"
    assert len(result["participants"]) == len(query["parts"])
    assert punctuation_field.replay(query) == query


@pytest.mark.parametrize("text", ['geometry. geometry.', 'geometry! ?', 'geometry.;',
                                   'geometry.,', 'geometry...', 'Dr.', 'geometry'])
def test_nonterminal_or_ambiguous_closure_still_refuses(punctuation_field, text):
    query = punctuation_field.construct(text)
    assert not query["refusals"]
    assert punctuation_field.compose(query, relation="sentence")["code"] == "SENTENCE_CLOSURE_UNRESOLVED"


def test_explicit_open_ambiguity_is_a_resolved_nonboundary(field):
    text = "Dr. creates geometry."
    query = field.construct(text, boundary_decisions={
        "2": {"closed": False, "source": "operator:abbreviation-not-sentence-end"}})
    assert query["closure"][0]["state"] == "open"
    assert field.compose(query, relation="sentence")["standing"] == "logically-closed"
    assert field.replay(query) == query
    undecided = field.construct(text)
    assert field.compose(undecided, relation="sentence")["code"] == "SENTENCE_CLOSURE_UNRESOLVED"
    nonterminal = field.construct(text, boundary_decisions={
        "2": {"closed": True, "source": "operator:independent-boundary"}})
    assert field.compose(nonterminal, relation="sentence")["code"] == "SENTENCE_CLOSURE_UNRESOLVED"


@pytest.mark.parametrize("sql", [
    "ALTER TABLE characters ADD COLUMN extra TEXT",
    "ALTER TABLE words ADD COLUMN extra TEXT",
    "DROP INDEX components_word",
    "CREATE VIEW extra AS SELECT * FROM words",
    "CREATE VIEW sqliteXextra AS SELECT * FROM words",
    "CREATE TRIGGER sqliteXextra AFTER INSERT ON words BEGIN SELECT 1; END",
    "CREATE TRIGGER extra AFTER INSERT ON words BEGIN SELECT 1; END",
])
def test_resealed_schema_tamper_refuses_before_query(tmp_path, sql):
    root = tmp_path / "state"
    make(root)
    reseal(root, lambda db: db.execute(sql))
    with pytest.raises(StructuralError, match="schema"):
        verify(root)
    with pytest.raises(StructuralError, match="schema"):
        StructuralField(root)


def test_manifest_edits_do_not_redefine_verified_field(field):
    original = field.construct("Dr.")
    exposed = field.manifest
    exposed["receipt_sha256"] = "forged"
    exposed["metadata"]["profile_sha256"] = "forged"
    exposed["metadata"]["profile"]["abbreviations"].remove("Dr")
    assert field.construct("Dr.") == original
    assert field.replay(original) == original
    assert field.manifest != exposed
    with pytest.raises(AttributeError):
        field.manifest = exposed
    with pytest.raises(AttributeError):
        field.abbreviations = ()
    with pytest.raises(AttributeError):
        field.abbreviations.remove("Dr")


def test_implementation_inputs_are_the_full_forge_check_surface():
    from english_gonol.structural_construct import IMPLEMENTATION_FILES
    assert set(IMPLEMENTATION_FILES) == {
        "structural_rules.py", "structural_construct.py", "structural_query.py",
        "hyperspace_construct.py", "full_construct_run.py", "language/source.py"}


@pytest.mark.parametrize("text", ["'geometry.'", "'geometry!?'", "'geometry.'  "])
def test_ascii_single_quote_is_a_terminal_closer(punctuation_field, text):
    query = punctuation_field.construct(text)
    assert not query["refusals"]
    assert punctuation_field.compose(query, relation="sentence")["standing"] == "logically-closed"
    assert punctuation_field.replay(query) == query


@pytest.mark.parametrize("operation", ["update", "replace"])
@pytest.mark.parametrize("timing", ["before-first-query", "after-first-query"])
def test_external_changes_cannot_replace_verified_query_rows(tmp_path, monkeypatch, operation, timing):
    from english_gonol import structural_query
    root = tmp_path / "state"
    make(root)
    path = root / "construct.db"
    replacement = tmp_path / "replacement.db"
    replacement.write_bytes(path.read_bytes())
    if operation == "update":
        # WAL permits a committed writer while the verified reader stays open.
        with closing(sqlite3.connect(path)) as db:
            assert db.execute("PRAGMA journal_mode=WAL").fetchone() == ("wal",)
    with StructuralField(root) as original:
        expected_word = original.word("geometry")
        rid = original.db.execute("SELECT MIN(id) FROM records WHERE kind='definition'").fetchone()[0]
        expected_definition = original.definition(rid)
        expected_query = original.construct("geometry")
        expected_manifest = original.manifest
    mutations = []

    def mutate():
        target = path if operation == "update" else replacement
        with closing(sqlite3.connect(target)) as db:
            db.execute("UPDATE words SET surface='forged' WHERE surface='geometry'")
            db.execute("UPDATE records SET text='forged' WHERE kind='definition'")
            db.commit()
        if operation == "replace":
            replacement.replace(path)
        mutations.append(operation)

    original_canonical = structural_query.canonical
    def mutate_after_verification(value):
        if timing == "before-first-query" and not mutations:
            mutate()
        return original_canonical(value)
    monkeypatch.setattr(structural_query, "canonical", mutate_after_verification)
    with StructuralField(root) as field:
        if timing == "after-first-query":
            assert field.word("geometry") == expected_word
            assert field.definition(rid) == expected_definition
            mutate()
        assert mutations == [operation]
        assert field.word("geometry") == expected_word
        assert field.definition(rid) == expected_definition
        assert field.construct("geometry") == expected_query
        assert field.manifest == expected_manifest
        assert "forged" not in field.words
    with pytest.raises(StructuralError, match="receipt"):
        verify(root)


@pytest.mark.parametrize("stage", ["verification", "initialization"])
def test_verified_snapshot_closes_on_initialization_failure(tmp_path, monkeypatch, stage):
    from english_gonol import structural_construct, structural_query
    root = tmp_path / "state"
    make(root)
    connections = []
    original_open = structural_construct.open_readonly
    def track_open(path):
        db = original_open(path)
        connections.append(db)
        return db
    monkeypatch.setattr(structural_construct, "open_readonly", track_open)
    if stage == "verification":
        manifest = json.loads((root / "manifest.json").read_bytes())
        manifest["receipt_sha256"] = "forged"
        (root / "manifest.json").write_bytes(canonical(manifest))
    else:
        def refuse_inventory(_db):
            raise StructuralError("inventory failure")
        monkeypatch.setattr(structural_query, "glyph_inventory", refuse_inventory)
    with pytest.raises(StructuralError):
        StructuralField(root)
    assert len(connections) == 1
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        connections[0].execute("SELECT 1")


def test_verified_snapshot_readonly_and_close(tmp_path):
    root = tmp_path / "state"
    make(root)
    with StructuralField(root) as field:
        assert field.db.in_transaction
        with pytest.raises(sqlite3.OperationalError, match="readonly"):
            field.db.execute("UPDATE words SET surface='forged'")
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        field.db.execute("SELECT 1")
    field.close()
    with pytest.raises(RuntimeError, match="caller failure"):
        with StructuralField(root) as field:
            raise RuntimeError("caller failure")
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        field.db.execute("SELECT 1")


@pytest.mark.parametrize("kind", ["lexeme", "synset"])
@pytest.mark.parametrize("variant", ["pretty", "escape", "duplicate-key"])
def test_resealed_noncanonical_evidence_is_rejected(tmp_path, kind, variant):
    root = tmp_path / "state"
    make(root)
    def change(db):
        raw = db.execute("SELECT payload FROM evidence WHERE kind=? AND ordinal=0", (kind,)).fetchone()[0]
        item = json.loads(raw)
        if variant == "pretty":
            mutated = json.dumps(item, ensure_ascii=False, indent=2, sort_keys=True)
        elif variant == "escape":
            mutated = raw.replace("geometry", "\\u0067eometry")
        else:
            key = next(iter(item))
            mutated = "{" + canonical(key).decode() + ":" + canonical(item[key]).decode() + "," + raw[1:]
        assert mutated != raw and json.loads(mutated) == item
        db.execute("UPDATE evidence SET payload=? WHERE kind=? AND ordinal=0", (mutated, kind))
    reseal(root, change)
    with pytest.raises(StructuralError, match="noncanonical source evidence"):
        verify(root)
    with pytest.raises(StructuralError, match="noncanonical source evidence"):
        StructuralField(root)


@pytest.mark.parametrize("carrier", [False, True])
def test_word_glyph_axes_follow_inventory(tmp_path, carrier):
    root = tmp_path / "state"
    positions = {c: i for i, c in enumerate("ytromge.")} if carrier else {}
    build(snapshot(), out_dir=root, public_position=positions.get, producer={"standing": "fixture-only"})
    with StructuralField(root) as field:
        word = field.word("geometry")
        inventory = glyph_inventory(field.db)
        assert word["glyph_axis_set"] == sorted({inventory[c].axis_index for c in "geometry"})
        assert word["glyph_axis_set"] != sorted(set(word["glyph_ids"]))
        assert word["glyph_axis_set"] == (list(range(7)) if carrier else sorted({gid - 1 for gid in word["glyph_ids"]}))
        assert word["occurrence_count"] == 8
        assert word["glyph_ids"][1] == word["glyph_ids"][4]
        assert word["glyph_origin"] == "O_G"
        assert word["gonal_order"] == "hmmm:UCNS_OPERATION_REQUIRED"


@pytest.mark.parametrize("variant", ["pretty", "escape", "duplicate-key"])
def test_resealed_noncanonical_metadata_is_rejected(tmp_path, variant):
    root = tmp_path / "state"
    make(root)
    def change(db):
        raw = db.execute("SELECT value FROM meta WHERE key='producer'").fetchone()[0]
        item = json.loads(raw)
        if variant == "pretty":
            mutated = json.dumps(item, ensure_ascii=False, indent=2, sort_keys=True)
        elif variant == "escape":
            mutated = raw.replace("fixture", "\\u0066ixture")
        else:
            mutated = '{"standing":"fixture-only",' + raw[1:]
        assert mutated != raw and json.loads(mutated) == item
        db.execute("UPDATE meta SET value=? WHERE key='producer'", (mutated,))
    reseal(root, change)
    with pytest.raises(StructuralError, match="noncanonical metadata"):
        verify(root)
    with pytest.raises(StructuralError, match="noncanonical metadata"):
        StructuralField(root)
# ratios: loc_comments=431:60 imports_exports=16:36 calls_definitions=246:43
