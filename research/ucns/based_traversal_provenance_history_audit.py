"""Audit local UCNS provenance for a geometry-selected based traversal.

The predecessor audit proved that current geometry does not select a based
return word.  This audit searches the reachable history of the authoritative
UCNS repository and the exact A0 source-provenance repository for the five
missing certificate fields.  Candidate artifacts are retained, but caller
order, source order, API defaults, partial source-bound seams, and superseded
mixed-domain wrappers never qualify as geometric selectors.
"""

# === MODULE_BUILD ===
# id: ucns_based_traversal_provenance_history_audit
#   module_name: based_traversal_provenance_history_audit
#   module_kind: experiment
#   summary: searches pinned UCNS and exact A0 source provenance for the five fields required to select a based recursive traversal and freezes the no-source stop condition
#   owner: The Interdependency
#   public_surface: ProvenanceAuditError, RepositorySnapshot, EvidenceArtifact, CertificateFieldFinding, ProvenanceHistoryAudit, repository_snapshots, evidence_artifacts, excluded_candidate_clusters, certificate_field_findings, audit, receipt_payload, receipt_bytes, receipt_digest, formatted_receipt_bytes, write_frozen_receipt
#   internal_surface: _stack_root, _source_root, _repository_path, _git_bytes, _git_text, _git_lines, _is_ancestor, _line_digest, _history_matches, _repository_snapshot, _verify_artifact, _source_file_digests, _previous_audit_receipt, _producer_code_reference, main
#   auth_boundary: none; committed objects are read from local clones of The-Interdependency/ucns and The-Interdependency/a0-betatest
#   storage_boundary: read-only except explicit generation of the fixed stack-local receipt path
#   network_boundary: none; no fetch or web search
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_based_traversal_provenance_history_audit.py
#   rollout: stack-local provenance obstruction research only; no UCNS canon, PCEA, traversal, arithmetic, or successor promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_geometry_selected_based_traversal_audit, gonol-build construction discipline
#   since: 2026-09-03
#   unresolved: origin-to-groupoid attachment; geometry-selected tangent or chirality; rotation system; marked outgoing dart; recursive complete-return closure rule
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: traversal_provenance_audit_binds_search_universe
#   given: the provenance audit runs against the local UCNS and A0 repositories
#   then: repository remotes, anchor commits and trees, all-ref identities, unique tips, reachable commit counts, search expressions, and candidate-set digests are frozen
#   class: evidence
#   since: 2026-09-03
#
# id: traversal_provenance_audit_binds_candidate_artifacts
#   given: a historically promising geometry, traversal, initiation, or source artifact is cited
#   then: its repository, commit, path, blob identity, content digest, authority standing, observed capability, and disqualifier replay exactly
#   class: evidence
#   since: 2026-09-03
#
# id: traversal_provenance_audit_requires_geometric_selection
#   given: an artifact exposes an origin, two directions, a local return, a marked source seam, or an ordered codec
#   then: it supplies no certificate field unless it geometrically attaches and selects that field for the recursive relation groupoid
#   class: safety
#   since: 2026-09-03
#
# id: traversal_provenance_audit_freezes_five_unresolved_fields
#   given: all audited current, historical, and exact-source candidates are classified
#   then: origin attachment, directed tangent or chirality, rotation system, marked outgoing dart, and closure rule each remain unresolved with no qualifying source
#   class: doctrine
#   since: 2026-09-03
#
# id: traversal_provenance_audit_stops_constructor
#   given: any required certificate field has no qualifying authoritative source
#   then: status is STOP_NO_GEOMETRY_SELECTED_BASED_TRAVERSAL and traversal word, monodromy, arithmetic readout, successor, and fourth gonol remain null
#   class: safety
#   since: 2026-09-03
#
# id: traversal_provenance_audit_classifies_pcea_control
#   given: no independent UCNS constructor has run
#   then: the PCEA interpolation control 164513086777 is UNRESOLVED, with neither SURVIVED nor FALSIFIED assigned
#   class: doctrine
#   since: 2026-09-03
#
# id: traversal_provenance_audit_receipt_replays
#   given: the audited repositories, source files, and predecessor receipt are unchanged
#   then: canonical payload bytes, payload digest, and formatted frozen receipt replay byte-identically
#   class: evidence
#   since: 2026-09-03
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


SCHEMA_ID = "the-interdependency.stack-research.ucns.based-traversal-provenance-history-audit"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-committed-history-provenance-obstruction-audit"
SELECTION_EFFECT = "none"

HISTORY_STATUS = "NO_AUTHORITATIVE_CERTIFICATE_SOURCE_FOUND_IN_AUDITED_PROVENANCE"
CONSTRUCTOR_STATUS = "STOP_NO_GEOMETRY_SELECTED_BASED_TRAVERSAL"
FIELD_STATUS = "UNRESOLVED_NO_QUALIFYING_GEOMETRIC_SOURCE"
PCEA_CONTROL_PREDICTION = 164_513_086_777
PCEA_CONTROL_STATUS = "UNRESOLVED"

UCNS_PINNED_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"
UCNS_PINNED_TREE = "06c2fe6cf2e148d610808c6f00f4a26e85f43d62"
A0_SOURCE_COMMIT = "7af8debf6ef3905f01baff02b43d8c3bee16ccbc"
A0_SOURCE_TREE = "fd53c96ddb57dbabce9386593232c3961c49fc6f"

REPOSITORY_KEYS = ("ucns", "a0-betatest")
EXPECTED_REMOTES = {
    "ucns": "https://github.com/The-Interdependency/ucns.git",
    "a0-betatest": "https://github.com/The-Interdependency/a0-betatest.git",
}
ANCHORS = {
    "ucns": (UCNS_PINNED_COMMIT, UCNS_PINNED_TREE),
    "a0-betatest": (A0_SOURCE_COMMIT, A0_SOURCE_TREE),
}

