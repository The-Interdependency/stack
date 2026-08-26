from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.stack_msdmd_docs import build_book, prefix_collection_path, render_human, write_docs


class StackMsdmdDocsTest(unittest.TestCase):
    def test_prefix_collection_path_anchors_owned_files_under_collection_directory(self) -> None:
        self.assertEqual(
            "research/metapat/src/metapat/catalog.py",
            prefix_collection_path("research/metapat/metapat_msdmd.ts", "src/metapat/catalog.py"),
        )
        self.assertEqual(
            "skill-lib/msdmd/collect.py",
            prefix_collection_path("skill-lib/skill-lib_msdmd.ts", "msdmd/collect.py"),
        )

    def test_build_book_groups_direct_and_collection_data_by_directory_chapters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            alpha = root / "alpha"
            alpha.mkdir()
            (alpha / "module.py").write_text(
                """# === DOCS ===
# id: alpha_docs
#   summary: alpha module docs
# === END DOCS ===
""",
                encoding="utf-8",
            )
            (alpha / "alpha_msdmd.ts").write_text(
                """import { defineMsdmdCollection } from "./msdmd/collection";

export default defineMsdmdCollection({
  repo: "alpha",
  declarations: [
    {
      file: "notes.md",
      block: "DOCS",
      id: "alpha_notes",
      fields: { summary: "collection notes" },
    },
    {
      file: "module.py",
      block: "DOCS",
      id: "alpha_docs",
      fields: { summary: "alpha module docs" },
    },
  ],
  gaps: [],
  edges: [
    {
      from: "alpha_notes",
      to: "alpha_docs",
      kind: "covers",
      source_block: "DOCS",
      source_id: "alpha_notes",
    },
  ],
});
""",
                encoding="utf-8",
            )
            beta = root / "beta"
            beta.mkdir()
            (beta / "module.py").write_text("print('beta')\n", encoding="utf-8")

            book = build_book(root, repo="stack", source_commit="abc123")

            self.assertEqual("stack.msdmd.docs.v1", book["schema"])
            self.assertEqual("abc123", book["source_commit"])
            self.assertIn("alpha", {chapter["id"] for chapter in book["chapters"]})
            alpha_chapter = next(chapter for chapter in book["chapters"] if chapter["id"] == "alpha")
            self.assertEqual(2, alpha_chapter["counts"]["declarations"])
            self.assertEqual(["alpha/alpha_msdmd.ts"], alpha_chapter["collection_points"])
            self.assertNotIn("alpha/alpha_msdmd.ts", alpha_chapter["unannotated_files"])
            self.assertIn("beta/module.py", book["chapters"][1]["unannotated_files"])

            declarations = {item["key"]: item for item in book["declarations"]}
            merged = declarations["alpha/module.py::DOCS::alpha_docs"]
            self.assertEqual(["collection_point", "direct"], sorted(source["kind"] for source in merged["sources"]))
            self.assertIn("alpha/notes.md::DOCS::alpha_notes", declarations)

            human = render_human(book)
            self.assertIn("# stack", human)
            self.assertIn("## Chapter 1: Alpha", human)
            self.assertIn("`alpha_notes` in `alpha/notes.md`", human)

    def test_write_docs_outputs_machine_and_human_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book = build_book(root, repo="stack", source_commit="abc123")
            machine = root / "out" / "machine.json"
            human = root / "out" / "human.md"

            write_docs(book, machine, human)

            self.assertTrue(machine.exists())
            self.assertTrue(human.exists())
            self.assertIn('"schema": "stack.msdmd.docs.v1"', machine.read_text(encoding="utf-8"))
            self.assertIn("# stack", human.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
