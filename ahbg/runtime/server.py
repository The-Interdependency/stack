"""Thin HTTP bridge between the canonical runtime and mobile/embedded clients.

This is a transport only. It serves the canonical presentation board (static
files from ``ahbg/presentation``) and exposes the same observe/plan/act
contract as the in-process harness:

* ``POST /session``            — start a plane; returns session_id + first observation;
* ``POST /session/<id>/plan``  — submit one plan; returns effect + next observation;
* ``GET  /session/<id>/state`` — persisted field/result;
* ``GET  /session/<id>/entitlements`` — entitlement gate status.

Basic play and harness connectivity never require an entitlement. Benchmark
Lab features are gated by ``ahbg.runtime.entitlements``.

Run::

    PYTHONPATH=.:libs/ucns/src python -m ahbg.runtime.server --port 8765
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

from .entitlements import EntitlementGate
from .harness import A0Harness
from .protocol import Effect, Observation, Plan, ProtocolError, build_legal_actions, parse_plan_payload
from .runtime import RuntimeConfig, run_plane

PRESENTATION_DIR = Path(__file__).resolve().parents[1] / "presentation"
_STATIC_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
}


@dataclass
class LiveSession:
    """One open plane between HTTP turns. State is persisted after each turn."""

    session_id: str
    config: RuntimeConfig
    agent: Any
    out_dir: Path
    result: Any | None = None
    # Turn-stepping state is replayed from persisted events on each request
    # so an HTTP client can always reload the exact canonical state.

    def start_observation(self) -> dict[str, Any]:
        from .engine import load_engine
        from .runtime import _observation

        _patch, _chain, _keep, _round = load_engine()
        field, chain = _keep.load_field(self.out_dir / "state") if (self.out_dir / "state" / "events.jsonl").exists() else self._fresh_field()
        self._field = field
        self._chain = chain
        manifest = self.agent.manifest()
        capabilities = tuple(manifest.get("capabilities") or ("observe", "plan", "relocate"))
        return _observation(
            session_id=self.session_id,
            opened=field,
            chain=chain,
            config=self.config,
            turn_messages=(),
            capabilities=capabilities,
        ).as_dict()

    def _fresh_field(self):
        from .engine import load_engine

        _patch, _chain, _keep, _round = load_engine()
        tiles = _patch.tile_from_ucns()
        units = [dict(unit) for unit in self.config.units] if self.config.units else self._default_units(tiles)
        field = _patch.Field.open(seed=self.config.seed, tiles=tiles, units=units)
        chain = _chain.Chain()
        chain.append(_chain.KIND_PLANE_INIT, 0, {"field": field.snapshot()})
        return field, chain

    def _default_units(self, tiles):
        by_slot = {str(tile["ucns_slot"]): str(tile["tile_id"]) for tile in tiles}
        origin = by_slot.get("CENTER") or by_slot.get("c") or tiles[0]["tile_id"]
        return [{"unit_id": "A0", "tile_id": origin, "label": "A0"}]

    def step(self, raw_plan: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], bool]:
        from .engine import load_engine

        _patch, _chain, _keep, _round = load_engine()
        if not hasattr(self, "_field"):
            self.start_observation()
        field = self._field
        chain = self._chain
        cycle = _round.Cycle(field, chain)

        manifest = self.agent.manifest()
        capabilities = tuple(manifest.get("capabilities") or ("observe", "plan", "relocate"))
        observation = self.start_observation()
        plan = parse_plan_payload(raw_plan, Observation(
            session_id=self.session_id,
            turn=field.turn,
            field=field.snapshot(),
            capabilities=capabilities,
            legal=build_legal_actions(field),
        ))

        cycle.open_turn()
        before = len(chain.records)
        moves = [intent.as_move() for intent in plan.intents]
        cycle.resolve(moves)
        cycle.close_turn()
        effect = Effect(
            session_id=self.session_id,
            turn=field.turn - 1,
            events=tuple(record.payload() for record in chain.records[before:]),
        )

        _keep.dump_field(field, chain, self.out_dir / "state")
        done = field.turn >= self.config.turns
        next_observation = None if done else self.start_observation()
        return effect.as_dict(), next_observation, done


class _Sessions:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._items: dict[str, LiveSession] = {}

    def put(self, session: LiveSession) -> None:
        with self._lock:
            self._items[session.session_id] = session

    def get(self, session_id: str) -> LiveSession | None:
        with self._lock:
            return self._items.get(session_id)

    def entitlements(self, session_id: str, claims: tuple[str, ...]) -> dict[str, Any]:
        session = self.get(session_id)
        if session is None:
            return {}
        gate = EntitlementGate.from_claims(claims)
        return gate.as_dict()


def make_server(port: int = 8765) -> ThreadingHTTPServer:
    sessions = _Sessions()

    class Handler(BaseHTTPRequestHandler):
        def _json(self, payload: Mapping[str, Any], status: int = 200) -> None:
            body = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json(self) -> Mapping[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                return {}
            raw = self.rfile.read(length)
            return json.loads(raw.decode("utf-8"))

        def _static(self, name: str) -> None:
            path = (PRESENTATION_DIR / name).resolve()
            if PRESENTATION_DIR.resolve() not in path.parents and path != PRESENTATION_DIR.resolve():
                self._json({"error": "not found"}, 404)
                return
            if not path.is_file():
                self._json({"error": "not found"}, 404)
                return
            body = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", _STATIC_TYPES.get(path.suffix, "application/octet-stream"))
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            parts = [part for part in parsed.path.split("/") if part]
            if parts == ["board.html"] or parts == ["board.js"] or parts == ["board.css"] or parts == ["sample_snapshot.json"]:
                self._static(parts[0])
                return
            if len(parts) == 3 and parts[0] == "session" and parts[2] == "state":
                session = sessions.get(parts[1])
                if session is None:
                    self._json({"error": "unknown session"}, 404)
                    return
                from .engine import load_engine

                _patch, _chain, _keep, _round = load_engine()
                field, chain = _keep.load_field(session.out_dir / "state")
                self._json(
                    {
                        "session_id": session.session_id,
                        "field": field.snapshot(),
                        "presentation": field_to_presentation(field),
                        "turn": field.turn,
                        "config": session.config.as_dict(),
                    }
                )
                return
            if len(parts) == 3 and parts[0] == "session" and parts[2] == "entitlements":
                claims_raw = parsed.query.split("claims=", 1)
                claims = tuple(claims_raw[1].split(",")) if len(claims_raw) == 2 and claims_raw[1] else ()
                self._json({"entitlements": sessions.entitlements(parts[1], claims)})
                return
            self._json({"error": "not found"}, 404)

        def do_POST(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            parts = [part for part in parsed.path.split("/") if part]
            try:
                if parts == ["session"]:
                    body = self._read_json()
                    seed = int(body.get("seed", 1))
                    turns = int(body.get("turns", 8))
                    if turns < 1 or turns > 1000:
                        raise ProtocolError("turns must be in [1, 1000]")
                    agent = A0Harness(salt=f"http:{seed}:{turns}")
                    config = RuntimeConfig(seed=seed, turns=turns)
                    import hashlib

                    session_id = hashlib.sha256(json.dumps({"seed": seed, "turns": turns}, sort_keys=True).encode("utf-8")).hexdigest()[:12]
                    out_dir = Path(body.get("out_dir") or f"/tmp/ahbg-http-{session_id}")
                    live = LiveSession(session_id=session_id, config=config, agent=agent, out_dir=Path(out_dir))
                    observation = live.start_observation()
                    sessions.put(live)
                    self._json({"session_id": session_id, "observation": observation})
                    return
                if len(parts) == 3 and parts[0] == "session" and parts[2] == "plan":
                    session = sessions.get(parts[1])
                    if session is None:
                        self._json({"error": "unknown session"}, 404)
                        return
                    body = self._read_json()
                    plan_raw = body.get("plan")
                    if not isinstance(plan_raw, Mapping):
                        raise ProtocolError("plan body requires a plan object")
                    effect, next_observation, done = session.step(plan_raw)
                    self._json({"effect": effect, "observation": next_observation, "done": done})
                    return
                self._json({"error": "not found"}, 404)
            except ProtocolError as exc:
                self._json({"error": str(exc)}, 422)
            except Exception as exc:  # pragma: no cover - defensive bridge surface
                self._json({"error": f"{type(exc).__name__}: {exc}"}, 500)

        def log_message(self, *args: Any) -> None:  # quiet bridge
            return

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="AHBG runtime HTTP bridge")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--bind", default="127.0.0.1")
    args = parser.parse_args(argv)

    server = make_server(args.port)
    server.server_address = (args.bind, args.port)
    print(f"ahbg runtime bridge on http://{args.bind}:{args.port}")
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def field_to_presentation(field: Any, *, plane_id: str = "plane-0") -> dict[str, Any]:
    """Project engine field state into a strict presentation snapshot.

    Display coordinates come from UCNS band centers (``ucns.mobius_seed``);
    this function only reads those centers, it never reconstructs them.
    """

    from ucns.mobius_seed import build_mobius_seed_of_life

    seed = build_mobius_seed_of_life()
    centers = {band.slot.value: band.center.to_float() for band in seed.bands}
    tiles = []
    for tile in field.snapshot()["tiles"]:
        x, y = centers.get(tile["ucns_slot"], (0.0, 0.0))
        tiles.append(
            {
                "id": tile["tile_id"],
                "source_slot": tile["ucns_slot"],
                "x": x,
                "y": y,
                "label": tile["tile_id"],
            }
        )
    units = [
        {"id": unit["unit_id"], "tile": unit["tile_id"], "label": unit.get("label") or unit["unit_id"]}
        for unit in field.snapshot()["units"]
    ]
    return {
        "kind": "ahbg.presentation.snapshot",
        "standing": "not-mechanics",
        "plane_id": plane_id,
        "turn": field.turn,
        "geometry_source": {
            "repository": "The-Interdependency/ucns",
            "commit": "1975fe70cf4e0826a8020c2da3047569e277af64",
            "module": "src/ucns/mobius_seed.py",
            "schema_id": "ucns.mobius-seed-of-life",
            "schema_version": "0.1.0",
            "projection_id": "seed-of-life-seven-equal-circles",
            "selection_effect": "none",
        },
        "tiles": tiles,
        "units": units,
        "selected_tile": units[0]["tile"] if units else None,
        "feed": [{"turn": field.turn, "text": f"plane turn {field.turn}"}],
        "motions": [],
    }
