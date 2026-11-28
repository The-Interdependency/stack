"""Dispatch commander, rival and builder through A0 to one local menu-scored model."""

import argparse
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import threading
import time
from dataclasses import replace
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import ClassVar

from .controllers import MODELS, ORDERS, LocalModel
from .mission import Case, play


def score(model, messages, menu):
    """Mean conditional log probability over each exact complete menu string."""
    import torch

    encoded = model.tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    )
    scores = {}
    with torch.inference_mode():
        for item in menu:
            suffix = model.tokenizer.encode(
                item, add_special_tokens=False, return_tensors="pt"
            )
            ids = torch.cat((encoded, suffix), dim=1)
            pred = model.model(ids, use_cache=False).logits[
                0, encoded.shape[1] - 1 : -1
            ]
            logp = pred.log_softmax(dim=-1).gather(1, suffix[0, :, None])
            scores[item] = float(logp.mean())
    return scores


def run(a0, model_name, cache, out, builder=None, rival=None):
    if out.exists():
        raise ValueError("a fresh dispatch trial requires a new output directory")
    out.mkdir(parents=True)
    assignments = {
        "commander": model_name,
        "builder": builder or model_name,
        "autonomous-rival": rival or model_name,
    }
    models = {
        name: LocalModel(name, cache) for name in sorted(set(assignments.values()))
    }
    credential = secrets.token_urlsafe(32)
    records = []

    class Provider(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            if (
                self.path != "/v1/chat/completions"
                or self.headers.get("Authorization") != f"Bearer {credential}"
            ):
                self.send_error(400)
                return
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 16384:
                self.send_error(400)
                return
            request = json.loads(self.rfile.read(length))
            messages = request["messages"]
            view = json.loads(messages[-1]["content"])
            start = time.monotonic()
            model = models[assignments[view["unit"]]]
            if request["model"] != model.identity["repo"]:
                self.send_error(400)
                return
            scores = score(model, messages, view["menu"])
            chosen = max(scores, key=scores.get)
            records.append(
                {
                    "role": view["unit"],
                    "view": view,
                    "model": request["model"],
                    "choices_mean_logp": scores,
                    "chosen": chosen,
                    "inference_ms": 1000 * (time.monotonic() - start),
                }
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            chunk = {
                "choices": [{"delta": {"content": chosen}, "finish_reason": "stop"}]
            }
            self.wfile.write(
                ("data: " + json.dumps(chunk) + "\n\ndata: [DONE]\n\n").encode()
            )

    server = HTTPServer(("127.0.0.1", 0), Provider)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def decide(view):
        request = {
            "id": view["unit"],
            "model": models[assignments[view["unit"]]].identity["repo"],
            "credential": credential,
            "messages": [
                {"role": "user", "content": json.dumps(view), "attachments": []}
            ],
        }
        native = subprocess.run(
            [
                shutil.which("node"),
                str(Path(__file__).with_name("a0_dispatch.mjs")),
                str(a0),
                f"http://127.0.0.1:{server.server_port}/v1",
            ],
            input=json.dumps(request),
            text=True,
            capture_output=True,
            timeout=35,
            check=True,
            env={"PATH": os.environ["PATH"], "NODE_ENV": "test"},
        )
        return json.loads(native.stdout)["text"]

    class Builder:
        identity: ClassVar = {
            "controller": "a0-local-menu",
            "role": "builder",
            "model": models[assignments["builder"]].identity,
        }

        def choose(self, view):
            return decide(view)

    try:
        # The scout report is read from the actual initial field. Only the addressed
        # recipient gets the command. The rival never sees that command.
        from ahbg.runtime.runtime import Field, tile_from_ucns

        case = Case()
        field = Field.open(case.seed, tile_from_ucns(), list(case.config().units))
        center = "occupied" if field.occupant_on("CENTER") is not None else "clear"
        order = decide(
            {
                "unit": "commander",
                "mission": "Direct the Builder to a legal exit after scouting.",
                "reports": [{"from": "explorer", "center": center}],
                "address": "builder",
                "menu": [*ORDERS, "Hold"],
            }
        )
        fauna = decide(
            {
                "unit": "autonomous-rival",
                "drive": "Contest an empty neighboring feeding tile.",
                "menu": ["Contest A", "HOLD"]
                if "RING_1" in field.neighbors("RING_2")
                and field.occupant_on("RING_1") is None
                else ["HOLD"],
            }
        )
        result = play(
            replace(
                case, order=order, competitor=fauna == "Contest A", visibility="report"
            ),
            Builder(),
            out / "turn",
        )
        files = {
            str(file.relative_to(a0)): hashlib.sha256(file.read_bytes()).hexdigest()
            for file in [
                a0 / "apps/server/src" / (name + ".js")
                for name in ("runs", "providers", "vault")
            ]
        }
        commit = subprocess.check_output(
            ["git", "-c", f"safe.directory={a0}", "-C", str(a0), "rev-parse", "HEAD"],
            text=True,
        ).strip()
        receipt = {
            "a0_commit": commit,
            "native_files": files,
            "runtime": "A0 dispatchParticipant",
            "vault": "A0 MemoryVault with one dummy loopback credential",
            "policy": "highest mean conditional token log probability; ties use menu order",
            "models": {name: model.identity for name, model in models.items()},
            "assignments": assignments,
            "pid": os.getpid(),
            "roles": records,
            "outcome": result,
        }
        (out / "dispatch.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print([(r["role"], r["chosen"]) for r in records], result["outcome"])
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("a0_source", type=Path)
    p.add_argument("model", choices=MODELS)
    p.add_argument("out", type=Path)
    p.add_argument("--cache", type=Path, default=Path.home() / ".cache/ahbg-122")
    p.add_argument("--builder", choices=MODELS)
    p.add_argument("--rival", choices=MODELS)
    args = p.parse_args()
    run(
        args.a0_source.resolve(),
        args.model,
        args.cache,
        args.out,
        args.builder,
        args.rival,
    )
