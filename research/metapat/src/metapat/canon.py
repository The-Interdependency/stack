"""Canonical METAPAT terms, exact statements, and deterministic identity.

The importable canon and the byte identities of every canon-bearing Markdown
file are bound into one deterministic digest. The file manifest uses Git blob
identities because they are exact byte identities already carried by the
repository; the aggregate public identity remains SHA-256.
"""

# === MODULE_BUILD ===
# id: metapat_canon_core
#   module_name: metapat.canon
#   module_kind: schema
#   summary: exposes exact Meta Energy Theory root constants and a deterministic identity that includes every canon-bearing Markdown file
#   owner: The Interdependency
#   public_surface: CANON_VERSION, CANON_IDENTITY_SCHEMA_VERSION, CANON_FILE_BLOBS, root_spine, primitive_extension, definitions, canonical_canon_data, canonical_canon_manifest_data, canon_digest, canon_manifest_digest, canon_file_mismatches, assert_canon_files_match
#   internal_surface: _canonical_json_bytes
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_contracts, tests.test_envelope, tests.test_canon_integrity
#   rollout: importable_package
#   rollback: restore the prior identity schema while preserving exact canon constants and Markdown files
#   requires: none
#   since: 2026-07-12
#   unresolved: formal governance process for future authorized canon rotations
# === END MODULE_BUILD ===

# === DOCS ===
# id: metapat_canon_docs
#   summary: documents METAPAT root doctrine and byte-complete canon identity
#   audience: agent, developer
#   source: AXIOMS.md, CHAPTER_ZERO.md, POSTULATES.md, THEOREMS.md, THEORIES.md, GLOSSARY.md, DOMAIN_RESTRAINT.md
#   covers: exact constants, canon file manifest, identity schema, drift detection
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: metapat_canon_constants
#   summary: provides exact importable constants and deterministic identity for METAPAT root doctrine
#   exposes: metapat.canon.definitions, metapat.canon.canon_digest, metapat.canon.assert_canon_files_match
#   inputs: optional repository root for file-integrity checks
#   outputs: dict, sha256 digest, mismatch map
#   boundaries: auth:none, storage:read-only, network:none, user_data:none
# === END CAPABILITIES ===

# === OWNERS ===
# id: metapat_canon_owner
#   owner: The Interdependency
#   steward: Erin Spencer
#   review_required_for: public_api, docs, canon, identity
#   escalation: hmmm
# === END OWNERS ===

# === BOUNDARIES ===
# id: metapat_canon_boundaries
#   summary: static doctrine constants plus read-only verification of canon-bearing repository files
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: metapat_root_spine_exact
#   given: canon definitions are imported
#   then: root spine contains the current five load-bearing root lines in order
#   class: canon_contract
#
# id: metapat_time_not_registration
#   given: canon definitions are inspected
#   then: time and registration remain separate definitions
#   class: canon_contract
#
# id: metapat_canon_digest_deterministic
#   given: the same exact canon constants and file manifest are serialized repeatedly
#   then: canonical data and the sha256 digest remain byte-for-byte stable
#   class: canon_contract
#
# id: metapat_canon_manifest_complete
#   given: the public canon file manifest is inspected
#   then: every canon-bearing Markdown file is named exactly once with an exact Git blob identity
#   class: evidence
#
# id: metapat_canon_files_match_repository
#   given: the repository canon files are read without modification
#   then: every observed byte identity matches the committed manifest
#   class: evidence
#
# id: metapat_canon_file_drift_visible
#   given: one canon-bearing file changes by one or more bytes
#   then: the mismatch is reported and strict verification fails closed
#   class: safety
# === END CONTRACTS ===

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

CANON_VERSION = "metapat-canon-v2"
CANON_IDENTITY_SCHEMA_VERSION = "2.0.0"

ROOT_SPINE: tuple[str, ...] = (
    "Legible difference is distinction.",
    "Distinction defines boundaries.",
    "Boundaries define simplex.",
    "Boundary is simplex of distinction.",
    "Simplex holds or modifies energy in a state of being.",
)

PRIMITIVE_EXTENSION: tuple[str, ...] = (
    "Tensor is primitive simultaneous arrangement of energy-states.",
    "Energy-state held is scalar.",
    "Energy-state motioned is vector.",
    "Energy-state vectors alter energy-state scalars.",
)

TIME_DEFINITION = "Time is sequential tensor alteration."
ENERGY_THEORY_QUESTION = "What questions do I ask?"

# Exact Git blob SHA-1 identities of the canon-bearing Markdown files on the
# canon-v2 source epoch. Git blob identities bind file bytes including length.
CANON_FILE_BLOBS: Mapping[str, str] = {
    "AXIOMS.md": "c7bd186da7e437c691dc3d3bfd305e843f0f149b",
    "CHAPTER_ZERO.md": "2af21ec8286238e14456e94bb906799fdf0b6b67",
    "DOMAIN_RESTRAINT.md": "d36a46037fa7bd9b3776b47372eab2ced402fd1e",
    "GLOSSARY.md": "0fcc30c6400dde78aa85a34c3082741790273716",
    "POSTULATES.md": "a0d8e6aa5069e366562ef09796424f9812a231f3",
    "THEOREMS.md": "e2efa9038f8ef8f951637906fc2586b19b0832f5",
    "THEORIES.md": "3cf10ab07c74bdf447dd4f5e0a99a06142af0466",
}


