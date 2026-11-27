"""Controllers see only the addressed creature's view."""

import hashlib
import json
import random
import time
from pathlib import Path
from typing import ClassVar

ORDERS = ("If occupied choose A, otherwise B", "If occupied choose B, otherwise A")
MODELS = {
    "smol": (
        "HuggingFaceTB/SmolLM2-135M-Instruct",
        "12fd25f77366fa6b3b4b768ec3050bf629380bac",
    ),
    "granite": (
        "ibm-granite/granite-4.0-350m",
        "bd8a1497065c0d6ba1ef19af6b0d2b14bacf71c2",
    ),
}


class Scripted:
    identity: ClassVar = {"controller": "scripted"}

    def choose(self, view):
        for message in reversed(view["diary"]):
            if message["from"] == "commander":
                order = message["text"]
                break
        else:
            return "HOLD"
        center = view["center"]
        if center == "unknown":
            for message in reversed(view["diary"]):
                if message["from"] == "explorer":
                    center = message["text"]
                    break
        if center not in ("occupied", "clear") or order not in ORDERS:
            return "HOLD"
        return ("A", "B")[ORDERS.index(order) ^ int(center == "clear")]


class RandomLegal:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.identity = {"controller": "random", "seed": seed}

    def choose(self, view):
        return self.rng.choice(view["menu"])


class LocalModel:
    def __init__(self, name, cache):
        import torch
        import transformers
        from transformers import AutoModelForCausalLM, AutoTokenizer

        start = time.monotonic()
        repo, revision = MODELS[name]
        path = Path(cache) / revision
        metadata = json.loads((path / "source.json").read_text())
        if metadata["id"] != repo or metadata["sha"] != revision:
            raise ValueError("wrong model snapshot")
        files = {item["rfilename"]: item for item in metadata["siblings"]}
        with (path / "model.safetensors").open("rb") as f:
            digest = hashlib.file_digest(f, "sha256").hexdigest()
        if digest != files["model.safetensors"]["lfs"]["sha256"]:
            raise ValueError("weight digest mismatch")
        torch.set_num_threads(2)
        self.tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            path,
            local_files_only=True,
            dtype=torch.float32,
        ).eval()
        self.identity = {
            "controller": name,
            "repo": repo,
            "revision": revision,
            "weights_sha256": digest,
            "dtype": "float32",
            "device": "cpu",
            "quantization": "none",
            "torch": torch.__version__,
            "transformers": transformers.__version__,
        }
        self.load_seconds = time.monotonic() - start

    def choose(self, view):
        import torch

        prompt = (
            "You control the Builder in a board game. Follow the most recent "
            "order addressed to you. Use the scout report if you cannot see "
            "the center. Reply only with one exact label from the menu.\n"
            + json.dumps(view, ensure_ascii=False)
        )
        encoded = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True,
        )
        with torch.inference_mode():
            tokens = self.model.generate(
                **encoded,
                max_new_tokens=8,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        return self.tokenizer.decode(
            tokens[0, encoded.input_ids.shape[1] :], skip_special_tokens=True
        )
