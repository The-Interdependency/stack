"""Run provenance binding for AHBG benchmark evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def integration_provenance(
    agent_manifest: Mapping[str, Any],
    *,
    graph_path: Path | None = None,
) -> dict[str, Any]:
    """Bind a run to the reviewed cross-repository work graph.

    This is identity/provenance evidence only.  The digest is not a signature
    and does not transfer authority or scientific standing between producers.
    """

    path = graph_path or (
        Path(__file__).resolve().parents[1] / "integration" / "work-graph.json"
    )
    raw = json.loads(path.read_text(encoding="utf-8"))
    canonical = _canonical_bytes(raw)
    return {
        "schema": "interdependency.ahbg.run-provenance/1",
        "integration_work_graph_sha256": hashlib.sha256(canonical).hexdigest(),
        "integration_work_graph_schema": raw["schema"],
        "stack_base_commit": raw["stack_base_commit"],
        "agent_manifest": dict(agent_manifest),
        "boundaries": dict(raw["boundaries"]),
    }
