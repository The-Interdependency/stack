# === MODULE_BUILD ===
# id: stack_consistency_checker
#   module_name: check_stack_consistency
#   module_kind: verification-tool
#   summary: fail-closed structural consistency checks across stack manifests, research bases, authority projections, and work-graph identity
#   owner: The-Interdependency/stack
#   public_surface: command-line exit status and human-readable findings
#   internal_surface: manifest digest, repository/base cross-checks, separated-component checks
#   auth_boundary: none
#   storage_boundary: read-only repository files
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: exercised in .github/workflows/stack-consistency.yml and by local invocation
#   rollout: required structural drift gate
#   rollback: revert checker/workflow together only if replaced by an equivalent or stricter gate
#   requires: Python standard library, stack-manifest.json, STACK_MANIFEST.md
#   since: 2026-09-12
#   unresolved: semantic responsibility cannot be inferred exhaustively from source code
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: stack_work_graph_digest_reproduces
#   given: stack-manifest.json declares repositories, research_participants, boundaries, and work_graph_sha256
#   then: canonical JSON over the three hashed fields reproduces the declared SHA-256 exactly
#   class: evidence
#   since: 2026-09-12
#
# id: stack_human_machine_authority_agree
#   given: stack-manifest.json and STACK_MANIFEST.md describe repository participants
#   then: every machine-declared repository identity, commit, and authority is represented in the human manifest
#   class: evidence
#   since: 2026-09-12
#
# id: separated_stack_component_has_graph_identity
#   given: a research BASE.json declares a project name distinct from its source repository name
#   then: the project has an explicit research_participants record and the former source owner does not retain a known superseded authority claim
#   class: boundary
#   since: 2026-09-12
# === END CONTRACTS ===

