"""Generate the frozen METAPAT/UCNS digital-metric vertical-slice receipt.

Usage guidance
--------------
Run only with clean checkouts at the commits pinned by ``WORK_GRAPH.json``::

    python3 research/digital-metrics/generate_receipt_cli.py \
      --metapat-root /path/to/metapat \
      --ucns-root /path/to/ucns \
      --edcm-root /path/to/edcm \
      --output /tmp/digital-metrics-receipt.json

The generator imports the current METAPAT application constructor and executes
the current UCNS exact native Möbius transition.  It produces integrity and
structural observations only.  It does not invoke EDCM or claim measurement,
theorem, semantic, or empirical validity. It does execute the pinned EDCM
decoder's missing-field rejection as a prerequisite guard.
"""

from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_digital_metric_receipt_generator
#   module_name: digital metric vertical-slice generator
#   module_kind: experiment
#   summary: binds current METAPAT affixiation semantics and exact UCNS native Mobius transitions into strict Stack-local integrity observations
#   owner: The-Interdependency/stack
#   public_surface: build_receipt,main
#   internal_surface: exact checkout verification, isolated producer loading, structural observation construction
#   auth_boundary: none
#   storage_boundary: writes one requested JSON receipt
#   network_boundary: none
#   user_data_boundary: public research fixtures only
#   admin_only: false
#   tests: research/digital-metrics/tests/test_metric_protocol.py
#   rollout: explicit command only; noncanonical Stack research
#   rollback: remove this workspace and its manifest projections
#   requires: stack_digital_metric_protocol,current METAPAT and UCNS producer checkouts,pinned fail-closed EDCM decoder prerequisite
#   since: 2026-09-20
#   unresolved: EDCM projection selection and calibration remain out of this structural slice
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: digital_metric_generator_requires_source_bound_entry
#   given: the current generator implementation is entered without a source digest binding
#   then: receipt generation rejects before resolving any producer
#   class: provenance
#
# id: digital_metric_generator_requires_exact_clean_producers
#   given: a producer root is not its Git top level, differs from the work-graph commit, or has tracked changes
#   then: receipt generation fails before importing producer code
#   class: provenance
#
# id: digital_metric_work_graph_requires_fixed_participants
#   given: the v0 work graph omits, duplicates, adds, or reorders a declared participant
#   then: generation rejects the graph before resolving any producer
#   class: provenance
#
# id: digital_metric_generator_requires_repository_work_graph
#   given: receipt generation is pointed at a copied, caller-edited, or projection-divergent work graph
#   then: generation requires the repository-owned WORK_GRAPH.json and exact agreement with the machine Stack projection before loading any producer
#   class: provenance
#
# id: digital_metric_generator_loads_committed_sources_only
#   given: an untracked shadow or altered working-tree dependency differs from the pinned METAPAT commit
#   then: the source finder executes only Python blobs read from the participant commit object
#   class: provenance
#
# id: digital_metric_generator_imports_verified_metapat
#   given: a different METAPAT package or module is already present in the Python import cache
#   then: generation loads the module from the verified checkout, confirms its origin, and restores the prior cache afterward
#   class: provenance
#
# id: digital_metric_generator_bypasses_cached_bytecode
#   given: timestamp-valid stale bytecode exists beside a verified METAPAT or UCNS source file
#   then: the producer loader compiles the verified source bytes directly and never executes the cached bytecode
#   class: provenance
#
# id: digital_metric_generator_ignores_git_replacements
#   given: a producer checkout defines a Git replacement object for the pinned commit
#   then: identity, tree, and blob reads resolve the original commit objects only
#   class: provenance
#
# id: digital_metric_metapat_binding_is_constraint_only
#   given: the affixiation-harmonics application is bound into a receipt
#   then: its exact identity and digest are retained while authority and measurement-status transfer remain false
#   class: boundary
#
# id: digital_metric_ucns_transition_uses_native_law
#   given: the exact pinned UCNS producer is available
#   then: the generator observes native one-turn and two-turn visible/complete-state equality directly from producer objects
#   class: evidence
#
# id: digital_metric_generator_requires_fail_closed_edcm_decoder
#   given: the work graph pins EDCM as the merged missing-metric decoder prerequisite
#   then: generation executes the committed decoder and rejects unless an omitted token_count raises ValueError before metric construction
#   class: correctness
# === END CONTRACTS ===

