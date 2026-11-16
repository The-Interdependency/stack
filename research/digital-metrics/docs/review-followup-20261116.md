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

hmmm: current-head hosted checks and review remain separate evidence. No EDCM
measurement, signature or arbitrary-Python attestation follows from this repair.

GPT generated; context, prompt Erin Spencer.