CERTIFICATE_FIELDS = (
    "origin_attachment",
    "directed_tangent_or_chirality",
    "rotation_system",
    "marked_outgoing_dart",
    "closure_rule",
)

EXACT_CERTIFICATE_TERMS = (
    "rotation system",
    "outgoing dart",
    "marked outgoing",
    "basepoint attachment",
    "origin attachment",
    "attaching word",
    "canonical basepoint",
    "canonical traversal",
    "geometry-selected",
    "selected traversal",
)
EXACT_CERTIFICATE_REGEX = "|".join(EXACT_CERTIFICATE_TERMS)
SEMANTIC_CANDIDATE_REGEX = (
    "origin|basepoint|attachment|tangent|chirality|rotation system|"
    "outgoing dart|traversal|attaching word|closure rule|monodromy"
)
SEARCH_PATHS = (
    "*.py",
    "*.md",
    "*.lean",
)

NONCLAIMS = (
    "not proof that no certificate exists outside the audited local reachable histories",
    "not proof that deleted unreachable Git objects contain no candidate",
    "not permission to promote a historical mixed-domain artifact into current UCNS authority",
    "not a geometry-selected basepoint, orientation, traversal, attaching word, or monodromy",
    "not an arithmetic readout or numerical gonol constructor",
    "not a PCEA security, entropy, hardness, authenticity, replay-resistance, or recovery claim",
)

FALSIFICATION_CONDITIONS = (
    "an audited authoritative artifact is shown to define a geometric origin-to-recursive-groupoid attachment",
    "an audited authoritative artifact is shown to select tangent or chirality from geometry rather than caller or source order",
    "an audited authoritative artifact is shown to define cyclic incidence among recursive return germs",
    "an audited authoritative artifact is shown to mark one outgoing recursive dart geometrically",
    "an audited authoritative artifact is shown to close the selected multi-generator return as an attaching or monodromy word",
    "a cited repository, commit, tree, blob, content digest, ancestry relation, or history-search result does not replay",
    "the PCEA interpolation control is labeled survived or falsified before an independent constructor is executed",
)

PROMOTION_EVIDENCE = (
    "supply the authoritative UCNS commit and exact artifact defining the missing field",
    "show that the definition is intrinsic geometry and not carrier order, source order, caller order, an API default, an id, or a hash",
    "map Public Gonol or Structural Null geometry into the recursive relation groupoid explicitly",
    "preserve basepoint, orientation, cyclic incidence, outgoing mark, and closure through deterministic replay",
    "rerun the successor experiment only after all five fields are executable",
)

HMMM = (
    "position zero is an authoritative carrier origin, but no audited source attaches it to the recursive relation-groupoid base object",
    "clockwise and counterclockwise helpers expose two caller-selected directions; neither is selected by geometry",
    "the lifted Public Gonol path orders source text, not recursive relation germs",
    "historical marked seams are source-bound partial receipts and explicitly nonselecting",
    "generic traversal delegates child enumeration, identity, policy, and budget to its caller",
    "prime-link basepoints and marked meridians remain scoped to separate P5/P7 experiments with no Public Gonol bridge",
    "post-pinned seed construction makes every ring slot buildable from the center and declares selection effect none",
    "the five-field constructor certificate remains absent in the audited reachable provenance",
)


class ProvenanceAuditError(RuntimeError):
    """Raised when frozen provenance or the research boundary fails closed."""


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _source_root() -> Path:
    return _stack_root().parent


def _repository_path(key: str) -> Path:
    if key not in REPOSITORY_KEYS:
        raise ProvenanceAuditError(f"unknown repository key: {key}")
    path = _source_root() / key
    if not (path / ".git").exists():
        raise ProvenanceAuditError(f"required local Git repository is absent: {path}")
    return path


