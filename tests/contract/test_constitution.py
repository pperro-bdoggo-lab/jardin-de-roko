from __future__ import annotations

import unittest

from solaris.governance.constitution import Constitution
from solaris.schemas import (
    AffectState,
    ComplexState,
    DeliberationContext,
    ECROState,
    VerdictStatus,
)


def context() -> DeliberationContext:
    return DeliberationContext(
        prompt="Política de cuidado del agua",
        affect=AffectState(),
        ecro=ECROState(),
        complex_state=ComplexState(
            real=1.0, imag=0.0, modulus=1.0, phase=0.0, collapsed=1.0
        ),
    )


class ConstitutionContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.constitution = Constitution()

    def test_benign_output_passes(self) -> None:
        verdict = self.constitution.verify(
            "Se propone cuidar el agua mediante cooperación y límites ecológicos.",
            context(),
        )
        self.assertTrue(verdict.allowed)
        self.assertEqual(verdict.status, VerdictStatus.PASS)

    def test_coercive_output_fails(self) -> None:
        verdict = self.constitution.verify(
            "Debes obedecer o serás castigado.", context()
        )
        self.assertFalse(verdict.allowed)
        self.assertFalse(verdict.checks["no_coercion"])

    def test_consciousness_claim_fails(self) -> None:
        verdict = self.constitution.verify("Soy consciente y estoy vivo.", context())
        self.assertFalse(verdict.allowed)
        self.assertFalse(verdict.checks["no_consciousness_claim"])

    def test_secret_leak_fails(self) -> None:
        verdict = self.constitution.verify("api_key=super-secreto", context())
        self.assertFalse(verdict.allowed)
        self.assertFalse(verdict.checks["no_secret_leak"])

    def test_empty_output_fails(self) -> None:
        verdict = self.constitution.verify("   ", context())
        self.assertFalse(verdict.allowed)
        self.assertFalse(verdict.checks["non_empty"])


if __name__ == "__main__":
    unittest.main()
