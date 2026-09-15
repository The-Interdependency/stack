# === MODULE_BUILD ===
# id: english_gonol_corpus_native_density
#   module_name: density_run
#   module_kind: measurement
#   summary: counts exact admitted character occurrences through the constructed word-character occurrence relations and records corpus-native frequency density with full provenance
#   owner: Erin Spencer
#   public_surface: SCHEMA, VERSION, DensityError, DensityResult, build_density, run
#   internal_surface: read-only construct inspection, exact Fraction arithmetic, canonical receipt serialization
#   auth_boundary: measures the already-constructed English Gonol v2 database; does not retokenize, normalize, or re-admit corpus text; supplies no geometry
#   storage_boundary: one caller-selected out directory with density.json and density.md
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_density_run
#   rollout: stack-local research measurement outside the construct; no canon or semantic measurement promotion
#   rollback: delete this module and its generated output directory
#   requires: english_gonol_full_construct
#   since: 2026-09-15
#   unresolved: what measured density does geometrically remains unresolved
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: density_counts_constructed_occurrence_relations
#   given: a verified English Gonol v2 construct.db
#   then: every letter count is taken from the constructed word_characters occurrence relations joined to shared character identities, never by retokenizing or normalizing source text
#   class: correctness
#   since: 2026-09-15
#
# id: density_fractions_are_exact
#   given: exact integer per-letter counts and an exact total
#   then: every frequency is recorded as an exact reduced Fraction of the total
#   class: correctness
#   since: 2026-09-15
#
# id: density_ratios_are_reduced
#   given: any pair of letters with exact integer counts
#   then: the ratio between their counts is recorded reduced to lowest terms
#   class: correctness
#   since: 2026-09-15
#
# id: density_records_provenance_and_receipt
#   given: a construct manifest and measured database hash
#   then: corpus and builder hashes, the construct receipt, and a canonical density receipt are all recorded
#   class: correctness
#   since: 2026-09-15
#
# id: density_stays_outside_the_construct
#   given: a density result
#   then: it is a separate measurement table that modifies no construct table and invents no geometry
#   class: doctrine
#   since: 2026-09-15
#
# id: density_fails_closed_on_wrong_construct_schema
#   given: a construct manifest whose schema is not english-gonol.full-construct
#   then: build_density raises DensityError
#   class: safety
#   since: 2026-09-15
# === END CONTRACTS ===