def _git_bytes(repository: Path, *args: str) -> bytes:
    process = subprocess.run(
        ("git", "-C", str(repository), *args),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode != 0:
        detail = process.stderr.decode("utf-8", errors="replace").strip()
        raise ProvenanceAuditError(
            f"git {' '.join(args)} failed in {repository}: {detail}"
        )
    return process.stdout


def _git_text(repository: Path, *args: str) -> str:
    return _git_bytes(repository, *args).decode("utf-8")


def _git_lines(repository: Path, *args: str) -> tuple[str, ...]:
    return tuple(line for line in _git_text(repository, *args).splitlines() if line)


def _is_ancestor(repository: Path, ancestor: str, descendant: str) -> bool:
    process = subprocess.run(
        ("git", "-C", str(repository), "merge-base", "--is-ancestor", ancestor, descendant),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode not in (0, 1):
        detail = process.stderr.decode("utf-8", errors="replace").strip()
        raise ProvenanceAuditError(f"cannot test ancestry: {detail}")
    return process.returncode == 0


def _line_digest(lines: tuple[str, ...]) -> str:
    data = b"" if not lines else ("\n".join(lines) + "\n").encode("ascii")
    return sha256(data).hexdigest()


@lru_cache(maxsize=None)
def _history_matches(key: str, expression: str) -> tuple[str, ...]:
    repository = _repository_path(key)
    matches = _git_lines(
        repository,
        "log",
        "--all",
        "--root",
        "-i",
        "--format=%H",
        "-G",
        expression,
        "--",
        *SEARCH_PATHS,
    )
    return tuple(sorted(set(matches)))


@dataclass(frozen=True, slots=True)
class RepositorySnapshot:
    """The exact committed-history universe searched in one local clone."""

    key: str
    remote_url: str
    head_commit: str
    origin_main_commit: str
    anchor_commit: str
    anchor_tree: str
    ref_count: int
    ref_set_sha256: str
    unique_tip_count: int
    unique_tip_set_sha256: str
    reachable_commit_count: int
    exact_term_match_count: int
    exact_term_match_set_sha256: str
    semantic_candidate_count: int
    semantic_candidate_set_sha256: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "repository": self.key,
            "remote_url": self.remote_url,
            "head_commit": self.head_commit,
            "origin_main_commit": self.origin_main_commit,
            "anchor_commit": self.anchor_commit,
            "anchor_tree": self.anchor_tree,
            "all_local_refs": {
                "count": self.ref_count,
                "name_and_object_set_sha256": self.ref_set_sha256,
                "unique_tip_count": self.unique_tip_count,
                "unique_tip_set_sha256": self.unique_tip_set_sha256,
            },
            "unique_reachable_commit_count": self.reachable_commit_count,
            "history_search": {
                "scope": "all local refs, root diffs included, committed Python/Markdown/Lean source and specification paths only",
                "pathspecs": list(SEARCH_PATHS),
                "exact_certificate_terms": list(EXACT_CERTIFICATE_TERMS),
                "exact_term_match_count": self.exact_term_match_count,
                "exact_term_match_set_sha256": self.exact_term_match_set_sha256,
                "semantic_candidate_regex": SEMANTIC_CANDIDATE_REGEX,
                "semantic_candidate_count": self.semantic_candidate_count,
                "semantic_candidate_set_sha256": self.semantic_candidate_set_sha256,
            },
        }


@lru_cache(maxsize=None)
def _repository_snapshot(key: str) -> RepositorySnapshot:
    repository = _repository_path(key)
    anchor_commit, expected_tree = ANCHORS[key]
    remote = _git_text(repository, "remote", "get-url", "origin").strip()
    if remote != EXPECTED_REMOTES[key]:
        raise ProvenanceAuditError(f"unexpected {key} origin remote: {remote}")
    anchor_tree = _git_text(repository, "rev-parse", f"{anchor_commit}^{{tree}}").strip()
    if anchor_tree != expected_tree:
        raise ProvenanceAuditError(f"{key} anchor tree changed")

    ref_lines = tuple(sorted(_git_lines(
        repository,
        "for-each-ref",
        "--format=%(refname) %(objectname)",
    )))
    unique_tips = tuple(sorted({line.rsplit(" ", 1)[1] for line in ref_lines}))
    reachable_commits = tuple(sorted(set(_git_lines(repository, "rev-list", "--all"))))
    exact_matches = _history_matches(key, EXACT_CERTIFICATE_REGEX)
    semantic_matches = _history_matches(key, SEMANTIC_CANDIDATE_REGEX)
    return RepositorySnapshot(
        key=key,
        remote_url=remote,
        head_commit=_git_text(repository, "rev-parse", "HEAD").strip(),
        origin_main_commit=_git_text(repository, "rev-parse", "refs/remotes/origin/main").strip(),
        anchor_commit=anchor_commit,
        anchor_tree=anchor_tree,
        ref_count=len(ref_lines),
        ref_set_sha256=_line_digest(ref_lines),
        unique_tip_count=len(unique_tips),
        unique_tip_set_sha256=_line_digest(unique_tips),
        reachable_commit_count=len(reachable_commits),
        exact_term_match_count=len(exact_matches),
        exact_term_match_set_sha256=_line_digest(exact_matches),
        semantic_candidate_count=len(semantic_matches),
        semantic_candidate_set_sha256=_line_digest(semantic_matches),
    )


@lru_cache(maxsize=1)
def repository_snapshots() -> tuple[RepositorySnapshot, ...]:
    """Return exact snapshots of both searched committed-history universes."""

    return tuple(_repository_snapshot(key) for key in REPOSITORY_KEYS)


@dataclass(frozen=True, slots=True)
class ArtifactSpec:
    artifact_id: str
    repository: str
    commit: str
    path: str
    blob_oid: str
    content_sha256: str
    authority_standing: str
    candidate_fields: tuple[str, ...]
    observed_capability: str
    disqualifier: str
    required_fragments: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class EvidenceArtifact:
    """One exact candidate artifact and why it does not fill the certificate."""

    artifact_id: str
    repository: str
    commit: str
    commit_tree: str
    path: str
    blob_oid: str
    content_sha256: str
    authority_standing: str
    candidate_fields: tuple[str, ...]
    qualifying_certificate_fields: tuple[str, ...]
    observed_capability: str
    disqualifier: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "repository": self.repository,
            "commit": self.commit,
            "commit_tree": self.commit_tree,
            "path": self.path,
            "blob_oid": self.blob_oid,
            "content_sha256": self.content_sha256,
            "authority_standing": self.authority_standing,
            "candidate_fields": list(self.candidate_fields),
            "qualifying_certificate_fields": list(self.qualifying_certificate_fields),
            "observed_capability": self.observed_capability,
            "disqualifier": self.disqualifier,
        }


