"""Populate the local inference cache from immutable released model revisions."""

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from urllib.request import urlopen

from .controllers import MODELS

FILES = {
    "config.json",
    "generation_config.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "special_tokens_map.json",
    "chat_template.jinja",
    "model.safetensors",
    "README.md",
}


def verified(path, item):
    if not path.is_file() or path.stat().st_size != item["size"]:
        return False
    with path.open("rb") as f:
        if "lfs" in item:
            return hashlib.file_digest(f, "sha256").hexdigest() == item["lfs"]["sha256"]
        h = hashlib.sha1(f"blob {item['size']}\0".encode(), usedforsecurity=False)
        h.update(f.read())
        return h.hexdigest() == item["blobId"]


def fetch(name, cache):
    repo, rev = MODELS[name]
    directory = cache / rev
    directory.mkdir(parents=True, exist_ok=True)
    with urlopen(
        f"https://huggingface.co/api/models/{repo}/revision/{rev}?blobs=true",
        timeout=60,
    ) as stream:
        metadata = json.load(stream)
    if metadata["id"] != repo or metadata["sha"] != rev:
        raise ValueError("model snapshot identity mismatch")
    for item in metadata["siblings"]:
        filename = item["rfilename"]
        if filename not in FILES:
            continue
        target = directory / filename

        if verified(target, item):
            continue
        with tempfile.NamedTemporaryFile(dir=directory, delete=False) as tmp:
            staging = Path(tmp.name)
        try:
            with (
                urlopen(
                    f"https://huggingface.co/{repo}/resolve/{rev}/{filename}",
                    timeout=120,
                ) as src,
                staging.open("wb") as dst,
            ):
                shutil.copyfileobj(src, dst)
            if not verified(staging, item):
                raise ValueError(f"wrong file digest: {filename}")
            os.replace(staging, target)
        finally:
            staging.unlink(missing_ok=True)
    (directory / "source.json").write_text(json.dumps(metadata))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("name", choices=MODELS)
    p.add_argument("--cache", type=Path, default=Path.home() / ".cache/ahbg-122")
    args = p.parse_args()
    fetch(args.name, args.cache)
