# Grok AHBG freeze

Frozen implementation SHA:

```text
cce9cec7dae61304118efcd47bc0d7461200d335
```

Short SHA: `cce9cec`

Commit subject: `Add independent Grok a0 and AHBG smoke-epoch calibration pair`

This file is post-freeze metadata. Reciprocal review identity is that SHA, not
later metadata or review commits on `agent/ahbg-grok`.

## Verification at freeze

- A0 tests: 3 OK
- AHBG tests: 3 OK
- Smoke: plain_move_loop SURVIVED, hard_veto_illegal_action SURVIVED,
  occupied_target_collision UNRESOLVED, dual_target_collision UNRESOLVED

## Usage

```bash
git switch agent/ahbg-grok
cd stack/ahbg/grok
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s a0/tests -p 'test*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ahbg/tests -p 'test*.py'
```

Implementation source and smoke artifacts under `a0/`, `ahbg/`, and
`artifacts/` must not change in post-freeze commits.

## war_v3 engine divergence (recorded post-freeze)

The canonical `main` line adopted war_v3 after the frozen build. The engine
now resolves War deterministically (`patch.py` defender-holds + smallest-unit
priority, `KIND_WAR` events) and imports UCNS from the pinned canonical
`libs/ucns/src` view. This diverges from frozen SHA `cce9cec`; reciprocal
review identity remains `cce9cec` for historical comparison.
