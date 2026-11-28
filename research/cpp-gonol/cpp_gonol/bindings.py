# ratios: loc_comments=15:145 imports_exports=3:2 calls_definitions=71:12
# === CONTRACTS ===
# id: cpp23_local_binding_relation
#   given: an admitted int-main program with lexical scopes and ordered native token frames
#   then: recover bindings, reaching writes, statement interiors and the portable integer return
# === END CONTRACTS ===
"""Closed token and statement gonols for the opt-in C++23 int-main profile."""
from __future__ import annotations

from dataclasses import dataclass
import re

# Phases 1 and 2 have already run. The only tokens admitted by this grammar are
# ASCII names, unsuffixed decimal numbers, and the punctuation below.
_LEXEME = re.compile(r"[ \t\v\f\n]+|//[^\n]*|/\*.*?\*/|[A-Za-z_][A-Za-z_0-9]*|[0-9]+|[{}();=+]", re.DOTALL)
_NAME = re.compile(r"[a-z][A-Za-z0-9_]*")
_KEYWORDS = frozenset("""
    alignas alignof and and_eq asm auto bitand bitor bool break case catch char char8_t
    char16_t char32_t class compl concept const consteval constexpr constinit const_cast
    continue co_await co_return co_yield decltype default delete do double dynamic_cast else
    enum explicit export extern false float for friend goto if inline int long mutable namespace
    new noexcept not not_eq nullptr operator or or_eq private protected public register
    reinterpret_cast requires return short signed sizeof static static_assert static_cast
    struct switch template this thread_local throw true try typedef typeid typename union
    unsigned using virtual void volatile wchar_t while xor xor_eq
""".split())


@dataclass
class Binding:
    declaration: int
    write: int | None = None
    value: int | None = None


class _Program:
    def __init__(self, text, origins, source_id, native, recursive):
        self.frames = []
        self.spellings = []
        self.origins = []
        self.source_id = source_id
        self.recursive = recursive
        self.cursor = 0
        self.scopes = []
        self.parts = []
        self.events = []
        cache = {}
        pos = 0
        while pos < len(text):
            match = _LEXEME.match(text, pos)
            if match is None:
                raise ValueError(f"outside int-main profile at physical scalar {origins[pos]}")
            start, pos = match.span()
            spelling = match.group()
            if spelling[0] in " \t\v\f\n" or spelling.startswith(("//", "/*")):
                continue
            if spelling not in cache:
                cache[spelling] = native.build_unicode_scalar_frame(spelling)
            frame = cache[spelling]
            self.frames.append(frame)
            self.spellings.append(frame.recover())
            self.origins.append(origins[start:pos])

    def peek(self):
        return self.spellings[self.cursor] if self.cursor < len(self.spellings) else None

    def take(self, expected=None):
        token = self.peek()
        if token is None or (expected is not None and token != expected):
            raise ValueError(f"int-main token {self.cursor}: expected {expected or 'an operand'}")
        index = self.cursor
        self.cursor += 1
        return index

    def name(self):
        token = self.peek() or ""
        if not _NAME.fullmatch(token) or "__" in token or token in _KEYWORDS:
            raise ValueError(f"int-main token {self.cursor}: expected an admitted local name")
        return token, self.take()

    def lookup(self, name):
        for _, scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise ValueError(f"unbound local name: {name}")

    def expression(self):
        reads = []
        value = 0
        while True:
            spelling = self.peek() or ""
            if spelling.isascii() and spelling.isdecimal():
                self.take()
                if (len(spelling) > 1 and spelling.startswith("0")) or len(spelling) > 5:
                    raise ValueError("outside portable decimal literal profile")
                value += int(spelling)
            else:
                name, ordinal = self.name()
                binding = self.lookup(name)
                if binding.write is None:
                    raise ValueError(f"read before initialization: {name}")
                reads.append({"token": ordinal, "declaration": binding.declaration, "write": binding.write})
                value += binding.value
            if value > 32767:
                raise ValueError("outside portable int range 0..32767")
            if self.peek() != "+":
                return value, reads
            self.take("+")

    def statement(self):
        start = self.cursor
        scope_id, scope = self.scopes[-1]
        target = None
        if self.peek() == "int":
            self.take("int")
            kind = "declare"
            name, target = self.name()
            if name in scope:
                raise ValueError(f"duplicate local declaration: {name}")
            # Its locus precedes the initializer, including when an outer name exists.
            binding = scope[name] = Binding(target)
        elif self.peek() == "return":
            self.take("return")
            if len(self.scopes) != 1:
                raise ValueError("the profile requires a terminal return in the outer block")
            kind = "return"
        else:
            kind = "assign"
            name, target = self.name()
            binding = self.lookup(name)
        if target is not None:
            self.take("=")
        value, reads = self.expression()
        self.take(";")
        frame = self.recursive.close_unicode(
            tuple(self.frames[start:self.cursor]), relation="cpp23." + kind,
            source=f"{self.source_id}#tokens[{start},{self.cursor})")
        event = {"kind": kind, "scope": scope_id, "tokens": [start, self.cursor],
                 "frame": frame.receipt, "reads": reads, "value": value}
        if target is not None:
            binding.write, binding.value = target, value
            event.update(target=target, declaration=binding.declaration)
        self.parts.append(frame)
        self.events.append(event)
        return kind

    def delimiter(self, token):
        ordinal = self.take(token)
        self.parts.append(self.frames[ordinal])
        return ordinal

    def run(self):
        for token in ("int", "main", "(", ")"):
            self.delimiter(token)
        self.scopes.append((self.delimiter("{"), {}))
        while self.scopes:
            token = self.peek()
            if token == "{":
                self.scopes.append((self.delimiter("{"), {}))
            elif token == "}":
                self.delimiter("}")
                self.scopes.pop()
            elif self.statement() == "return":
                self.delimiter("}")
                self.scopes.pop()
                if self.peek() is not None:
                    raise ValueError("expected the end of the int-main program")
        if self.peek() is not None or not self.events or self.events[-1]["kind"] != "return":
            raise ValueError("the profile requires exactly one terminal return")
        root = self.recursive.close_unicode(tuple(self.parts), relation="cpp23.int-main", source=self.source_id)
        return {"profile": "cpp23.int-main/1", "token_occurrences": self.origins, "events": self.events,
                "graph": self.recursive.export_unicode_graph(root), "return_value": self.events[-1]["value"]}


def int_main(text, origins, source_id, native, recursive):
    """Construct ordered native frames, lexical scopes, reaching writes and a return value."""
    return _Program(text, origins, source_id, native, recursive).run()
# ratios: loc_comments=15:145 imports_exports=3:2 calls_definitions=71:12
