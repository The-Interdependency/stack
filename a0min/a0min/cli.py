# ratios: loc_comments=201:10 imports_exports=8:1 calls_definitions=84:9
"""Minimal CLI for the a0min agent harness.

Commands:
    list                 list potential sub-agent options from the superpotential
    create REGION        create one potential sub-agent from a declared region
    show ID              show a created sub-agent
    merge ID             mark a created sub-agent merged
    superpotential       dump the imported platonic superpotential
    caps                 show spawn caps for a tier

Every command accepts ``--json`` for machine-readable output.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from .harness import (
    SUPPORTED_CUT_MODES,
    SUPPORTED_ORCHESTRATION_MODES,
    Harness,
    SpawnCapExceeded,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="a0min",
        description="Minimal agent harness over the imported a0 platonic superpotential.",
    )
    parser.add_argument(
        "--state",
        default=os.environ.get("A0MIN_STATE"),
        help="JSON state file for created sub-agents (env: A0MIN_STATE)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="list potential sub-agent options")
    list_parser.add_argument("--json", action="store_true", dest="as_json")

    create_parser = sub.add_parser(
        "create", help="create one potential sub-agent from a region"
    )
    create_parser.add_argument("region", help="declared semantic region name")
    create_parser.add_argument("--task", default="", help="task summary for the sub-agent")
    create_parser.add_argument(
        "--bind",
        action="append",
        default=[],
        metavar="K=V",
        help="projection binding; repeatable; values parse as JSON when possible",
    )
    create_parser.add_argument(
        "--mode",
        default="single",
        choices=SUPPORTED_ORCHESTRATION_MODES,
        help="orchestration mode (default: single)",
    )
    create_parser.add_argument(
        "--cut",
        default="soft",
        choices=SUPPORTED_CUT_MODES,
        help="cut mode (default: soft)",
    )
    create_parser.add_argument("--tier", default="free", help="spawn-cap tier")
    create_parser.add_argument(
        "--provider", action="append", default=None, help="provider tag; repeatable"
    )
    create_parser.add_argument(
        "--parent", default=None, help="parent sub_agent_id for depth/fanout accounting"
    )
    create_parser.add_argument("--json", action="store_true", dest="as_json")

    show_parser = sub.add_parser("show", help="show a created sub-agent")
    show_parser.add_argument("sub_agent_id")
    show_parser.add_argument("--json", action="store_true", dest="as_json")

    merge_parser = sub.add_parser("merge", help="mark a created sub-agent merged")
    merge_parser.add_argument("sub_agent_id")
    merge_parser.add_argument("--json", action="store_true", dest="as_json")

    super_parser = sub.add_parser(
        "superpotential", help="dump the imported platonic superpotential"
    )
    super_parser.add_argument("--json", action="store_true", dest="as_json")

    caps_parser = sub.add_parser("caps", help="show spawn caps for a tier")
    caps_parser.add_argument("--tier", default="free", help="spawn-cap tier")
    caps_parser.add_argument("--json", action="store_true", dest="as_json")

    return parser


def _parse_binding(text: str) -> tuple[str, Any]:
    key, sep, value = text.partition("=")
    if not sep or not key:
        raise ValueError(f"binding must be K=V: {text}")
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        parsed = value
    return key, parsed


def _print_or_json(payload: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2))
        return
    if isinstance(payload, dict):
        for key, value in payload.items():
            print(f"{key}: {value}")
        return
    for item in payload:
        print(item)


def _list_potential(harness: Harness, as_json: bool) -> int:
    options = harness.potential_sub_agents()
    if as_json:
        print(json.dumps([option.as_dict() for option in options], indent=2))
        return 0
    print(f"potential sub-agents from {harness.superpotential.agent_id}:")
    for option in options:
        print(f"  {option.region}")
        print(f"    {option.description}")
        print(f"    dims: {', '.join(option.dimensions)}")
        print(f"    surfaces: {', '.join(option.surfaces)}")
        print(
            f"    modes: {', '.join(option.orchestration_modes)} | "
            f"cuts: {', '.join(option.cut_modes)}"
        )
    return 0


def _create(harness: Harness, args: argparse.Namespace) -> int:
    try:
        bindings = dict(_parse_binding(text) for text in args.bind)
        parent = harness.get(args.parent) if args.parent else None
        sub_agent = harness.create(
            args.region,
            bindings,
            task=args.task,
            orchestration_mode=args.mode,
            cut_mode=args.cut,
            providers=args.provider,
            parent=parent,
        )
    except (ValueError, KeyError, SpawnCapExceeded) as exc:
        print(f"create failed: {exc}", file=sys.stderr)
        return 1
    if args.as_json:
        print(json.dumps(sub_agent.as_dict(), indent=2))
        return 0
    print(
        f"created {sub_agent.sub_agent_id} {sub_agent.name} "
        f"run={sub_agent.run_id} depth={sub_agent.depth} "
        f"region={sub_agent.region} mode={sub_agent.orchestration_mode} "
        f"cut={sub_agent.cut_mode}"
    )
    print(f"  selected: {', '.join(sub_agent.selected) or '-'}")
    print(f"  unresolved: {', '.join(sub_agent.unresolved) or '-'}")
    print(f"  omitted: {', '.join(sub_agent.omitted) or '-'}")
    return 0


def _show(harness: Harness, args: argparse.Namespace) -> int:
    try:
        sub_agent = harness.get(args.sub_agent_id)
    except KeyError as exc:
        print(f"show failed: {exc}", file=sys.stderr)
        return 1
    if args.as_json:
        print(json.dumps(sub_agent.as_dict(), indent=2))
        return 0
    for key, value in sub_agent.as_dict().items():
        print(f"{key}: {value}")
    return 0


def _merge(harness: Harness, args: argparse.Namespace) -> int:
    try:
        sub_agent = harness.merge(args.sub_agent_id)
    except KeyError as exc:
        print(f"merge failed: {exc}", file=sys.stderr)
        return 1
    if args.as_json:
        print(json.dumps(sub_agent.as_dict(), indent=2))
        return 0
    print(f"merged {sub_agent.sub_agent_id} {sub_agent.name} (status={sub_agent.status})")
    return 0


def _superpotential(harness: Harness, as_json: bool) -> int:
    payload = harness.superpotential_dict()
    if as_json:
        print(json.dumps(payload, indent=2))
        return 0
    print(f"superpotential: {payload['agent_id']}")
    for dimension in payload["dimensions"]:
        print(f"  dimension {dimension['name']}: {dimension['description']}")
    for region in payload["regions"]:
        print(f"  region {region['region']}: {region['description']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    tier = getattr(args, "tier", "free")
    state_path = getattr(args, "state", None)
    if state_path and Path(state_path).exists():
        harness = Harness.load(state_path, tier=tier)
    else:
        harness = Harness(tier=tier)

    if args.command == "list":
        code = _list_potential(harness, args.as_json)
    elif args.command == "create":
        code = _create(harness, args)
    elif args.command == "show":
        code = _show(harness, args)
    elif args.command == "merge":
        code = _merge(harness, args)
    elif args.command == "superpotential":
        code = _superpotential(harness, args.as_json)
    elif args.command == "caps":
        if args.as_json:
            print(json.dumps(harness.caps, indent=2))
        else:
            _print_or_json(harness.caps, False)
        code = 0
    else:
        parser.error(f"unknown command: {args.command}")
        code = 2

    if state_path and code == 0:
        harness.save(state_path)
    return code
# ratios: loc_comments=201:10 imports_exports=8:1 calls_definitions=84:9
