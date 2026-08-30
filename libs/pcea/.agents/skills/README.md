# Repo-local agent skills

This repo consumes The Interdependency organization skill library.

Canonical source:
- Preferred: `The-Interdependency/skill-lib`
- Temporary source: `The-Interdependency/a0/skill-lib`

Source commit: `The-Interdependency/skill-lib` @ `a0cb6285e37734609b4b487ae4a2e44c6108d2b8` (verbatim sync).

Installed skills:
- `msdmd/` — Module Self-Declared Metadata Markdown
- `test-build/` — test contract metadata blocks
- `meta-module-build/` — metadata-first module scaffolding
- `manifest/` — living-spec generator for `CLAUDE.md` (vendored from `The-Interdependency/skill-lib@05ee7aa`); CI runs `generate.py --check`. Refresh with `python .agents/skills/manifest/generate.py --write`.

Agents working in this repo should read `meta-module-build/SKILL.md` before
creating new modules, routes, services, schemas, adapters, workers, engines,
UI panels, migrations, or experiments.
