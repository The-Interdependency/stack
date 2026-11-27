"""WSGI boundary for the phone. Serve only through the dedicated HTTPS virtual host."""
import hashlib
import json
import logging
import os
import re
import secrets
import sqlite3
from http.cookies import SimpleCookie
from pathlib import Path

from ahbg.runtime.protocol import ProtocolError
from .game import fingerprint
from .store import Rejected, Store

ASSETS = Path(__file__).resolve().parents[1] / "presentation"
FILES = {"": ("play.html", "text/html"), "board.html": ("play.html", "text/html"),
         "credits.html": ("credits.html", "text/html"),
         "play.css": ("play.css", "text/css"), "play.js": ("play.js", "text/javascript"),
         "board.css": ("board.css", "text/css"), "board.js": ("board.js", "text/javascript"),
         "sample_snapshot.json": ("sample_snapshot.json", "application/json")}
COOKIE = "__Host-ahbg-seat"


def application(database, site):
    store = Store(database)

    def app(env, respond):
        from http import HTTPStatus
        route = env["PATH_INFO"].strip("/")
        method = env["REQUEST_METHOD"]
        headers = [("Cache-Control", "no-store"), ("X-Content-Type-Options", "nosniff"),
                   ("Referrer-Policy", "no-referrer"),
                   ("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")]
        def send(status, obj, mime="application/json"):
            raw = obj if isinstance(obj, bytes) else json.dumps(obj, ensure_ascii=False).encode()
            respond(f"{status} {HTTPStatus(status).phrase}", headers + [
                ("Content-Type", mime + "; charset=utf-8"), ("Content-Length", str(len(raw)))])
            return [raw]
        try:
            if method == "GET" and route in FILES:
                name, mime = FILES[route]
                return send(200, (ASSETS / name).read_bytes(), mime)
            if method not in ("GET", "POST"):
                raise Rejected(405, "method unavailable")
            if method == "POST":
                if env.get("HTTP_ORIGIN") not in (None, site) or env.get("CONTENT_TYPE", "").split(";")[0] != "application/json":
                    raise Rejected(403, "same-origin JSON required")
                length = int(env.get("CONTENT_LENGTH") or "0")
                if not 1 <= length <= 8192:
                    raise Rejected(413, "request must fit 8192 bytes")
                data = json.loads(env["wsgi.input"].read(length))
                if not isinstance(data, dict):
                    raise Rejected(400, "expected a JSON object")
            cookie = SimpleCookie()
            cookie.load(env.get("HTTP_COOKIE", ""))
            token = cookie[COOKIE].value if COOKIE in cookie else ""
            valid = re.fullmatch(r"[a-zA-Z0-9_-]{43}", token)
            if route == "api/identity" and method == "POST":
                if not valid:
                    token = secrets.token_urlsafe(32)
                    headers.append(("Set-Cookie", f"{COOKIE}={token}; Path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=31536000"))
                return send(200, {"ready": True})
            if not valid:
                raise Rejected(401, "start a player identity")
            actor = hashlib.sha256(token.encode()).hexdigest()
            # The public proxy overwrites X-Real-IP. The WSGI listener is loopback only.
            origin = hashlib.sha256(env.get("HTTP_X_REAL_IP", env.get("REMOTE_ADDR", "")).encode()).hexdigest()
            if route == "api/rooms":
                if method == "GET":
                    return send(200, {"rooms": store.rooms(actor)})
                return send(201, store.create(actor, origin, data.get("mode"), data.get("request_id")))
            if route == "api/join" and method == "POST":
                return send(200, store.join(actor, data.get("invite")))
            match = re.fullmatch(r"api/rooms/([0-9a-f]{24})/(state|plan|fork|invite)", route)
            if match:
                key, action = match.groups()
                if action == "state" and method == "GET":
                    return send(200, store.state(actor, key))
                if action == "plan" and method == "POST":
                    store.commit(actor, key, data)
                    return send(200, store.state(actor, key))
                if action == "invite" and method == "POST":
                    with store.connection(True) as db:
                        room, seat = store.authorize(db, actor, key)
                        if seat != "amber" or room["mode"] != "duel" or room["indigo"]:
                            raise Rejected(409, "no open seat")
                        invite = secrets.token_urlsafe(24)
                        db.execute("UPDATE rooms SET invite=? WHERE id=?", (fingerprint(invite), key))
                    return send(200, {"invite": invite})
                if action == "fork" and method == "POST":
                    return send(201, store.create(actor, origin, "environment", data.get("request_id"),
                                                  key, data.get("turn")))
            raise Rejected(404, "route unavailable")
        except Rejected as exc:
            return send(exc.status, {"error": str(exc)})
        except (ProtocolError, ValueError, UnicodeError) as exc:
            return send(400, {"error": str(exc)[:150]})
        except sqlite3.OperationalError:
            logging.exception("storage unavailable")
            return send(503, {"error": "storage busy; retry the same plan"})
        except Exception:
            logging.exception("game request failed")
            return send(500, {"error": "turn unavailable; your committed history is preserved"})
    return app


def configured():
    return application(os.environ["AHBG_PLAY_DB"], os.environ["AHBG_PLAY_ORIGIN"])
