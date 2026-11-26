# ratios: loc_comments=151:6 imports_exports=5:2 calls_definitions=60:8
"""Apply an operator-selected skill view at the AHBG planning boundary."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

from ahbg.runtime.harness import SkillContextMiss


def build_view(resolver, *, visible, activate=(), disclosed_runners=()):
    """Resolve the requested task roots inside the session's permitted skill set."""
    permitted = frozenset(visible)
    requested = sorted(set(activate))
    if not set(requested) <= permitted:
        raise ValueError("a requested skill is outside the session's visible set")
    resolution = resolver.resolve(requested) if requested else {"order": [], "reasons": {}}
    if not set(resolution["order"]) <= permitted:
        raise ValueError("a required skill is outside the session's visible set")

    records = {name: resolver.get(name) for name in sorted(permitted)}
    runners = set(disclosed_runners)
    active_names = set(resolution["order"])
    declared = set(resolver.declared_runners)
    for owner, path in runners:
        if (owner, path) not in declared or owner not in records or records[owner].get("runner") != path:
            raise ValueError("disclosed runner must belong to a visible skill")
    forbidden = {path for owner, path in declared
                 if (owner, path) not in runners or owner not in active_names}
    discovery = []
    for name, record in records.items():
        if any(path in record["description"] for path in forbidden):
            discovery.append({"name": name, "description_withheld": "runner disclosure"})
        else:
            discovery.append({"name": name, "description": record["description"]})
    activated = []
    for name in resolution["order"]:
        record = records[name]
        body = resolver.read_body(name)
        if sha256(body.encode("utf-8")).hexdigest() != record["sha256"]:
            raise ValueError("activated instructions disagree with resolved revision")
        if any(path in body for path in forbidden):
            raise ValueError("required instructions contain a runner outside the session disclosure policy")
        skill = {
            "name": name,
            "sha256": record["sha256"],
            "instructions": body,
            "reasons": resolution["reasons"][name],
        }
        runner = record.get("runner")
        if runner and (name, runner) in runners:
            skill["runner"] = runner
        activated.append(skill)

    view = {
        "schema": "ahbg.skill-view/1",
        "source": resolver.source,
        "discovery": discovery,
        "roots": requested,
        "activated": activated,
    }
    # Cover names, reasons, or other record fields as well as literal prose.
    serialized = json.dumps(view, ensure_ascii=False)
    if any(path in serialized for path in forbidden):
        raise ValueError("skill view contains a runner outside the session disclosure policy")
    return view


class SkillHarness:
    """Pass the same read-only view through in-process and subprocess planners."""

    def __init__(self, agent, view, *, experiment, activation_root=None):
        self._agent = agent
        self._view = json.dumps(view, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self._receipt = {
            "experiment": experiment,
            "source": view["source"],
            "view_sha256": sha256(self._view.encode("utf-8")).hexdigest(),
            "view_bytes": len(self._view.encode("utf-8")),
            "roots": view["roots"],
            "activation_order": [record["name"] for record in view["activated"]],
        }
        if activation_root is not None:
            self._receipt["activation_root"] = activation_root
        self._last_delivery = None
        self._last_turn = None

    def manifest(self):
        return self._agent.manifest()

    def _select_delivery(self, probe, view):
        """Only a fresh receiver response can suppress currently disclosed text."""
        session, turn = probe["session_id"], probe["turn"]
        inspect = getattr(self._agent, "retained_skill_context", None)
        if (not callable(inspect) or not isinstance(session, str) or type(turn) is not int
                or self._last_turn != (session, turn - 1)):
            return view, "full", []
        state = inspect(dict(probe))
        if (not isinstance(state, Mapping) or state.get("type") != "skill_context_state"
                or type(state.get("turn")) is not int
                or any(state.get(key) != value for key, value in probe.items())
                or type(state.get("full_view")) is not bool
                or not isinstance(state.get("retained"), list)):
            return view, "full", []

        expected = {item["name"]: item["sha256"] for item in view["activated"]}
        confirmed = set()
        for claim in state["retained"]:
            if not isinstance(claim, Mapping):
                return view, "full", []
            name = claim.get("name")
            if (not isinstance(name, str) or name not in expected or name in confirmed
                    or claim.get("sha256") != expected[name]):
                return view, "full", []
            confirmed.add(name)
        retained = [name for name in expected if name in confirmed]
        if state["full_view"] and len(retained) == len(expected):
            return {"schema": "ahbg.skill-view-ref/1", "view_sha256": probe["view_sha256"]}, "reference", retained
        if not retained:
            return view, "full", []
        for item in view["activated"]:
            if item["name"] in confirmed:
                del item["instructions"]
                item["instructions_retained"] = True
        view.update(schema="ahbg.skill-view-delta/1", view_sha256=probe["view_sha256"])
        return view, "delta", retained

    def plan(self, observation):
        self._last_delivery = None
        session, turn = observation["session_id"], observation["turn"]
        probe = {"session_id": session, "turn": turn, "view_sha256": self._receipt["view_sha256"]}
        try:
            payload, mode, retained = self._select_delivery(probe, json.loads(self._view))
        finally:
            self._last_turn = None
        wire = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        retry_bytes = 0
        try:
            result = self._agent.plan({**observation, "skill_library": payload})
        except SkillContextMiss as miss:
            if mode == "full":
                raise
            # The adapter rejected the reference before calling its planner.
            retry_bytes = len(wire) if miss.sent else 0
            mode, retained = "full", []
            wire = self._view.encode()
            result = self._agent.plan({**observation, "skill_library": json.loads(self._view)})
        receipt = {**self._receipt, "delivery": mode, "delivery_bytes": len(wire),
                   "delivery_sha256": sha256(wire).hexdigest(),
                   "sent_bodies": [n for n in self._receipt["activation_order"] if n not in retained],
                   "retained_bodies": retained}
        if retry_bytes:
            receipt["retry_bytes"] = retry_bytes
        self._last_turn = (session, turn)
        self._last_delivery = receipt
        return result

    def turn_provenance(self) -> dict[str, Any]:
        get = getattr(self._agent, "turn_provenance", None)
        inner = get() if callable(get) else None
        if inner is not None and not isinstance(inner, Mapping):
            raise ValueError("planner turn provenance must be a mapping")
        provenance = dict(inner or {})
        if self._last_delivery is not None:
            provenance["skill_library"] = self._last_delivery
            self._last_delivery = None
        return provenance

    def close(self):
        close = getattr(self._agent, "close", None)
        if callable(close):
            close()
# ratios: loc_comments=151:6 imports_exports=5:2 calls_definitions=60:8
