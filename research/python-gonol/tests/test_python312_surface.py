# === CHECKS ===
# id: python312_full_surface_affixiates_check
#   proves: python_constructions_affixiate_closed_gonols, python_affixiation_is_lossless_and_replayable
#   call: self::test_python312_surface_affixiates_from_letters_through_module
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: spanless_python_relations_remain_intrinsic_check
#   proves: python_constructions_affixiate_closed_gonols, parser_objects_never_become_gonols
#   call: self::test_spanless_grammar_relations_remain_inside_the_source_parent
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from python_gonol import (
    affixiate_python_source,
    reconstruct_source,
    replay_python_affixiation,
)


PYTHON_312_SURFACE = '''\
from __future__ import annotations
import os as operating_system
from .package import value as renamed

type Pair[T] = tuple[T, T]

@decorate(flag=True)
class Example[T](Base, metaclass=Meta):
    class_attr: int = 1

    def method(self, x: int = 0, /, *args: str, flag=True, **kwargs) -> int:
        global module_name
        local: int
        local = (x := x + 1)
        assert local >= 0, "nonnegative"
        if flag and local:
            values = [item * 2 for item in range(local) if item % 2]
        elif not flag or local is None:
            values = {key: value for key, value in enumerate(args)}
        else:
            values = {*(1, 2), *range(3)}
        for item in values:
            if item == 2:
                continue
            break
        while local > 0:
            local -= 1
        try:
            with open("path") as handle, lock:
                data = handle.read()
        except OSError as exc:
            raise RuntimeError("failed") from exc
        else:
            pass
        finally:
            del local
        match data:
            case {"x": [first, *rest]} if first > 0:
                point = first
            case Example(value=point):
                point = point
            case 1 | 2:
                point = 0
            case _:
                point = -1
        return lambda y: y if y else None

    async def stream(self, source):
        async with source as opened:
            async for value in opened:
                yield f"{value=!r:>{width}}"
        await source.close()


def nested():
    captured = 1
    def inner():
        nonlocal captured
        captured += 1
        return captured
    return inner


def generator():
    yield from (number for number in range(3))


def grouped_errors():
    try:
        raise ExceptionGroup("group", [ValueError()])
    except* ValueError as errors:
        pass


raw = rb"bytes\\x00"
text = r"raw" "joined"
ellipsis_value = ...
mapping = {"slice": values[1:10:2], "call": callable(*args, **kwargs)}
comparisons = 0 < value <= 10 != other
bits = (~value & mask) | (value ^ mask) << 2 >> 1
matrix = left @ right
power = base ** exponent // divisor / ratio
'''


def test_python312_surface_affixiates_from_letters_through_module() -> None:
    receipt = affixiate_python_source(PYTHON_312_SURFACE, source_id="fixtures/python312.py")
    assert receipt.standing == "implemented-candidate"
    assert reconstruct_source(receipt) == PYTHON_312_SURFACE
    replay_python_affixiation(receipt)
    relations = {gonol.relation.kind for gonol in receipt.gonols}
    expected = {
        "python.grammar.Module",
        "python.grammar.TypeAlias",
        "python.grammar.TypeVar",
        "python.grammar.ClassDef",
        "python.grammar.FunctionDef",
        "python.grammar.AsyncFunctionDef",
        "python.grammar.AsyncFor",
        "python.grammar.AsyncWith",
        "python.grammar.Await",
        "python.grammar.Yield",
        "python.grammar.YieldFrom",
        "python.grammar.Try",
        "python.grammar.TryStar",
        "python.grammar.Match",
        "python.grammar.MatchMapping",
        "python.grammar.MatchSequence",
        "python.grammar.MatchClass",
        "python.grammar.MatchOr",
        "python.grammar.NamedExpr",
        "python.grammar.JoinedStr",
        "python.grammar.FormattedValue",
        "python.grammar.ListComp",
        "python.grammar.DictComp",
        "python.grammar.Set",
        "python.grammar.GeneratorExp",
        "python.grammar.comprehension",
        "python.grammar.Lambda",
        "python.grammar.arguments",
        "python.grammar.keyword",
        "python.grammar.alias",
    }
    assert expected <= relations
    assert any(gonol.relation.kind == "python.delimiter.parentheses" for gonol in receipt.gonols)
    assert any(gonol.relation.kind == "python.delimiter.brackets" for gonol in receipt.gonols)
    assert any(gonol.relation.kind == "python.delimiter.braces" for gonol in receipt.gonols)
    decorated_class = next(
        gonol for gonol in receipt.gonols if gonol.relation.kind == "python.grammar.ClassDef"
    )
    assert decorated_class.span.start == PYTHON_312_SURFACE.index("@decorate")


def test_spanless_grammar_relations_remain_inside_the_source_parent() -> None:
    source = "# type: ignore[index]\ndef empty():\n    pass\n"
    receipt = affixiate_python_source(source, source_id="fixtures/spanless-relations.py")
    module = receipt.gonols[-1]
    function = next(
        gonol for gonol in receipt.gonols if gonol.relation.kind == "python.grammar.FunctionDef"
    )
    module_properties = dict(module.relation.properties)
    function_properties = dict(function.relation.properties)
    assert '"grammar_construct":"TypeIgnore"' in module_properties[
        "grammar_field.type_ignores[0].spanless_relation"
    ]
    assert '"grammar_construct":"arguments"' in function_properties[
        "grammar_field.args.spanless_relation"
    ]
    replay_python_affixiation(receipt)
