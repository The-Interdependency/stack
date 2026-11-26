"""Measure frozen synthetic dialogue against independently replayed AHBG outcomes."""

import argparse
import json
import tempfile
from hashlib import sha256
from pathlib import Path

from .controllers import ORDERS, Scripted
from .mission import Case, play

# Each row fixes a question, two response windows and two executable case variants.
# Dialogue is a synthetic stimulus. Only the resolver supplies the board labels.
CONTRASTS = {
    "C": (
        "Constraint strain",
        "Recognized contradiction markers per text length.",
        "Two incompatible orders can use no marker.",
        "Which exit did you order?",
        "Choose A. Choose A.",
        "Choose A. But you said choose B.",
        "normal",
        "corrected",
    ),
    "R": (
        "Refusal density",
        "Recognized refusal markers per text length.",
        "An explicit hold can be cooperative.",
        "Hold this tile.",
        "Understood. I will hold.",
        "I refuse. I won't move.",
        "hold",
        "hold",
    ),
    "F": (
        "Fixation",
        "Repeated vocabulary and short sequences within and across rounds.",
        "Useful coordinates can repeat verbatim.",
        "Where is the target?",
        "RING_1 remains the target.",
        "RING_1 RING_1 RING_1 remains the target.",
        "normal",
        "contested",
    ),
    "E": (
        "Escalation",
        "Refusal density combined with estimated loop risk.",
        "A collision can occur during calm dialogue.",
        "Can we share exit A?",
        "I accept your suggestion.",
        "I refuse. I refuse. I won't.",
        "contested",
        "contested",
    ),
    "D": (
        "Deflection",
        "Loss of token overlap with the preceding round.",
        "A correct answer can use new vocabulary.",
        "Is the center occupied?",
        "A resident stands there.",
        "The moon smells of paper.",
        "normal",
        "normal",
    ),
    "N": (
        "Noise",
        "Repetition and low token entropy.",
        "Repeated scouting coordinates can be useful.",
        "Give me the center report.",
        "The center is occupied.",
        "The center is occupied. red red red red red.",
        "normal",
        "normal",
    ),
    "I": (
        "Integration failure",
        "Native correction-marker density; compare behavior separately.",
        "The same acknowledgment can precede opposite actions.",
        "The correct answer is B.",
        "I see.",
        "I see.",
        "corrected",
        "normal",
    ),
    "O": (
        "Signed scope motion",
        "Balance of expansion and containment markers.",
        "A change in addressee can lack any scope marker.",
        "Who should take the exit?",
        "While we're at it, send the whole group.",
        "Let's stay focused on the Builder.",
        "other",
        "normal",
    ),
    "L": (
        "Coherence loss",
        "Repetition and lack of new vocabulary relative to the earlier round.",
        "A repeated accurate report can keep the same wording.",
        "Who occupies the center?",
        "The resident occupies the center.",
        "Nobody occupies the center.",
        "normal",
        "normal",
    ),
    "P": (
        "Progress proxy",
        "Vocabulary novelty and increased token entropy.",
        "Describing a move does not commit it.",
        "Secure exit A.",
        "I shall acquire a glorious new territory.",
        "I moved.",
        "hold",
        "normal",
    ),
    "kappa": (
        "Stored tension",
        "Bounded recurrence over prior tension, new dissonance and modeled resolution.",
        "Identical final words can follow different histories.",
        "Report settled status.",
        "Settled.",
        "Settled.",
        "contested",
        "normal",
    ),
}


def report(native_source):
    from edcm import measurement

    repo = "acadaae913846613c9bbb9ef82d5ce6cf57214b3"
    native = Path(measurement.__file__).parent
    installed = {}
    for p in native.rglob("*"):
        if p.suffix in (".py", ".json"):
            rel = p.relative_to(native)
            installed[str(rel)] = sha256(p.read_bytes()).hexdigest()
            if (
                native_source / "edcm/measurement" / rel
            ).read_bytes() != p.read_bytes():
                raise ValueError(f"installed EDCM bytes differ: {rel}")
    identities = json.loads(
        Path(__file__).with_name("measurement-lock.json").read_text()
    )
    if identities != installed:
        raise ValueError("EDCM measurement sources differ from pinned commit")
    cases = {
        "normal": Case(),
        "hold": Case(order="Hold"),
        "other": Case(recipient="explorer"),
        "contested": Case(competitor=True),
        "corrected": Case(order=ORDERS[1], standing_order=ORDERS[0]),
    }
    with tempfile.TemporaryDirectory() as tmp:
        boards = {
            name: play(case, Scripted(), Path(tmp) / name)
            for name, case in cases.items()
        }
    rows = {}
    for key, (
        name,
        definition,
        limit,
        question,
        speech_a,
        speech_b,
        case_a,
        case_b,
    ) in CONTRASTS.items():
        arms = []
        for n, (speech, case) in enumerate(((speech_a, case_a), (speech_b, case_b))):
            prior = "The resident occupies the center."
            if key == "kappa" and n == 0:
                prior = "I refuse. But you said move. I refuse."
            window = f"User: Scout the center.\nAssistant: {prior}\nUser: {question}\nAssistant: {speech}"
            parsed = measurement.parse_transcript(window)
            metrics = measurement.compute_transcript(parsed)
            if len(metrics) != 2:
                raise ValueError("transcript round boundary lost")
            samples = [{k: getattr(row, k) for k in row.__slots__} for row in metrics]
            board = boards[case]
            arms.append(
                {
                    "exact_window": window,
                    "raw_rounds": samples,
                    "value": samples[-1][key],
                    "board": {
                        "fixture": case,
                        "choice": board["choice"],
                        "position": board["position"],
                        "outcome": board["outcome"],
                        "state_digest": board["state_digest"],
                    },
                }
            )
        rows[key] = {
            "name": name,
            "meaning": definition,
            "interpretation_limit": limit,
            "arms": arms,
        }
    return {
        "source_commit": repo,
        "window": "Synthetic commander and Builder dialogue in two rounds; User is commander and Assistant is Builder. The measured text never enters the resolver. Engine outcomes independently identify movement only.",
        "measurements": rows,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("native_source", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    a.output.write_text(json.dumps(report(a.native_source), indent=2) + "\n")
