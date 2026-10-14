# Vendored agent skills

This directory contains repo-local consumed copies of canonical skills from
`The-Interdependency/skill-lib`.

Installed subset:

- `stack-update` — source `The-Interdependency/skill-lib@321e721fb660e0fea5bb8c37d943611963039a57`, path `stack-update/SKILL.md`, source blob `9ec21b07d01a099021778a0c8774b810c2619d63`.

Canonical doctrine remains in `skill-lib`; vendoring does not transfer authority.
Structural stack changes must follow `.agents/skills/stack-update/SKILL.md` and pass
`python tools/check_stack_consistency.py` before merge.
