"""Local commander and individual policies. Each choice sees one individual's observations."""
import json
import os
import time
from functools import lru_cache

from ahbg.campaign.controllers import LocalModel


@lru_cache(maxsize=2)
def weights(name):
    return LocalModel(name, os.environ["AHBG_MODEL_CACHE"])


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
        order = ""
        with torch.inference_mode():
            if seat != "wild":
                command = encode("You command a builder on this game board. Give one short order. " + json.dumps(private))
                tokens = model.model.generate(**command, do_sample=False, max_new_tokens=12,
                                              pad_token_id=model.tokenizer.eos_token_id)
                order = model.tokenizer.decode(tokens[0, command.input_ids.shape[1]:],
                                               skip_special_tokens=True).strip()[:256]
            menu = [None, *private["legal"]]
            labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:len(menu)]
            prompt = json.dumps({"role": unit, "observation": private, "order": order,
                                 "choices": dict(zip(labels, menu)), "instruction": "Choose one letter. Null means hold."})
            encoded = encode(prompt)
            logits = model.model(**encoded).logits[0, -1]
            ids = [model.tokenizer.encode(c, add_special_tokens=False) for c in labels]
            if any(len(label) != 1 for label in ids):
                raise ValueError("model requires single-token action labels")
            scores = [float(logits[t[0]]) for t in ids]
            selected = max(range(len(menu)), key=scores.__getitem__)
        return menu[selected], order, {**model.identity, "individual": unit, "role": seat,
            "choice": labels[selected], "logits": scores, "commander_order": order,
            "input": private, "elapsed_ms": round(1000 * (time.monotonic() - started), 2)}