ARTIFACT_SPECS = (
    ArtifactSpec(
        "pinned_public_gonol",
        "ucns",
        UCNS_PINNED_COMMIT,
        "src/ucns/public_gonol.py",
        "c1955e46e2dc918fb657cb346e42106d71937e91",
        "2da287ce9691b494fc921d14684a3bf7e0633f3a579ea040e3b6ddbaf0d92f27",
        "pinned-authority",
        ("origin_attachment",),
        "fixes the exact ordered 157-position carrier and position-zero origin",
        "defines no operation attaching the carrier origin to a recursive relation-groupoid object",
    ),
    ArtifactSpec(
        "pinned_direct_mobius",
        "ucns",
        UCNS_PINNED_COMMIT,
        "src/ucns/direct_mobius.py",
        "14a4cee36b5bbfa72cf3c03703c427abdac7f33d",
        "d8d1360c753dac7431071e007c5105a21b5396dd9e2f7e5ba4089d99e056a5bf",
        "pinned-authority",
        ("origin_attachment", "directed_tangent_or_chirality", "closure_rule"),
        "fixes carrier position zero, two frame labels, signed caller displacement, and local two-turn return",
        "explicitly leaves attachment to full gonol constructions unresolved and does not select displacement sign or a multi-generator closure",
        ("unresolved: attachment to higher-dimensional", "def advance(self, turns:"),
    ),
    ArtifactSpec(
        "pinned_directed_carrier",
        "ucns",
        UCNS_PINNED_COMMIT,
        "src/ucns/carrier.py",
        "7f39c03a6794bddffe5b1be808e2117dc48fb26f",
        "7983f49df68271b2b6b758ba74ea19a3bec332279ef667616456c5ea6b1acf7f",
        "pinned-authority",
        ("directed_tangent_or_chirality", "closure_rule"),
        "defines a coordinate-free Structural Null and directed 4-pi local cover",
        "the contract explicitly forbids inferring chirality or frame inversion and supplies no recursive attachment",
        ("topology_does_not_invent_orientation_algebra", "Structural Null has no coordinate"),
    ),
    ArtifactSpec(
        "pinned_geometry_boundary",
        "ucns",
        UCNS_PINNED_COMMIT,
        "docs/GEOMETRY.md",
        "81ac41bf9f9edd0a2cbdc7d921ca00891f1921c2",
        "5350ebeec5b909957d9a5c40b6d938744ef2e1c23eac46d8dbc0c49e5998a13e",
        "pinned-authority",
        (),
        "defines what may count as current UCNS geometric authority",
        "states that historical existence is not current authority and excludes generic nongeometric traversal frameworks",
        ("Historical existence is not current authority.", "generic evaluator, holdout, laboratory, policy, envelope, or traversal frameworks"),
    ),
    ArtifactSpec(
        "merged_public_gonol_contract",
        "ucns",
        "23c32d90ce78f9b9da37308e098df30448c9df15",
        "docs/public-gonol.md",
        "6521f866cc739e2e416cc36e03a3f85265d50a7c",
        "b4c211e279e74e50944aefdfb2b680ebf68e5a588e9e7aab2ebb5f716a1c1912",
        "merged-history-superseded-by-current-boundary",
        ("origin_attachment", "directed_tangent_or_chirality", "closure_rule"),
        "documents fixed origin, local orientation flip, and 720-degree carrier return",
        "explicitly says the bridge into another UCNS representation is future work and must not be invented",
        ("A future bridge between them must be explicitly specified and ratified.", "promotion does not invent one"),
    ),
    ArtifactSpec(
        "merged_public_gonol_formal",
        "ucns",
        "23c32d90ce78f9b9da37308e098df30448c9df15",
        "formal/Ucns/PublicGonol.lean",
        "e2fa9997b7fde5d03f53f69244f6b11a71853075",
        "1c929a0ca5c6fbc9ed116067d52a5c180a8ce200a7068b6741909e7d2828adcd",
        "merged-history-superseded-by-current-boundary",
        ("origin_attachment", "directed_tangent_or_chirality", "closure_rule"),
        "formalizes position-zero origin and local one- and two-circuit frame behavior",
        "explicitly does not map public vertices into recursive factorization values and leaves that bridge hmmm",
        ("does not", "invent a map from the 157 public vertices", "That bridge remains hmmm"),
    ),
    ArtifactSpec(
        "merged_public_gonol_faces",
        "ucns",
        "038b96b5899650449db067cbd2b30ade96f0bef0",
        "ucns/public_gonol_faces.py",
        "1d90b10161c7df1a75ea92df37dfeb5e9531ce27",
        "455e29d9d519b0d3f76204e0939e17f08d3417205bcc3c70aece78c152caad8f",
        "merged-history-superseded-by-current-boundary",
        ("directed_tangent_or_chirality",),
        "provides clockwise and counterclockwise neighbor operations",
        "direction is a required caller argument and both signs are exported; geometry selects neither",
        ("def chirality(k: int, direction: int)", "direction must be +1 or -1"),
    ),
    ArtifactSpec(
        "merged_public_gonol_lifted_text_path",
        "ucns",
        "fd95f23daaf1301d4f4dbc24e8794f1d72b55bc1",
        "ucns/public_gonol_lifted_path.py",
        "c6a817a917c06674b9244f2d04afb3c689149aea",
        "0e42060a76607ef6d5eae087285a2057fdc941fa9833fe0a53a8483216808334",
        "merged-history-superseded-by-current-boundary",
        ("origin_attachment", "directed_tangent_or_chirality", "rotation_system"),
        "starts at the carrier origin and advances positively through caller text order",
        "it is a lossless text codec over source order, not a traversal of recursive relation germs",
        ("prev_abs = ORIGIN", "for ch in text:", "delta = ((target - prev_vertex - 1) % ARITY) + 1"),
    ),
    ArtifactSpec(
        "merged_generic_recursive_traversal",
        "ucns",
        "35e54e744365f49ab16c7f1370dc4570c46c5d53",
        "src/ucns/traversal.py",
        "690de4273b0a3af796d23758d700b8795dc748f6",
        "84a1144997fe86a387a9fbfd34051ad2cecf9fd9710faac5dbd677c9c875c3bd",
        "merged-history-superseded-by-current-boundary",
        ("rotation_system", "closure_rule"),
        "implements cycle-safe recursion under explicit identity, child, policy, and budget inputs",
        "caller child enumeration and policy determine order and closure behavior; canonical recursive semantics are unresolved",
        ("unresolved: canonical recursive identity", "children: Children", "policy: TraversalPolicy"),
    ),
    ArtifactSpec(
        "merged_v015_partial_attachment",
        "ucns",
        "31249681e0c66e8ce269d7b7aff30bd5dde9487e",
        "docs/FULL_CARRIER_ATTACHMENT_EVIDENCE_V015.md",
        "aa542f47a3c3b7d7494be2ccf6ae5db69f146cf8",
        "e2e5245e706dfa05a4d7fe9d99e763b1838b5cae680387391319017244d5c9fc",
        "merged-history-superseded-by-current-boundary",
        ("origin_attachment",),
        "records source-bound partial root attachments at a marked initiation seam",
        "the evidence is nonselecting, excludes a total Structural Null relation, and leaves marked-versus-intrinsic seam choice unresolved",
        ("carrier selection:              none", "marked-versus-intrinsic target seam choice remains unresolved"),
    ),
    ArtifactSpec(
        "merged_v017_source_bound_initiation",
        "ucns",
        "7b126e82fae01a25350e7f88beef4d258e0633e0",
        "docs/GONOL_INITIATION_STRUCTURAL_NULL_V017.md",
        "eda4ebeb9b3af53e27dc22be464a60bce874937c",
        "c8db3c390de65fc88db649f0d790b77aef9c85067900ddae5d828e26ffac767f",
        "merged-history-superseded-by-current-boundary",
        ("origin_attachment", "closure_rule"),
        "records one source-bound twist receipt and bounded root-loop return",
        "no geometric position is assigned, selection effect is none, and higher-gonol composition remains unresolved",
        ("no geometric position", "selection effect:                    none", "Higher-gonol composition"),
    ),
    ArtifactSpec(
        "geometry_only_purge_receipt",
        "ucns",
        "9985835bda9a84b71c8f14367d01988c314ab870",
        "docs/GEOMETRY_PURGE_RECEIPT.md",
        "30a1e48fa517ec492e5a49c84f69baa73e39eb0d",
        "5ff4fe5c86539c66749090cdbe0ac53c4885a9bdbe6b1856df0d14cda69037ed",
        "merged-current-authority-boundary",
        (),
        "records the geometry-only purge and preserves Git history as recovery mechanism",
        "mixed wrappers do not retain active standing merely because they contain geometric calculations",
        ("Mixed wrappers themselves do not retain active standing",),
    ),
    ArtifactSpec(
        "post_pinned_seed_construction",
        "ucns",
        "828c0b8bbcfc267efb5701da714191c1f73a81ff",
        "src/ucns/mobius_seed_construction.py",
        "193fb7a27d9a827a7eeec0ae4a2e79aae7f5285d",
        "895fc402099b0ec95d116e94b20ddd3a027f510f0ab41a58a67997d63bfc8b36",
        "post-pinned-not-audit-authority",
        ("rotation_system", "marked_outgoing_dart"),
        "starts at the center and derives currently buildable slots from seed relations",
        "all six ring slots are initially buildable, returned ordering is implementation sorting, and selection effect is none",
        ("CONSTRUCTION_SELECTION_EFFECT = \"none\"", "every ring slot is buildable next"),
    ),
    ArtifactSpec(
        "p5_p7_marked_link_preregistration",
        "ucns",
        "828c0b8bbcfc267efb5701da714191c1f73a81ff",
        "docs/PREREGISTRATION_P7_P5_NILPOTENT_DISCRIMINATOR.md",
        "dd661782b8add5933bb12f5232e9836c1c916dbc",
        "ffaecb935e8086200fa9a27c5d55ba6e759721107d8c4979049eed760eae8aee",
        "post-pinned-separate-experiment",
        ("origin_attachment", "directed_tangent_or_chirality", "marked_outgoing_dart", "closure_rule"),
        "uses fixed link basepoints and marked meridian-longitude data in a prime-link experiment",
        "the marks are scoped to P5/P7 ribbon/link presentations and no artifact maps them to Public Gonol recursive return generators",
    ),
    ArtifactSpec(
        "old_twist_seam_specification",
        "ucns",
        "f69fc13621dcb95227a5faeebb8c983651a3bda2",
        "ucns-spec.md",
        "bef3616bdd12018ccd75d47becbad808a4091c16",
        "c8374d4ac36434c0df05385cd6105f93e3f8295549a1edd661c665f27ffef998",
        "merged-history-superseded-by-current-boundary",
        ("origin_attachment", "directed_tangent_or_chirality"),
        "calls the twist seam the beginning",
        "the same specification says the seam has no orientation to carry a path forward and it predates later boundary corrections",
        ("The seam has no orientation to carry the path forward.",),
    ),
    ArtifactSpec(
        "a0_source_architecture_foundation",
        "a0-betatest",
        A0_SOURCE_COMMIT,
        "memory/ARCHITECTURE_FOUNDATION.md",
        "d7d22cc771ee6cb10cfe54b16033d1ea51851c9c",
        "f46518f47405a8433f7e093cc91e99f319f77e02b14738fa2b3472a0804de5eb",
        "exact-upstream-source-provenance",
        ("origin_attachment", "directed_tangent_or_chirality", "closure_rule"),
        "records position-zero SPACE/ZERO origin and the source lifted-path model",
        "defines no map from source carrier or text traversal into recursive relation-groupoid generators",
    ),
    ArtifactSpec(
        "a0_source_faces",
        "a0-betatest",
        A0_SOURCE_COMMIT,
        "backend/interdependent_lib/gonal/faces.py",
        "0246f1033154e5a8b41f68fb592087051b02fc77",
        "14356d5b32de0b51a3201b08dc57befdf7ac45b09c07357c4f41e069b5696261",
        "exact-upstream-source-provenance",
        ("directed_tangent_or_chirality",),
        "defines both directional neighbor operations",
        "direction is caller supplied and no operation selects one sign",
    ),
    ArtifactSpec(
        "a0_source_lifted_text_path",
        "a0-betatest",
        A0_SOURCE_COMMIT,
        "backend/interdependent_lib/gonal/lifted_path.py",
        "190f80084a0bb36ce38a1fe774e95e397c803f1f",
        "ddf0c04f1292567cd1bf30fd47fafe67d6c1e50be774cc200f1681771a03b871",
        "exact-upstream-source-provenance",
        ("origin_attachment", "directed_tangent_or_chirality", "rotation_system"),
        "walks source text from origin in positive carrier order",
        "caller text order selects targets; it does not order recursive relation germs",
    ),
    ArtifactSpec(
        "a0_lifted_path_scope_correction",
        "a0-betatest",
        "1635a2b0768132bf08c3eda6aef337a0719c9173",
        "backend/interdependent_lib/gonal/lifted_path.py",
        "a7f17cf4af9bcc07235d2a39f6171632c60cf42a",
        "af651efea68596b8222b0a8341590e3d4663b896307f7d83370319b1e7a617f3",
        "later-source-boundary-correction",
        ("origin_attachment", "directed_tangent_or_chirality", "rotation_system"),
        "retains deterministic source-frame text traversal",
        "explicitly scopes it to a text codec and rejects current UCNS double-cover authority",
        ("source-frame text codec only", "not a current UCNS double-cover proof"),
    ),
    ArtifactSpec(
        "a0_faces_scope_correction",
        "a0-betatest",
        "7fcd7cc0aab604f35b7db6fedf1e719abfb53031",
        "backend/interdependent_lib/gonal/faces.py",
        "0bb1e0b7a7908bf0cbbfb3523dee4bffb25076ab",
        "a7aa0b4dd0846a396f06d55c055485cd3764aca163005f6a799d92dce0216266",
        "later-source-boundary-correction",
        ("directed_tangent_or_chirality",),
        "retains source-frame labels and both adjacency signs",
        "explicitly says these labels are not current lawful seam-crossing parity",
        ("not current UCNS seam-crossing parity", "direction must be +1 or -1"),
    ),
    ArtifactSpec(
        "a0_reset_boundary",
        "a0-betatest",
        "544301c150e8567d1dbc98bb56d5c96b6d5736db",
        "memory/UCNS_RESET_BOUNDARY.md",
        "3bf9b5666c22d24062ac0d96ba8b3ce654c653e5",
        "24db1905a84ab4151ca4e1d66acca85802d074949114804ab31b3b574b0d1984",
        "later-source-boundary-correction",
        ("origin_attachment",),
        "preserves the exact 157-glyph source fixture",
        "states that lawful projection into the restarted UCNS object remains unresolved",
        ("lawful projection from that fixture", "remains unresolved"),
    ),
)

