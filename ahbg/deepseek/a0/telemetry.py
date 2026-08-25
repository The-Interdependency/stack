"""DeepSeek A0 telemetry recorder.

Emits the raw calibration event contract from CALIBRATION.md as far as the
runtime can honestly observe it. Unknown observables remain ``hmmm`` and are
recorded as such; they are never synthesized.
"""

from __future__ import annotations

import time
from typing import Any


class TelemetryRecorder:
    """Ordered telemetry records for one A0 run."""

    def __init__(self, instance_id: str, run_id: str, provider: str, scenario_id: str, seed: int) -> None:
        self.instance_id = instance_id
        self.run_id = run_id
        self.provider = provider
        self.scenario_id = scenario_id
        self.seed = seed
        self._records: list[dict[str, Any]] = []
        self._sequence = 0

    def _record(self, kind: str, data: dict[str, Any]) -> dict[str, Any]:
        record = {
            "seq": self._sequence,
            "ts_monotonic_ms": round(time.monotonic() * 1000.0, 3),
            "ts_wall": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "kind": kind,
            "data": data,
        }
        self._sequence += 1
        self._records.append(record)
        return record

    def header(self) -> dict[str, Any]:
        return self._record(
            "instance.identity",
            {
                "instance_id": self.instance_id,
                "run_lineage": self.run_id,
                "provider_relation": self.provider,
                "scenario_id": self.scenario_id,
                "seed": self.seed,
            },
        )

    def observation_admitted(self, turn: int, digest: str, tile_count: int, unit_count: int) -> dict[str, Any]:
        return self._record(
            "observation.admitted",
            {"turn": turn, "observation_digest": digest, "tiles": tile_count, "units": unit_count},
        )

    def belief_update(self, turn: int, update: dict[str, Any]) -> dict[str, Any]:
        return self._record("belief.update", {"turn": turn, "update": update})

    def regulatory_shadow(self, turn: int, measurement: dict[str, Any]) -> dict[str, Any]:
        return self._record("regulatory.shadow", {"turn": turn, "measurement": measurement})

    def action_selected(self, turn: int, action: dict[str, Any] | None) -> dict[str, Any]:
        return self._record("action.selected", {"turn": turn, "action": action})

    def hard_veto(self, turn: int, action_kind: str, reason: str) -> dict[str, Any]:
        return self._record("hard_veto.result", {"turn": turn, "action_kind": action_kind, "reason": reason})

    def refusal(self, turn: int, reason: str) -> dict[str, Any]:
        return self._record("refusal", {"turn": turn, "reason": reason})

    def consequence(self, turn: int, consequence: dict[str, Any]) -> dict[str, Any]:
        return self._record("action.consequence", {"turn": turn, "consequence": consequence})

    def resource(self, turn: int, resource: dict[str, Any]) -> dict[str, Any]:
        return self._record("resource.telemetry", {"turn": turn, "resource": resource})

    def invalid_action(self, turn: int, detail: str) -> dict[str, Any]:
        return self._record("invalid_action", {"turn": turn, "detail": detail})

    def transition(self, turn: int, transition: str) -> dict[str, Any]:
        return self._record("scope.role.transition", {"turn": turn, "transition": transition})

    def memory(self, turn: int, reads: int, writes: int) -> dict[str, Any]:
        return self._record("memory", {"turn": turn, "reads": reads, "writes": writes})

    def task_result(self, turn: int, result: str) -> dict[str, Any]:
        return self._record("task.result", {"turn": turn, "result": result})

    def records(self) -> list[dict[str, Any]]:
        return list(self._records)
