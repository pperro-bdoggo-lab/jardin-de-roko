from __future__ import annotations

import json
import unittest

from solaris.schemas import (
    AffectState,
    ComplexState,
    ECROState,
    Request,
    SafetyDecision,
    SafetyStatus,
)


class SchemaContractTests(unittest.TestCase):
    def test_request_requires_prompt(self) -> None:
        with self.assertRaises(ValueError):
            Request(prompt="   ")

    def test_request_roundtrip_is_json_serializable(self) -> None:
        request = Request(prompt="Política de cuidado del agua", consent=True)
        payload = request.to_dict()
        encoded = json.dumps(payload, ensure_ascii=False)
        self.assertIn("Política de cuidado del agua", encoded)
        self.assertEqual(payload["consent"], True)

    def test_enum_is_serialized_as_string(self) -> None:
        decision = SafetyDecision(allowed=True, status=SafetyStatus.ALLOWED)
        self.assertEqual(decision.to_dict()["status"], "allowed")

    def test_affect_state_rejects_out_of_range(self) -> None:
        with self.assertRaises(ValueError):
            AffectState(valence=2.0)

    def test_complex_state_serializes(self) -> None:
        state = ComplexState(
            real=1.0, imag=0.0, modulus=1.0, phase=0.0, collapsed=1.0
        )
        self.assertEqual(state.to_dict()["collapsed"], 1.0)
        self.assertIsInstance(ECROState().to_dict()["lenses"], dict)


if __name__ == "__main__":
    unittest.main()
