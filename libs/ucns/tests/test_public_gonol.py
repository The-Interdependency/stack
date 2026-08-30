# === CHECKS ===
# id: public_gonol_geometry_check
#   proves: public_gonol_has_exactly_157_unique_positions, every_public_gonol_glyph_is_a_function_position
#   call: self::test_public_gonol_exact_and_unclassified
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from ucns.public_gonol import (
    PUBLIC_GONOL_157,
    PUBLIC_GONOL_SHA256,
    public_gonol_function,
    public_gonol_position,
    public_gonol_sha256,
)


def test_public_gonol_exact_and_unclassified() -> None:
    assert len(PUBLIC_GONOL_157) == 157
    assert len(set(PUBLIC_GONOL_157)) == 157
    assert PUBLIC_GONOL_157[0] == " "
    assert public_gonol_sha256() == PUBLIC_GONOL_SHA256

    for index, glyph in enumerate(PUBLIC_GONOL_157):
        function = public_gonol_function(index)
        assert function.index == index
        assert function.glyph == glyph
        assert public_gonol_function(glyph) == function
        assert public_gonol_position(glyph) == index

    assert public_gonol_function("a").__class__ is public_gonol_function("'").__class__
    assert public_gonol_function("1").__class__ is public_gonol_function("∫").__class__
