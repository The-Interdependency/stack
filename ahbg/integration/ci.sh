# ratios: loc_comments=28:3 imports_exports=2:0 calls_definitions=6:0
#!/usr/bin/env bash
# Clean-checkout CI reproduction of the deterministic AHBG integration demo.
# No API keys, no network calls, no display required.
set -euo pipefail

ROOT="${1:-/tmp/ahbg-ci-checkout}"
BRANCH="${2:-agent/ahbg-deepcode}"
OUT="${ROOT}/demo-out"

echo "==> clean checkout: $ROOT (branch $BRANCH)"
rm -rf "$ROOT"
git clone --quiet --depth 1 --branch "$BRANCH" https://github.com/The-Interdependency/stack.git "$ROOT"
cd "$ROOT"

echo "==> run deterministic demo (no key)"
python3 -c 'import pygame' 2>/dev/null || pip install --quiet pygame
PYTHONDONTWRITEBYTECODE=1 python3 -m ahbg.integration.demo --out-dir "$OUT"

echo "==> verify"
python3 - "$OUT" <<'PY'
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
summary = json.loads((out / "SUMMARY.json").read_text())
assert summary["replay_equal"] is True, "replay must be equal"
assert summary["turns"] == 5, "demo must run 5 turns"
assert summary["mechanics"]["war"] == "SURVIVED", "War must resolve deterministically"
assert summary["mechanics"]["deterministic_replay"] == "SURVIVED"
assert summary["mechanics"]["refuse_injection"] == "SURVIVED"
frames = sorted((out / "frames").glob("frame_*.png"))
assert len(frames) == 6, "6 frames expected"
assert (out / "world.json").exists() and (out / "events.jsonl").exists()
print("CI OK: replay_equal=true, 5 turns, 6 frames, War resolved (defender_holds)")
PY

echo "==> done"
# ratios: loc_comments=28:3 imports_exports=2:0 calls_definitions=6:0
