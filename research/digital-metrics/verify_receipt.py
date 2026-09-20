"""Verify and independently replay a digital-metric vertical-slice receipt.

Usage guidance::

    python3 research/digital-metrics/verify_receipt.py \
      research/digital-metrics/receipts/native-mobius-v0.json \
      --metapat-root /path/to/metapat \
      --ucns-root /path/to/ucns

The command validates every strict field and digest, reruns the generator from
the exact producer commits, and requires byte-identical canonical JSON.
"""

from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_digital_metric_receipt_verifier
#   module_name: digital metric receipt verifier
#   module_kind: instrument
#   summary: validates and byte-replays the Stack-local METAPAT/UCNS metric receipt from exact producer identities
#   owner: The-Interdependency/stack
#   public_surface: verify_and_replay,main
#   internal_surface: strict receipt load and canonical byte comparison
#   auth_boundary: none
#   storage_boundary: read-only
#   network_boundary: none
#   user_data_boundary: public research fixtures only
#   admin_only: false
#   tests: research/digital-metrics/tests/test_metric_protocol.py
#   rollout: explicit verifier command only
#   rollback: remove with the digital-metrics research workspace
#   requires: stack_digital_metric_protocol,stack_digital_metric_receipt_generator
#   since: 2026-09-20
#   unresolved: this verifier shares protocol code with the generator; an independent implementation remains required
# === END MODULE_BUILD ===

import argparse
import json
from pathlib import Path

from generate_receipt import build_receipt
from metric_protocol import MetricProtocolError, canonical_json, verify_receipt


def verify_and_replay(
    receipt_path: Path,
    *,
    metapat_root: Path,
    ucns_root: Path,
    work_graph_path: Path,
) -> dict:
    raw = receipt_path.read_bytes()
    if not raw.endswith(b"\n"):
        raise MetricProtocolError("receipt must end with exactly one canonical newline")
    parsed = json.loads(raw.decode("utf-8"))
    validated = verify_receipt(parsed)
    if raw != (canonical_json(validated) + "\n").encode("utf-8"):
        raise MetricProtocolError("receipt bytes are not canonical")
    replayed = build_receipt(
        metapat_root=metapat_root,
        ucns_root=ucns_root,
        work_graph_path=work_graph_path,
    )
    if canonical_json(replayed) != canonical_json(validated):
        raise MetricProtocolError("receipt replay differs from committed receipt")
    return validated


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--metapat-root", type=Path, required=True)
    parser.add_argument("--ucns-root", type=Path, required=True)
    parser.add_argument(
        "--work-graph",
        type=Path,
        default=Path(__file__).resolve().parent / "WORK_GRAPH.json",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    receipt = verify_and_replay(
        args.receipt,
        metapat_root=args.metapat_root,
        ucns_root=args.ucns_root,
        work_graph_path=args.work_graph,
    )
    print(f"verified {args.receipt} ({receipt['receipt_sha256']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
