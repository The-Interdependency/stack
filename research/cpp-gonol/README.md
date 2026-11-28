# C++23 source construction

The physical profile constructs UTF-8 C++ source using native UCNS Unicode
glyphs. Its phase-2 map retains physical scalar ranges for the initial BOM,
newline spellings, splices and synthesized final newline. The original file is
recovered from the ordered glyph diameters. Under the optional binding profile
each declaration, assignment and return closes over native token frames. Blocks
and the complete function retain their child frames, ordinal radii, endpoint and
additive resultant. Each name read identifies its declaration and reaching write.

The implementation and acceptance suite originate in this Stack workspace.
The extracted UCHC package supplies the running consumer. Exact dependencies,
language revision, corpus and wheel identity are in [BASE.json](BASE.json).
[The UCHC guide](https://github.com/The-Interdependency/uchc/blob/455c74cfab50f346380a7327feb01fe871b4c346/programming/cpp/README.md)
specifies the admitted integer grammar and shows how to inspect its return value.

## Run a clean consumer

From Stack's root, use Python 3.12+ with the UCNS repository at
`1edfa593ae9d8c9ad394b5462638bcc717f99fbd` in a sibling directory named
`ucns`. The compiler cases require a C++23 compiler available as `c++` or `CXX`.

```sh
python -m venv /tmp/cpp-uchc
p=/tmp/cpp-uchc/bin/python
"$p" -m pip install --no-deps ../ucns
mkdir -p /tmp/cpp-dist
curl -fsSL -o /tmp/cpp-dist/uchc-0.2.0a5-py3-none-any.whl \
  https://github.com/The-Interdependency/uchc/releases/download/uchc-v0.2.0a5/uchc-0.2.0a5-py3-none-any.whl
"$p" -m pip install --no-deps --require-hashes --find-links /tmp/cpp-dist --no-index -r integration/uchc/cpp-requirements.txt
"$p" -I -m cpp_gonol build example.cpp binding.json --bindings
"$p" -I -m cpp_gonol verify binding.json --original example.cpp
"$p" -I -m unittest discover -s research/cpp-gonol/tests -v
```

## Reproduce the evidence

The corpus includes every tracked blob with one of the declared C++ source or
header suffixes in fmt 11.2.0, including its tests and bundled sources. The
qualifier reads the exact Git objects. Its per-file rows bind the path, Git
blob, original SHA-256, occurrence count and construct receipt. It does not
execute corpus inputs. A separate sweep checks every valid Unicode scalar,
including exact bytes, SPACE-relative turn and optional Public Gonol position.

```sh
git clone --depth=1 --branch 11.2.0 https://github.com/fmtlib/fmt.git /tmp/cpp-fmt
"$p" -I research/cpp-gonol/qualify.py corpus /tmp/cpp-fmt > /tmp/cpp-fmt.json
cmp /tmp/cpp-fmt.json research/cpp-gonol/evidence/fmt-11.2.0.json
"$p" -I research/cpp-gonol/qualify.py unicode > /tmp/cpp-unicode.json
cmp /tmp/cpp-unicode.json research/cpp-gonol/evidence/unicode.json
```

To exercise the forge source, use the same UCNS installation and the released
UCHC ordinal-halving API, then place `research/cpp-gonol` on `PYTHONPATH` and
omit `-I`. The compiler is an independent witness on eight fixed integer
programs. Unsupported programs retain their physical source. Binding mode
rejects inputs outside its grammar.

**hmmm** — Macro expansion, templates, overloads and general C++ execution
require their own construction and replay evidence.
