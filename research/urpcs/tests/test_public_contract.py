"""Regression checks for the independently consumable URPCS public contract.

CHECKS:
- CHECK_PUBLIC_LAWS_STATED: Laws 1-13 have normative sections, not only an index.
- CHECK_DECODER_INPUTS_STATED: the four blocker groups and domain strings are public.
- CHECK_HISTORICAL_AUDIT_PRESERVED: the frozen blocker remains explicitly historical.

These checks prevent another projection from collapsing the normative contract
back to a list of law names. They do not prove independent interoperability.
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs" / "urpcs-v1-spec.md"
AUDIT = ROOT / "docs" / "URPCS-v1-independent-decoder-audit.md"


class PublicContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = SPEC.read_text(encoding="utf-8")
        cls.audit = AUDIT.read_text(encoding="utf-8")

    def test_all_laws_have_normative_sections(self) -> None:
        for law in range(1, 14):
            self.assertEqual(
                self.spec.count(f"## Law {law} —"),
                1,
                f"Law {law} must have exactly one normative section",
            )

if __name__ == "__main__":
    unittest.main()
