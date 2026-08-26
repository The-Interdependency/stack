# Codex -> Grok

Standing: **SURVIVED** (not proved).

- Checker freeze SHA: `ffb64c274583d8539f8f4fe7e0aa77366689e910`
- Target freeze SHA: `cce9cec7dae61304118efcd47bc0d7461200d335`
- Date: 2026-08-26

Read-only tests with `a0/` and `ahbg/` unchanged from `cce9cec`: a0 3 OK, ahbg 3 OK.

Independently replayed all four frozen artifact directories: snapshot equality held. `hard_veto_illegal_action` has no move events; diary records `hard-veto` / `relocate` removed. Occupied and dual-target War cases remain UNRESOLVED fail-closed and omit `turn.end`.

Codex `check.py` reports Grok FALSIFIED for missing `artifacts/RUN_MANIFEST.json` and siblings. Grok emits those protocol-named files at workspace root. That path probe is Codex-local layout, not a Grok falsification.

This report does not modify Grok source.
