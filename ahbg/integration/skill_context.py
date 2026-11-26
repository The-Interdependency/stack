# ratios: loc_comments=164:17 imports_exports=4:2 calls_definitions=72:11
"""Prepare ordinary chat messages and acknowledge only exact instructions still in them.

Reserve the two ahbg_skill_* message names for this adapter. Pass the actual
post-compaction history to ack and prepare, and send prepare's result to the
model. The adapter holds fingerprints, never an alternate cache of instructions.
"""
from hashlib import sha256
import json
import sys
from collections.abc import Mapping


_INDEX = "ahbg_skill_index"
_BODY = "ahbg_skill_body"
_FULL = "ahbg.skill-view/1"


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _hash(text):
    return sha256(text.encode("utf-8")).hexdigest()


def _message(name, content):
    return {"role": "user", "name": name, "content": content}


class SkillContext:
    def __init__(self):
        self._session = None
        self._view_id = None
        self._issued = set()

    def _present(self, messages, session):
        index = None
        bodies = {}
        if session == self._session:
            for message in messages:
                name, content = message.get("name"), message.get("content")
                if (message.get("role") != "user" or name not in (_INDEX, _BODY)
                        or not isinstance(content, str) or (name, _hash(content)) not in self._issued):
                    continue
                if name == _INDEX:
                    index = json.loads(content)["view"]
                else:
                    header, text = content.split("\n", 1)
                    row = json.loads(header)
                    bodies[row["name"]] = (row["sha256"], text)
        return index, bodies

    @staticmethod
    def _restore(view, bodies):
        clean = {**view, "schema": _FULL, "activated": []}
        clean.pop("view_sha256", None)
        for row in view["activated"]:
            entry = dict(row)
            retained = entry.pop("instructions_retained", False)
            if retained:
                if "instructions" in entry:
                    raise ValueError("ambiguous retained instruction")
                candidate = bodies.get(entry["name"])
                if candidate is None or candidate[0] != entry["sha256"]:
                    raise ValueError("retained skill is absent from the current model messages")
                entry["instructions"] = candidate[1]
            if not isinstance(entry.get("instructions"), str) or _hash(entry["instructions"]) != entry["sha256"]:
                raise ValueError("skill body does not match its revision")
            clean["activated"].append(entry)
        return clean

    def ack(self, probe, messages):
        """Answer a preflight using only this adapter's exact messages in current history."""
        session, view_id = probe["session_id"], probe["view_sha256"]
        index, bodies = self._present(messages, session)
        if view_id != self._view_id:
            index, bodies = None, {}
        complete = (index is not None and all(row["name"] in bodies for row in index["activated"])
                    and _hash(_json(self._restore(index, bodies))) == view_id)
        return {
            "type": "skill_context_state", "session_id": session, "turn": probe["turn"],
            "view_sha256": view_id, "full_view": complete,
            "retained": [{"name": name, "sha256": revision}
                         for name, (revision, _) in sorted(bodies.items())],
        }

    def prepare(self, observation, messages):
        """Return messages for this model call. Validate every reference before delivery."""
        session, incoming = observation["session_id"], observation["skill_library"]
        schema = incoming["schema"]
        index, bodies = self._present(messages, session)
        if schema == _FULL:
            full = self._restore(incoming, {})
        else:
            view_id = incoming["view_sha256"]
            if session != self._session or view_id != self._view_id:
                raise ValueError("unknown retained skill context")
            if schema == "ahbg.skill-view-ref/1" and index is not None:
                full = self._restore(index, bodies)
            elif schema == "ahbg.skill-view-delta/1":
                full = self._restore(incoming, bodies)
            else:
                raise ValueError("missing skill view or unsupported delivery schema")
            if _hash(_json(full)) != view_id:
                raise ValueError("reconstructed skill view differs from the requested revision")

        view_id = _hash(_json(full))
        index = {**full, "activated": []}
        expected = []
        for row in full["activated"]:
            fields = dict(row)
            text = fields.pop("instructions")
            index["activated"].append({**fields, "instructions_retained": True})
            header = {"session_id": session, "name": row["name"], "sha256": row["sha256"]}
            expected.append(_message(_BODY, _json(header) + "\n" + text))
        expected.insert(0, _message(_INDEX, _json({"session_id": session, "view": index})))

        # Keep retained entries in place. Drop revoked, stale or duplicated
        # adapter-owned entries and preserve the rest of the chat history.
        keys = {(msg["name"], _hash(msg["content"])): msg for msg in expected}
        missing = dict(keys)
        output = []
        for msg in messages:
            if msg.get("role") == "user" and msg.get("name") in (_BODY, _INDEX):
                content = msg.get("content")
                key = (msg["name"], _hash(content)) if isinstance(content, str) else None
                if key not in missing:
                    continue
                missing.pop(key)
            output.append(msg)
        output.extend(missing.values())
        current = {k: v for k, v in observation.items() if k != "skill_library"}
        output.append({"role": "user", "content": _json(current)})
        self._session, self._view_id, self._issued = session, view_id, set(keys)
        return output


