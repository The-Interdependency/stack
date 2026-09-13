"""Command line entry point for Python Gonol Construction.

Usage guidance::

    python -m python_gonol source.py --out source.gonol.json
    python -m python_gonol --verify source.gonol.json

The construction command exits 2 when source syntax remains ``hmmm``. The
receipt is still written so admitted character, definition, and lexical
closures survive.
"""

# === MODULE_BUILD ===
# id: python_gonol_cli
#   module_name: python_gonol.__main__
#   module_kind: adapter
#   summary: provides file-to-receipt character-first construction and receipt verification commands
#   owner: Python Gonol Construction (stack-local research)
#   public_surface: python -m python_gonol
#   internal_surface: main
#   auth_boundary: none
#   storage_boundary: reads source or receipt files and writes an explicitly named receipt file or stdout
#   network_boundary: none
#   user_data_boundary: read and write at caller-selected paths
#   admin_only: false
#   tests: tests.test_affixiation
#   rollout: explicit command only
#   rollback: remove the CLI while retaining the importable constructor
#   requires: python_gonol_affixiation, python_gonol_model
#   since: 2026-09-12
#   unresolved: streaming receipts for very large sources remain hmmm
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: python_gonol_cli_file_boundary
#   summary: reads one caller-selected local source or receipt and writes only the explicit output path
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   pii: possible
#   secrets: read
#   owner: caller
# === END BOUNDARIES ===

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .affixiation import (
    affixiate_python_bytes,
    reconstruct_source,
    replay_python_affixiation,
)
from .model import PythonAffixiationReceipt


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Affixiate Python 3.12 source into gonols from characters upward."
    )
    parser.add_argument("source", nargs="?", help="Python source file")
    parser.add_argument("--out", help="receipt path; omit for stdout")
    parser.add_argument("--verify", metavar="RECEIPT", help="verify an existing receipt")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.verify:
        if args.source or args.out:
            raise SystemExit("--verify does not accept source or --out")
        receipt = PythonAffixiationReceipt.from_json(
            Path(args.verify).read_text(encoding="utf-8")
        )
        replay_python_affixiation(receipt)
        print(
            f"verified {receipt.receipt_digest} source={receipt.source_id} standing={receipt.standing}"
        )
        return 0
    if not args.source:
        raise SystemExit("source is required unless --verify is used")
    path = Path(args.source)
    receipt = affixiate_python_bytes(path.read_bytes(), source_id=path.as_posix())
    rendered = receipt.to_json(pretty=args.pretty)
    if args.out:
        Path(args.out).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    if receipt.standing == "hmmm":
        for item in receipt.hmmm:
            if item.startswith(("tokenizer:", "grammar:", "unmatched", "delimiter mismatch")):
                print(f"hmmm: {item}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