LEXICAL_BRANCH_CANDIDATE_COMMITS = (
    "17a1202bb3645e7daa7de50b66a02139551d9e39",
    "568a29da5f834c751d4d81aeb66276a4c9a152be",
    "9c74fb79cc1750a54b8da444011d24eedc8fdc05",
)


def _verify_authority_standing(spec: ArtifactSpec, repository: Path) -> None:
    if spec.repository == "ucns":
        if spec.authority_standing == "pinned-authority":
            if spec.commit != UCNS_PINNED_COMMIT:
                raise ProvenanceAuditError(f"{spec.artifact_id} is not pinned")
        elif spec.authority_standing.startswith("post-pinned"):
            if not _is_ancestor(repository, UCNS_PINNED_COMMIT, spec.commit):
                raise ProvenanceAuditError(f"{spec.artifact_id} is not post-pinned")
        elif not _is_ancestor(repository, spec.commit, UCNS_PINNED_COMMIT):
            raise ProvenanceAuditError(f"{spec.artifact_id} is not in pinned ancestry")
    elif spec.authority_standing == "exact-upstream-source-provenance":
        if spec.commit != A0_SOURCE_COMMIT:
            raise ProvenanceAuditError(f"{spec.artifact_id} is not exact source provenance")
    elif not _is_ancestor(repository, A0_SOURCE_COMMIT, spec.commit):
        raise ProvenanceAuditError(f"{spec.artifact_id} is not a later A0 correction")


