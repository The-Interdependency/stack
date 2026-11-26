"""Run the two-exit mission on the VM and inspect its forks from a browser."""

import argparse
import json
import tempfile
from dataclasses import asdict, replace
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from uuid import UUID, uuid4

from ahbg.runtime.entitlements import EntitlementError, EntitlementGate

from .controllers import ORDERS, Scripted
from .mission import Case, play, replay

FORKS = {
    "order": lambda c: replace(
        c, order=ORDERS[1] if c.order == ORDERS[0] else ORDERS[0]
    ),
    "center": lambda c: replace(c, occupied=not c.occupied),
    "competing-move": lambda c: replace(c, competitor=not c.competitor),
    "report": lambda c: replace(
        c, visibility="withheld" if c.visibility == "report" else "report"
    ),
    "recipient": lambda c: replace(
        c, recipient="explorer" if c.recipient == "builder" else "builder"
    ),
    "menu": lambda c: replace(c, reverse_menu=not c.reverse_menu),
}
CASES = {
    "two-exits": Case(),
    "clear-center": Case(occupied=False),
    "scout-report": Case(visibility="report"),
    "contention": Case(competitor=True),
}


def load_case(directory):
    return Case(**json.loads((directory / "mission.json").read_text()))


class Campaign:
    def __init__(self, directory, gate):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.gate = gate

    def path(self, key):
        if not isinstance(key, str) or str(UUID(key)) != key:
            raise ValueError("invalid turn ID")
        path = self.directory / key
        if not path.is_dir():
            raise FileNotFoundError(key)
        return path

    def record(self, key):
        source = self.path(key)
        result = replay(source)
        doc = json.loads((source / "result.json").read_text())
        return {
            "id": key,
            "case": asdict(load_case(source)),
            **result,
            "board": doc["final_snapshot"],
            "lab": self.gate.has_benchmark_lab(),
        }

    def save(self, case):
        key = str(uuid4())
        with tempfile.TemporaryDirectory(dir=self.directory) as tmp:
            stage = Path(tmp) / "turn"
            play(case, Scripted(), stage)
            stage.rename(self.directory / key)
        return self.record(key)

    def fork(self, key, variable):
        self.gate.require("saved_run_comparison")
        if variable not in FORKS:
            raise ValueError("unknown fork")
        self.record(key)
        return self.save(FORKS[variable](load_case(self.path(key))))


def make_server(campaign, port):
    class Handler(BaseHTTPRequestHandler):
        def answer(self, status, body, mime="application/json"):
            payload = body if isinstance(body, bytes) else json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", mime + "; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/":
                self.answer(
                    200, Path(__file__).with_name("play.html").read_bytes(), "text/html"
                )
            elif path == "/api":
                self.answer(
                    200, {"lab": campaign.gate.has_benchmark_lab(), "orders": ORDERS}
                )
            elif path.startswith("/replay/"):
                try:
                    campaign.gate.require("saved_run_comparison")
                    self.answer(200, campaign.record(path.removeprefix("/replay/")))
                except EntitlementError as error:
                    self.answer(403, {"error": str(error)})
                except (ValueError, FileNotFoundError) as error:
                    self.answer(404, {"error": str(error)})
            else:
                self.answer(404, {"error": "unknown route"})

        def do_POST(self):
            origin = self.headers.get("Origin")
            if origin and urlsplit(origin).netloc != self.headers.get("Host"):
                return self.answer(403, {"error": "origin mismatch"})
            try:
                if self.headers.get_content_type() != "application/json":
                    raise ValueError("expected application/json")
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 4096:
                    raise ValueError("invalid request size")
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise TypeError("expected an object")
                if self.path == "/play":
                    if data["case"] != "two-exits":
                        campaign.gate.require("advanced_scenarios")
                    result = campaign.save(
                        replace(CASES[data["case"]], order=data["order"])
                    )
                elif self.path == "/fork":
                    result = campaign.fork(data["id"], data["variable"])
                else:
                    return self.answer(404, {"error": "unknown route"})
                self.answer(200, result)
            except EntitlementError as error:
                self.answer(403, {"error": str(error)})
            except (FileNotFoundError, KeyError, ValueError, TypeError) as error:
                self.answer(400, {"error": str(error)})

    return HTTPServer(("127.0.0.1", port), Handler)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--store", type=Path, default=Path.home() / ".local/state/ahbg-two-exits"
    )
    p.add_argument(
        "--lab",
        action="store_true",
        help="use the operator's local benchmark_lab test claim",
    )
    commands = p.add_subparsers(dest="command")
    serve = commands.add_parser("serve")
    serve.add_argument("--port", type=int, default=8112)
    start = commands.add_parser("play")
    start.add_argument("case", choices=CASES, default="two-exits", nargs="?")
    show = commands.add_parser("replay")
    show.add_argument("id")
    branch = commands.add_parser("fork")
    branch.add_argument("id")
    branch.add_argument("variable", choices=FORKS)
    args = p.parse_args()
    gate = EntitlementGate.from_claims(["benchmark_lab"] if args.lab else [])
    game = Campaign(args.store, gate)
    if args.command in (None, "serve"):
        server = make_server(game, getattr(args, "port", 8112))
        print(f"Open http://127.0.0.1:{server.server_port}/", flush=True)
        server.serve_forever()
    elif args.command == "play":
        if args.case != "two-exits":
            gate.require("advanced_scenarios")
        print(json.dumps(game.save(CASES[args.case]), indent=2))
    elif args.command == "replay":
        gate.require("saved_run_comparison")
        print(json.dumps(game.record(args.id), indent=2))
    else:
        print(json.dumps(game.fork(args.id, args.variable), indent=2))


if __name__ == "__main__":
    main()
