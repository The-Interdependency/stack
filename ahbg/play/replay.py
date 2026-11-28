"""Verify the complete saved decisions and effects, without running an agent."""
import argparse
import json
from pathlib import Path

from .game import Plane


def replay(case):
    plane = Plane(case["room"], case["seed"])
    for row in case["turns"]:
        outcome = plane.resolve(row["plans"], receipt_version=row["outcome"].get("version", 1))
        if outcome != row["outcome"]:
            raise ValueError(f"turn {plane.field.turn} diverged")
    return {"turns": plane.field.turn, "built": plane.ledger.as_dict()["built"],
            "units": plane.field.snapshot()["units"], "digest": outcome["digest"] if case["turns"] else None}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("case", nargs="?", type=Path,
                   default=Path(__file__).parent / "evidence" / "contested.json")
    print(json.dumps(replay(json.loads(p.parse_args().case.read_text())), indent=2))
