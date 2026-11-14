# ratios: loc_comments=84:14 imports_exports=9:2 calls_definitions=42:2
"""Run an independent full-field check and retain a reproducible Unicode corpus witness."""
import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from english_gonol import unicode_construction as unicode
from english_gonol import unicode_corpus as corpus
from english_gonol.language.character_definitions import CharacterDefinitionLayer, load_character_definition_table
from english_gonol.structural_rules import canonical, digest

# === MODULE_BUILD ===
# id: english_unicode_corpus_witness
#   module_name: verify_unicode_corpus
#   public_surface: witness, main
#   summary: independently check Unicode geometry, corpus ownership and native recursive re-entry
#   owner: Erin Spencer
#   tests: complete Unicode corpus workflow
# === END MODULE_BUILD ===
# === CHECKS ===
# id: complete_unicode_corpus_replay
#   proves: unicode_corpus_replay, unicode_corpus_preserves_ownership, unicode_corpus_declared_placement
#   call: self::witness
# === END CHECKS ===


def witness(directory, native_root):
    native = unicode._native(native_root)
    with corpus._verified(directory, native) as (source, _, db, manifest):
        glyphs = {}
        for cp, char, utf8, diameter, n, d, receipt in db.execute('SELECT * FROM glyphs ORDER BY cp'):
            turn = Fraction((ord(char) - 32) % 0x110000, 0x110000)
            if (cp, utf8, diameter, n, d) != (ord(char), char.encode(), ord(char).to_bytes(4,'big'),
                                              turn.numerator,turn.denominator):
                raise ValueError('independent scalar replay mismatch')
            glyphs[char] = (receipt, [n,d])
        word_count = occurrence_count = 0
        for wid, text, receipt in db.execute('SELECT * FROM words ORDER BY id'):
            frame = native.unicode_gonol.build_unicode_scalar_frame(text)
            if (frame.recover(), frame.utf32_be, frame.receipt) != (text, text.encode('utf-32-be'), receipt):
                raise ValueError(f'word frame mismatch: {wid}')
            if len(frame.placements) != len(text):
                raise ValueError('missing glyph occurrence')
            for index, (char, placement) in enumerate(zip(text, frame.placements, strict=True)):
                expected_receipt, turn = glyphs[char]
                if (placement.ordinal != index or placement.radius != 1 or placement.glyph.character != char
                        or placement.glyph.receipt != expected_receipt or placement.turn != Fraction(*turn)):
                    raise ValueError('independent word placement mismatch')
                occurrence_count += 1
            word_count += 1
        definition_count = number_names = unknown = 0
        closure_digest = sha256()
        for cp, ordinal, entry_json, relation, _, word_id in db.execute('SELECT * FROM definitions ORDER BY cp,ordinal'):
            char = chr(cp)
            bearings = (Fraction(0),) if word_id is None else (Fraction(0), Fraction(1,2))
            item = corpus._definition(source, db, char, ordinal, native, bearings)
            restored = native.unicode_recursive.replay_unicode_graph(item['construction'])
            entry = json.loads(entry_json)
            if restored.recover() != char + (entry['number_name'] if word_id is not None else ''):
                raise ValueError('inherited definition failed recursive replay')
            if word_id is not None:
                stored, = db.execute('SELECT receipt FROM words WHERE id=?',(word_id,)).fetchone()
                if restored.participants[1].receipt != stored:
                    raise ValueError('number-name word differs from the corpus object')
                number_names += 1
            unknown += relation == 'definition:hmmm'
            closure_digest.update(canonical([cp, ordinal, restored.receipt]) + b'\n')
            definition_count += 1
        record_id = 150508
        compound = corpus._record(source, db, record_id,native,(0, Fraction(1,4),Fraction(1,2),Fraction(3,4)))
        owner = source.execute('SELECT text FROM records WHERE id=?',(compound['owner_record_id'],)).fetchone()
        if owner != ('a cappella',) or compound['recovered'] != 'sung without instrumental accompaniment':
            raise ValueError('compound ownership or source text drift')
        entries = load_character_definition_table()
        layer = CharacterDefinitionLayer(entries, {}, (), '')
        return {'profile':corpus.PROFILE, 'admission':manifest['admission'],
                'source_counts':manifest['source_counts'], 'rows':manifest['counts'],
                'geometry_rows_sha256':manifest['geometry_rows_sha256'], 'manifest_sha256':digest(manifest),
                'verified_native_words':word_count, 'verified_word_glyph_occurrences':occurrence_count,
                'verified_glyphs':len(glyphs), 'corpus_lexical_definitions':source.execute(
                    "SELECT count(*) FROM records WHERE kind='definition'").fetchone()[0],
                'verified_inherited_definitions':definition_count, 'explicit_unknown_definitions':unknown,
                'verified_number_name_interiors':number_names, 'definition_closures_sha256':closure_digest.hexdigest(),
                'declared_definition_bearings':{'owner':[0,1],'number_name':[1,2]},
                'compound_fixture':{'record':record_id,'owner':owner[0],'attachment':compound['attachment_reference'],
                                    'declared_word_turns':[[0,1],[1,4],[1,2],[3,4]],
                                    'root':compound['construction']['root']},
                'inherited_behavior':{'try_ing':layer.final_y_realization('y','r','ing',True),
                                      'try_ed':layer.final_y_realization('y','r','ed',True)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('native_root', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    result = canonical(witness(args.directory,args.native_root)) + b'\n'
    if args.expect is not None and result != args.expect.read_bytes():
        raise ValueError('corpus witness differs from complete replay')
    print(result.decode(), end='')


if __name__ == '__main__':
    main()
# ratios: loc_comments=84:14 imports_exports=9:2 calls_definitions=42:2
