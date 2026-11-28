"""Private seats on the canonical seven-tile plane. SQLite stores committed inputs and effects."""
import hashlib
import json
import random

from ahbg.runtime.construction import ConstructionError, ConstructionLedger
from ahbg.runtime.protocol import LegalAction, Observation, ProtocolError, build_legal_actions, parse_plan_payload
from ahbg.runtime.runtime import Chain, Cycle, Field, KIND_PLANE_INIT, tile_from_ucns
from ahbg.runtime.server import field_to_presentation

TURN_LIMIT = 16
SEATS = {
    "amber": (("builder", "RING_0", "Builder"), ("explorer", "RING_1", "Explorer")),
    "indigo": (("rival", "RING_3", "Rival builder"),),
    "wild": (("fauna", "RING_4", "Fauna"),),
}
BUILDERS = {"builder", "rival"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class Plane:
    def __init__(self, room, seed):
        self.room = room
        self.field = Field.open(seed, tile_from_ucns(), [
            {"unit_id": unit, "tile_id": tile, "label": label}
            for roster in SEATS.values() for unit, tile, label in roster
        ])
        self.chain = Chain()
        self.chain.append(KIND_PLANE_INIT, 0, {"field": self.field.snapshot()})
        self.ledger = ConstructionLedger.open(self.field)
        self.history = []
        self.diaries = {unit: [] for unit in self.field.occupants}
        self.discovered = {unit: self.visible([unit]) for unit in self.field.occupants}

    def visible(self, units):
        tiles = set()
        for unit in units:
            source = self.field.occupants[unit].tile_id
            tiles.update([source, *self.field.neighbors(source)])
        return tiles

    def observe(self, seat, individual=None):
        units = [row[0] for row in SEATS[seat]]
        if individual is not None:
            if individual not in units:
                raise ValueError("unit outside seat")
            units = [individual]
        sight = self.visible(units)
        board = field_to_presentation(self.field, plane_id=self.room)
        board["units"] = [u for u in board["units"] if u["tile"] in sight]
        board["selected_tile"] = self.field.occupants[units[0]].tile_id
        legal = [a for a in build_legal_actions(self.field) if a.unit_id in units]
        for unit in units:
            source = self.field.occupants[unit].tile_id
            if unit in BUILDERS:
                legal.extend(LegalAction(unit, "construct", source, tile)
                             for tile in self.ledger.legal_build_tiles(self.field)
                             if tile in self.visible([unit]))
        state = self.field.snapshot()
        state["units"] = [u for u in state["units"] if u["tile_id"] in sight]
        obs = Observation(self.room, self.field.turn, state, legal=tuple(legal),
                          inbox=tuple(m for u in units for m in self.diaries[u][-8:])).as_dict()
        # The seed and other participants' plans are operator replay material.
        del obs["field"]["seed"]
        obs.update(owned=units, visible=sorted(sight), presentation=board,
                   built=sorted(set(self.ledger.as_dict()["built"]) & sight),
                   scouting={unit: {"visible": sorted(self.visible([unit])),
                                    "discovered": sorted(self.discovered[unit])} for unit in units})
        return obs

    def validate(self, seat, raw):
        view = self.observe(seat)
        if not isinstance(raw, dict) or not isinstance(raw.get("intents"), list):
            raise ProtocolError("plan needs an intents list; an empty list holds")
        obs = Observation(self.room, self.field.turn, view["field"])
        plan = parse_plan_payload(raw, obs)
        legal = view["legal"]
        if any(i.as_dict() not in legal for i in plan.intents):
            raise ProtocolError("action is outside your legal menu")
        messages = raw.get("messages", {})
        if not isinstance(messages, dict) or any(
            u not in view["owned"] or not isinstance(t, str) or len(t) > 256
            for u, t in messages.items()
        ):
            raise ProtocolError("orders must address an owned unit and fit 256 Unicode code points")
        accepted = {"session_id": self.room, "turn": self.field.turn,
                    "intents": [i.as_dict() for i in plan.intents], "messages": messages}
        if "report_tile" in raw:
            tile = raw["report_tile"]
            if "explorer" not in view["owned"] or tile not in view["scouting"]["explorer"]["visible"]:
                raise ProtocolError("choose a tile in the Explorer's current sight to report")
            accepted["report_tile"] = tile
        return accepted

    def scout_report(self, tile):
        occupant = self.field.occupant_on(tile)
        built = tile in self.ledger.as_dict()["built"]
        return {"kind": "scout_report", "turn": self.field.turn, "from": "explorer", "to": "builder",
                "tile": tile, "occupant": occupant, "built": built,
                "text": f"{tile}: {occupant or 'unoccupied'}, {'constructed' if built else 'unconstructed'}."}

    def resolve(self, plans, *, receipt_version=2):
        if type(receipt_version) is not int or receipt_version not in (1, 2):
            raise ValueError("unknown turn receipt version")
        if set(plans) != set(SEATS):
            raise ValueError("all seats must commit")
        intents = []
        views = {}
        for seat in SEATS:
            plan = self.validate(seat, plans[seat])
            intents.extend(plan["intents"])
            views[seat] = set(self.observe(seat)["visible"])
            for unit, text in plan["messages"].items():
                self.diaries[unit].append({"turn": self.field.turn, "from": seat, "to": unit, "text": text})
            if "report_tile" in plan:
                self.diaries["builder"].append(self.scout_report(plan["report_tile"]))
        cycle = Cycle(self.field, self.chain)
        cycle.open_turn()
        start = len(self.chain.records)
        cycle.resolve([(i["unit_id"], i["from_tile_id"], i["to_tile_id"]) for i in intents if i["action"] == "relocate"])
        events = [{"kind": r.kind, **r.data} for r in self.chain.records[start:]]
        for i in intents:
            if i["action"] == "construct":
                args = {k: i[k] for k in ("unit_id", "from_tile_id", "to_tile_id")}
                try:
                    self.ledger, event = self.ledger.apply_build(self.field, **args)
                except ConstructionError:
                    event = {"kind": "build_refused", **args}
                events.append(event)
        cycle.close_turn()
        for unit in self.discovered:
            self.discovered[unit].update(self.visible([unit]))
        committed = [self.field.snapshot(), self.ledger.as_dict(), events, self.diaries]
        if receipt_version == 2:
            committed.append({unit: sorted(tiles) for unit, tiles in self.discovered.items()})
        private = {}
        for seat, sight in views.items():
            units = [row[0] for row in SEATS[seat]]
            private[seat] = [{k: v for k, v in e.items() if k != "built_count"}
                             for e in events if e["unit_id"] in units or
                             {e["from_tile_id"], e["to_tile_id"]} <= sight]
        self.history.append(private)
        result = {"events": events, "digest": fingerprint(committed)}
        if receipt_version == 2:
            result["version"] = receipt_version
        return result

    def bot(self, seat, controller, seed):
        view = self.observe(seat)
        plan = {"session_id": self.room, "turn": self.field.turn, "intents": [], "messages": {}}
        records = []
        for unit in view["owned"]:
            private = self.observe(seat, unit)
            actions = private["legal"]
            if controller:
                action, order, trace = controller.choose(private, unit, seat)
                if order:
                    plan["messages"][unit] = order
            else:
                rng = random.Random(f"{seed}/{self.field.turn}/{unit}")
                action = rng.choice([None, *actions])
                trace = {"controller": "seeded legal", "individual": unit}
            if action is not None:
                plan["intents"].append(action)
            records.append(trace)
        return self.validate(seat, plan), records
