import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ahbg.play.web import application


class HttpBoundaryTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.app = application(Path(tmp.name)/"state.db", "https://phone.example")

    def request(self, path, body=None, cookie="", origin="https://phone.example"):
        raw = json.dumps(body).encode()
        env = {"PATH_INFO": path, "REQUEST_METHOD": "GET" if body is None else "POST",
               "wsgi.input": io.BytesIO(raw), "CONTENT_LENGTH": str(len(raw)),
               "CONTENT_TYPE": "application/json", "HTTP_ORIGIN": origin, "HTTP_COOKIE":cookie}
        meta = []
        response = self.app(env, lambda status, headers: meta.extend([int(status.split()[0]), dict(headers)]))
        return *meta, json.loads(b"".join(response))

    def test_private_cookie_origin_and_room_access(self):
        status, headers, _ = self.request("/api/identity", {})
        self.assertEqual(status, 200)
        cookie = headers["Set-Cookie"].split(";")[0]
        for attr in ("HttpOnly","Secure","SameSite=Strict"):
            self.assertIn(attr, headers["Set-Cookie"])
        data = {"mode":"environment","request_id":"browser-retry-01"}
        self.assertEqual(self.request("/api/rooms", data, cookie, "https://elsewhere.example")[0], 403)
        key = self.request("/api/rooms", data, cookie)[2]["room"]
        self.assertEqual(self.request("/api/rooms", data, cookie)[2]["room"],key)
        path="/api/rooms/"+key+"/state"
        self.assertEqual(self.request(path)[0],401)
        other=self.request("/api/identity",{})[1]["Set-Cookie"].split(";")[0]
        self.assertEqual(self.request(path,cookie=other)[0],404)
        self.assertEqual(self.request(path,cookie=cookie)[2]["seat"],"amber")

    def test_fork_changes_only_fauna_after_replaying_the_saved_turn(self):
        cookie = self.request("/api/identity", {})[1]["Set-Cookie"].split(";")[0]

        def call(path, body=None, status=200):
            actual, _, payload = self.request("/api/" + path, body, cookie)
            self.assertEqual(actual, status, payload)
            return payload

        observed = []

        def choose(council, observation, unit, seat):
            observed.append((council.name, seat, unit, observation))
            return None, "Keep watch" if seat == "indigo" else "", {"controller": council.name}

        create = {"mode": "smol", "request_id": "select-fauna-test", "fauna_mode": "granite"}
        call("rooms", dict(create, fauna_mode="unknown"), 400)
        room = call("rooms", create, 201)["room"]
        root = f"rooms/{room}/"
        with patch("ahbg.play.models.Council.choose", choose):
            plan = {"session_id": room, "turn": 0, "intents": []}
            checkpoint = call(root + "plan", plan)
            self.assertEqual(checkpoint["fauna_mode"], "granite")
            call(root + "plan", dict(plan, turn=1))
            original = observed.copy()
            self.assertEqual([(m, s, u) for m, s, u, _ in original],
                             [("smol", "indigo", "rival"), ("granite", "wild", "fauna")] * 2)
            for request_id, override in (("fork-inherited", {}), ("fork-swapped", {"fauna_mode": "smol"})):
                observed.clear()
                fork = call(root + "fork", {"turn": 1, "request_id": request_id, **override}, 201)["room"]
                route = f"rooms/{fork}/"
                before = call(route + "state")
                self.assertFalse(observed, "restoring recorded decisions invoked inference")
                self.assertEqual(before["history"], checkpoint["history"])
                self.assertEqual(before["observation"]["field"], checkpoint["observation"]["field"])
                call(route + "plan", dict(plan, session_id=fork, turn=1))
                self.assertEqual([m for m, _, _, _ in observed],
                                 ["smol", override.get("fauna_mode", "granite")])
                for (_, seat, unit, view), (_, old_seat, old_unit, old) in zip(observed, original[2:]):
                    self.assertEqual((seat, unit), (old_seat, old_unit))
                    for key in ("owned", "turn", "field", "legal", "inbox"):
                        self.assertEqual(view[key], old[key])
                self.assertEqual(observed[0][3]["inbox"][0]["text"], "Keep watch")
                self.assertEqual(observed[1][3]["inbox"], [])
