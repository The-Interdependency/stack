# ratios: loc_comments=90:4 imports_exports=4:2 calls_definitions=39:7
"""Apply an operator-selected skill view at the AHBG planning boundary."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping


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
        self._delivered = False

    def manifest(self):
        return self._agent.manifest()

    def plan(self, observation):
        self._delivered = True
        return self._agent.plan({**observation, "skill_library": json.loads(self._view)})

    def turn_provenance(self) -> dict[str, Any]:
        get = getattr(self._agent, "turn_provenance", None)
        inner = get() if callable(get) else None
        if inner is not None and not isinstance(inner, Mapping):
            raise ValueError("planner turn provenance must be a mapping")
        provenance = dict(inner or {})
        if self._delivered:
            provenance["skill_library"] = self._receipt.copy()
            self._delivered = False
        return provenance

    def close(self):
        close = getattr(self._agent, "close", None)
        if callable(close):
            close()
# ratios: loc_comments=90:4 imports_exports=4:2 calls_definitions=39:7
