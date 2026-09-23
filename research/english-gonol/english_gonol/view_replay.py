# ratios: loc_comments=72:28 imports_exports=5:4 calls_definitions=21:7
"""Independent exact reconstruction of the pinned four-view formulas.

Used by full_view_audit over every admitted word. This implementation reads
the complete construct once, never invokes the native view/motion functions,
and retains the distinction between numeric addresses and glyph constructions.
"""

# === MODULE_BUILD ===
# id: english_views_independent_replay
#   module_name: view_replay
#   module_kind: audit
#   summary: reconstruct complete pinned view records using exact integer arithmetic and bulk source reads
#   owner: The-Interdependency/stack
#   public_surface: Corpus, canonical, record_from_views, freeze_views
#   storage_boundary: read-only caller SQLite connection; in-memory indexes
#   network_boundary: none
#   user_data_boundary: pinned public corpus only
#   tests: tests.test_full_view_audit
#   rollout: explicit full-corpus comparison; no geometry selection
#   rollback: remove audit implementation while preserving sealed evidence
#   unresolved: view usefulness for inference is outside this replay
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: full_views_exact_reconstruction
#   given: complete word glyph sequences and word-rooted definition constituents
#   then: derive the pinned phase/frame from the exact sum, retain typed absence, and reproduce all native view fields
#   class: correctness
# === END CONTRACTS ===

from collections import defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations
import json


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def record_from_views(word_id, views):
    v1, v2, v3, v4 = views
    record = {
        "schema": "english-gonol.hyperspace-views", "version": "0.1.0",
        "word_id": word_id,
        "views": dict(zip(VIEW_NAMES, views)),
        "synthesis": [v1, v2["phase"], v2["frame"], v3["lift"], v4["lift"]],
    }
    record["receipt_sha256"] = hashlib.sha256(canonical(record)).hexdigest()
    return record


VIEW_NAMES = (
    "view1_definition_inner_product_density", "view2_word_axis_angle",
    "view3_provenance_interval_lift", "view4_canonical_witness_lift",
)


def freeze_views(views):
    """Exact equality keys; do not coerce None to zero or drop native fields."""
    return tuple(None if view is None else tuple(sorted(view.items())) for view in views)


class Corpus:
    """All source rows required by the audited formulas; no sampling option."""

    def __init__(self, db):
        self.words = db.execute("SELECT id,surface FROM words ORDER BY id").fetchall()
        self.characters = db.execute("SELECT id,scalar,public_position FROM characters ORDER BY id").fetchall()
        self.glyphs = defaultdict(list)
        for word_id, ordinal, character_id in db.execute(
            "SELECT word_id,ordinal,character_id FROM word_characters ORDER BY word_id,ordinal"
        ):
            self.glyphs[word_id].append((ordinal, character_id))
        self.definitions = defaultdict(list)
        for definition_id, word_id in db.execute(
            "SELECT id,origin_word_id FROM definitions ORDER BY origin_word_id,ordinal"
        ):
            self.definitions[word_id].append(definition_id)
        self.axes = defaultdict(set)
        for definition_id, word_id in db.execute(
            "SELECT definition_id,word_id FROM definition_components WHERE kind='word'"
        ):
            if word_id is not None:
                self.axes[definition_id].add(word_id)

    def overlap(self, word_id):
        definitions = self.definitions[word_id]
        if len(definitions) < 2:
            return None
        overlaps = [len(self.axes[a] & self.axes[b]) for a, b in combinations(definitions, 2)]
        return {
            "definition_count": len(definitions), "pair_count": len(overlaps),
            "orthogonal_pair_count": sum(value == 0 for value in overlaps),
            "shared_sum": sum(overlaps),
        }

    def views(self, word_id, *, renamed_word_id=None, reverse_glyph_ids=False, overlap=None):
        if overlap is None:
            overlap = self.overlap(word_id)
        glyphs = self.glyphs[word_id]
        if not glyphs:
            raise ValueError(f"word {word_id} has no glyph construction")
        count = len(self.characters)
        total = sum(ordinal + (count + 1 - char if reverse_glyph_ids else char)
                    for ordinal, char in glyphs)
        residue = total % 157
        phase = Fraction(residue, 157)
        frame = "reversed-local-frame" if (total // 157) % 2 else "positive-local-frame"
        deck = (word_id if renamed_word_id is None else renamed_word_id) // 157
        return (
            overlap,
            {"phase": f"{phase.numerator}/{phase.denominator}", "frame": frame},
            {"deck": deck, "residue": residue, "lift": 157 * deck + residue},
            {"residue": residue, "lift": 157 + residue},
        )
# ratios: loc_comments=72:28 imports_exports=5:4 calls_definitions=21:7
