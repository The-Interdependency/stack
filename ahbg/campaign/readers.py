"""Compare equally trained readers of the same delivered order on the VM."""

import argparse
import hashlib
import json
import re
import tempfile
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

from ahbg.integration.uchc import UchcSession, UchcSettings

from .controllers import ORDERS, Scripted
from .learned import evidence, families
from .mission import play


def digest(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def compare(database, output):
    import uchc_halving as geometry

    with UchcSession(UchcSettings(database)) as session:

        @lru_cache(maxsize=64)
        def features(text):
            if not text:
                return {mode: "" for mode in modes}
            frame = session.resolve_text(text, source_id="mission:order").to_dict()
            members = tuple(
                geometry.construct_text(token, source="mission:member")
                for token in re.findall(r"\s+|\S+", text)
            )
            obj = geometry.construct_sequence(members, source="mission:order")
            record = geometry.closed_record(obj)
            if geometry.closed_record(geometry.replay_closed(record)) != record:
                raise ValueError("ordinal graph replay differs")
            vectors = record["vectors"]
            return {
                "text": text,
                "native-input": digest(
                    [
                        (g["character_id"], g["ordinal"])
                        for g in frame["glyph_occurrences"]
                    ]
                ),
                "ordinal": digest(vectors["placement_endpoint"]),
                "additive": digest(vectors["additive_resultant"]),
                "both": digest(vectors),
                "recursive": digest(record["graph"]),
            }

        modes = ("text", "native-input", "ordinal", "additive", "both", "recursive")

        class Reader:
            def __init__(self, mode):
                self.mode = mode
                self.identity = {"controller": "fixed-budget-reader", "mode": mode}
                self.votes = defaultdict(Counter)
                self.mismatch = False

            def key(self, view):
                text, center = json.loads(evidence(view))
                if self.mismatch and text in ORDERS:
                    text = ORDERS[1 - ORDERS.index(text)]
                return (features(text)[self.mode], center)

            def choose(self, view):
                counts = self.votes.get(self.key(view))
                return (
                    max(view["menu"], key=lambda k: counts.get(k, 0))
                    if counts
                    else "HOLD"
                )

        readers = [Reader(mode) for mode in modes]
        rows = []
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for i, (split, family, case) in enumerate(families()):
                correct = play(case, Scripted(), root / f"teacher-{i}")
                for reader in readers:
                    if split == "train":
                        reader.votes[reader.key(correct["builder_view"])][
                            correct["choice"]
                        ] += 1
                        continue
                    for mismatch in (False, True):
                        reader.mismatch = mismatch
                        actual = play(
                            case, reader, root / f"{reader.mode}-{i}-{mismatch}"
                        )
                        rows.append(
                            {
                                "mode": reader.mode,
                                "mismatch": mismatch,
                                "family": family,
                                "case": i,
                                "expected": correct["choice"],
                                "chosen": actual["choice"],
                                "outcome": actual["outcome"],
                                "digest": actual["state_digest"],
                            }
                        )
        totals = {
            mode: {
                str(swap): sum(
                    r["expected"] == r["chosen"]
                    for r in rows
                    if r["mode"] == mode and r["mismatch"] == swap
                )
                for swap in (False, True)
            }
            for mode in modes
        }
        save = {
            "producer": session.provenance,
            "geometry": geometry.authority(),
            "training_examples_per_reader": 16,
            "test_examples_per_reader": 16,
            "method": "One lookup per order representation and permitted center. Raw order visible only to text reader. All readers get the same separate center signal. Mismatches swap the two order representations at test time.",
            "totals": totals,
            "rows": rows,
            "order_features": [features(order) for order in ORDERS],
            "structural_reader": "unmeasured; complete hash-locked structural field required",
        }
        output.write_text(json.dumps(save, indent=2) + "\n")
        print(totals)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("database", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    compare(args.database, args.output)
