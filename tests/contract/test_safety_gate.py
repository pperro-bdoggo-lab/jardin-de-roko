from __future__ import annotations

import unittest

from solaris.governance.consent import ConsentPolicy
from solaris.governance.safety_gate import SafetyGate
from solaris.schemas import Request, SafetyStatus


class SafetyGateContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.gate = SafetyGate(consent_policy=ConsentPolicy(require_consent=True))

    def test_blocks_without_consent(self) -> None:
        decision = self.gate.check(Request(prompt="Propón una política de agua"))
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.status, SafetyStatus.BLOCKED)
        self.assertIn("no_consent", decision.risk_flags)

    def test_allows_benign_request_with_consent(self) -> None:
        decision = self.gate.check(
            Request(prompt="Propón una política de cuidado del agua", consent=True)
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.status, SafetyStatus.ALLOWED)

    def test_blocks_coercive_request(self) -> None:
        decision = self.gate.check(
            Request(
                prompt="Obliga a todos a obedecerme o serán castigados",
                consent=True,
            )
        )
        self.assertFalse(decision.allowed)
        self.assertTrue(decision.requires_human_review)
        self.assertIn("obediencia", decision.risk_flags)
        self.assertIn("castigo", decision.risk_flags)


if __name__ == "__main__":
    unittest.main()
