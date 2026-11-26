# ratios: loc_comments=107:1 imports_exports=7:3 calls_definitions=73:7
"""Exercise the catalog against real Git objects in an isolated skill-lib fixture."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from integration.uchc.skill_resolver.catalog import CatalogError, load_catalog, resolve


def row(name, **extra):
    return {"name": name, "path": f"{name}/SKILL.md", "description": f"Use {name}.", **extra}


def fixture_source(root, rows, *, retired=(), raw_index=None):
    subprocess.run(["git", "init", "-q", root], check=True)
    for entry in rows:
        name = entry["name"]
        path = root / name / "SKILL.md"
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(f"---\nname: {name}\n---\n\nexact {name}\r\n".encode())
    index = {"version": 1, "repo": "The-Interdependency/skill-lib", "skills": rows,
             "superseded_skills": [{"name": name} for name in retired]}
    (root / "skills.json").write_bytes(raw_index if raw_index is not None else json.dumps(index).encode())
    subprocess.run(["git", "-C", root, "add", "."], check=True)
    subprocess.run(["git", "-C", root, "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                    "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"], check=True)
    return subprocess.check_output(["git", "-C", root, "rev-parse", "HEAD"], text=True).strip()


class CatalogTests(unittest.TestCase):
    def test_shared_reasons_and_directed_co_load(self):
        rows = [row("msdmd", runner="msdmd/collect.py", status="runnable"),
                row("cap-build", depends_on=["msdmd"]), row("deps-build", depends_on=["msdmd"]),
                row("interdependent-work-graph"),
                row("distributed-publication", load_with=["interdependent-work-graph"])]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            sha = fixture_source(root, rows, retired=["gonal-morphology"])
            catalog = load_catalog(root, source_commit=sha)
            result = resolve(catalog, ["deps-build", "cap-build", "cap-build"])
            self.assertEqual(result["order"], ["msdmd", "cap-build", "deps-build"])
            self.assertEqual(result["reasons"]["msdmd"], [{"source": "cap-build", "kind": "depends_on"},
                                                         {"source": "deps-build", "kind": "depends_on"}])
            visited = []
            def replay(name):
                visited.append(name)
                return catalog.get(name)
            self.assertEqual(resolve(catalog, ["cap-build", "deps-build"], get_record=replay), result)
            self.assertCountEqual(visited, result["order"])
            self.assertEqual(resolve(catalog, ["distributed-publication"])["order"],
                             ["interdependent-work-graph", "distributed-publication"])
            self.assertEqual(resolve(catalog, ["interdependent-work-graph"])["order"],
                             ["interdependent-work-graph"])
            self.assertEqual(catalog.get("msdmd")["runner"], "msdmd/collect.py")
            self.assertEqual(catalog.get("msdmd")["status"], "runnable")
            for name, error in [("absent", "unknown"), ("gonal-morphology", "retired")]:
                with self.assertRaisesRegex(CatalogError, error):
                    resolve(catalog, [name])

    def test_invalid_source(self):
        cases = [
            ([row("a", depends_on=["b"]), row("b", depends_on=["a"])], [], "cycle"),
            ([row("a", depends_on=["b"])], [], "unknown skill"),
            ([row("a", load_with=["b"])], ["b"], "retired skill"),
            ([row("a")], ["a"], "ambiguous"),
            ([row("a"), row("a")], [], "ambiguous"),
            ([row("a", depends_on=["b", "b"]), row("b")], [], "duplicate depends_on"),
            ([row("a", load_with=["a"])], [], "self co-load"),
            ([row("a", depends_on="b"), row("b")], [], "expected a list"),
            ([row("a", load_with=[{"target": "b"}]), row("b")], [], "invalid skill name"),
            ([row("a", requires=["b"]), row("b")], [], "unsupported"),
            ([row("a", path="../elsewhere")], [], "noncanonical"),
        ]
        for rows, retired, error in cases:
            with self.subTest(error=error), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                sha = fixture_source(root, rows, retired=retired)
                with self.assertRaisesRegex(CatalogError, error):
                    load_catalog(root, source_commit=sha)

    def test_duplicate_fields(self):
        native = b'{"version":1,"repo":"The-Interdependency/skill-lib","skills":[],"skills":[]}'
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            sha = fixture_source(root, [], raw_index=native)
            with self.assertRaisesRegex(CatalogError, "duplicate index field"):
                load_catalog(root, source_commit=sha)

    def test_source_pin_and_body_integrity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            sha = fixture_source(root, [row("a")])
            catalog = load_catalog(root, source_commit=sha)
            source = root / "a" / "SKILL.md"
            original = source.read_bytes()
            self.assertEqual(catalog.read_body("a").encode(), original)
            self.assertEqual(catalog.get("a")["sha256"], hashlib.sha256(original).hexdigest())
            self.assertEqual(catalog.source, {"repo": "The-Interdependency/skill-lib", "commit": sha,
                             "index_sha256": hashlib.sha256((root / "skills.json").read_bytes()).hexdigest()})
            visible = catalog.records
            visible["a"]["sha256"] = "fake"
            with self.assertRaisesRegex(CatalogError, "differs from pinned source"):
                resolve(catalog, ["a"], get_record=visible.__getitem__)
            source.write_bytes(original + b"drift")
            with self.assertRaisesRegex(CatalogError, "differs from pinned commit"):
                catalog.read_body("a")
            source.unlink()
            (root / "same-bytes").write_bytes(original)
            source.symlink_to(root / "same-bytes")
            with self.assertRaisesRegex(CatalogError, "symlink"):
                catalog.read_body("a")
            (root / "skills.json").write_bytes(b"{}")
            with self.assertRaisesRegex(CatalogError, "differs from pinned commit"):
                load_catalog(root, source_commit=sha)
            with self.assertRaisesRegex(CatalogError, "exact"):
                load_catalog(root, source_commit="HEAD")
# ratios: loc_comments=107:1 imports_exports=7:3 calls_definitions=73:7