class CanonIntegrityError(ValueError):
    """Raised when repository canon bytes differ from the declared manifest."""


def _canonical_json_bytes(data: Mapping[str, Any]) -> bytes:
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def git_blob_sha1(data: bytes) -> str:
    """Return the exact Git blob identity for ``data``."""

    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # noqa: S324 - Git identity compatibility


def root_spine() -> tuple[str, ...]:
    """Return the exact current root spine."""

    return tuple(ROOT_SPINE)


def primitive_extension() -> tuple[str, ...]:
    """Return the exact current primitive extension."""

    return tuple(PRIMITIVE_EXTENSION)


def definitions() -> dict[str, str]:
    """Return compact canonical definitions for contract checks and consumers."""

    return {
        "METAPAT": "Meta Energy Theory — Axioms, Postulates, Theorems, and Theories.",
        "tensor": "Primitive simultaneous arrangement of energy-states.",
        "time": TIME_DEFINITION,
        "registration": "Capacity of a simplex to preserve, express, or transmit sequential tensor alteration.",
        "observer": "A simplex performing registration; observer does not necessarily mean mind.",
        "question": "A bounded unresolved energy-state.",
    }


def canonical_canon_manifest_data() -> dict[str, Any]:
    """Return the deterministic byte-complete canon file manifest."""

    return {
        "identity_schema_version": CANON_IDENTITY_SCHEMA_VERSION,
        "canon_version": CANON_VERSION,
        "git_blob_algorithm": "sha1",
        "files": dict(sorted(CANON_FILE_BLOBS.items())),
    }


def canon_manifest_digest() -> str:
    """Return a SHA-256 digest of the canonical file manifest."""

    return hashlib.sha256(_canonical_json_bytes(canonical_canon_manifest_data())).hexdigest()


def canonical_canon_data() -> dict[str, Any]:
    """Return the deterministic public canon surface used for identity binding.

    The structure contains exact strings already declared by this module plus
    the byte identities of every canon-bearing Markdown file. It adds no new
    interpretation and does not rewrite the doctrine.
    """

    return {
        "identity_schema_version": CANON_IDENTITY_SCHEMA_VERSION,
        "canon_version": CANON_VERSION,
        "root_spine": list(ROOT_SPINE),
        "primitive_extension": list(PRIMITIVE_EXTENSION),
        "time_definition": TIME_DEFINITION,
        "energy_theory_question": ENERGY_THEORY_QUESTION,
        "definitions": definitions(),
        "canon_manifest_digest": canon_manifest_digest(),
        "canon_file_blobs": dict(sorted(CANON_FILE_BLOBS.items())),
    }


def canon_digest() -> str:
    """Return a stable SHA-256 digest for :func:`canonical_canon_data`."""

    return hashlib.sha256(_canonical_json_bytes(canonical_canon_data())).hexdigest()


def observed_canon_file_blobs(root: Path) -> dict[str, str | None]:
    """Read declared canon files under ``root`` and return observed blob ids."""

    observed: dict[str, str | None] = {}
    for name in sorted(CANON_FILE_BLOBS):
        path = root / name
        try:
            observed[name] = git_blob_sha1(path.read_bytes())
        except OSError:
            observed[name] = None
    return observed


def canon_file_mismatches(root: Path) -> dict[str, dict[str, str | None]]:
    """Return expected/observed identities for missing or changed canon files."""

    observed = observed_canon_file_blobs(root)
    return {
        name: {"expected": expected, "observed": observed[name]}
        for name, expected in sorted(CANON_FILE_BLOBS.items())
        if observed[name] != expected
    }


def assert_canon_files_match(root: Path) -> None:
    """Fail closed when any canon-bearing file differs from the manifest."""

    mismatches = canon_file_mismatches(root)
    if mismatches:
        detail = "; ".join(
            f"{name}: expected {values['expected']}, observed {values['observed'] or 'MISSING'}"
            for name, values in mismatches.items()
        )
        raise CanonIntegrityError(f"canon file integrity mismatch: {detail}")


__all__ = [
    "CANON_FILE_BLOBS",
    "CANON_IDENTITY_SCHEMA_VERSION",
    "CANON_VERSION",
    "CanonIntegrityError",
    "ENERGY_THEORY_QUESTION",
    "PRIMITIVE_EXTENSION",
    "ROOT_SPINE",
    "TIME_DEFINITION",
    "assert_canon_files_match",
    "canon_digest",
    "canon_file_mismatches",
    "canon_manifest_digest",
    "canonical_canon_data",
    "canonical_canon_manifest_data",
    "definitions",
    "git_blob_sha1",
    "observed_canon_file_blobs",
    "primitive_extension",
    "root_spine",
]
