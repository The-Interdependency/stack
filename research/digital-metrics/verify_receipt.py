"""Verify and deterministically replay a digital-metric vertical-slice receipt.

Usage guidance::

    python3 research/digital-metrics/verify_receipt_cli.py \
      research/digital-metrics/receipts/native-mobius-v0.json \
      --metapat-root /path/to/metapat \
      --ucns-root /path/to/ucns \
      --edcm-root /path/to/edcm

To turn a generator-created pending candidate into an attested receipt::

    python3 research/digital-metrics/verify_receipt_cli.py pending.json \
      --metapat-root /path/to/metapat --ucns-root /path/to/ucns \
      --edcm-root /path/to/edcm \
      --attest-output attested.json

The command validates every strict field and digest and reruns the generator
from exact producer commits. Only this post-replay path may change a candidate's
verification result from ``pending`` to ``pass``.
"""

from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_digital_metric_receipt_verifier
#   module_name: digital metric receipt verifier
#   module_kind: instrument
#   summary: validates and byte-replays the Stack-local METAPAT/UCNS metric receipt from exact producer identities
#   owner: The-Interdependency/stack
#   public_surface: source-loaded verify_and_replay
#   internal_surface: strict receipt load, canonical byte comparison, and post-replay attestation
#   auth_boundary: none
#   storage_boundary: read-only unless an explicit attestation output path is supplied
#   network_boundary: none
#   user_data_boundary: public research fixtures only
#   admin_only: false
#   tests: research/digital-metrics/tests/test_metric_protocol.py
#   rollout: source-loading CLI launcher or explicit source-loaded API only
#   rollback: remove with the digital-metrics research workspace
#   requires: stack_digital_metric_protocol,stack_digital_metric_receipt_generator
#   since: 2026-09-20
#   unresolved: this verifier shares protocol code with the generator; an independent implementation remains required
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: digital_metric_pass_requires_completed_replay
#   given: the generator emits a pending candidate and the named verifier is asked to attest it
#   then: pass is written only after exact producer replay matches the candidate byte-for-byte
#   class: provenance
#
# id: digital_metric_verifier_bypasses_cached_bytecode
#   given: timestamp-valid stale bytecode exists for the verifier, protocol, or generator module
#   then: the supported entry compiles all three modules from recorded source bytes before replay
#   class: provenance
#
# id: digital_metric_replay_binds_executing_source_bytes
#   given: Stack protocol, generator, or verifier files change after their modules are loaded
#   then: replay records the digests of the exact source bytes compiled for execution
#   class: provenance
#
# id: digital_metric_verifier_requires_source_bound_entry
#   given: the current outer verifier implementation is entered without a source digest binding
#   then: replay and attestation reject before reading or writing a receipt
#   class: provenance
# === END CONTRACTS ===

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from types import ModuleType

_LOADED_VERIFIER_SHA256 = globals().get("__source_sha256__")


def _load_source_module(module_name: str, source_path: Path) -> ModuleType:
    source_path = source_path.resolve()
    source = source_path.read_bytes()
    module = ModuleType(module_name)
    module.__file__ = str(source_path)
    module.__cached__ = None
    module.__package__ = ""
    module.__source_sha256__ = hashlib.sha256(source).hexdigest()
    previous = sys.modules.get(module_name)
    sys.modules[module_name] = module
    try:
        code = compile(source, str(source_path), "exec", dont_inherit=True)
        exec(code, module.__dict__)
    finally:
        if previous is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = previous
    return module


_WORKSPACE = Path(__file__).resolve().parent
_METRIC_PROTOCOL = _load_source_module(
    "_stack_digital_metric_protocol_verifier",
    _WORKSPACE / "metric_protocol.py",
)
_GENERATOR = _load_source_module(
    "_stack_digital_metric_generator_verifier",
    _WORKSPACE / "generate_receipt.py",
)
if _METRIC_PROTOCOL.__source_sha256__ != _GENERATOR._LOADED_PROTOCOL_SHA256:
    raise RuntimeError("verifier and generator loaded different protocol source bytes")

MetricProtocolError = _METRIC_PROTOCOL.MetricProtocolError
canonical_json = _METRIC_PROTOCOL.canonical_json
sha256_json = _METRIC_PROTOCOL.sha256_json
verify_receipt = _METRIC_PROTOCOL.verify_receipt
build_receipt = _GENERATOR.build_receipt


def _require_source_bound_verifier() -> None:
    if _LOADED_VERIFIER_SHA256 is None:
        raise MetricProtocolError(
            "verifier API must be source-loaded; use the direct CLI or source loader"
        )



def _attest_after_replay(candidate: dict) -> dict:
    attested = deepcopy(verify_receipt(candidate))
    if attested["verification"]["result"] != "pending":
        raise MetricProtocolError("only a pending generator candidate can be attested")
    attested["verification"]["result"] = "pass"
    attested.pop("receipt_sha256")
    attested["receipt_sha256"] = sha256_json(attested)
    return verify_receipt(attested)


def verify_and_replay(
    receipt_path: Path,
    *,
    metapat_root: Path,
    ucns_root: Path,
    edcm_root: Path,
    work_graph_path: Path,
    attest_output: Path | None = None,
) -> dict:
    _require_source_bound_verifier()
    raw = receipt_path.read_bytes()
    if not raw.endswith(b"\n"):
        raise MetricProtocolError("receipt must end with exactly one canonical newline")
    parsed = json.loads(raw.decode("utf-8"))
    validated = verify_receipt(parsed)
    if raw != (canonical_json(validated) + "\n").encode("utf-8"):
        raise MetricProtocolError("receipt bytes are not canonical")
    candidate = build_receipt(
        metapat_root=metapat_root,
        ucns_root=ucns_root,
        edcm_root=edcm_root,
        work_graph_path=work_graph_path,
        verifier_sha256=_LOADED_VERIFIER_SHA256,
    )
    if candidate["verification"]["result"] != "pending":
        raise MetricProtocolError("generator must emit a pending receipt")
    expected = (
        candidate
        if validated["verification"]["result"] == "pending"
        else _attest_after_replay(candidate)
    )
    if canonical_json(expected) != canonical_json(validated):
        raise MetricProtocolError("receipt replay differs from committed receipt")
    if attest_output is not None:
        if validated["verification"]["result"] != "pending":
            raise MetricProtocolError("attestation input must be pending")
        attested = _attest_after_replay(candidate)
        attest_output.write_text(canonical_json(attested) + "\n", encoding="utf-8")
        return attested
    return validated


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--metapat-root", type=Path, required=True)
    parser.add_argument("--ucns-root", type=Path, required=True)
    parser.add_argument("--edcm-root", type=Path, required=True)
    parser.add_argument(
        "--work-graph",
        type=Path,
        default=Path(__file__).resolve().parent / "WORK_GRAPH.json",
    )
    parser.add_argument("--attest-output", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    receipt = verify_and_replay(
        args.receipt,
        metapat_root=args.metapat_root,
        ucns_root=args.ucns_root,
        edcm_root=args.edcm_root,
        work_graph_path=args.work_graph,
        attest_output=args.attest_output,
    )
    action = "attested" if args.attest_output is not None else "replayed"
    destination = args.attest_output if args.attest_output is not None else args.receipt
    print(f"{action} {destination} ({receipt['receipt_sha256']}, {receipt['verification']['result']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(
        "run verify_receipt_cli.py so verifier execution is source-bound"
    )
