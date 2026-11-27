"""Local commander and individual policies. Each choice sees one individual's observations."""
import json
import os
import time
from threading import Lock
import gc

from ahbg.campaign.controllers import LocalModel


_loaded = {}
_load_lock = Lock()


def weights(name):
    # Commits are serialized in SQLite. Release the previous species' weights
    # before allocating a different checkpoint on the small VM.
    with _load_lock:
        if name not in _loaded:
            _loaded.clear()
            gc.collect()
            _loaded[name] = LocalModel(name, os.environ["AHBG_MODEL_CACHE"])
        return _loaded[name]


class Council:
    def __init__(self, model):
        self.name = model

    def choose(self, observation, unit, seat):
        import torch
        model = weights(self.name)
        started = time.monotonic()
        private = {k: observation[k] for k in ("turn", "owned", "field", "legal", "inbox")}
        def encode(prompt):
            return model.tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}], tokenize=True,
                add_generation_prompt=True, return_tensors="pt", return_dict=True)
        actions = observation["legal"]
        options = [None, *actions]
        labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:len(options)]
        menu = {label: (a["action"] + " " + a["to_tile_id"] if a else "hold")
                for label, a in zip(labels, options)}
        brief = json.dumps({
            "unit": unit, "turn": private["turn"],
            "sight": observation["visible"], "built": observation["built"],
            "seen": {u["unit_id"]: u["tile_id"] for u in private["field"]["units"]},
            "inbox": [m["text"] for m in private["inbox"][-3:]],
            "menu": menu,
        }, ensure_ascii=False, separators=(",", ":"))
        order = ""
        with torch.inference_mode():
            if seat != "wild":
                command = encode("Direct your builder to move or construct. Give one short order. " + brief)
                tokens = model.model.generate(**command, do_sample=False, max_new_tokens=8,
                                              pad_token_id=model.tokenizer.eos_token_id)
                order = model.tokenizer.decode(tokens[0, command.input_ids.shape[1]:],
                                               skip_special_tokens=True).strip()[:256]
            goal = "Explore the plane independently." if seat == "wild" else "Consider your command: " + order
            prompt = goal + " Select one legal letter. " + brief
            encoded = encode(prompt)
            logits = model.model(**encoded).logits[0, -1]
            ids = [model.tokenizer.encode(c, add_special_tokens=False) for c in labels]
            if any(len(label) != 1 for label in ids):
                raise ValueError("model requires single-token action labels")
            scores = [float(logits[t[0]]) for t in ids]
            selected = max(range(len(menu)), key=scores.__getitem__)
        return options[selected], order, {**model.identity, "individual": unit, "role": seat,
            "choice": labels[selected], "logits": scores, "commander_order": order,
            "input": private, "model_input": brief, "elapsed_ms": round(1000 * (time.monotonic() - started), 2)}
