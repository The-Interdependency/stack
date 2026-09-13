# === MODULE_BUILD ===
# id: stack_consistency_checker
#   module_name: check_stack_consistency
#   module_kind: verification-tool
#   summary: fail-closed structural consistency checks across stack manifests, research bases, authority projections, work-graph identity, and vendored-skill provenance
#   owner: The-Interdependency/stack
#   public_surface: command-line exit status and human-readable findings
#   internal_surface: manifest digest, repository/base cross-checks, separated-component checks, vendored-skill provenance
#   auth_boundary: none
#   storage_boundary: read-only repository files
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: exercised in .github/workflows/stack-consistency.yml and by local invocation
#   rollout: required structural drift gate
#   rollback: revert checker/workflow together only if replaced by an equivalent or stricter gate
#   requires: Python standard library, Git with full repository history, stack-manifest.json, STACK_MANIFEST.md
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
# id: alternate_research_source_is_explicit
#   given: a research BASE.json source commit differs from its repository's manifest-pinned libs commit
#   then: the workspace carries an explicit matching research_participants source identity rather than silently rebasing the libs pin
#   class: boundary
#   since: 2026-09-12
#
# id: separated_stack_component_has_graph_identity
#   given: a research BASE.json declares a project name distinct from its source repository name
#   then: the project has an explicit research_participants record and the former source owner does not retain a known superseded authority claim
#   class: boundary
#   since: 2026-09-12
#
# id: vendored_stack_skill_has_exact_source_identity
#   given: stack vendors .agents/skills/stack-update/SKILL.md
#   then: provenance pins an immutable skill-lib commit and source blob, authority_transfer is false, and the local Git blob identity matches the declared source blob
#   class: boundary
#   since: 2026-09-12
# === END CONTRACTS ===

