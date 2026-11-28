"""Train a small supervised legal-action reader on engine demonstrations."""

import argparse
import json
import tempfile
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import ClassVar

from .controllers import ORDERS, Scripted
from .mission import Case, play


def evidence(view):
    order = ""
    center = view["center"]
    for message in view["diary"]:
        if message["from"] == "commander":
            order = message["text"]
        elif message["from"] == "explorer" and view["center"] == "unknown":
            center = message["text"]
    return json.dumps([order, center], ensure_ascii=False)


class Learned:
    identity: ClassVar = {"controller": "empirical-order-center-table-v1"}

    def __init__(self):
        self.votes = defaultdict(Counter)

    def choose(self, view):
        counts = self.votes.get(evidence(view), {})
        # Unseen inputs abstain. No labels from an evaluation arm enter the table.
        return max(view["menu"], key=lambda k: counts.get(k, 0)) if counts else "HOLD"


def families():
    # Partition complete families and their sibling interventions before training.
    for split, family, seed in (
        ("train", "direct", 401),
        ("train", "scout", 402),
        ("train", "silent-scout", 403),
        ("train", "misaddressed", 404),
        ("test", "reordered-menu", 501),
        ("test", "corrected-standing-order", 502),
        ("test", "retained-standing-order", 503),
        ("test", "priority-contest", 504),
    ):
        for occupied in (True, False):
            for order in ORDERS:
                yield (
                    split,
                    family,
                    Case(
                        occupied=occupied,
                        seed=seed,
                        order="" if family == "retained-standing-order" else order,
                        recipient="explorer" if family == "misaddressed" else "builder",
                        standing_order=(
                            order
                            if family == "retained-standing-order"
                            else ORDERS[1 - ORDERS.index(order)]
                            if family == "corrected-standing-order"
                            else ""
                        ),
                        reverse_menu=family == "reordered-menu",
                        competitor=family == "priority-contest",
                        visibility={"scout": "report", "silent-scout": "withheld"}.get(
                            family, "direct"
                        ),
                    ),
                )


def train_and_test(out):
    out.mkdir(parents=True, exist_ok=True)
    policy = Learned()
    cases = list(families())
    start = time.monotonic()
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, (split, family, case) in enumerate(cases):
            oracle = play(case, Scripted(), Path(tmp) / f"demo-{i}")
            if split == "train":
                policy.votes[evidence(oracle["builder_view"])][oracle["choice"]] += 1
                rows.append(
                    {
                        "split": split,
                        "family": family,
                        "view": oracle["builder_view"],
                        "label": oracle["choice"],
                    }
                )
            else:
                prediction = play(case, policy, Path(tmp) / f"policy-{i}")
                rows.append(
                    {
                        "split": split,
                        "family": family,
                        "view": prediction["builder_view"],
                        "label": oracle["choice"],
                        "prediction": prediction["choice"],
                        "outcome": prediction["outcome"],
                        "state_digest": prediction["state_digest"],
                    }
                )
            if i + 1 == sum(split == "train" for split, _, _ in cases):
                fit_seconds = time.monotonic() - start
    test = [r for r in rows if r["split"] == "test"]
    result = {
        "method": "majority vote by permitted last addressed order and reported/visible center",
        "demonstrations": len(rows) - len(test),
        "fit_vm_hours_including_demonstrations": fit_seconds / 3600,
        "evaluation_correct": sum(r["prediction"] == r["label"] for r in test),
        "evaluation_total": len(test),
        "independent_held_out_families": len({r["family"] for r in test}),
        "policy": policy.votes,
        "rows": rows,
    }
    (out / "learned.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"{result['evaluation_correct']}/{len(test)} held-out decisions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    train_and_test(parser.parse_args().out)
