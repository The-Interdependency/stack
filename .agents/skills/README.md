# Vendored agent skills

This directory contains repo-local consumed copies of canonical skills from
`The-Interdependency/skill-lib`.

Installed subset:

- `stack-update` — source `The-Interdependency/skill-lib@a7b95f891d2e88c62e61524dc52a2e1577c9983d`, path `stack-update/SKILL.md`, source blob `a1e914893fa047e28d039050395937a1cf6e0138`.

Canonical doctrine remains in `skill-lib`; vendoring does not transfer authority.
Structural stack changes must follow `.agents/skills/stack-update/SKILL.md` and pass
`python tools/check_stack_consistency.py` before merge.
