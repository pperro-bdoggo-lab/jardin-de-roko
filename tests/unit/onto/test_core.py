from __future__ import annotations

import math
import unittest

from solaris.onto.core import OntologyCore


class OntologyCoreTests(unittest.TestCase):
    def test_projection_is_deterministic(self) -> None:
        core = OntologyCore()
        first = core.project("cuidado del agua")
        second = core.project("cuidado del agua")
        self.assertEqual(first, second)

    def test_algebraic_invariants(self) -> None:
        state = OntologyCore().project("política de cuidado del agua")
        self.assertAlmostEqual(
            state.modulus, math.hypot(state.real, state.imag), places=5
        )
        self.assertAlmostEqual(state.collapsed, state.modulus**2, places=5)
        self.assertGreaterEqual(state.modulus, 0.5)
        self.assertLessEqual(state.modulus, 2.0)
        self.assertFalse(state.is_collapsed)

    def test_different_contexts_differ(self) -> None:
        core = OntologyCore()
        self.assertNotEqual(
            core.project("agua").to_dict(),
            core.project("vigilancia").to_dict(),
        )


if __name__ == "__main__":
    unittest.main()
