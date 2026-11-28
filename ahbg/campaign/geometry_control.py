"""Replay normal, removal, restoration and irrelevant-change geometry arms."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "node_modules")
        for sub in (
            "ahbg/campaign",
            "ahbg/runtime",
            "ahbg/integration",
            "ahbg/grok/ahbg",
            "libs/ucns/src",
        ):
            shutil.copytree(ROOT / sub, root / sub, ignore=ignore)

        def probe():
            p = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    "-c",
                    (
                        "from pathlib import Path; from tempfile import TemporaryDirectory; "
                        "from ahbg.campaign.mission import Case, play; from ahbg.campaign.controllers import Scripted; "
                        "d=TemporaryDirectory(); r=play(Case(),Scripted(),Path(d.name)); print(r['state_digest'])"
                    ),
                ],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONPATH": str(root), "PYTHONNOUSERSITE": "1"},
            )
            return {
                "ok": p.returncode == 0,
                "result": (p.stdout if p.returncode == 0 else p.stderr)
                .strip()
                .splitlines()[-1],
            }

        source = root / "libs/ucns/src/ucns/mobius_seed.py"
        saved = source.read_bytes()
        normal = probe()
        source.rename(source.with_suffix(".absent"))
        missing = probe()
        source.write_bytes(saved)
        restored = probe()
        (root / "unread.txt").write_text("irrelevant change\n")
        irrelevant = probe()
        if (
            not normal["ok"]
            or missing["ok"]
            or "mobius_seed" not in missing["result"]
            or not normal == restored == irrelevant
        ):
            raise ValueError("geometry control evidence differs")
        return {
            "normal": normal,
            "removed": missing,
            "restored": restored,
            "irrelevant": irrelevant,
        }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
