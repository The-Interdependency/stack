"""Run with the pinned UCNS: pytest -q tests/test_ordinal_definitions.py.

These adversarial fixtures verify inheritance and placement, not full-corpus
admission. The hosted complete build remains the full-source witness.
"""
# === CHECKS ===
# id: inherited_definitions_match_prior_source
#   proves: ordinal_inherited_definition_preservation
#   call: self::test_inherited_entries_and_behavior_are_unchanged
# id: definition_geometry_has_no_historical_fallback
#   proves: ordinal_definition_replay
#   call: self::test_no_old_constructor_and_independent_checker
# id: definition_corruption_is_rejected
#   proves: ordinal_definition_replay
#   call: self::test_tampering_refuses
# === END CHECKS ===
from copy import deepcopy
from dataclasses import asdict
from fractions import Fraction
import json
from types import SimpleNamespace

import pytest
from english_gonol import ordinal_definitions as definitions
from english_gonol.ordinal_construct import Factory
from english_gonol.language import character_definitions as prior


@pytest.fixture
def factory():
    names = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
    public = {'identities': list(prior.PUBLIC_GONOL_157) + ['𝟠'], 'fixture': True}
    return Factory(public, dict(enumerate(names)), 'fixture-source')


def test_inherited_entries_and_behavior_are_unchanged(factory):
    payload = definitions.build_definitions(factory)
    layer = definitions.verify_definitions(factory, payload)
    old = prior.load_character_definition_table()
    assert len(layer.entries) == 158
    assert list(layer.entries) == list(factory.glyph_carrier.identities)
    for char, entry in old.items():
        assert asdict(layer.entries[char]) == asdict(entry)
    assert layer.entries['-'].classes == ('operator', 'punctuation')
    assert layer.entries['y'].classes == ('vowel', 'consonant')
    assert layer.entries['3'].number_name == 'three'
    assert layer.entries['A'].hmmm and layer.entries['𝟠'].hmmm
    for final in ('y', 'Y', 'a'):
        for preceding in ('r', 'a', None, '𝟠'):
            for suffix, initial in (('ing', True), ('ed', True), ('s', False)):
                expected = prior.CharacterDefinitionLayer.final_y_realization(
                    SimpleNamespace(entries=old), final, preceding, suffix, initial)
                assert layer.final_y_realization(final, preceding, suffix, initial) == expected
    with pytest.raises(TypeError):
        layer.entries['x'] = layer.entries['y']


def test_relation_plan_matches_previous_builder(factory, monkeypatch):
    calls = []
    def capture(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(gonol=SimpleNamespace(receipt_digest=kwargs['source_id']),
                               receipt_digest=kwargs['source_id'])
    monkeypatch.setattr(prior, 'construct_gonol', capture)
    prior.build_character_definition_layer()
    observed = {c['source_id']: c.get('relation') for c in calls if c['scale'] == 'definition'}
    payload = definitions.build_definitions(factory)
    reconstructed = {d['source_id']: d['construction']['relation']
                     for d in payload['definitions'] if d['owner'] in prior.PUBLIC_GONOL_157}
    assert reconstructed == observed


def test_no_old_constructor_and_independent_checker(factory, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError('forbidden constructor called')
    monkeypatch.setattr(prior, 'construct_gonol', forbidden)
    payload = definitions.build_definitions(factory)
    monkeypatch.setattr(definitions, 'affixiate', forbidden)
    monkeypatch.setattr(factory, 'word', forbidden)
    definitions.verify_definitions(factory, payload)


def test_new_angles_and_recursive_number_name_recovery(factory):
    payload = definitions.build_definitions(factory)
    d = next(d for d in payload['definitions'] if d['source_id'] == 'char-def:3:number-name')
    positions = d['construction']['placements']
    assert d['construction']['origin'] == 'SPACE'
    assert [p['radius']['power_of_two_denominator'] for p in positions] == [2, 1]
    assert positions[0]['arity'] == 158
    assert Fraction(*positions[0]['turn']) == factory.glyph_carrier.turn('3')
    assert Fraction(*positions[1]['turn']) == factory.word_carrier.turn('three')
    assert positions[0]['interior_receipt'] == payload['characters']['3']['receipt']
    assert positions[1]['interior_receipt'] == payload['number_names']['three']['receipt']
    word = payload['number_names']['three']['construction']['placements']
    assert [p['identity'] for p in word] == list('three')
    assert [p['radius']['power_of_two_denominator'] for p in word] == [5, 4, 3, 2, 1]
    assert payload['number_names']['three']['receipt'] == factory.word(factory.word_ids['three']).receipt


@pytest.mark.parametrize('mutate', [
    lambda p: p['entries'].pop(),
    lambda p: p['entries'].reverse(),
    lambda p: p['definitions'].pop(),
    lambda p: p['definitions'][0]['construction']['placements'][0].update(arity=157),
    lambda p: p['definitions'][0]['construction']['placements'][0]['radius'].update(power_of_two_denominator=2),
    lambda p: p['definitions'][0]['construction']['placements'][0].update(interior_receipt=None),
    lambda p: p['counts'].update(characters=True),
    lambda p: p['characters']['A']['construction'].update(origin='A'),
    lambda p: p['entries'][-1]['entry'].update(hmmm=False),
    lambda p: p['source'].update(text='invented table'),
    lambda p: p.update(hmmm=[]),
])
def test_tampering_refuses(factory, mutate):
    payload = definitions.build_definitions(factory)
    mutate(payload)
    with pytest.raises(ValueError, match='replay mismatch'):
        definitions.verify_definitions(factory, payload)


def test_json_roundtrip_preserves_every_entry_and_closure(factory):
    payload = definitions.build_definitions(factory)
    restored = json.loads(json.dumps(payload, ensure_ascii=False))
    assert definitions.verify_definitions(factory, payload).receipt == definitions.verify_definitions(factory, restored).receipt


def test_missing_number_name_refuses_without_carrier_mutation(factory):
    words = {i: word for i, word in factory.words.items() if word != 'three'}
    narrowed = Factory(factory.public, words, factory.source_receipt)
    before = narrowed.word_carrier.receipt
    with pytest.raises(ValueError, match='not admitted: three'):
        definitions.build_definitions(narrowed)
    assert narrowed.word_carrier.receipt == before


def test_default_manifest_requires_definition_receipt():
    from english_gonol import ordinal_construct as implementation
    from test_ordinal_construct import manifest_fixture
    manifest = manifest_fixture()
    assert implementation._validate_manifest(manifest) is None
    manifest.pop('character_definitions_receipt')
    with pytest.raises(ValueError, match='manifest schema'):
        implementation._validate_manifest(manifest)


def test_default_build_and_verifier_consume_definition_component():
    import ast
    import inspect
    from english_gonol import ordinal_construct as implementation
    producer = ast.parse(inspect.getsource(implementation.build))
    checker = ast.parse(inspect.getsource(implementation.verify))
    def names(tree):
        return {n.func.id for n in ast.walk(tree)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert 'build_definitions' in names(producer)
    assert 'verify_definitions' in names(checker)
    for tree in (producer, checker):
        assert any(isinstance(n, ast.Constant) and n.value == 'character-definitions.json'
                   for n in ast.walk(tree))
