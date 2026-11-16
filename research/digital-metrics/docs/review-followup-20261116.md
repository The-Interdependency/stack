# Multiline-comment projection repair

At reviewed head `86cc63e45cba2fd14f9b8258e8be1def3fce315b`, replacing the
authority header with `| Repository | Auth<!--\n-->ority |` produces no finding.
The comment remover joins separate physical lines, manufacturing a table that
the human Markdown does not render. This reproduces review comment 4581911495.

`rendered_markdown_lines` now preserves every CR/LF boundary in both closed and
unterminated comments. The regression rejects split headers and headings for LF,
CRLF and CR, checks closed/unterminated comment boundaries, and retains admission
of an inline comment that does not split the header.

The reviewed suite passes all 35 tests with zero skips. Static linkage has 30
contracts and 35 checks, with zero behavioral verification credit. Stack
consistency and portfolio validation pass. Both changed Python ratio gates and
the whitespace check pass. The repaired receipt still replays byte for byte with
payload `456f16a7b6348209f9399ffa8723105d7959dac73f862b99083a1d2315517a19`;
neither receipt nor producer pins changed.

Run the acceptance commands in [the initial repair record](review-repair-20261115.md).
That record's 34-test result remains historical; this follow-up adds one test.

## Block-comment follow-up

Fresh review of `e8783952cf2bb5afa14a722df1e7b0cfb63e8836` reproduced another
false admission: `<!-- hidden\n-->| Repository | Authority |` promotes the
terminating line's suffix into a table header. Both comments 4581963896 and
4581963901 report that same defect. GFM's
[HTML-block rules](https://github.github.com/gfm/#html-blocks) include the entire
terminating line in the block.

Comment handling now follows the existing fence/raw-block state. Block comments
consume whole lines, including their closing line. Multiline inline comments are
conservatively excluded through their closing line; only valid single-line inline
comments can join visible text. Malformed inline HTML cannot manufacture a
projection. A second regression covers both headings and headers, all three
newline formats, zero to three spaces, same-line and multiline block comments,
fenced comment text and malformed inline comments. The valid inline control stays
admitted. No general Markdown renderer is claimed.

Current result: **36 reviewed tests pass**, zero skips; static linkage has 30
contracts and 36 checks with zero behavioral verification credit. Consistency,
portfolio validation, both changed-source ratio gates and whitespace checks pass.
Receipt replay retains the same payload and bytes. The earlier 34/35-test records
remain historical observations.

hmmm: current-head hosted checks and review remain separate evidence. No EDCM
measurement, signature or arbitrary-Python attestation follows from this repair.

GPT generated; context, prompt Erin Spencer.