"""Verify stack authority/provenance projections agree.

Usage guidance
--------------
Run from the repository root before and after any structural stack mutation::

    python tools/check_stack_consistency.py

The command is intentionally read-only and stdlib-only. Exit status 0 means the
checks implemented here agree; it does not promote research to canon or prove any
scientific, semantic, measurement, or graduation claim.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "stack-manifest.json"
HUMAN_MANIFEST_PATH = ROOT / "STACK_MANIFEST.md"
README_PATH = ROOT / "README.md"
HASHED_FIELDS = ("repositories", "research_participants", "boundaries")
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_digest(manifest: dict[str, Any]) -> str:
    payload = {key: manifest[key] for key in HASHED_FIELDS}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def error(findings: list[str], code: str, message: str) -> None:
    findings.append(f"{code}: {message}")


def check_manifest_shape(manifest: dict[str, Any], findings: list[str]) -> None:
    if manifest.get("schema") != "the-interdependency.stack-manifest":
        error(findings, "manifest.schema", "unexpected or missing stack-manifest schema")
    for key in (*HASHED_FIELDS, "work_graph_sha256"):
        if key not in manifest:
            error(findings, "manifest.missing", f"missing required field {key!r}")
    for entry in manifest.get("repositories", []):
        commit = entry.get("commit", "")
        if not HEX40.fullmatch(commit):
            error(findings, "repository.commit", f"{entry.get('repository')}: invalid commit {commit!r}")
    for entry in manifest.get("research_participants", []):
        commit = entry.get("commit", "")
        if not HEX40.fullmatch(commit):
            error(findings, "research.commit", f"{entry.get('workspace')}:{entry.get('participant_id')}: invalid commit {commit!r}")
        if entry.get("authority_transfer") is not False:
            error(findings, "research.authority_transfer", f"{entry.get('workspace')}:{entry.get('participant_id')} must keep authority_transfer=false")


def check_digest(manifest: dict[str, Any], human: str, findings: list[str]) -> None:
    try:
        actual = manifest_digest(manifest)
    except KeyError as exc:
        error(findings, "digest.input", f"cannot compute digest; missing {exc.args[0]!r}")
        return
    declared = manifest.get("work_graph_sha256", "")
    if declared != actual:
        error(findings, "digest.mismatch", f"declared {declared!r}, recomputed {actual!r}")
    if declared and declared not in human:
        error(findings, "digest.human_drift", "STACK_MANIFEST.md does not carry the machine-declared work-graph digest")


def check_repository_projection(manifest: dict[str, Any], human: str, findings: list[str]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for entry in manifest.get("repositories", []):
        repository = entry.get("repository", "")
        if repository in index:
            error(findings, "repository.duplicate", f"duplicate manifest repository {repository!r}")
            continue
        index[repository] = entry
        for field in (repository, entry.get("commit", ""), entry.get("authority", "")):
            if field and field not in human:
                error(findings, "repository.human_drift", f"STACK_MANIFEST.md is missing {repository!r} projection value {field!r}")
    return index


def check_research_participants(manifest: dict[str, Any], human: str, findings: list[str]) -> set[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    for entry in manifest.get("research_participants", []):
        key = (entry.get("workspace", ""), entry.get("participant_id", ""))
        if key in seen:
            error(findings, "research.duplicate", f"duplicate research participant {key!r}")
        seen.add(key)
        workspace = entry.get("workspace", "")
        commit = entry.get("commit", "")
        if workspace and workspace not in human:
            error(findings, "research.human_drift", f"STACK_MANIFEST.md does not mention workspace {workspace!r}")
        if commit and commit not in human:
            error(findings, "research.human_drift", f"STACK_MANIFEST.md does not mention research commit {commit!r}")
    return seen


def check_base_records(
    repositories: dict[str, dict[str, Any]],
    research_participants: set[tuple[str, str]],
    readme: str,
    findings: list[str],
) -> None:
    research_root = ROOT / "research"
    if not research_root.exists():
        error(findings, "research.missing", "research/ directory is missing")
        return

    for base_path in sorted(research_root.glob("*/BASE.json")):
        base = load_json(base_path)
        workspace_name = base_path.parent.name
        workspace = f"research/{workspace_name}/"
        project = str(base.get("project", workspace_name))
        source_repository = str(base.get("source_repository", ""))
        source_commit = str(base.get("source_commit", ""))
        source_entry = repositories.get(source_repository)

        if source_entry and source_commit != source_entry.get("commit"):
            error(
                findings,
                "base.source_drift",
                f"{base_path.relative_to(ROOT)} pins {source_repository}@{source_commit}, manifest pins {source_entry.get('commit')}",
            )

        source_name = source_repository.rsplit("/", 1)[-1] if source_repository else ""
        if project and source_name and project != source_name:
            if (workspace, project) not in research_participants:
                error(
                    findings,
                    "base.separated_unrepresented",
                    f"{workspace} declares separated project {project!r} from source {source_repository!r} but has no matching research_participants record",
                )
            if f"{workspace_name}/" not in readme and workspace not in readme:
                error(findings, "base.readme_drift", f"README.md does not expose separated workspace {workspace!r}")


def check_english_gonol_regression(
    repositories: dict[str, dict[str, Any]],
    research_participants: set[tuple[str, str]],
    human: str,
    readme: str,
    findings: list[str],
) -> None:
    base_path = ROOT / "research" / "english-gonol" / "BASE.json"
    if not base_path.exists():
        return

    edcm = repositories.get("The-Interdependency/edcm")
    if edcm is None:
        error(findings, "english_gonol.edcm_missing", "EDCM is absent from repositories manifest")
        return

    authority = str(edcm.get("authority", "")).lower()
    if "gonol construction" in authority or "text-gonol construction" in authority:
        error(findings, "english_gonol.stale_edcm_authority", "EDCM still claims English/text gonol construction authority after separation")

    expected = ("research/english-gonol/", "english-gonol")
    if expected not in research_participants:
        error(findings, "english_gonol.graph_missing", "English Gonol is missing its explicit stack research-participant identity")

    for surface_name, surface in (("STACK_MANIFEST.md", human), ("README.md", readme)):
        if "research/english-gonol/" not in surface and "english-gonol/" not in surface:
            error(findings, "english_gonol.projection_missing", f"{surface_name} does not expose English Gonol's separated workspace")


def main() -> int:
    findings: list[str] = []
    try:
        manifest = load_json(MANIFEST_PATH)
        human = HUMAN_MANIFEST_PATH.read_text(encoding="utf-8")
        readme = README_PATH.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"stack consistency: fail: unable to read required inputs: {exc}")
        return 1

    check_manifest_shape(manifest, findings)
    check_digest(manifest, human, findings)
    repositories = check_repository_projection(manifest, human, findings)
    research_participants = check_research_participants(manifest, human, findings)
    check_base_records(repositories, research_participants, readme, findings)
    check_english_gonol_regression(repositories, research_participants, human, readme, findings)

    if findings:
        for finding in findings:
            print(f"error: {finding}")
        print(f"stack consistency: fail ({len(findings)} error(s))")
        return 1

    print(f"stack consistency: pass ({len(repositories)} repositories, {len(research_participants)} research participant identities)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