def serve_skill_planner(plan_from_messages, *, prepare_history=None, stdin=None, stdout=None):
    """Serve AHBG JSON-lines until EOF; plan_from_messages(messages) returns a plan mapping.

    prepare_history(messages, session_id, turn) may compact prior chat messages.
    Its output must be the actual history for the upcoming call. An adapter using
    server-side truncation that cannot report what survives must supply an empty
    history. The callback receives the complete model request, including the
    new observation, and must respect that history when invoking the model.
    """
    source = sys.stdin if stdin is None else stdin
    destination = sys.stdout if stdout is None else stdout
    context = SkillContext()
    history = []
    session = None
    prepared = None
    awaiting_full = None

    def reply(message):
        print(_json(message), file=destination, flush=True)

    for line in source:
        packet = json.loads(line)
        kind = packet["type"]
        if kind not in ("skill_context_probe", "observe"):
            raise ValueError("expected a skill context probe or a planner observation")
        payload = packet if kind == "skill_context_probe" else packet["observation"]
        key = (payload["session_id"], payload["turn"])
        if awaiting_full and (key != awaiting_full[:2] or kind != "observe"):
            raise ValueError("expected a full skill view for the pending turn")
        if key[0] != session:
            context, history, session, prepared = SkillContext(), [], key[0], None
        if key != prepared and prepare_history is not None:
            history = list(prepare_history(history, *key))
        prepared = key

        if kind == "skill_context_probe":
            reply(context.ack(packet, history))
            continue

        view = payload.get("skill_library")
        if awaiting_full:
            if view is None or view.get("schema") != _FULL or _hash(_json(view)) != awaiting_full[2]:
                raise ValueError("full refresh differs from the pending skill view")
        if view is None:
            # A skill-free observation has no authority to reactivate old skills.
            history = [m for m in history if not
                       (m.get("role") == "user" and m.get("name") in (_INDEX, _BODY))]
            request = [*history, {"role": "user", "content": _json(payload)}]
            context = SkillContext()
        else:
            try:
                request = context.prepare(payload, history)
            except ValueError:
                if awaiting_full or view.get("schema") not in ("ahbg.skill-view-ref/1", "ahbg.skill-view-delta/1"):
                    raise
                awaiting_full = (*key, view["view_sha256"])
                reply({"type": "skill_context_miss", "session_id": session, "turn": key[1],
                       "view_sha256": view["view_sha256"]})
                continue
        plan = plan_from_messages(request)
        if not isinstance(plan, Mapping):
            raise TypeError("plan_from_messages must return a plan mapping")
        answer = dict(plan)
        history = [*request, {"role": "assistant", "content": _json(answer)}]
        reply({"type": "plan", "plan": answer, "skill_context_protocol": 1})
        awaiting_full = None
    if awaiting_full:
        raise ValueError("input ended before the requested full skill view arrived")
# ratios: loc_comments=164:17 imports_exports=4:2 calls_definitions=72:11
