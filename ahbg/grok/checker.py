"""Read-only reciprocal checker. Writes only under this workspace.

Sealed evaluation starts after all three pairs are frozen. Until then sibling
checks are BLOCKED, not invented.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SIBLINGS = {
    "codex": ROOT.parent / "codex",
    "deepseek": ROOT.parent / "deepseek",
}


def _blocked(sibling: str, reason: str) -> dict:
    return {
        "checker": "Grok",
        "checker_workspace": "stack/ahbg/grok",
        "subject": sibling,
        "evidence_standing": "BLOCKED",
        "reason": reason,
        "sealed_epoch": False,
    }


def main() -> None:
    reviews = ROOT / "reviews"
    for name, path in SIBLINGS.items():
        dest = reviews / name
        dest.mkdir(parents=True, exist_ok=True)
        has_pair = (path / "a0").is_dir() and (path / "ahbg").is_dir()
        if not has_pair:
            payload = _blocked(name, "sibling a0+ahbg pair is absent")
        else:
            payload = _blocked(
                name,
                "sealed reciprocal epoch has not started; Grok/Codex/DeepSeek are not all frozen",
            )
        (dest / "CHECK_RESULT.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        (dest / "CHECK_REPORT.md").write_text(
            f"# Grok -> {name}\n\nStanding: {payload['evidence_standing']}\n\n{payload['reason']}\n",
            encoding="utf-8",
        )
        print(name, payload["evidence_standing"])


if __name__ == "__main__":
    main()
