import io
import json
import tempfile
import unittest
from pathlib import Path

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
