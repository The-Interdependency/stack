"""Atomic plane creation, private seat commits, and verified reconstruction from decisions."""
import hmac
import json
import secrets
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

from ahbg.campaign.controllers import MODELS
from .game import Plane, SEATS, TURN_LIMIT, canonical, fingerprint
from .models import Council


class Rejected(Exception):
    def __init__(self, status, message):
        self.status = status
        super().__init__(message)


class Store:
    def __init__(self, path):
        self.path = Path(path)
        with self.connection() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id TEXT PRIMARY KEY, seed INTEGER NOT NULL, mode TEXT NOT NULL,
                    amber TEXT NOT NULL, indigo TEXT, invite TEXT UNIQUE, origin TEXT NOT NULL,
                    created INTEGER NOT NULL, request TEXT NOT NULL, UNIQUE(amber, request)
                );
                CREATE TABLE IF NOT EXISTS fauna_controllers (
                    room TEXT PRIMARY KEY REFERENCES rooms(id), controller TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS commits (
                    room TEXT NOT NULL, turn INTEGER NOT NULL, seat TEXT NOT NULL, plan TEXT NOT NULL,
                    PRIMARY KEY(room,turn,seat)
                );
                CREATE TABLE IF NOT EXISTS turns (
                    room TEXT NOT NULL, turn INTEGER NOT NULL, plans TEXT NOT NULL, result TEXT NOT NULL,
                    agents TEXT NOT NULL, PRIMARY KEY(room,turn)
                );
            """)

    @contextmanager
    def connection(self, write=False):
        db = sqlite3.connect(self.path, timeout=25)
        db.row_factory = sqlite3.Row
        try:
            if write:
                db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        finally:
            db.close()

    @staticmethod
    def fauna_mode(db, room):
        override = db.execute("SELECT controller FROM fauna_controllers WHERE room=?",
                              (room["id"],)).fetchone()
        if override:
            return override["controller"]
        # Planes created before separate fauna selection used the opponent's
        # checkpoint, or the seeded controller when both seats were human.
        return room["mode"] if room["mode"] in MODELS else "environment"

    def create(self, actor, ip, mode, request, parent=None, fork_turn=0, *, fauna_mode=None):
        if mode not in ("environment", "duel", *MODELS):
            raise Rejected(400, "unknown opponent")
        if fauna_mode is not None and fauna_mode not in ("environment", *MODELS):
            raise Rejected(400, "unknown fauna controller")
        if not isinstance(request, str) or not 12 <= len(request) <= 64:
            raise Rejected(400, "creation needs a request ID")
        with self.connection(True) as db:
            prior = db.execute("SELECT * FROM rooms WHERE amber=? AND request=?", (actor, request)).fetchone()
            if prior:
                return {"room": prior["id"]}
            if db.execute("SELECT count(*) FROM rooms WHERE origin=? AND created>?", (ip, int(time.time())-3600)).fetchone()[0] >= 24:
                raise Rejected(429, "plane creation limit reached for this hour")
            if db.execute("SELECT count(*) FROM rooms").fetchone()[0] >= 512:
                raise Rejected(503, "alpha storage limit reached")
            room, seed = secrets.token_hex(12), secrets.randbits(31)
            invite = secrets.token_urlsafe(24) if mode == "duel" else None
            if parent:
                source, _ = self.authorize(db, actor, parent)
                rows = list(db.execute("SELECT * FROM turns WHERE room=? ORDER BY turn", (parent,)))
                if source["mode"] == "duel" or type(fork_turn) is not int or not 0 <= fork_turn <= len(rows):
                    raise Rejected(400, "choose a completed position from a solo plane")
                mode, seed, invite = source["mode"], source["seed"], None
                if fauna_mode is None:
                    fauna_mode = self.fauna_mode(db, source)
            db.execute("INSERT INTO rooms VALUES (?,?,?,?,?,?,?,?,?)",
                       (room, seed, mode, actor, None, fingerprint(invite) if invite else None,
                        ip, int(time.time()), request))
            if fauna_mode is not None:
                db.execute("INSERT INTO fauna_controllers VALUES (?,?)", (room, fauna_mode))
            if parent:
                for row in rows[:fork_turn]:
                    plans = json.loads(row["plans"])
                    for plan in plans.values():
                        plan["session_id"] = room
                    db.execute("INSERT INTO turns VALUES (?,?,?,?,?)",
                               (room, row["turn"], canonical(plans), row["result"], row["agents"]))
            return {"room": room, **({"invite": invite} if invite else {})}

    def join(self, actor, invite):
        if not isinstance(invite, str) or not 24 <= len(invite) <= 64:
            raise Rejected(404, "invite unavailable")
        with self.connection(True) as db:
            room = db.execute("SELECT * FROM rooms WHERE invite=?", (fingerprint(invite),)).fetchone()
            if not room or room["amber"] == actor:
                raise Rejected(404, "invite unavailable")
            db.execute("UPDATE rooms SET indigo=?, invite=NULL WHERE id=?", (actor, room["id"]))
            return {"room": room["id"]}

    @staticmethod
    def authorize(db, actor, key):
        room = db.execute("SELECT * FROM rooms WHERE id=? AND (amber=? OR indigo=?)",
                          (key, actor, actor)).fetchone()
        if not room:
            raise Rejected(404, "plane unavailable")
        return room, "amber" if hmac.compare_digest(actor, room["amber"]) else "indigo"

    @staticmethod
    def restore(db, room):
        plane = Plane(room["id"], room["seed"])
        for row in db.execute("SELECT * FROM turns WHERE room=? ORDER BY turn", (room["id"],)):
            expected = json.loads(row["result"])
            replayed = plane.resolve(json.loads(row["plans"]), receipt_version=expected.get("version", 1))
            if replayed != expected:
                raise RuntimeError("recorded turn failed deterministic replay")
        return plane

    def rooms(self, actor):
        with self.connection() as db:
            return [dict(row) for row in db.execute(
                "SELECT id, mode FROM rooms WHERE amber=? OR indigo=? ORDER BY created DESC, rowid DESC",
                (actor, actor))]

    def observe_unit(self, actor, key, unit):
        with self.connection() as db:
            db.execute("BEGIN")
            room, seat = self.authorize(db, actor, key)
            if unit not in {row[0] for row in SEATS[seat]}:
                raise Rejected(404, "unit unavailable")
            return self.restore(db, room).observe(seat, unit)

    def state(self, actor, key):
        with self.connection() as db:
            db.execute("BEGIN")
            room, seat = self.authorize(db, actor, key)
            p = self.restore(db, room)
            turn = p.field.turn
            waiting = db.execute("SELECT plan FROM commits WHERE room=? AND turn=? AND seat=?",
                                 (key, turn, seat)).fetchone()
            return {"observation": p.observe(seat), "seat": seat, "mode": room["mode"],
                    "fauna_mode": self.fauna_mode(db, room),
                    "turn_limit": TURN_LIMIT, "done": turn >= TURN_LIMIT, "committed": bool(waiting),
                    "own_commit": json.loads(waiting["plan"]) if waiting else None,
                    "waiting_join": room["mode"] == "duel" and not room["indigo"],
                    "history": [events[seat] for events in p.history]}

    def commit(self, actor, key, payload):
        if not isinstance(payload, dict) or type(payload.get("turn")) is not int:
            raise Rejected(400, "expected a turn and plan")
        with self.connection(True) as db:
            room, seat = self.authorize(db, actor, key)
            prior = db.execute("SELECT plan FROM commits WHERE room=? AND turn=? AND seat=?",
                               (key, payload["turn"], seat)).fetchone()
            if prior:
                if prior["plan"] != canonical(payload):
                    raise Rejected(409, "this seat already committed a different plan")
                return
            plane = self.restore(db, room)
            if plane.field.turn >= TURN_LIMIT or payload["turn"] != plane.field.turn:
                raise Rejected(409, "turn closed; reload this plane")
            plan = plane.validate(seat, payload)
            db.execute("INSERT INTO commits VALUES (?,?,?,?)", (key, plane.field.turn, seat, canonical(payload)))
            plans = {seat: plan}
            traces = {}
            for player in ("amber", "indigo", "wild"):
                if player == seat:
                    continue
                if player == "amber" or (player == "indigo" and room["mode"] == "duel"):
                    row = db.execute("SELECT plan FROM commits WHERE room=? AND turn=? AND seat=?",
                                     (key, plane.field.turn, player)).fetchone()
                    if not row:
                        return
                    plans[player] = plane.validate(player, json.loads(row["plan"]))
                else:
                    mode = self.fauna_mode(db, room) if player == "wild" else room["mode"]
                    controller = Council(mode) if mode in MODELS else None
                    plans[player], traces[player] = plane.bot(player, controller, room["seed"])
            turn = plane.field.turn
            result = plane.resolve(plans)
            db.execute("INSERT INTO turns VALUES (?,?,?,?,?)",
                       (key, turn, canonical(plans), canonical(result), canonical(traces)))