def _verify_artifact(spec: ArtifactSpec) -> EvidenceArtifact:
    repository = _repository_path(spec.repository)
    _verify_authority_standing(spec, repository)
    blob_oid = _git_text(repository, "rev-parse", f"{spec.commit}:{spec.path}").strip()
    if blob_oid != spec.blob_oid:
        raise ProvenanceAuditError(f"blob identity changed for {spec.artifact_id}")
    content = _git_bytes(repository, "show", f"{spec.commit}:{spec.path}")
    content_digest = sha256(content).hexdigest()
    if content_digest != spec.content_sha256:
        raise ProvenanceAuditError(f"content digest changed for {spec.artifact_id}")
    text = content.decode("utf-8")
    missing = tuple(fragment for fragment in spec.required_fragments if fragment not in text)
    if missing:
        raise ProvenanceAuditError(
            f"required evidence fragments missing for {spec.artifact_id}: {missing}"
        )
    unknown_fields = set(spec.candidate_fields) - set(CERTIFICATE_FIELDS)
    if unknown_fields:
        raise ProvenanceAuditError(f"unknown certificate fields: {sorted(unknown_fields)}")
    return EvidenceArtifact(
        artifact_id=spec.artifact_id,
        repository=spec.repository,
        commit=spec.commit,
        commit_tree=_git_text(repository, "rev-parse", f"{spec.commit}^{{tree}}").strip(),
        path=spec.path,
        blob_oid=blob_oid,
        content_sha256=content_digest,
        authority_standing=spec.authority_standing,
        candidate_fields=spec.candidate_fields,
        qualifying_certificate_fields=(),
        observed_capability=spec.observed_capability,
        disqualifier=spec.disqualifier,
    )


