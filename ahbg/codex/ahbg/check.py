"""Read-only artifact checks for reciprocal AHBG review."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REQUIRED_ARTIFACTS = (
    "BUILD_MANIFEST.json",
    "RUN_MANIFEST.json",
    "CALIBRATION_RESULT.json",
    "CALIBRATION_REPORT.md",
    "EVENTS.jsonl or */events.jsonl",
)

AGGREGATE_ARTIFACTS = (
    "RUN_MANIFEST.json",
    "EVENTS.jsonl",
    "CALIBRATION_RESULT.json",
    "CALIBRATION_REPORT.md",
)
PER_SCENARIO_ARTIFACTS = (
    "RUN_MANIFEST.json",
    "CALIBRATION_RESULT.json",
    "CALIBRATION_REPORT.md",
)


@dataclass(frozen=True)
class ArtifactLayout:
    name: str
    root: Path
    event_files: tuple[Path, ...]


def _json_file(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _layout_at(root: Path, name: str) -> ArtifactLayout | None:
    if all((root / relative).is_file() for relative in AGGREGATE_ARTIFACTS):
        return ArtifactLayout(
            name=f"{name}:aggregate-events",
            root=root,
            event_files=(root / "EVENTS.jsonl",),
        )

    scenario_events = tuple(sorted(root.glob("*/events.jsonl")))
    if scenario_events and all((root / relative).is_file() for relative in PER_SCENARIO_ARTIFACTS):
        return ArtifactLayout(name=f"{name}:per-scenario-events", root=root, event_files=scenario_events)

    return None


def _candidate_layouts(target: Path) -> list[ArtifactLayout]:
    layouts: list[ArtifactLayout] = []
    seen: set[Path] = set()

    def add(root: Path, name: str) -> None:
        if root in seen:
            return
        seen.add(root)
        layout = _layout_at(root, name)
        if layout is not None:
            layouts.append(layout)

    corpus_root = target / "corpus-run"
    if corpus_root.is_dir():
        run_dirs = (path for path in corpus_root.iterdir() if path.is_dir())
        for run_dir in sorted(run_dirs, reverse=True):
            add(run_dir, f"corpus-run/{run_dir.name}")

    add(target / "artifacts", "artifacts")
    add(target, "top-level")
    return layouts


def _build_manifest_path(target: Path, artifact_root: Path) -> Path | None:
    for path in (
        target / "BUILD_MANIFEST.json",
        artifact_root / "BUILD_MANIFEST.json",
        artifact_root.parent / "BUILD_MANIFEST.json",
        artifact_root.parent.parent / "BUILD_MANIFEST.json",
    ):
        if path.is_file():
            return path
    return None


def _label(path: Path, target: Path) -> str:
    try:
        return str(path.relative_to(target))
    except ValueError:
        return str(path)


def _check_event_file(path: Path, target: Path, findings: list[dict[str, Any]]) -> None:
    try:
        previous_seq = -1
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError("event record must be a JSON object")
            seq = record.get("seq")
            if isinstance(seq, bool) or not isinstance(seq, int) or seq <= previous_seq:
                raise ValueError("event seq must strictly increase")
            previous_seq = seq
    except Exception as exc:  # noqa: BLE001
        findings.append({"standing": "FALSIFIED", "path": _label(path, target), "reason": str(exc)})


def _summary_count(summary: dict[str, Any], key: str) -> int:
    for candidate in (key, key.lower(), key.upper()):
        value = summary.get(candidate)
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
    return 0


def check_artifact_dir(root: str | Path) -> dict[str, Any]:
    """Check a frozen build directory without modifying it."""
    target = Path(root)
    findings: list[dict[str, Any]] = []
    layouts = _candidate_layouts(target)
    if not layouts:
        return {
            "schema": "interdependency.ahbg.codex.artifact-check/1.1.0",
            "target": str(target),
            "artifact_root": None,
            "layout": None,
            "standing": "FALSIFIED",
            "findings": [
                {
                    "standing": "FALSIFIED",
                    "path": str(target),
                    "reason": "no supported AHBG artifact layout found",
                }
            ],
        }

    layout = layouts[0]
    build_manifest = _build_manifest_path(target, layout.root)
    if build_manifest is None:
        findings.append(
            {
                "standing": "FALSIFIED",
                "path": "BUILD_MANIFEST.json",
                "reason": "missing from target or artifact owner",
            }
        )

    parsed: dict[str, Any] = {}
    for path in (
        build_manifest,
        layout.root / "RUN_MANIFEST.json",
        layout.root / "CALIBRATION_RESULT.json",
    ):
        if path is not None and path.is_file():
            try:
                parsed[path.name] = _json_file(path)
            except Exception as exc:  # noqa: BLE001 - checker reports, does not repair.
                findings.append({"standing": "FALSIFIED", "path": _label(path, target), "reason": str(exc)})

    for events in layout.event_files:
        _check_event_file(events, target, findings)

    result = parsed.get("CALIBRATION_RESULT.json")
    if isinstance(result, dict):
        summary = result.get("summary")
        if not isinstance(summary, dict):
            findings.append(
                {
                    "standing": "FALSIFIED",
                    "path": _label(layout.root / "CALIBRATION_RESULT.json", target),
                    "reason": "missing summary",
                }
            )
        elif _summary_count(summary, "falsified"):
            findings.append(
                {
                    "standing": "FALSIFIED",
                    "path": _label(layout.root / "CALIBRATION_RESULT.json", target),
                    "reason": "result contains falsifications",
                }
            )

    return {
        "schema": "interdependency.ahbg.codex.artifact-check/1.1.0",
        "target": str(target),
        "artifact_root": str(layout.root),
        "layout": layout.name,
        "standing": "SURVIVED" if not findings else "FALSIFIED",
        "findings": findings,
    }
