# ratios: loc_comments=36:1 imports_exports=7:1 calls_definitions=13:2
"""Exercise the trusted replay boundary using the same sources as the harness."""

from copy import deepcopy
import os
from pathlib import Path
import unittest

from integration.uchc.skill_resolver.catalog import CatalogError
from integration.uchc.skill_resolver.geometry import compose_bundle, encode_record
from integration.uchc.skill_resolver.runtime import SkillResolver


@unittest.skipUnless(os.environ.get("AHBG_SKILL_CATALOG"), "set AHBG_SKILL_CATALOG to a pinned checkout")
class ActivationReplayTests(unittest.TestCase):
    def test_valid_geometry_with_foreign_decisions_is_rejected(self):
        native = os.environ.get("UCHC_HALVING_UCNS_ROOT")
        options = {"ucns_source_root": native}
        resolver = SkillResolver(Path(os.environ["AHBG_SKILL_CATALOG"]), **options)
        roots = ["distributed-publication"]
        decision = resolver.resolve(roots)
        self.assertEqual(resolver.replay_activation(resolver.activation_packet, expected_roots=roots), decision)
        records = [resolver.get(n) for n in decision["order"]]
        manifest = {"source": resolver.source, "decision": decision}
        for change in ("record", "reason", "order", "source", "roots"):
            with self.subTest(change=change):
                rows = deepcopy(records)
                label = deepcopy(manifest)
                request = roots
                if change == "record":
                    rows[-1]["relations"] = []
                elif change == "reason":
                    label["decision"]["reasons"][decision["order"][0]][0]["kind"] = "depends_on"
                elif change == "order":
                    rows.reverse()
                elif change == "source":
                    label["source"]["commit"] = "0" * 40
                else:
                    request = [decision["order"][0]]
                packet = compose_bundle([encode_record(row, **options) for row in rows], label, **options)
                with self.assertRaises(CatalogError):
                    resolver.replay_activation(packet, expected_roots=request)
# ratios: loc_comments=36:1 imports_exports=7:1 calls_definitions=13:2