@lru_cache(maxsize=1)
def evidence_artifacts() -> tuple[EvidenceArtifact, ...]:
    """Verify and return all high-signal provenance candidates."""

    artifacts = tuple(_verify_artifact(spec) for spec in ARTIFACT_SPECS)
    ids = tuple(item.artifact_id for item in artifacts)
    if len(ids) != len(set(ids)):
        raise ProvenanceAuditError("artifact ids must be unique")
    return artifacts


@lru_cache(maxsize=1)
def excluded_candidate_clusters() -> tuple[dict[str, Any], ...]:
    """Bind the strongest branch-only candidate cluster and its exclusion."""

    repository = _repository_path("ucns")
    commits = []
    for commit in LEXICAL_BRANCH_CANDIDATE_COMMITS:
        resolved = _git_text(repository, "rev-parse", commit).strip()
        if resolved != commit:
            raise ProvenanceAuditError(f"lexical candidate commit changed: {commit}")
        if _is_ancestor(repository, commit, UCNS_PINNED_COMMIT):
            raise ProvenanceAuditError(
                f"branch-only lexical candidate entered pinned ancestry: {commit}"
            )
        commits.append({
            "commit": commit,
            "tree": _git_text(repository, "rev-parse", f"{commit}^{{tree}}").strip(),
            "subject": _git_text(repository, "show", "-s", "--format=%s", commit).strip(),
        })
    return ({
        "cluster_id": "branch_only_lexical_recursive_gonol",
        "repository": "ucns",
        "commits": commits,
        "authority_standing": "reachable-branch-only-not-in-pinned-ancestry",
        "candidate_capability": "lexical and source-order gonol composition",
        "qualifying_certificate_fields": [],
        "disqualifier": (
            "the cluster is not in pinned ancestry, derives composition from lexical/source "
            "order rather than intrinsic geometry, and was excluded by the geometry-only boundary"
        ),
    },)


FIELD_REASONS = {
    "origin_attachment": (
        "an intrinsic carrier origin exists, but no audited source defines its geometric morphism to one recursive return-groupoid object",
        "an authoritative map from Public Gonol or Structural Null origin into the recursive based path object",
    ),
    "directed_tangent_or_chirality": (
        "local signs and frame labels exist, but they are caller selected or reflection symmetric before an attachment",
        "a direction or chirality transported intrinsically through the origin attachment",
    ),
    "rotation_system": (
        "no audited source defines cyclic incidence among recursive return germs; available orders are source or caller orders",
        "an oriented cyclic order on all incident recursive return germs derived from geometric incidence",
    ),
    "marked_outgoing_dart": (
        "no audited source geometrically marks one recursive outgoing germ; partial seams and unrelated link marks do not do so",
        "one intrinsic marked outgoing germ that fixes the start within the rotation system",
    ),
    "closure_rule": (
        "local two-turn return exists, but no audited source closes a selected multi-generator traversal as an attaching or monodromy word",
        "a deterministic recursive complete-return closure over the selected based oriented traversal",
    ),
}


@dataclass(frozen=True, slots=True)
class CertificateFieldFinding:
    """Disposition of one required constructor-certificate field."""

    field: str
    status: str
    candidate_artifact_ids: tuple[str, ...]
    qualifying_artifact_ids: tuple[str, ...]
    reason: str
    promotion_requirement: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "field": self.field,
            "status": self.status,
            "candidate_artifact_ids": list(self.candidate_artifact_ids),
            "qualifying_artifact_ids": list(self.qualifying_artifact_ids),
            "reason": self.reason,
            "promotion_requirement": self.promotion_requirement,
        }


@lru_cache(maxsize=1)
def certificate_field_findings() -> tuple[CertificateFieldFinding, ...]:
    """Freeze all five fields as unresolved after candidate classification."""

    artifacts = evidence_artifacts()
    findings = []
    for field in CERTIFICATE_FIELDS:
        candidates = tuple(
            item.artifact_id for item in artifacts if field in item.candidate_fields
        )
        qualifying = tuple(
            item.artifact_id
            for item in artifacts
            if field in item.qualifying_certificate_fields
        )
        if qualifying:
            raise ProvenanceAuditError(
                f"{field} gained a qualifying source; stop status requires review"
            )
        reason, promotion = FIELD_REASONS[field]
        findings.append(CertificateFieldFinding(
            field=field,
            status=FIELD_STATUS,
            candidate_artifact_ids=candidates,
            qualifying_artifact_ids=qualifying,
            reason=reason,
            promotion_requirement=promotion,
        ))
    return tuple(findings)


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def _file_digest(root: Path, relative_path: str) -> tuple[str, str]:
    return relative_path, sha256((root / relative_path).read_bytes()).hexdigest()


def _source_file_digests() -> tuple[tuple[str, str], ...]:
    root = _stack_root()
    return tuple(
        _file_digest(root, path)
        for path in (
            "research/ucns/BASE.json",
            "research/ucns/geometry_selected_based_traversal_audit.py",
            "research/ucns/receipts/geometry-selected-based-traversal-audit-v0.json",
        )
    )


