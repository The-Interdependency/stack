"""One addressed decision on the existing UCNS plane."""

import json
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from ahbg.runtime.runtime import RuntimeConfig, load_field, run_plane

from .controllers import ORDERS

EXITS = {"A": "RING_1", "B": "RING_5"}


@dataclass(frozen=True)
class Case:
    occupied: bool = True
    order: str = ORDERS[0]
    recipient: str = "builder"
    visibility: str = "direct"
    competitor: bool = False
    reverse_menu: bool = False
    standing_order: str = ""
    seed: int = 122

    def __post_init__(self):
        if self.visibility not in ("direct", "report", "withheld"):
            raise ValueError("unknown visibility")
        if self.recipient not in ("builder", "explorer"):
            raise ValueError("unknown recipient")
        if any(
            type(flag) is not bool
            for flag in (self.occupied, self.competitor, self.reverse_menu)
        ):
            raise ValueError("expected a boolean mission setting")
        if type(self.seed) is not int or self.seed < 0:
            raise ValueError("expected a nonnegative seed")
        for text in (self.order, self.standing_order):
            if not isinstance(text, str) or len(text) > 256:
                raise ValueError("mission orders have a 256 Unicode code point limit")

    def config(self):
        units = [
            {"unit_id": "builder", "tile_id": "RING_0"},
            {"unit_id": "autonomous-rival", "tile_id": "RING_2"},
            {"unit_id": "explorer", "tile_id": "RING_3"},
        ]
        if self.occupied:
            units.append({"unit_id": "resident", "tile_id": "CENTER"})
        messages = [
            {"from": "commander", "to": recipient, "text": text}
            for recipient, text in (
                ("builder", self.standing_order),
                (self.recipient, self.order),
            )
            if text
        ]
        # Fixture settings travel with the replay but are filtered before any decision.
        messages.append(
            {
                "from": "scenario",
                "to": "resolver",
                "visibility": self.visibility,
                "competitor": self.competitor,
                "reverse_menu": self.reverse_menu,
            }
        )
        return RuntimeConfig(
            seed=self.seed,
            turns=1,
            units=tuple(units),
            turn_messages={0: messages},
            deadline_ms=15000,
            injection_handling="observe-only",
        )


class MissionHarness:
    def __init__(self, controller):
        self.controller = controller
        self.record = {}

    def manifest(self):
        return {
            "agent": "two-exits",
            "capabilities": ["observe", "plan", "relocate"],
            **self.controller.identity,
        }

    def plan(self, observation):
        messages = observation["inbox"]
        settings = messages[-1]
        legal = observation["legal"]
        options = {
            label: action
            for label, tile in EXITS.items()
            for action in legal
            if action["unit_id"] == "builder" and action["to_tile_id"] == tile
        }
        if options.keys() != EXITS.keys():
            raise ValueError("the mission requires two legal exits")
        committed = []
        if settings["competitor"]:
            committed.append(
                next(
                    action
                    for action in legal
                    if action["unit_id"] == "autonomous-rival"
                    and action["to_tile_id"] == EXITS["A"]
                )
            )
        occupied = any(u["tile_id"] == "CENTER" for u in observation["field"]["units"])
        center = "occupied" if occupied else "clear"
        diary = [m for m in messages if m.get("to") == "builder"]
        if settings["visibility"] == "report":
            diary.append({"from": "explorer", "to": "builder", "text": center})
        menu = list(options)
        if settings["reverse_menu"]:
            menu.reverse()
        view = {
            "unit": "builder",
            "center": center if settings["visibility"] == "direct" else "unknown",
            "menu": [*menu, "HOLD"],
            "diary": diary,
        }
        start = time.monotonic()
        raw = self.controller.choose(view)
        elapsed_ms = 1000 * (time.monotonic() - start)
        choice = raw.strip()
        if elapsed_ms > observation["deadline_ms"]:
            status = "timeout"
        elif choice not in view["menu"]:
            status = "invalid"
        elif choice == "HOLD":
            status = "hold"
        else:
            status = "submitted"
        intents = list(committed)
        if status == "submitted":
            intents.append(options[choice])
        self.record = {
            "builder_view": view,
            "explorer_observation": {"center": center},
            "legal_menu": options,
            "rival_commit": committed,
            "raw": raw,
            "status": status,
            "choice": choice if choice in view["menu"] else None,
            "elapsed_ms": elapsed_ms,
        }
        return {
            "session_id": observation["session_id"],
            "turn": observation["turn"],
            "intents": intents,
            "note": status,
        }

    def turn_provenance(self):
        return self.record


def summarize(result):
    row = result["turn_records"][0]
    record = row["agent_provenance"]
    position = next(
        u["tile_id"]
        for u in result["final_snapshot"]["units"]
        if u["unit_id"] == "builder"
    )
    outcome = record["status"]
    if outcome == "submitted":
        outcome = "arrived" if position == EXITS[record["choice"]] else "displaced"
    return {
        "choice": record["choice"],
        "outcome": outcome,
        "position": position,
        "builder_view": record["builder_view"],
        "raw": record["raw"],
        "events": row["effect"]["events"],
        "state_digest": result["state_digest"],
    }


def play(case, controller, directory):
    directory = Path(directory)
    if directory.exists() and any(directory.iterdir()):
        raise ValueError("use a new directory for a fresh turn")
    result = run_plane(
        config=case.config(), agent=MissionHarness(controller), out_dir=directory
    )
    (directory / "mission.json").write_text(
        json.dumps(asdict(case), ensure_ascii=False, indent=2)
    )
    return summarize(result.as_dict())


def replay(directory):
    directory = Path(directory)
    field, journal = load_field(directory / "state")
    result = json.loads((directory / "result.json").read_text())
    stored = json.loads((directory / "state/field.json").read_text())
    if field.snapshot() != result["final_snapshot"] or field.snapshot() != stored:
        raise ValueError("replayed field differs from saved board")
    case = Case(**json.loads((directory / "mission.json").read_text()))
    if case.config().as_dict() != result["config"]:
        raise ValueError("saved mission differs from runtime config")
    row = result["turn_records"][0]
    events = [
        r.payload() for r in journal.records if r.kind in ("move", "war", "turn.end")
    ]
    if (
        events != row["effect"]["events"]
        or row["state_digest"] != result["state_digest"]
    ):
        raise ValueError("resolver evidence differs from journal")

    class Recorded:
        def manifest(self):
            return result["provenance"]["agent_manifest"]

        def plan(self, observation):
            if observation["turn"] != row["turn"]:
                raise ValueError("unexpected turn during decision replay")
            return row["submitted_plan"]

    with tempfile.TemporaryDirectory() as temporary:
        repeated = run_plane(agent=Recorded(), config=case.config(), out_dir=temporary)
    if (
        repeated.final_snapshot != field.snapshot()
        or repeated.turn_records[0]["effect"] != row["effect"]
        or repeated.construction != result["construction"]
    ):
        raise ValueError("recorded decision fails to reproduce resolved turn")
    return summarize(result)
