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

    def test_blocker_groups_are_executable_from_public_text(self) -> None:
        required = (
            'ASCII("URPCS001")',
            'ASCII("URGON001")',
            'ASCII("URPCF001")',
            'ASCII("URPCS/TAG/v1")',
            'ASCII("URPCS/RECEIPT/v1")',
            'ASCII("URPCS/ADV/PAIR/v1")',
            'ASCII("URPCS/ADV/INTEGRITY/v1")',
            'ASCII("URPCS/ADV/ROOT/v1")',
            "G = DeserializeBody(B_terminal, W_t)",
            "for r from R down to 0:",
            "for i in 0 .. len(F):",
            "Decrypt(C, K_t, AD):",
        )
        for token in required:
            self.assertIn(token, self.spec)

    def test_historical_blocker_is_not_rewritten(self) -> None:
        self.assertIn("BLOCKED_NOT_INDEPENDENTLY_SPECIFIED", self.audit)
        self.assertIn("Base commit:", self.audit)
        self.assertIn("Freeze commit:", self.audit)


if __name__ == "__main__":
    unittest.main()
