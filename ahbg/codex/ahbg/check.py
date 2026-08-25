"""Read-only artifact checks for reciprocal AHBG review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_ARTIFACTS = (
    "BUILD_MANIFEST.json",
    "artifacts/RUN_MANIFEST.json",
    "artifacts/EVENTS.jsonl",
    "artifacts/CALIBRATION_RESULT.json",
    "artifacts/CALIBRATION_REPORT.md",
)


def _json_file(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def check_artifact_dir(root: str | Path) -> dict[str, Any]:
    """Check a frozen build directory without modifying it."""
    target = Path(root)
    findings: list[dict[str, Any]] = []
    for relative in REQUIRED_ARTIFACTS:
        path = target / relative
        if not path.is_file():
            findings.append({"standing": "FALSIFIED", "path": relative, "reason": "missing"})

    parsed: dict[str, Any] = {}
    for relative in (
        "BUILD_MANIFEST.json",
        "artifacts/RUN_MANIFEST.json",
        "artifacts/CALIBRATION_RESULT.json",
    ):
        path = target / relative
        if path.is_file():
            try:
                parsed[relative] = _json_file(path)
            except Exception as exc:  # noqa: BLE001 - checker reports, does not repair.
                findings.append({"standing": "FALSIFIED", "path": relative, "reason": str(exc)})

    events = target / "artifacts" / "EVENTS.jsonl"
    if events.is_file():
        try:
            previous_seq = -1
            for line in events.read_text(encoding="utf-8").splitlines():
                record = json.loads(line)
                seq = record.get("seq")
                if isinstance(seq, bool) or not isinstance(seq, int) or seq <= previous_seq:
                    raise ValueError("event seq must strictly increase")
                previous_seq = seq
        except Exception as exc:  # noqa: BLE001
            findings.append({"standing": "FALSIFIED", "path": "artifacts/EVENTS.jsonl", "reason": str(exc)})

    result = parsed.get("artifacts/CALIBRATION_RESULT.json")
    if isinstance(result, dict):
        summary = result.get("summary")
        if not isinstance(summary, dict):
            findings.append({"standing": "FALSIFIED", "path": "artifacts/CALIBRATION_RESULT.json", "reason": "missing summary"})
        elif summary.get("falsified", 0):
            findings.append({"standing": "FALSIFIED", "path": "artifacts/CALIBRATION_RESULT.json", "reason": "result contains falsifications"})

    return {
        "schema": "interdependency.ahbg.codex.artifact-check/1.0.0",
        "target": str(target),
        "standing": "SURVIVED" if not findings else "FALSIFIED",
        "findings": findings,
    }
