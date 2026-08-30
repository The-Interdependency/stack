# Grok A0 smoke-epoch calibration report

Independent realization in `stack/ahbg/grok/`. Provider is a relation, not identity.
Shadow epoch: C_lambda is logged and does not select actions.

| scenario | standing | seed | replay |
|---|---|---:|---|
| plain_move_loop | SURVIVED | 7 | True |
| hard_veto_illegal_action | SURVIVED | 11 | True |
| occupied_target_collision | UNRESOLVED | 13 | True |
| dual_target_collision | UNRESOLVED | 17 | True |

Hard veto removes relocate. Occupied and dual-target intents fail closed as UNRESOLVED (War).
This is not the sealed triplicate corpus and not a reciprocal check.

## Usage

```bash
cd stack/ahbg/grok
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s a0/tests -p 'test*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ahbg/tests -p 'test*.py'
PYTHONDONTWRITEBYTECODE=1 python3 run.py
python3 checker.py
```