import argparse
from contextlib import contextmanager
from fractions import Fraction
import hashlib
import importlib
import importlib.abc
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from types import ModuleType
from typing import Any, Iterator, Mapping

_LOADED_GENERATOR_SHA256 = globals().get("__source_sha256__")


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


_METRIC_PROTOCOL = _load_source_module(
    "_stack_digital_metric_protocol_generator",
    Path(__file__).resolve().parent / "metric_protocol.py",
)
boolean_value = _METRIC_PROTOCOL.boolean_value
canonical_json = _METRIC_PROTOCOL.canonical_json
make_metric_definition = _METRIC_PROTOCOL.make_metric_definition
make_observation = _METRIC_PROTOCOL.make_observation
measure_retention = _METRIC_PROTOCOL.measure_retention
seal_receipt = _METRIC_PROTOCOL.seal_receipt
seal_structure = _METRIC_PROTOCOL.seal_structure
sha256_json = _METRIC_PROTOCOL.sha256_json
_LOADED_PROTOCOL_SHA256 = _METRIC_PROTOCOL.__source_sha256__


WORK_GRAPH_SCHEMA = "the-interdependency.digital-metric-work-graph"
WORK_GRAPH_VERSION = "0.1.0"
EXPECTED_PARTICIPANT_REPOSITORIES = (
    "The-Interdependency/stack",
    "The-Interdependency/skill-lib",
    "The-Interdependency/metapat",
    "The-Interdependency/ucns",
    "The-Interdependency/edcm",
)


class ProducerIdentityError(ValueError):
    """Raised before producer import when source identity is not exact."""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _execution_source_digests(
    *,
    verifier_path: Path,
    verifier_sha256: str | None = None,
) -> dict[str, str]:
    if not isinstance(_LOADED_GENERATOR_SHA256, str) or re.fullmatch(
        r"[0-9a-f]{64}", _LOADED_GENERATOR_SHA256
    ) is None:
        raise ProducerIdentityError(
            "generator API must be source-loaded; use generate_receipt_cli.py"
        )
    if verifier_sha256 is None:
        verifier_sha256 = _sha256_file(verifier_path)
    elif re.fullmatch(r"[0-9a-f]{64}", verifier_sha256) is None:
        raise ProducerIdentityError("executing verifier digest must be a lowercase SHA-256")
    return {
        "generator": _LOADED_GENERATOR_SHA256,
        "protocol": _LOADED_PROTOCOL_SHA256,
        "verifier": verifier_sha256,
    }


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "--no-replace-objects", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ProducerIdentityError(f"git {' '.join(args)} failed for {root}: {detail}")
    return result.stdout.strip()


def _participant(work_graph: Mapping[str, Any], repository: str) -> dict[str, Any]:
    matches = [item for item in work_graph["participants"] if item.get("repository") == repository]
    if len(matches) != 1:
        raise ProducerIdentityError(f"work graph must contain exactly one {repository} participant")
    return matches[0]