def _previous_audit_receipt() -> dict[str, Any]:
    path = _stack_root() / "research/ucns/receipts/geometry-selected-based-traversal-audit-v0.json"
    raw = path.read_bytes()
    payload = json.loads(raw)
    recorded_digest = payload.pop("receipt_sha256")
    replayed_digest = sha256(_canonical_bytes(payload)).hexdigest()
    if recorded_digest != replayed_digest:
        raise ProvenanceAuditError("predecessor audit receipt digest does not replay")
    if payload["audit"]["status"] != CONSTRUCTOR_STATUS:
        raise ProvenanceAuditError("predecessor audit no longer carries the stop status")
    return {
        "payload_sha256": recorded_digest,
        "formatted_file_sha256": sha256(raw).hexdigest(),
        "status": payload["audit"]["status"],
    }


@dataclass(frozen=True, slots=True)
class ProvenanceHistoryAudit:
    """Final no-source result and its deliberately null constructor outputs."""

    history_status: str
    constructor_status: str
    fields: tuple[CertificateFieldFinding, ...]
    constructor_certificate: dict[str, None]
    geometry_selected_traversal_word: None
    monodromy: None
    arithmetic_readout: None
    successor: None
    fourth_gonol: None

    def to_payload(self) -> dict[str, Any]:
        return {
            "history_status": self.history_status,
            "constructor_status": self.constructor_status,
            "certificate_fields": [item.to_payload() for item in self.fields],
            "constructor_certificate": self.constructor_certificate,
            "constructor_outputs": {
                "geometry_selected_traversal_word": self.geometry_selected_traversal_word,
                "monodromy": self.monodromy,
                "arithmetic_readout": self.arithmetic_readout,
                "successor": self.successor,
                "fourth_gonol": self.fourth_gonol,
            },
            "pcea_interpolation_control": {
                "prediction": PCEA_CONTROL_PREDICTION,
                "status": PCEA_CONTROL_STATUS,
                "comparison_performed": False,
                "survived": None,
                "falsified": None,
                "reason": "no independent UCNS constructor emitted a comparison value",
            },
        }


@lru_cache(maxsize=1)
def audit() -> ProvenanceHistoryAudit:
    """Search, classify, and stop without constructing missing geometry."""

    snapshots = repository_snapshots()
    unexpected_exact_matches = {
        item.key: item.exact_term_match_count
        for item in snapshots
        if item.exact_term_match_count
    }
    if unexpected_exact_matches:
        raise ProvenanceAuditError(
            "exact certificate terminology appeared and requires manual review: "
            f"{unexpected_exact_matches}"
        )
    _previous_audit_receipt()
    fields = certificate_field_findings()
    if tuple(item.field for item in fields) != CERTIFICATE_FIELDS:
        raise ProvenanceAuditError("certificate field registry changed")
    certificate = {field: None for field in CERTIFICATE_FIELDS}
    return ProvenanceHistoryAudit(
        history_status=HISTORY_STATUS,
        constructor_status=CONSTRUCTOR_STATUS,
        fields=fields,
        constructor_certificate=certificate,
        geometry_selected_traversal_word=None,
        monodromy=None,
        arithmetic_readout=None,
        successor=None,
        fourth_gonol=None,
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def receipt_payload() -> dict[str, Any]:
    """Return the canonical provenance-audit payload without its outer digest."""

    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source": {
            "authority": "The-Interdependency/ucns",
            "stack_head": _git_text(_stack_root(), "rev-parse", "HEAD").strip(),
            "pinned_ucns_commit": UCNS_PINNED_COMMIT,
            "pinned_ucns_tree": UCNS_PINNED_TREE,
            "a0_source_commit": A0_SOURCE_COMMIT,
            "a0_source_tree": A0_SOURCE_TREE,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in _source_file_digests()
            ],
            "predecessor_audit_receipt": _previous_audit_receipt(),
        },
        "search_boundary": {
            "network_used": False,
            "working_trees_searched": False,
            "committed_reachable_history_only": True,
            "excluded_path_classes": (
                "non-source/spec paths such as raw conversation exports and generated UI data; "
                "the executable search is restricted to Python, Markdown, and Lean"
            ),
            "repository_snapshots": [
                item.to_payload() for item in repository_snapshots()
            ],
            "review_method": (
                "exact certificate-term search plus broad semantic candidate search; "
                "high-signal current, merged-history, post-pinned, and exact-source artifacts "
                "are bound and manually classified below"
            ),
        },
        "evidence_artifacts": [item.to_payload() for item in evidence_artifacts()],
        "excluded_candidate_clusters": list(excluded_candidate_clusters()),
        "audit": audit().to_payload(),
        "nonclaims": list(NONCLAIMS),
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "hmmm": list(HMMM),
    }


def receipt_bytes() -> bytes:
    return _canonical_bytes(receipt_payload())


def receipt_digest() -> str:
    return sha256(receipt_bytes()).hexdigest()


def formatted_receipt_bytes() -> bytes:
    payload = dict(receipt_payload())
    payload["receipt_sha256"] = receipt_digest()
    return (json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n").encode("ascii")


def write_frozen_receipt() -> Path:
    """Write only this module's fixed stack-local generated receipt."""

    path = _stack_root() / "research/ucns/receipts/based-traversal-provenance-history-audit-v0.json"
    path.write_bytes(formatted_receipt_bytes())
    return path


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] == "--write-receipt":
        print(write_frozen_receipt())
        return
    if len(sys.argv) != 1:
        raise SystemExit("usage: based_traversal_provenance_history_audit.py [--write-receipt]")
    sys.stdout.buffer.write(formatted_receipt_bytes())


if __name__ == "__main__":
    main()
