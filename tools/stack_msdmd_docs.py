#!/usr/bin/env python3
"""Assemble stack MSDMD declarations into machine and human docs."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SKILL_LIB = ROOT / "skill-lib"
if str(SKILL_LIB) not in sys.path:
    sys.path.insert(0, str(SKILL_LIB))

from msdmd.collect import DEFAULT_BLOCK_NAMES, collect as collect_msdmd  # noqa: E402
from msdmd.parsers.universal import marker_for  # noqa: E402
from msdmd.visualize import load_collection  # noqa: E402


# === MODULE_BUILD ===
# id: stack_msdmd_docs_runner
#   summary: assembles stack MSDMD blocks and collection points into machine and human docs
#   inputs: module-local MSDMD blocks, *_msdmd.ts collection points
#   outputs: docs/stack-msdmd.machine.json, docs/stack-msdmd.human.md
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: stack_msdmd_docs_directory_chapters
#   given: stack MSDMD data with files under top-level directories
#   then:  the machine and human docs group entries by directory chapters
#   class: documentation_topology
# id: stack_msdmd_docs_collection_points
#   given: generated or hand-authored *_msdmd.ts collection files
#   then:  the runner imports their declarations, gaps, and edges as read-only source data
#   class: metadata_ingestion
# id: stack_msdmd_docs_deduplicates_sources
#   given: the same declaration or edge appears through multiple input sources
#   then:  the runner emits one record with all source references preserved
#   class: metadata_integrity
# === END CONTRACTS ===


DOC_SCHEMA = "stack.msdmd.docs.v1"
DEFAULT_MACHINE_OUT = Path("docs/stack-msdmd.machine.json")
DEFAULT_HUMAN_OUT = Path("docs/stack-msdmd.human.md")
COLLECTION_GLOB = "*_msdmd.ts"
FRONT_MATTER = "front-matter"
SKIP_DIRS = {
    ".git",
    ".skill-lib",
    ".mypy_cache",
    ".next",
    ".nuxt",
    ".pytest_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "target",
    "venv",
}


def _git_value(root: Path, *args: str) -> str | None:
    try:
        return subprocess.check_output(
            ("git", *args),
            cwd=root,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def current_commit(root: Path) -> str | None:
    return _git_value(root, "rev-parse", "HEAD")


def is_dirty(root: Path) -> bool:
    return bool(_git_value(root, "status", "--porcelain"))


def repo_relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def chapter_for(file_path: str) -> str:
    parts = PurePosixPath(file_path).parts
    if not parts or parts[0] in ("", "."):
        return FRONT_MATTER
    return parts[0] if len(parts) > 1 else FRONT_MATTER


def chapter_title(chapter: str) -> str:
    if chapter == FRONT_MATTER:
        return "Front Matter"
    return chapter.replace("-", " ").replace("_", " ").title()


def section_for(file_path: str, chapter: str) -> str:
    if chapter == FRONT_MATTER:
        return "."
    parts = PurePosixPath(file_path).parts
    if len(parts) <= 2:
        return "."
    return parts[1]


def prefix_collection_path(collection_file: str, owned_file: str) -> str:
    base = PurePosixPath(collection_file).parent.as_posix()
    normalized = PurePosixPath(owned_file).as_posix()
    if normalized in ("", "."):
        return base
    if base in ("", "."):
        return normalized
    if normalized == base or normalized.startswith(f"{base}/"):
        return normalized
    return f"{base}/{normalized}"


def iter_collection_points(root: Path) -> list[Path]:
    points: list[Path] = []
    for path in root.rglob(COLLECTION_GLOB):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        points.append(path)
    return sorted(points, key=lambda path: repo_relative(root, path))


def iter_source_files(root: Path) -> list[str]:
    files: list[str] = []

    def walk(path: Path) -> None:
        try:
            children = sorted(path.iterdir())
        except OSError:
            return
        for child in children:
            if child.is_dir():
                if child.name not in SKIP_DIRS:
                    walk(child)
            elif child.is_file() and marker_for(child) is not None:
                files.append(repo_relative(root, child))

    walk(root)
    return files


def normalize_direct_collection(collection: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    repo = str(collection.get("repo", "stack"))
    source_ref = {"kind": "direct", "repo": repo}
    declarations = []
    for declaration in collection.get("declarations", []):
        item = {
            "file": str(declaration["file"]),
            "block": str(declaration["block"]),
            "id": str(declaration["id"]),
            "fields": {str(k): str(v) for k, v in declaration.get("fields", {}).items()},
            "sources": [source_ref],
        }
        declarations.append(item)

    gaps = []
    for gap in collection.get("gaps", []):
        gaps.append(
            {
                "file": str(gap["file"]),
                "missing": [str(item) for item in gap.get("missing", [])],
                "sources": [source_ref],
            }
        )

    edges = []
    for edge in collection.get("edges", []):
        edges.append(_edge_with_source(edge, source_ref))
    return declarations, gaps, edges


def normalize_collection_point(
    root: Path,
    path: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rel = repo_relative(root, path)
    collection = load_collection(path)
    source_ref = {
        "kind": "collection_point",
        "path": rel,
        "repo": str(collection.get("repo", "")),
    }
    if collection.get("source_commit"):
        source_ref["source_commit"] = str(collection["source_commit"])

    declarations: list[dict[str, Any]] = []
    for declaration in collection.get("declarations", []):
        item = {
            "file": prefix_collection_path(rel, str(declaration["file"])),
            "block": str(declaration["block"]),
            "id": str(declaration["id"]),
            "fields": {str(k): str(v) for k, v in declaration.get("fields", {}).items()},
            "sources": [
                {
                    **source_ref,
                    "owned_file": str(declaration["file"]),
                }
            ],
        }
        declarations.append(item)

    gaps: list[dict[str, Any]] = []
    for gap in collection.get("gaps", []):
        gaps.append(
            {
                "file": prefix_collection_path(rel, str(gap["file"])),
                "missing": [str(item) for item in gap.get("missing", [])],
                "reason": str(gap["reason"]) if gap.get("reason") else None,
                "sources": [source_ref],
            }
        )

    edges = [_edge_with_source(edge, source_ref) for edge in collection.get("edges", [])]
    meta = {
        "path": rel,
        "repo": str(collection.get("repo", "")),
        "source_commit": collection.get("source_commit"),
        "counts": {
            "declarations": len(collection.get("declarations", [])),
            "gaps": len(collection.get("gaps", [])),
            "edges": len(collection.get("edges", [])),
        },
    }
    return meta, declarations, gaps, edges


def _edge_with_source(edge: dict[str, Any], source_ref: dict[str, Any]) -> dict[str, Any]:
    return {
        "from": str(edge["from"]),
        "to": str(edge["to"]),
        "kind": str(edge["kind"]),
        "source_block": str(edge["source_block"]),
        "source_id": str(edge["source_id"]),
        "sources": [source_ref],
    }


def declaration_key(declaration: dict[str, Any]) -> str:
    return f'{declaration["file"]}::{declaration["block"]}::{declaration["id"]}'


def edge_key(edge: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        str(edge["from"]),
        str(edge["to"]),
        str(edge["kind"]),
        str(edge["source_block"]),
        str(edge["source_id"]),
    )


def gap_key(gap: dict[str, Any]) -> tuple[str, tuple[str, ...]]:
    return (str(gap["file"]), tuple(sorted(str(item) for item in gap.get("missing", []))))


def merge_sources(items: Iterable[dict[str, Any]], key_field: str = "sources") -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for item in items:
        key = declaration_key(item)
        if key not in merged:
            merged[key] = {**item, "key": key, key_field: list(item.get(key_field, []))}
            continue
        current = merged[key]
        if current.get("fields") != item.get("fields"):
            current.setdefault("field_conflicts", []).append(
                {
                    "sources": item.get(key_field, []),
                    "fields": item.get("fields", {}),
                }
            )
        current[key_field].extend(item.get(key_field, []))
    return sorted(merged.values(), key=lambda item: (item["file"], item["block"], item["id"]))


def merge_edges(edges: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
    for edge in edges:
        key = edge_key(edge)
        if key not in merged:
            merged[key] = {**edge, "sources": list(edge.get("sources", []))}
            continue
        merged[key]["sources"].extend(edge.get("sources", []))
    return sorted(merged.values(), key=edge_key)


def merge_gaps(gaps: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[tuple[str, tuple[str, ...]], dict[str, Any]] = {}
    for gap in gaps:
        clean_gap = {key: value for key, value in gap.items() if value is not None}
        key = gap_key(clean_gap)
        if key not in merged:
            merged[key] = {**clean_gap, "sources": list(clean_gap.get("sources", []))}
            continue
        merged[key]["sources"].extend(clean_gap.get("sources", []))
    return sorted(merged.values(), key=lambda item: (item["file"], item["missing"]))


def summarize_blocks(declarations: Iterable[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(item["block"] for item in declarations).items()))


def summarize_source_kinds(declarations: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for declaration in declarations:
        for source in declaration.get("sources", []):
            counts[str(source.get("kind", "unknown"))] += 1
    return dict(sorted(counts.items()))


def declaration_chapters(declarations: list[dict[str, Any]]) -> dict[str, str]:
    return {item["id"]: item["chapter"] for item in declarations}


def add_chapter_fields(declarations: list[dict[str, Any]], gaps: list[dict[str, Any]], edges: list[dict[str, Any]]) -> None:
    for declaration in declarations:
        declaration["chapter"] = chapter_for(declaration["file"])
        declaration["section"] = section_for(declaration["file"], declaration["chapter"])
    for gap in gaps:
        gap["chapter"] = chapter_for(gap["file"])
        gap["section"] = section_for(gap["file"], gap["chapter"])
    chapters_by_id = declaration_chapters(declarations)
    for edge in edges:
        edge["chapter"] = chapters_by_id.get(str(edge["source_id"]), FRONT_MATTER)


def chapter_order(root: Path, declarations: list[dict[str, Any]], gaps: list[dict[str, Any]], collection_points: list[dict[str, Any]]) -> list[str]:
    chapters = {item["chapter"] for item in declarations}
    chapters.update(item["chapter"] for item in gaps)
    chapters.update(chapter_for(item["path"]) for item in collection_points)
    chapters.update(
        child.name
        for child in root.iterdir()
        if child.is_dir() and child.name not in SKIP_DIRS and child.name != "docs"
    )
    ordered = sorted(chapter for chapter in chapters if chapter != FRONT_MATTER)
    return ([FRONT_MATTER] if FRONT_MATTER in chapters else []) + ordered


def build_chapters(
    root: Path,
    declarations: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    collection_points: list[dict[str, Any]],
    unannotated_files: list[str],
) -> list[dict[str, Any]]:
    chapters: list[dict[str, Any]] = []
    for index, chapter in enumerate(chapter_order(root, declarations, gaps, collection_points), start=1):
        chapter_declarations = [item for item in declarations if item["chapter"] == chapter]
        chapter_gaps = [item for item in gaps if item["chapter"] == chapter]
        chapter_edges = [item for item in edges if item["chapter"] == chapter]
        chapter_points = [item for item in collection_points if chapter_for(item["path"]) == chapter]
        chapter_unannotated = [path for path in unannotated_files if chapter_for(path) == chapter]
        sections: dict[str, dict[str, Any]] = {}
        for declaration in chapter_declarations:
            section = declaration["section"]
            sections.setdefault(
                section,
                {
                    "id": section,
                    "title": "Chapter Root" if section == "." else chapter_title(section),
                    "counts": {"declarations": 0, "gaps": 0, "edges": 0, "unannotated_files": 0},
                    "blocks": {},
                },
            )
            sections[section]["counts"]["declarations"] += 1
            sections[section]["blocks"] = summarize_blocks(
                item for item in chapter_declarations if item["section"] == section
            )
        for gap in chapter_gaps:
            section = gap["section"]
            sections.setdefault(
                section,
                {
                    "id": section,
                    "title": "Chapter Root" if section == "." else chapter_title(section),
                    "counts": {"declarations": 0, "gaps": 0, "edges": 0, "unannotated_files": 0},
                    "blocks": {},
                },
            )
            sections[section]["counts"]["gaps"] += 1
        for edge in chapter_edges:
            section = "."
            source_decl = next((item for item in chapter_declarations if item["id"] == edge["source_id"]), None)
            if source_decl:
                section = source_decl["section"]
            sections.setdefault(
                section,
                {
                    "id": section,
                    "title": "Chapter Root" if section == "." else chapter_title(section),
                    "counts": {"declarations": 0, "gaps": 0, "edges": 0, "unannotated_files": 0},
                    "blocks": {},
                },
            )
            sections[section]["counts"]["edges"] += 1
        for file_path in chapter_unannotated:
            section = section_for(file_path, chapter)
            sections.setdefault(
                section,
                {
                    "id": section,
                    "title": "Chapter Root" if section == "." else chapter_title(section),
                    "counts": {"declarations": 0, "gaps": 0, "edges": 0, "unannotated_files": 0},
                    "blocks": {},
                },
            )
            sections[section]["counts"]["unannotated_files"] += 1

        chapters.append(
            {
                "number": index,
                "id": chapter,
                "title": chapter_title(chapter),
                "path": "." if chapter == FRONT_MATTER else chapter,
                "counts": {
                    "declarations": len(chapter_declarations),
                    "gaps": len(chapter_gaps),
                    "edges": len(chapter_edges),
                    "collection_points": len(chapter_points),
                    "unannotated_files": len(chapter_unannotated),
                },
                "blocks": summarize_blocks(chapter_declarations),
                "sections": sorted(sections.values(), key=lambda item: item["id"]),
                "collection_points": [item["path"] for item in chapter_points],
                "declaration_keys": [item["key"] for item in chapter_declarations],
                "gap_keys": [f'{item["file"]}::missing:{",".join(item["missing"])}' for item in chapter_gaps],
                "edge_keys": [list(edge_key(item)) for item in chapter_edges],
                "unannotated_files": chapter_unannotated,
            }
        )
    return chapters


def find_unannotated_source_files(
    source_files: list[str],
    declarations: list[dict[str, Any]],
    collection_point_paths: Iterable[str] = (),
) -> list[str]:
    annotated = {item["file"] for item in declarations if any(source.get("kind") == "direct" for source in item.get("sources", []))}
    indexed = set(collection_point_paths)
    return sorted(file for file in source_files if file not in annotated and file not in indexed)


def build_book(
    root: Path,
    *,
    repo: str = "stack",
    blocks: Iterable[str] = DEFAULT_BLOCK_NAMES,
    expected_blocks: Iterable[str] = (),
    source_commit: str | None = None,
    include_collection_points: bool = True,
    include_generated_at: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    source_commit = source_commit if source_commit is not None else current_commit(root)
    direct = collect_msdmd(root, repo, block_names=blocks, expected_blocks=expected_blocks, source_commit=source_commit)
    direct_declarations, direct_gaps, direct_edges = normalize_direct_collection(direct)

    collection_points: list[dict[str, Any]] = []
    imported_declarations: list[dict[str, Any]] = []
    imported_gaps: list[dict[str, Any]] = []
    imported_edges: list[dict[str, Any]] = []
    if include_collection_points:
        for point in iter_collection_points(root):
            meta, declarations, gaps, edges = normalize_collection_point(root, point)
            collection_points.append(meta)
            imported_declarations.extend(declarations)
            imported_gaps.extend(gaps)
            imported_edges.extend(edges)

    declarations = merge_sources([*direct_declarations, *imported_declarations])
    gaps = merge_gaps([*direct_gaps, *imported_gaps])
    edges = merge_edges([*direct_edges, *imported_edges])
    add_chapter_fields(declarations, gaps, edges)

    source_files = iter_source_files(root)
    unannotated_files = find_unannotated_source_files(
        source_files,
        declarations,
        (point["path"] for point in collection_points),
    )
    chapters = build_chapters(root, declarations, gaps, edges, collection_points, unannotated_files)
    summary = {
        "declarations": len(declarations),
        "gaps": len(gaps),
        "edges": len(edges),
        "collection_points": len(collection_points),
        "source_files": len(source_files),
        "unannotated_files": len(unannotated_files),
        "blocks": summarize_blocks(declarations),
        "source_kinds": summarize_source_kinds(declarations),
        "chapters": {chapter["id"]: chapter["counts"] for chapter in chapters},
    }

    book: dict[str, Any] = {
        "schema": DOC_SCHEMA,
        "repo": repo,
        "runner": {
            "path": "tools/stack_msdmd_docs.py",
            "machine_out": DEFAULT_MACHINE_OUT.as_posix(),
            "human_out": DEFAULT_HUMAN_OUT.as_posix(),
            "blocks": list(blocks),
            "expected_blocks": list(expected_blocks),
            "include_collection_points": include_collection_points,
        },
        "source_commit": source_commit,
        "source_dirty": is_dirty(root),
        "summary": summary,
        "chapters": chapters,
        "collection_points": collection_points,
        "declarations": declarations,
        "gaps": gaps,
        "edges": edges,
    }
    if include_generated_at:
        book["generated_at"] = datetime.now(timezone.utc).isoformat()
    return book


def _field_summary(fields: dict[str, Any]) -> str:
    for key in ("summary", "given", "then", "expects", "covers", "requires", "proves", "owner"):
        value = fields.get(key)
        if value:
            return str(value)
    if not fields:
        return ""
    first_key = sorted(fields)[0]
    return f"{first_key}: {fields[first_key]}"


def _source_summary(sources: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for source in sources:
        kind = source.get("kind", "unknown")
        if kind == "collection_point":
            parts.append(str(source.get("path", "collection_point")))
        else:
            parts.append(str(kind))
    return ", ".join(dict.fromkeys(parts))


def render_human(book: dict[str, Any], *, detail_limit: int = 0) -> str:
    summary = book["summary"]
    lines = [
        "# stack",
        "",
        "MSDMD book assembled from module-local declarations and repo collection points.",
        "",
        "## Machine Companion",
        "",
        "- Machine file: `docs/stack-msdmd.machine.json`",
        f"- Schema: `{book['schema']}`",
        f"- Source commit: `{book.get('source_commit') or 'unknown'}`",
        f"- Source dirty at generation: `{book.get('source_dirty')}`",
        f"- Regenerate: `PYTHONPATH=.:skill-lib python3 {book['runner']['path']} --root . --repo {book['repo']}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Declarations | {summary['declarations']} |",
        f"| Relationship edges | {summary['edges']} |",
        f"| Coverage gaps | {summary['gaps']} |",
        f"| Collection points | {summary['collection_points']} |",
        f"| Source files scanned | {summary['source_files']} |",
        f"| Source files without direct MSDMD | {summary['unannotated_files']} |",
        "",
        "## Blocks",
        "",
        "| Block | Count |",
        "|---|---:|",
    ]
    for block, count in summary["blocks"].items():
        lines.append(f"| `{block}` | {count} |")
    if not summary["blocks"]:
        lines.append("| hmmm | 0 |")

    declarations_by_key = {item["key"]: item for item in book["declarations"]}
    gaps_by_chapter: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for gap in book["gaps"]:
        gaps_by_chapter[gap["chapter"]].append(gap)

    lines.extend(["", "## Chapters", ""])
    for chapter in book["chapters"]:
        lines.append(f"## Chapter {chapter['number']}: {chapter['title']}")
        lines.append("")
        counts = chapter["counts"]
        lines.append(
            f"{counts['declarations']} declarations, {counts['edges']} edges, "
            f"{counts['gaps']} gaps, {counts['collection_points']} collection points, "
            f"{counts['unannotated_files']} source files without direct MSDMD."
        )
        lines.append("")
        if chapter["collection_points"]:
            lines.append("Collection points:")
            for point in chapter["collection_points"]:
                lines.append(f"- `{point}`")
            lines.append("")

        if chapter["sections"]:
            lines.append("| Section | Declarations | Edges | Gaps | Unannotated |")
            lines.append("|---|---:|---:|---:|---:|")
            for section in chapter["sections"]:
                section_counts = section["counts"]
                lines.append(
                    f"| `{section['id']}` | {section_counts['declarations']} | "
                    f"{section_counts['edges']} | {section_counts['gaps']} | "
                    f"{section_counts['unannotated_files']} |"
                )
            lines.append("")

        chapter_declarations = [declarations_by_key[key] for key in chapter["declaration_keys"]]
        declarations_by_block: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for declaration in chapter_declarations:
            declarations_by_block[declaration["block"]].append(declaration)
        for block in sorted(declarations_by_block):
            block_items = declarations_by_block[block]
            visible = block_items if detail_limit <= 0 else block_items[:detail_limit]
            lines.append(f"### {block}")
            lines.append("")
            for declaration in visible:
                summary_text = _field_summary(declaration.get("fields", {}))
                source_text = _source_summary(declaration.get("sources", []))
                suffix = f" - {summary_text}" if summary_text else ""
                lines.append(
                    f"- `{declaration['id']}` in `{declaration['file']}` "
                    f"({source_text}){suffix}"
                )
            hidden = len(block_items) - len(visible)
            if hidden > 0:
                lines.append(f"- ... {hidden} more `{block}` declarations in machine file.")
            lines.append("")

        chapter_gaps = gaps_by_chapter.get(chapter["id"], [])
        if chapter_gaps:
            lines.append("### Visible Gaps")
            lines.append("")
            visible_gaps = chapter_gaps if detail_limit <= 0 else chapter_gaps[:detail_limit]
            for gap in visible_gaps:
                lines.append(f"- `{gap['file']}` missing {', '.join(f'`{item}`' for item in gap['missing'])}")
            hidden = len(chapter_gaps) - len(visible_gaps)
            if hidden > 0:
                lines.append(f"- ... {hidden} more gaps in machine file.")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_docs(book: dict[str, Any], machine_out: Path, human_out: Path, *, detail_limit: int = 0) -> None:
    machine_out.parent.mkdir(parents=True, exist_ok=True)
    human_out.parent.mkdir(parents=True, exist_ok=True)
    machine_out.write_text(json.dumps(book, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    human_out.write_text(render_human(book, detail_limit=detail_limit), encoding="utf-8")


def output_path(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="stack repo root to scan")
    parser.add_argument("--repo", default="stack", help="repo/book title to record")
    parser.add_argument("--machine-out", type=Path, default=DEFAULT_MACHINE_OUT, help="machine-facing JSON output path")
    parser.add_argument("--human-out", type=Path, default=DEFAULT_HUMAN_OUT, help="human-facing Markdown output path")
    parser.add_argument("--source-commit", help="source commit SHA to record; defaults to git HEAD")
    parser.add_argument(
        "--block",
        action="append",
        dest="blocks",
        help="MSDMD block name to collect; may be repeated; defaults to all known blocks",
    )
    parser.add_argument(
        "--expected-block",
        action="append",
        default=[],
        help="block expected on every source file for visible gap reporting; may be repeated",
    )
    parser.add_argument(
        "--no-collection-points",
        action="store_true",
        help="only parse module-local blocks; do not import *_msdmd.ts files",
    )
    parser.add_argument(
        "--human-detail-limit",
        type=int,
        default=0,
        help="limit declarations/gaps shown per chapter block in Markdown; 0 means all",
    )
    parser.add_argument(
        "--include-generated-at",
        action="store_true",
        help="include a wall-clock generation timestamp in the machine file",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    book = build_book(
        root,
        repo=args.repo,
        blocks=args.blocks or DEFAULT_BLOCK_NAMES,
        expected_blocks=args.expected_block,
        source_commit=args.source_commit,
        include_collection_points=not args.no_collection_points,
        include_generated_at=args.include_generated_at,
    )
    machine_out = output_path(root, args.machine_out)
    human_out = output_path(root, args.human_out)
    write_docs(book, machine_out, human_out, detail_limit=args.human_detail_limit)
    print(f"wrote {machine_out.relative_to(root)}")
    print(f"wrote {human_out.relative_to(root)}")
    print(
        f"assembled {book['summary']['declarations']} declarations, "
        f"{book['summary']['edges']} edges, {book['summary']['collection_points']} collection points"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