def load_work_graph(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    expected = {"schema", "version", "participants", "boundaries", "work_graph_sha256"}
    if not isinstance(value, dict) or set(value) != expected:
        raise ProducerIdentityError("WORK_GRAPH.json has missing or unknown fields")
    if (value["schema"], value["version"]) != (WORK_GRAPH_SCHEMA, WORK_GRAPH_VERSION):
        raise ProducerIdentityError("unsupported digital metric work-graph schema/version")
    if not isinstance(value["participants"], list) or not value["participants"]:
        raise ProducerIdentityError("work graph participants must be a non-empty array")
    for item in value["participants"]:
        if not isinstance(item, dict) or set(item) != {"repository", "commit", "authority", "relation"}:
            raise ProducerIdentityError("work graph participant has missing or unknown fields")
        if not all(isinstance(item[field], str) and item[field] for field in item):
            raise ProducerIdentityError("work graph participant fields must be non-empty strings")
        if re.fullmatch(r"[0-9a-f]{40}", item["commit"]) is None:
            raise ProducerIdentityError("work graph participant commit must be exact")
    repositories = tuple(item["repository"] for item in value["participants"])
    if repositories != EXPECTED_PARTICIPANT_REPOSITORIES:
        raise ProducerIdentityError(
            "work graph must contain the exact ordered v0 participant set"
        )
    boundaries = value["boundaries"]
    if not isinstance(boundaries, dict) or set(boundaries) != {
        "authority_transfer", "proof_status_transfer", "measurement_status_transfer",
        "empirical_status_transfer", "semantic_mapping", "hmmm",
    }:
        raise ProducerIdentityError("work graph boundaries have missing or unknown fields")
    for field in (
        "authority_transfer", "proof_status_transfer", "measurement_status_transfer", "empirical_status_transfer",
    ):
        if boundaries[field] is not False:
            raise ProducerIdentityError(f"work graph {field} must be false")
    if boundaries["semantic_mapping"] != "external-provenance":
        raise ProducerIdentityError("work graph semantic_mapping must remain external-provenance")
    if not isinstance(boundaries["hmmm"], list) or not all(isinstance(item, str) and item for item in boundaries["hmmm"]):
        raise ProducerIdentityError("work graph hmmm must be an array of non-empty strings")
    payload = {"participants": value["participants"], "boundaries": boundaries}
    if value["work_graph_sha256"] != sha256_json(payload):
        raise ProducerIdentityError("work graph digest mismatch")
    return value


def _require_repository_work_graph(path: Path, workspace: Path) -> Path:
    expected = (workspace / "WORK_GRAPH.json").resolve()
    resolved = path.resolve()
    if resolved != expected:
        raise ProducerIdentityError(
            f"work graph must be the repository-owned path: {expected}"
        )
    return resolved


def _verify_stack_participant(
    work_graph: Mapping[str, Any], stack_root: Path
) -> None:
    participant = _participant(work_graph, "The-Interdependency/stack")
    stack_root = stack_root.resolve()
    git_root = Path(_git(stack_root, "rev-parse", "--show-toplevel")).resolve()
    if git_root != stack_root:
        raise ProducerIdentityError(
            f"Stack root is not the Git top level: {stack_root}"
        )
    commit = participant["commit"]
    resolved = _git(stack_root, "rev-parse", "--verify", f"{commit}^{{commit}}")
    if resolved != commit:
        raise ProducerIdentityError(
            f"Stack participant commit does not resolve exactly: {commit}"
        )
    ancestry = subprocess.run(
        [
            "git",
            "--no-replace-objects",
            "-C",
            str(stack_root),
            "merge-base",
            "--is-ancestor",
            commit,
            "HEAD",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if ancestry.returncode != 0:
        raise ProducerIdentityError(
            f"Stack participant commit is not an ancestor of HEAD: {commit}"
        )


def _validate_repository_work_graph_projection(
    work_graph: Mapping[str, Any], workspace: Path
) -> str:
    manifest_path = workspace.parents[1] / "stack-manifest.json"
    manifest_source = manifest_path.read_bytes()
    try:
        manifest = json.loads(manifest_source.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProducerIdentityError(f"invalid Stack manifest: {exc}") from exc
    try:
        manifest_payload = {
            key: manifest[key]
            for key in ("repositories", "research_participants", "boundaries")
        }
    except (KeyError, TypeError) as exc:
        raise ProducerIdentityError(f"invalid Stack manifest projection: {exc}") from exc
    if manifest.get("work_graph_sha256") != sha256_json(manifest_payload):
        raise ProducerIdentityError("Stack manifest digest mismatch")

    projected = [
        item
        for item in manifest["research_participants"]
        if item.get("workspace") == "research/digital-metrics/"
    ]
    participants = work_graph["participants"]
    if len(projected) != len(participants):
        raise ProducerIdentityError(
            "digital-metrics Stack projection participant count differs"
        )
    for graph_entry, manifest_entry in zip(participants, projected):
        repository = graph_entry["repository"]
        expected_id = (
            "digital-metrics"
            if repository == "The-Interdependency/stack"
            else repository.rsplit("/", 1)[-1]
        )
        if manifest_entry.get("participant_id") != expected_id:
            raise ProducerIdentityError(
                f"digital-metrics Stack projection participant_id differs for {repository}"
            )
        for field in ("repository", "commit", "authority", "relation"):
            if manifest_entry.get(field) != graph_entry.get(field):
                raise ProducerIdentityError(
                    f"digital-metrics Stack projection {field} differs for {repository}"
                )
        if manifest_entry.get("canonical_release") is not False:
            raise ProducerIdentityError(
                f"digital-metrics Stack projection canonical_release differs for {repository}"
            )
        if manifest_entry.get("authority_transfer") is not False:
            raise ProducerIdentityError(
                f"digital-metrics Stack projection authority_transfer differs for {repository}"
            )
    if not projected or projected[0].get("boundaries") != work_graph["boundaries"]:
        raise ProducerIdentityError("digital-metrics Stack projection boundaries differ")

    graph_skill = _participant(work_graph, "The-Interdependency/skill-lib")
    manifest_skills = [
        item
        for item in manifest["repositories"]
        if item.get("repository") == "The-Interdependency/skill-lib"
    ]
    if (
        len(manifest_skills) != 1
        or manifest_skills[0].get("commit") != graph_skill["commit"]
    ):
        raise ProducerIdentityError(
            "digital-metrics Stack projection skill-lib commit differs"
        )
    _verify_stack_participant(work_graph, workspace.parents[1])
    return hashlib.sha256(manifest_source).hexdigest()


def _verify_stack_base(
    work_graph: Mapping[str, Any],
    workspace: Path,
    base_path: Path | None = None,
) -> str:
    """Bind the research BASE record to the work graph's Stack participant."""
    source_path = base_path or workspace / "BASE.json"
    try:
        source = source_path.read_bytes()
        base = json.loads(source.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProducerIdentityError(f"invalid digital-metrics BASE.json: {exc}") from exc
    if not isinstance(base, dict):
        raise ProducerIdentityError("digital-metrics BASE.json must contain an object")
    stack = _participant(work_graph, "The-Interdependency/stack")
    expected = {
        "project": "digital-metrics",
        "source_repository": "The-Interdependency/stack",
        "source_commit": stack["commit"],
        "standing": "stack-local-research",
        "canon_path": None,
    }
    for field, expected_value in expected.items():
        if base.get(field) != expected_value:
            raise ProducerIdentityError(
                f"digital-metrics BASE.json {field} differs from work graph: "
                f"expected {expected_value!r}, got {base.get(field)!r}"
            )
    return hashlib.sha256(source).hexdigest()


def verify_checkout(root: Path, participant: Mapping[str, Any], required_paths: tuple[str, ...]) -> None:
    root = root.resolve()
    git_root = Path(_git(root, "rev-parse", "--show-toplevel")).resolve()
    if git_root != root:
        raise ProducerIdentityError(
            f"{participant['repository']} producer root is not the Git top level: {root}"
        )
    if _git(root, "rev-parse", "HEAD") != participant["commit"]:
        raise ProducerIdentityError(
            f"{participant['repository']} checkout is not at {participant['commit']}"
        )
    changed = _git(root, "status", "--porcelain", "--untracked-files=no")
    if changed:
        raise ProducerIdentityError(
            f"{participant['repository']} producer checkout has tracked changes"
        )
    for relative in required_paths:
        path = root / relative
        if not path.is_file():
            raise ProducerIdentityError(f"missing required producer file: {path}")
        committed = subprocess.run(
            [
                "git", "--no-replace-objects", "-C", str(root),
                "show", f"{participant['commit']}:{relative}",
            ],
            check=False,
            capture_output=True,
        )
        if committed.returncode or committed.stdout != path.read_bytes():
            raise ProducerIdentityError(f"producer file differs from committed bytes: {relative}")


def _git_blob(root: Path, commit: str, relative: str) -> bytes:
    result = subprocess.run(
        [
            "git", "--no-replace-objects", "-C", str(root.resolve()),
            "show", f"{commit}:{relative}",
        ],
        check=False,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ProducerIdentityError(f"cannot read committed producer blob {relative}: {detail}")
    return result.stdout


def _committed_python_sources(
    root: Path, commit: str, relative_root: str
) -> dict[Path, bytes]:
    root = root.resolve()
    names = _git(
        root,
        "ls-tree",
        "-r",
        "--name-only",
        commit,
        "--",
        relative_root,
    ).splitlines()
    return {
        root / name: _git_blob(root, commit, name)
        for name in names
        if name.endswith(".py")
    }


class _SourceBytesLoader(importlib.abc.Loader):
    def __init__(self, source_path: Path, source: bytes, *, is_package: bool) -> None:
        self.source_path = source_path
        self.source = source
        self.is_package = is_package

    def exec_module(self, module: ModuleType) -> None:
        module.__file__ = str(self.source_path)
        module.__cached__ = None
        if self.is_package:
            module.__path__ = [str(self.source_path.parent)]  # type: ignore[attr-defined]
        code = compile(self.source, str(self.source_path), "exec", dont_inherit=True)
        exec(code, module.__dict__)


class _SourceTreeFinder(importlib.abc.MetaPathFinder):
    def __init__(
        self,
        package: str,
        package_root: Path,
        allowed_sources: Mapping[Path, bytes],
    ) -> None:
        self.package = package
        self.package_root = package_root.resolve()
        self.allowed_sources = allowed_sources

    def find_spec(
        self,
        fullname: str,
        path: object = None,
        target: ModuleType | None = None,
    ) -> object:
        prefix = f"{self.package}."
        if fullname == self.package:
            relative_parts: tuple[str, ...] = ()
        elif fullname.startswith(prefix):
            relative_parts = tuple(fullname[len(prefix):].split("."))
        else:
            return None

        base = self.package_root.joinpath(*relative_parts)
        package_source = base / "__init__.py"
        module_source = base.with_suffix(".py")
        if package_source in self.allowed_sources:
            source_path = package_source
            is_package = True
        elif relative_parts and module_source in self.allowed_sources:
            source_path = module_source
            is_package = False
        else:
            raise ModuleNotFoundError(
                f"pinned Git tree has no committed module {fullname!r}"
            )
        loader = _SourceBytesLoader(
            source_path,
            self.allowed_sources[source_path],
            is_package=is_package,
        )
        return importlib.util.spec_from_loader(
            fullname,
            loader,
            origin=str(source_path),
            is_package=is_package,
        )


@contextmanager
def _isolated_source_package_import(
    package: str,
    package_root: Path,
    allowed_sources: Mapping[Path, bytes],
) -> Iterator[None]:
    prefix = f"{package}."
    saved = {
        name: module
        for name, module in tuple(sys.modules.items())
        if name == package or name.startswith(prefix)
    }
    for name in saved:
        sys.modules.pop(name, None)
    finder = _SourceTreeFinder(package, package_root, allowed_sources)
    sys.meta_path.insert(0, finder)
    try:
        importlib.invalidate_caches()
        yield
    finally:
        if finder in sys.meta_path:
            sys.meta_path.remove(finder)
        for name in tuple(sys.modules):
            if name == package or name.startswith(prefix):
                sys.modules.pop(name, None)
        sys.modules.update(saved)
        importlib.invalidate_caches()


def _load_metapat_application(root: Path, commit: str) -> tuple[Any, str]:
    expected_module_path = (root / "src/metapat/affixiation_harmonics.py").resolve()
    allowed_sources = _committed_python_sources(root, commit, "src/metapat")
    with _isolated_source_package_import(
        "metapat",
        root / "src/metapat",
        allowed_sources,
    ):
        module = importlib.import_module("metapat.affixiation_harmonics")
        actual_module_path = Path(module.__file__).resolve()
        if actual_module_path != expected_module_path:
            raise ProducerIdentityError(
                f"METAPAT module origin differs from verified checkout: {actual_module_path}"
            )
        application = module.affixiation_harmonics_application_module()
    if application.application_id != "metapat.application.affixiation_harmonics":
        raise ProducerIdentityError("unexpected METAPAT application identity")
    if application.application_version != "affixiation-harmonics-application-v4":
        raise ProducerIdentityError("unexpected METAPAT affixiation application version")
    if application.measurement_validity_claim is not False or application.ucns_theorem_status_transfer is not False:
        raise ProducerIdentityError("METAPAT application improperly transfers downstream status")
    return application, _sha256_bytes(
        _git_blob(root, commit, "docs/applications/affixiation-harmonics.md")
    )


def _load_ucns_native_module(root: Path, commit: str) -> tuple[Any, str]:
    source_path = (root / "src/ucns/direct_mobius.py").resolve()
    source = _git_blob(root, commit, "src/ucns/direct_mobius.py")
    module_name = "_stack_metric_ucns_direct_mobius"
    module = ModuleType(module_name)
    module.__file__ = str(source_path)
    module.__cached__ = None
    module.__package__ = ""
    sys.modules[module_name] = module
    try:
        code = compile(source, str(source_path), "exec", dont_inherit=True)
        exec(code, module.__dict__)
    finally:
        sys.modules.pop(module_name, None)
    return module, _sha256_bytes(source)


def _verify_edcm_decoder_guard(root: Path, commit: str) -> str:
    """Execute the pinned fail-closed decoder witness without measuring data."""
    relative = "edcm/measurement/compress.py"
    source_path = (root / relative).resolve()
    source = _git_blob(root, commit, relative)
    allowed_sources = _committed_python_sources(root, commit, "edcm")
    with _isolated_source_package_import("edcm", root / "edcm", allowed_sources):
        module = importlib.import_module("edcm.measurement.compress")
        actual_module_path = Path(module.__file__).resolve()
        if actual_module_path != source_path:
            raise ProducerIdentityError(
                f"EDCM decoder origin differs from verified checkout: {actual_module_path}"
            )
        slots = tuple(module.RoundMetrics.__slots__)
        if "token_count" not in slots:
            raise ProducerIdentityError(
                "EDCM RoundMetrics does not declare the token_count prerequisite field"
            )
        complete = {slot: 0 for slot in slots}
        try:
            decoded = module._dict_to_metrics(complete, round_index=0)
        except Exception as exc:
            raise ProducerIdentityError(
                f"EDCM decoder rejected a complete metric prerequisite fixture: {exc}"
            ) from exc
        if decoded.token_count != 0:
            raise ProducerIdentityError("EDCM complete metric prerequisite fixture changed")
        del complete["token_count"]
        try:
            module._dict_to_metrics(complete, round_index=0)
        except ValueError as exc:
            if "token_count" not in str(exc):
                raise ProducerIdentityError(
                    "EDCM missing-metric rejection did not name token_count"
                ) from exc
        except Exception as exc:
            raise ProducerIdentityError(
                f"EDCM incomplete metric record raised the wrong exception: {exc}"
            ) from exc
        else:
            raise ProducerIdentityError(
                "EDCM decoder accepted an incomplete metric record"
            )
    return _sha256_bytes(source)


def _state_record(state: Any, law_id: str, law_version: str) -> dict[str, Any]:
    phase = state.phase_turns
    return {
        "law_id": law_id,
        "law_version": law_version,
        "phase_turns": {"numerator": phase.numerator, "denominator": phase.denominator},
        "frame": state.frame.value,
    }


def _ucns_definition(
    *, metric_id: str, construct: str, interpretation: str, generator_sha256: str,
) -> dict[str, Any]:
    return make_metric_definition(
        metric_id=metric_id,
        metric_version="0.1.0",
        owner_repository="The-Interdependency/stack",
        construct=construct,
        subject_kind="exact-ucns-native-mobius-transition",
        value_kind="boolean",
        unit="truth-value",
        minimum=None,
        maximum=None,
        computation_id="stack.digital-metrics.ucns-native-mobius-v0",
        computation_sha256=generator_sha256,
        interpretation=interpretation,
        nonclaims=(
            "Records an exact result from the pinned UCNS producer; it does not transfer theorem status to Stack.",
            "Does not establish EDCM measurement validity, METAPAT validity, or external empirical truth.",
        ),
        validation_status="candidate",
    )


def build_receipt(
    *,
    metapat_root: Path,
    ucns_root: Path,
    edcm_root: Path,
    work_graph_path: Path,
    verifier_path: Path | None = None,
    verifier_sha256: str | None = None,
) -> dict[str, Any]:
    workspace = Path(__file__).resolve().parent
    source_digests = _execution_source_digests(
        verifier_path=(verifier_path or workspace / "verify_receipt.py").resolve(),
        verifier_sha256=verifier_sha256,
    )
    work_graph_path = _require_repository_work_graph(work_graph_path, workspace)
    work_graph = load_work_graph(work_graph_path)
    stack_manifest_sha256 = _validate_repository_work_graph_projection(
        work_graph, workspace
    )
    stack_base_sha256 = _verify_stack_base(work_graph, workspace)
    metapat_participant = _participant(work_graph, "The-Interdependency/metapat")
    ucns_participant = _participant(work_graph, "The-Interdependency/ucns")
    edcm_participant = _participant(work_graph, "The-Interdependency/edcm")

    verify_checkout(
        metapat_root,
        metapat_participant,
        (
            "src/metapat/affixiation_harmonics.py",
            "src/metapat/application.py",
            "src/metapat/catalog.py",
            "docs/applications/affixiation-harmonics.md",
        ),
    )
    verify_checkout(
        ucns_root,
        ucns_participant,
        ("src/ucns/direct_mobius.py",),
    )
    verify_checkout(
        edcm_root,
        edcm_participant,
        (
            "edcm/measurement/compress.py",
            "edcm/measurement/metrics/compute.py",
            "edcm/measurement/metrics/stats.py",
            "edcm/measurement/parser/turns_rounds.py",
        ),
    )

    application, metapat_source_sha256 = _load_metapat_application(
        metapat_root, metapat_participant["commit"]
    )
    ucns, ucns_source_sha256 = _load_ucns_native_module(
        ucns_root, ucns_participant["commit"]
    )
    edcm_decoder_sha256 = _verify_edcm_decoder_guard(
        edcm_root, edcm_participant["commit"]
    )
    origin = ucns.native_mobius_state()
    one_turn = origin.advance(1)
    two_turns = origin.advance(2)
    inverse = origin.advance(Fraction(7, 3)).advance(Fraction(-7, 3))
    state_bundle = {
        "origin": _state_record(origin, ucns.NATIVE_MOBIUS_LAW_ID, ucns.NATIVE_MOBIUS_LAW_VERSION),
        "one_turn": _state_record(one_turn, ucns.NATIVE_MOBIUS_LAW_ID, ucns.NATIVE_MOBIUS_LAW_VERSION),
        "two_turns": _state_record(two_turns, ucns.NATIVE_MOBIUS_LAW_ID, ucns.NATIVE_MOBIUS_LAW_VERSION),
        "inverse_round_trip": _state_record(inverse, ucns.NATIVE_MOBIUS_LAW_ID, ucns.NATIVE_MOBIUS_LAW_VERSION),
    }
    state_bundle_sha256 = sha256_json(state_bundle)
    generator_sha256 = source_digests["generator"]
    protocol_sha256 = source_digests["protocol"]
    verifier_sha256 = source_digests["verifier"]
    work_graph_sha256 = work_graph["work_graph_sha256"]

    ucns_provenance = {
        "work_graph_sha256": work_graph_sha256,
        "source_repository": ucns_participant["repository"],
        "source_revision": {"kind": "git-commit", "value": ucns_participant["commit"]},
        "source_artifact_sha256": ucns_source_sha256,
        "generator_id": "stack.digital-metrics.ucns-native-mobius-v0",
        "generator_sha256": generator_sha256,
    }
    definitions = [
        _ucns_definition(
            metric_id="stack.observation.ucns.visible_return_after_one_turn",
            construct="Whether one visible turn preserves the UCNS visible key.",
            interpretation="True records equality of the exact producer's visible keys after one turn.",
            generator_sha256=generator_sha256,
        ),
        _ucns_definition(
            metric_id="stack.observation.ucns.complete_return_after_one_turn",
            construct="Whether one visible turn preserves the UCNS complete framed key.",
            interpretation="False distinguishes visible return from complete local-state return.",
            generator_sha256=generator_sha256,
        ),
        _ucns_definition(
            metric_id="stack.observation.ucns.complete_return_after_two_turns",
            construct="Whether two visible turns restore the UCNS complete framed state.",
            interpretation="True records exact equality of the producer's complete states after two turns.",
            generator_sha256=generator_sha256,
        ),
        _ucns_definition(
            metric_id="stack.observation.ucns.exact_inverse_round_trip",
            construct="Whether exact rational displacement followed by its negation restores the complete UCNS state.",
            interpretation="True records exact inversion for the frozen 7/3-turn witness.",
            generator_sha256=generator_sha256,
        ),
    ]
    booleans = (
        one_turn.visible_key == origin.visible_key,
        one_turn.complete_key == origin.complete_key,
        two_turns.complete_key == origin.complete_key,
        inverse.complete_key == origin.complete_key,
    )
    observations = [
        make_observation(
            definition=definition,
            subject_id="ucns.native-mobius.origin-transition-bundle",
            subject_sha256=state_bundle_sha256,
            sequence_index=index,
            status="observed",
            value=boolean_value(result),
            reason=None,
            uncertainty_kind="exact",
            provenance=ucns_provenance,
        )
        for index, (definition, result) in enumerate(zip(definitions, booleans, strict=True))
    ]

    participants = [
        {"identity": "ucns.native-mobius.phase_turns", "provenance_sha256": ucns_source_sha256},
        {"identity": "ucns.native-mobius.local_frame", "provenance_sha256": ucns_source_sha256},
    ]
    relation = {
        "identity": "ucns.native-mobius.complete-key",
        "kind": "ordered-state-key",
        "ordered_participants": ["ucns.native-mobius.phase_turns", "ucns.native-mobius.local_frame"],
        "multiplicity": 1,
    }
    before = seal_structure(
        structure_id="ucns.native-mobius.origin",
        scale="native-mobius-complete-state",
        participants=participants,
        relations=[relation],
    )
    after = seal_structure(
        structure_id="ucns.native-mobius.one-turn",
        scale="native-mobius-complete-state",
        participants=participants,
        relations=[relation],
    )
    retention_provenance = {
        "work_graph_sha256": work_graph_sha256,
        "source_repository": "The-Interdependency/stack",
        "source_revision": {"kind": "candidate-content", "value": protocol_sha256},
        "source_artifact_sha256": protocol_sha256,
        "generator_id": "stack.digital-metrics.retention-v0",
        "generator_sha256": protocol_sha256,
    }
    retention_defs, retention_obs = measure_retention(
        before,
        after,
        provenance=retention_provenance,
        computation_sha256=protocol_sha256,
    )
    definitions.extend(retention_defs)
    observations.extend(retention_obs)

    application_record = application.to_dict()
    bindings = [
        {
            "kind": "semantic-constraint",
            "identity": application.application_id,
            "version": application.application_version,
            "repository": metapat_participant["repository"],
            "commit": metapat_participant["commit"],
            "artifact_sha256": metapat_source_sha256,
            "record_digest": application.application_digest,
            "authority_transfer": False,
            "measurement_status_transfer": False,
        },
        {
            "kind": "geometric-producer",
            "identity": ucns.NATIVE_MOBIUS_LAW_ID,
            "version": ucns.NATIVE_MOBIUS_LAW_VERSION,
            "repository": ucns_participant["repository"],
            "commit": ucns_participant["commit"],
            "artifact_sha256": ucns_source_sha256,
            "record_digest": sha256_json(
                {
                    "law_id": ucns.NATIVE_MOBIUS_LAW_ID,
                    "law_version": ucns.NATIVE_MOBIUS_LAW_VERSION,
                    "source_sha256": ucns_source_sha256,
                }
            ),
            "authority_transfer": False,
            "measurement_status_transfer": False,
        },
    ]
    inputs = [
        {"identity": "digital-metric-work-graph", "sha256": work_graph_sha256},
        {"identity": "stack-manifest-source", "sha256": stack_manifest_sha256},
        {"identity": "digital-metrics-base-source", "sha256": stack_base_sha256},
        {"identity": "metapat-affixiation-application", "sha256": application.application_digest},
        {"identity": "metapat-affixiation-application-record", "sha256": sha256_json(application_record)},
        {"identity": "ucns-native-mobius-source", "sha256": ucns_source_sha256},
        {"identity": "ucns-native-mobius-state-bundle", "sha256": state_bundle_sha256},
        {"identity": "edcm-fail-closed-decoder-source", "sha256": edcm_decoder_sha256},
        {"identity": "stack-digital-metric-protocol", "sha256": protocol_sha256},
        {"identity": "stack-digital-metric-generator", "sha256": generator_sha256},
    ]
    return seal_receipt(
        work_graph_sha256=work_graph_sha256,
        definitions=definitions,
        observations=observations,
        bindings=bindings,
        inputs=inputs,
        verifier_id="stack.digital-metrics.verify-replay-v0",
        verifier_sha256=verifier_sha256,
        hmmm=(
            "hmmm: EDCM measurement projection and empirical calibration are not selected by this structural receipt.",
            "hmmm: Producer identities are content-bound but not cryptographically authenticated signatures.",
            "hmmm: Independent implementation replay remains required before promotion beyond test-backed Stack research.",
        ),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metapat-root", type=Path, required=True)
    parser.add_argument("--ucns-root", type=Path, required=True)
    parser.add_argument("--edcm-root", type=Path, required=True)
    parser.add_argument(
        "--work-graph",
        type=Path,
        default=Path(__file__).resolve().parent / "WORK_GRAPH.json",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    receipt = build_receipt(
        metapat_root=args.metapat_root,
        ucns_root=args.ucns_root,
        edcm_root=args.edcm_root,
        work_graph_path=args.work_graph,
    )
    args.output.write_text(canonical_json(receipt) + "\n", encoding="utf-8")
    print(f"wrote {args.output} ({receipt['receipt_sha256']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(
        "run generate_receipt_cli.py so generator execution is source-bound"
    )