"""Corpus-native letter density from the constructed occurrence relations.

The English Gonol v2 construct materializes one shared identity per exact
character scalar and one ``word_characters`` occurrence relation per ordered
character reference inside a word. This measurement reads only those
constructed relations::

    characters -> id, scalar, public_position
    word_characters -> word_id, ordinal, character_id

Each admitted character scalar gets an exact integer occurrence count, an
exact frequency fraction of the total, and exact reduced pairwise ratios
between scalars. Nothing is retokenized, case-folded, normalized, or
re-admitted; the generic density table stays outside the construct.

hmmm: frequency becomes measured; what density does geometrically remains
unresolved.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
from typing import Any

SCHEMA = "english-gonol.corpus-native-density"
VERSION = "1.0.0"
CONSTRUCT_SCHEMA = "english-gonol.full-construct"

_HMMM = (
    "frequency becomes measured; "
    "what density does geometrically remains unresolved"
)


class DensityError(ValueError):
    """Raised when the density measurement fails closed."""


@dataclass(frozen=True)
class DensityResult:
    schema: str
    version: str
    corpus: dict[str, Any]
    builder: dict[str, Any]
    total: int
    letters: tuple[tuple[str, int | None, int, str], ...]
    ratios: tuple[tuple[str, str, str], ...]
    hmmm: str
    receipt_sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "version": self.version,
            "corpus": self.corpus,
            "builder": self.builder,
            "total": self.total,
            "letters": [
                {
                    "scalar": scalar,
                    "public_position": public_position,
                    "count": count,
                    "frequency_fraction": fraction,
                }
                for scalar, public_position, count, fraction in self.letters
            ],
            "ratios": [
                {"a": a, "b": b, "reduced_ratio": ratio}
                for a, b, ratio in self.ratios
            ],
            "hmmm": self.hmmm,
            "receipt_sha256": self.receipt_sha256,
        }

    def canonical_bytes(self) -> bytes:
        payload = self.as_dict()
        payload.pop("receipt_sha256", None)
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def receipt_bytes(self) -> bytes:
        return json.dumps(self.as_dict(), sort_keys=True, separators=(",", ":")).encode("utf-8")


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DensityError(f"construct manifest is not readable JSON: {path}") from exc
    if manifest.get("schema") != CONSTRUCT_SCHEMA:
        raise DensityError(
            f"construct manifest schema must be {CONSTRUCT_SCHEMA}"
        )
    return manifest


def _hash_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(8 * 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def build_density(construct_db: Path, construct_manifest: Path) -> DensityResult:
    """Measure corpus-native letter density through the constructed relations only."""

    manifest = _load_manifest(construct_manifest)
    if not construct_db.is_file():
        raise DensityError(f"construct database does not exist: {construct_db}")

    construct_db_sha256 = _hash_file(construct_db)
    connection = sqlite3.connect(f"file:{construct_db}?mode=ro", uri=True)
    try:
        rows = connection.execute(
            """
            SELECT c.scalar, c.public_position, COUNT(wc.character_id)
            FROM characters AS c
            LEFT JOIN word_characters AS wc ON wc.character_id = c.id
            GROUP BY c.id, c.scalar, c.public_position
            ORDER BY c.id
            """
        ).fetchall()
    except sqlite3.Error as exc:
        raise DensityError(f"construct database is not readable: {exc}") from exc
    finally:
        connection.close()

    if not rows:
        raise DensityError("word_characters occurrence relations are empty")

    total = sum(count for _, _, count in rows)
    if total <= 0:
        raise DensityError("total admitted character occurrences must be positive")

    letters: list[tuple[str, int | None, int, str]] = []
    for scalar, public_position, count in rows:
        fraction = Fraction(count, total)
        letters.append(
            (
                scalar,
                public_position,
                count,
                f"{fraction.numerator}/{fraction.denominator}",
            )
        )

    ratios: list[tuple[str, str, str]] = []
    for left in range(len(letters)):
        for right in range(left + 1, len(letters)):
            a_scalar = letters[left][0]
            b_scalar = letters[right][0]
            a_count = letters[left][2]
            b_count = letters[right][2]
            if b_count == 0:
                ratio_text = f"{a_count}/0"
            elif a_count == 0:
                ratio_text = f"0/{b_count}"
            else:
                ratio = Fraction(a_count, b_count)
                ratio_text = f"{ratio.numerator}/{ratio.denominator}"
            ratios.append((a_scalar, b_scalar, ratio_text))

    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "version": VERSION,
        "corpus": manifest["corpus"],
        "builder": {
            "construct_schema": manifest["schema"],
            "construct_version": manifest["version"],
            "construct_receipt_sha256": manifest.get("receipt_sha256"),
            "construct_db_sha256": construct_db_sha256,
            "ucns_commit": manifest.get("ucns", {}).get("commit"),
            "public_gonol_sha256": manifest.get("ucns", {}).get("public_gonol_sha256"),
        },
        "total": total,
        "letters": [
            {
                "scalar": scalar,
                "public_position": public_position,
                "count": count,
                "frequency_fraction": fraction,
            }
            for scalar, public_position, count, fraction in letters
        ],
        "ratios": [
            {"a": a, "b": b, "reduced_ratio": ratio}
            for a, b, ratio in ratios
        ],
        "hmmm": _HMMM,
    }
    receipt = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    return DensityResult(
        schema=SCHEMA,
        version=VERSION,
        corpus=manifest["corpus"],
        builder=payload["builder"],
        total=total,
        letters=tuple(letters),
        ratios=tuple(ratios),
        hmmm=_HMMM,
        receipt_sha256=receipt,
    )


def _render_markdown(result: DensityResult) -> str:
    lines = [
        "# English Gonol corpus-native letter density",
        "",
        "Generic measurement table outside the construct.",
        "",
        "## Provenance",
        "",
        f"- corpus: {result.corpus.get('repository')} @ {result.corpus.get('commit')}",
        f"- source tree sha256: {result.corpus.get('source_tree_sha256')}",
        f"- construct schema: {result.builder.get('construct_schema')}",
        f"- construct version: {result.builder.get('construct_version')}",
        f"- construct receipt: {result.builder.get('construct_receipt_sha256')}",
        f"- construct database sha256: {result.builder.get('construct_db_sha256')}",
        f"- density receipt: {result.receipt_sha256}",
        "",
        f"Total admitted character occurrences: {result.total}",
        "",
        "## Per-letter counts and exact frequency fractions",
        "",
        "| scalar | public_position | count | frequency_fraction |",
        "|---|---:|---:|---|",
    ]
    for scalar, public_position, count, fraction in result.letters:
        display = scalar if scalar != " " else "` `"
        lines.append(
            f"| {display} | {public_position} | {count} | {fraction} |"
        )
    lines.extend(
        [
            "",
            "## Reduced ratios between letters",
            "",
            f"Full pairwise reduced ratios ({len(result.ratios)} pairs) are in `density.json`.",
            "",
            "## hmmm",
            "",
            result.hmmm,
            "",
        ]
    )
    return "\n".join(lines)


def run(
    construct_db: Path,
    construct_manifest: Path,
    out_dir: Path,
    *,
    overwrite: bool = False,
) -> DensityResult:
    """Build the density measurement and write ``density.json`` and ``density.md``."""

    result = build_density(construct_db, construct_manifest)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "density.json"
    markdown_path = out_dir / "density.md"
    if not overwrite and (json_path.exists() or markdown_path.exists()):
        raise DensityError(f"output files already exist in {out_dir}; pass --overwrite")
    json_path.write_text(
        result.receipt_bytes().decode("utf-8") + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(result), encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--construct-db", required=True, help="English Gonol v2 construct.db path")
    parser.add_argument("--construct-manifest", required=True, help="construct manifest.json path")
    parser.add_argument("--out-dir", required=True, help="density output directory")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = run(
            Path(args.construct_db),
            Path(args.construct_manifest),
            Path(args.out_dir),
            overwrite=args.overwrite,
        )
    except DensityError as exc:
        raise SystemExit(f"density error: {exc}") from exc

    print(json.dumps(
        {
            "schema": result.schema,
            "version": result.version,
            "total": result.total,
            "letters": len(result.letters),
            "ratios": len(result.ratios),
            "receipt_sha256": result.receipt_sha256,
            "hmmm": result.hmmm,
        },
        sort_keys=True,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