"""Verify stack authority/provenance projections agree.

Usage guidance
--------------
Run from the repository root before and after any structural stack mutation::

    python tools/check_stack_consistency.py

Use a Git checkout with the historical commits named by the EPAC transition
receipt (`git fetch --unshallow` for a shallow clone). The command is read-only
and uses the Python standard library plus Git. Exit status 0 means the
checks implemented here agree; it does not promote research to canon or prove any
scientific, semantic, measurement, or graduation claim.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "stack-manifest.json"
HUMAN_MANIFEST_PATH = ROOT / "STACK_MANIFEST.md"
README_PATH = ROOT / "README.md"
SKILLS_README_PATH = ROOT / ".agents" / "skills" / "README.md"
STACK_UPDATE_SKILL_PATH = ROOT / ".agents" / "skills" / "stack-update" / "SKILL.md"
STACK_UPDATE_PROVENANCE_PATH = ROOT / ".agents" / "skills" / "stack-update" / "PROVENANCE.json"
HASHED_FIELDS = ("repositories", "research_participants", "boundaries")
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_digest(manifest: dict[str, Any]) -> str:
    payload = {key: manifest[key] for key in HASHED_FIELDS}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


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


def check_research_participants(
    manifest: dict[str, Any],
    human: str,
    findings: list[str],
) -> tuple[set[tuple[str, str]], set[tuple[str, str, str]]]:
    keys: set[tuple[str, str]] = set()
    sources: set[tuple[str, str, str]] = set()
    for entry in manifest.get("research_participants", []):
        workspace = str(entry.get("workspace", ""))
        participant_id = str(entry.get("participant_id", ""))
        repository = str(entry.get("repository", ""))
        commit = str(entry.get("commit", ""))
        key = (workspace, participant_id)
        if key in keys:
            error(findings, "research.duplicate", f"duplicate research participant {key!r}")
        keys.add(key)
        sources.add((workspace, repository, commit))
        if workspace and workspace not in human:
            error(findings, "research.human_drift", f"STACK_MANIFEST.md does not mention workspace {workspace!r}")
        if commit and commit not in human:
            error(findings, "research.human_drift", f"STACK_MANIFEST.md does not mention research commit {commit!r}")
    return keys, sources


def check_base_records(
    repositories: dict[str, dict[str, Any]],
    research_participant_keys: set[tuple[str, str]],
    research_source_identities: set[tuple[str, str, str]],
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
            explicit_source = (workspace, source_repository, source_commit)
            if explicit_source not in research_source_identities:
                error(
                    findings,
                    "base.source_drift",
                    f"{base_path.relative_to(ROOT)} pins {source_repository}@{source_commit}, manifest libs pin is {source_entry.get('commit')}, and no matching research_participants source identity exists",
                )

        source_name = source_repository.rsplit("/", 1)[-1] if source_repository else ""
        if project and source_name and project != source_name:
            if (workspace, project) not in research_participant_keys:
                error(
                    findings,
                    "base.separated_unrepresented",
                    f"{workspace} declares separated project {project!r} from source {source_repository!r} but has no matching research_participants record",
                )
            if f"{workspace_name}/" not in readme and workspace not in readme:
                error(findings, "base.readme_drift", f"README.md does not expose separated workspace {workspace!r}")


def check_english_gonol_regression(
    repositories: dict[str, dict[str, Any]],
    research_participant_keys: set[tuple[str, str]],
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
    if expected not in research_participant_keys:
        error(findings, "english_gonol.graph_missing", "English Gonol is missing its explicit stack research-participant identity")

    for surface_name, surface in (("STACK_MANIFEST.md", human), ("README.md", readme)):
        if "research/english-gonol/" not in surface and "english-gonol/" not in surface:
            error(findings, "english_gonol.projection_missing", f"{surface_name} does not expose English Gonol's separated workspace")


def check_stack_update_skill_provenance(findings: list[str]) -> None:
    if not STACK_UPDATE_SKILL_PATH.exists():
        error(findings, "skill.missing", "vendored stack-update/SKILL.md is missing")
        return
    if not STACK_UPDATE_PROVENANCE_PATH.exists():
        error(findings, "skill.provenance_missing", "vendored stack-update skill has no PROVENANCE.json")
        return

    try:
        provenance = load_json(STACK_UPDATE_PROVENANCE_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        error(findings, "skill.provenance_invalid", f"cannot read stack-update provenance: {exc}")
        return

    expected_values = {
        "schema": "the-interdependency.vendored-skill-provenance",
        "version": "1.0.0",
        "skill": "stack-update",
        "source_repository": "The-Interdependency/skill-lib",
        "source_path": "stack-update/SKILL.md",
    }
    for field, expected in expected_values.items():
        if provenance.get(field) != expected:
            error(findings, "skill.provenance_field", f"{field} must be {expected!r}, got {provenance.get(field)!r}")

    source_commit = str(provenance.get("source_commit", ""))
    source_blob_sha = str(provenance.get("source_blob_sha", ""))
    if not HEX40.fullmatch(source_commit):
        error(findings, "skill.source_commit", f"invalid source_commit {source_commit!r}")
    if not HEX40.fullmatch(source_blob_sha):
        error(findings, "skill.source_blob", f"invalid source_blob_sha {source_blob_sha!r}")
    if provenance.get("authority_transfer") is not False:
        error(findings, "skill.authority_transfer", "vendored stack-update must keep authority_transfer=false")

    actual_blob_sha = git_blob_sha(STACK_UPDATE_SKILL_PATH.read_bytes())
    if source_blob_sha and source_blob_sha != actual_blob_sha:
        error(findings, "skill.content_drift", f"vendored stack-update blob is {actual_blob_sha}, provenance pins {source_blob_sha}")

    if not SKILLS_README_PATH.exists():
        error(findings, "skill.index_missing", ".agents/skills/README.md is missing")
    else:
        skills_readme = SKILLS_README_PATH.read_text(encoding="utf-8")
        for value in (source_commit, source_blob_sha, "The-Interdependency/skill-lib"):
            if value and value not in skills_readme:
                error(findings, "skill.index_drift", f".agents/skills/README.md does not carry provenance value {value!r}")


def check_epac_graduation(manifest: dict[str, Any], findings: list[str]) -> None:
    """Check the declared transition's local evidence and severed source path.

    This checks coherent historical evidence, not current public availability or
    scientific standing. The EPAC CI consumer independently checks public bytes.
    """
    epac = next((r for r in manifest.get("repositories", [])
                 if r.get("repository") == "The-Interdependency/epac"), {})
    receipt_path = ROOT / "integration/epac/authority-transition.json"
    has_transition = (
        epac.get("lifecycle") in {"released-and-reconsumed", "graduated"}
        or "release" in epac
        or receipt_path.exists()
        or epac.get("authority") == "independent implementation and public-contract authority for EPAC"
    )
    if not has_transition:
        return

    def require(condition: bool, message: str) -> None:
        if not condition:
            error(findings, "epac.graduation", message)

    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def committed_bytes(commit: str, path: str) -> bytes:
        if HEX40.fullmatch(commit) is None:
            raise ValueError("invalid historical source commit")
        result = subprocess.run(["git", "-C", str(ROOT), "show", commit + ":" + path],
                                check=False, capture_output=True)
        if result.returncode:
            raise ValueError(f"missing historical Git object {commit}:{path}; fetch full history before checking")
        return result.stdout

    try:
        require(epac.get("lifecycle") == "graduated", "completed transition requires graduated lifecycle")
        require(epac["authority"] == "independent implementation and public-contract authority for EPAC", "graduated authority projection differs")
        require(epac["transition_receipt"] == "integration/epac/authority-transition.json", "unexpected transition receipt path")
        require(epac["release"]["lock"] == "integration/epac/release-lock.json", "unexpected release lock path")
        lock_path = ROOT / "integration/epac/release-lock.json"
        current_lock = load_json(lock_path)
        receipt = load_json(receipt_path)
        require(receipt["schema"] == "the-interdependency.scoped-authority-transition" and receipt["status"] == "completed" and receipt["lifecycle_state"] == "graduated", "completed scoped transition required")
        require(receipt["to"]["repository"] == epac["repository"], "graduated repository differs")
        require(current_lock["schema"] == "stack.epac-public-release-lock" and current_lock["version"] == 1, "current release lock schema differs")
        require(current_lock["source_commit"] == epac["commit"] and HEX40.fullmatch(epac["commit"]) is not None, "current release source identity differs")
        require(current_lock["release_tag"] == epac["release"]["tag"], "current release tag differs")
        require(current_lock["phase"] == "graduated", "graduated consumer phase required")
        require(digest(lock_path) == epac["release"]["lock_sha256"], "current release lock digest differs")
        require(current_lock["upstream"] == epac["upstream"], "current release upstream differs from manifest")
        for upstream in (current_lock["upstream"], receipt["upstream"]):
            require(upstream["repository"] == "The-Interdependency/ucns" and HEX40.fullmatch(upstream["commit"]) is not None and upstream["authority_transfer"] is False, "UCNS provenance or non-transfer boundary differs")
        assets = current_lock["assets"]
        wheels = [name for name in assets if name.endswith(".whl")]
        sdists = [name for name in assets if name.endswith(".tar.gz")]
        require(len(wheels) == len(sdists) == 1 and set(assets) == set(wheels + sdists + ["release-manifest.json", "SHA256SUMS"]), "current release asset inventory differs")
        for name, asset in assets.items():
            require(Path(name).name == name and name not in {"", ".", ".."}, "release asset filename invalid")
            require(re.fullmatch(r"[0-9a-f]{64}", asset["sha256"]) is not None, "release asset digest invalid")
            require(asset["url"] == f'https://github.com/The-Interdependency/epac/releases/download/{current_lock["release_tag"]}/{name}', "current public asset URL differs")
        mirror = ROOT / "libs/epac"
        if "unpopulated" in epac["relation"]:
            require(not mirror.is_symlink() and (not mirror.exists() or (mirror.is_dir() and not any(mirror.iterdir()))), "unpopulated libs/epac contains files or a symlink")
        required_gates = {"public_api", "independent_tests", "clean_build_install", "license_distribution_rights", "release_ownership_authority", "provenance_preserved", "exact_candidate_forge_verification", "stable_release", "downstream_reconsumption", "forge_implementation_retired", "clean_retired_source_verification"}
        require(set(receipt["gates"]) == required_gates and set(receipt["gates"].values()) == {"pass"}, "complete passed graduation gates required")
        require(receipt["scope"] == {"implementation_authority_transfer": True, "public_contract_authority_transfer": True, "semantic_status_transfer": False, "theorem_status_transfer": False, "proof_status_transfer": False, "certification_status_transfer": False, "measurement_status_transfer": False, "empirical_status_transfer": False, "upstream_license_transfer": False, "freshness_authority_transfer": False}, "authority scope differs")
        history_root = ROOT / "research/epac"
        require(not history_root.is_symlink() and not any(path.is_symlink() for path in history_root.rglob("*")), "historical research path contains a symlink")
        require(not list(history_root.rglob("*.py")), "forge Python implementation has returned")
        original_evidence = {"public-release.json", "candidate-matrix.json", "reproducibility.json", "stack-candidate.json", "stack-reconsumed.json", "stack-graduated.json", "retirement-inventory.json"}
        expected_evidence = {"public-release.json", "candidate-matrix.json", "reproducibility.json", "stack-candidate.json", "stack-reconsumed.json", "stack-graduated.json", "retirement-inventory.json", "graduation-release-lock.json", "transition-before-manifest.json", "transition-after-manifest.json"}
        prefix = "integration/epac/evidence/"
        require(set(receipt["evidence"]) == {prefix + name for name in expected_evidence}, "complete evidence inventory required")
        original_receipt = json.loads(committed_bytes(receipt["recorded_transition_source_commit"], "integration/epac/authority-transition.json"))
        historical_fields = ("schema", "version", "status", "lifecycle_state", "from", "to", "gates", "scope", "upstream", "retirement_source_commit", "retirement_source_tree", "before_work_graph_sha256", "after_work_graph_sha256", "release_lock_sha256")
        require(all(receipt[key] == original_receipt[key] for key in historical_fields), "historical transition facts differ from original committed receipt")
        records = {}
        for name in sorted(expected_evidence):
            path = ROOT / prefix / name
            require(digest(path) == receipt["evidence"].get(prefix + name), f"evidence digest differs: {name}")
            if name in original_evidence:
                require(path.read_bytes() == committed_bytes(receipt["recorded_transition_source_commit"], prefix + name), f"historical evidence differs from original committed bytes: {name}")
            records[name] = load_json(path)
        # Graduation evidence is immutable history, not the current release pin.
        require(receipt["graduation_release_lock"] == prefix + "graduation-release-lock.json", "unexpected historical release lock path")
        lock = records["graduation-release-lock.json"]
        require(digest(ROOT / receipt["graduation_release_lock"]) == receipt["release_lock_sha256"], "historical release lock digest differs")
        require(lock["source_commit"] == receipt["to"]["source_commit"] and lock["release_tag"] == receipt["to"]["release_tag"] and lock["phase"] == "graduated", "historical release identity differs")
        require(set(receipt["transition_manifests"]) == {"before", "after"}, "both historical manifest identities required")
        snapshots = {}
        for phase in ("before", "after"):
            name = f"transition-{phase}-manifest.json"
            identity = receipt["transition_manifests"][phase]
            snapshot = records[name]
            require(identity["path"] == prefix + name and identity["source_repository"] == "The-Interdependency/stack" and identity["source_path"] == "stack-manifest.json", f"{phase} historical manifest location differs")
            require(HEX40.fullmatch(identity["source_commit"]) is not None and HEX40.fullmatch(identity["source_blob_sha"]) is not None, f"{phase} historical Git identity invalid")
            snapshot_bytes = (ROOT / prefix / name).read_bytes()
            require(git_blob_sha(snapshot_bytes) == identity["source_blob_sha"], f"{phase} historical manifest blob differs")
            require(snapshot_bytes == committed_bytes(identity["source_commit"], "stack-manifest.json"), f"{phase} snapshot differs from claimed immutable Git source")
            require(manifest_digest(snapshot) == snapshot["work_graph_sha256"] == receipt[f"{phase}_work_graph_sha256"], f"{phase} historical graph differs")
            snapshots[phase] = snapshot
        require(receipt["transition_manifests"]["before"]["source_commit"] == receipt["from"]["source_commit"], "starting manifest source differs from forge source")
        require(receipt["transition_manifests"]["after"]["source_commit"] == receipt["recorded_transition_source_commit"], "completed manifest source differs from recorded transition")
        historical_epac = next(r for r in snapshots["after"]["repositories"] if r["repository"] == epac["repository"])
        require(historical_epac["commit"] == lock["source_commit"] and historical_epac["release"]["tag"] == lock["release_tag"] and historical_epac["release"]["lock_sha256"] == receipt["release_lock_sha256"], "completed manifest release differs from historical lock")
        require(historical_epac["authority"] == receipt["to"]["authority"] == epac["authority"], "historical authority scope differs")
        require(receipt["upstream"] == historical_epac["upstream"], "historical receipt upstream differs from completed manifest")
        other_repositories = [[r for r in snapshots[phase]["repositories"] if r["repository"] != epac["repository"]] for phase in ("before", "after")]
        require(other_repositories[0] == other_repositories[1], "EPAC transition altered another canonical repository pin or authority")
        public = records["public-release.json"]
        require(public["status"] == "passed" and public["immutable"] is True and public["source_commit"] == lock["source_commit"], "immutable public release evidence differs")
        require({name: item["sha256"] for name, item in lock["assets"].items()} == public["public_assets_sha256"], "public assets differ from lock")
        matrix = records["candidate-matrix.json"]
        require(matrix["status"] == "passed" and matrix["source_commit"] == lock["source_commit"] and set(matrix["runtimes"]) == {"3.10", "3.11", "3.12"}, "candidate matrix identity differs")
        for runtime in matrix["runtimes"].values():
            require(set(runtime["runs"]) == {"wheel", "sdist"}, "both installed artifacts required")
            require(all(run["tests"] == 209 and run["skips"] == 0 for run in runtime["runs"].values()), "complete clean-install tests required")
            require(runtime["assets_sha256"] == public["public_assets_sha256"], "matrix candidate bytes differ from publication")
        reproducibility = records["reproducibility.json"]
        require(reproducibility["status"] == "passed" and reproducibility["source_commit"] == lock["source_commit"] and reproducibility["artifacts_sha256"] == public["public_assets_sha256"] and set(reproducibility["umasks"]) == {"022", "077"}, "historical reproducible candidate differs")
        wheel_hash = lock["assets"]["interdependency_epac-0.1.0-py3-none-any.whl"]["sha256"]
        historical_verifier = committed_bytes(receipt["retirement_source_commit"], "integration/epac/verify_release.py")
        declarations = [node.value for node in ast.parse(historical_verifier).body
                        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "EXPECTED_STANDINGS" for target in node.targets)]
        require(len(declarations) == 1, "historical verifier standings declaration missing or ambiguous")
        expected_standings = ast.literal_eval(declarations[0])
        require(len(expected_standings) == 14 and set(expected_standings.values()) == {"FALSIFIED"}, "historical verifier standing contract differs")
        for phase in ("candidate", "reconsumed", "graduated"):
            record = records[f"stack-{phase}.json"]
            require(record["status"] == "passed" and record["phase"] == phase and record["source_unchanged"] is True, f"invalid {phase} consumer evidence")
            commit = record["source_commit"]
            require(HEX40.fullmatch(commit) is not None, f"{phase} consumer source commit invalid")
            if HEX40.fullmatch(commit) is None:
                raise ValueError("invalid consumer source commit")
            tree_result = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--verify", commit + "^{tree}"], capture_output=True, check=False)
            require(tree_result.returncode == 0 and tree_result.stdout.decode().strip() == record["source_tree"], f"{phase} consumer tree differs from Git source")
            require(hashlib.sha256(committed_bytes(commit, "integration/epac/verify_release.py")).hexdigest() == record["verifier_sha256"], f"{phase} consumer verifier differs from Git source")
            require(record["artifact_sha256"] == wheel_hash and record["ucns_source_commit"] == receipt["upstream"]["commit"], f"{phase} consumer artifact/dependency differs")
            require(record["empirical_status_transfer"] is False and record["comparison_standings"] == expected_standings, f"{phase} scientific boundary differs")
        require(records["stack-graduated.json"]["source_commit"] == receipt["retirement_source_commit"] and records["stack-graduated.json"]["source_tree"] == receipt["retirement_source_tree"], "retirement verification source differs")
        inventory = records["retirement-inventory.json"]
        require(inventory["epac_commit"] == lock["source_commit"] and len(inventory["proposed_python_retirements"]) == 37, "retirement source/inventory differs")
        require(len(inventory["preserved_historical_files"]) == 28 and len({item["path"] for item in inventory["preserved_historical_files"]}) == 28, "complete 28-path historical inventory required")
        for item in inventory["preserved_historical_files"]:
            path = ROOT / item["path"]
            if item["path"] == "research/epac/README.md":
                path = ROOT / "research/epac/README.forge-history.md"
            require(digest(path) == item["sha256"], f"retained historical bytes differ: {path.relative_to(ROOT)}")
        require(records["stack-graduated.json"]["verifier_sha256"] == hashlib.sha256(historical_verifier).hexdigest(), "retirement consumer verifier differs from its Git source")
        base = load_json(ROOT / "research/epac/BASE.json")
        require(base["successor"] == {key: receipt["to"][key] for key in ("repository", "source_commit", "release_tag")}, "historical BASE successor differs from graduation receipt")
        require(base["source_path"] == receipt["from"]["source_path"] and base["authority_transfer"] is False and base["canon_path"] is None, "historical BASE boundary differs")
        require(base["source_repository"] == receipt["from"]["repository"] and base["source_commit"] == receipt["from"]["source_commit"] and base["standing"] == "historical-forge-evidence", "historical forge BASE differs")
    except (KeyError, TypeError, ValueError, OSError, StopIteration, IndexError, SyntaxError) as exc:
        error(findings, "epac.graduation", f"invalid or missing transition evidence: {exc}")


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
    research_participant_keys, research_source_identities = check_research_participants(manifest, human, findings)
    check_base_records(repositories, research_participant_keys, research_source_identities, readme, findings)
    check_english_gonol_regression(repositories, research_participant_keys, human, readme, findings)
    check_stack_update_skill_provenance(findings)
    check_epac_graduation(manifest, findings)

    if findings:
        for finding in findings:
            print(f"error: {finding}")
        print(f"stack consistency: fail ({len(findings)} error(s))")
        return 1

    print(f"stack consistency: pass ({len(repositories)} repositories, {len(research_participant_keys)} research participant identities)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
