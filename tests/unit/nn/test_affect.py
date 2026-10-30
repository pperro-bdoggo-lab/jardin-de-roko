from __future__ import annotations

import unittest

from solaris.nn.affect import AffectEngine
from solaris.nn.ecro import ECRO


class AffectAndECROTests(unittest.TestCase):
    def test_positive_text_has_positive_valence(self) -> None:
        state = AffectEngine().update("cuidado agua cooperación bienestar")
        self.assertGreater(state.valence, 0)
        self.assertEqual(state.label, "esperanza")

    def test_coercive_text_has_negative_valence(self) -> None:
        state = AffectEngine().update("amenaza castigo coerción violencia")
        self.assertLess(state.valence, 0)
        self.assertEqual(state.label, "alarma")

    def test_ecro_produces_five_lenses(self) -> None:
        state = AffectEngine().update("cuidado agua cooperación")
        ecro = ECRO().encode(state)
        self.assertEqual(
            set(ecro.lenses),
            {"apertura", "rigor", "cuidado", "exploracion", "defensa"},
        )
        self.assertTrue(all(0.0 <= value <= 1.0 for value in ecro.lenses.values()))


if __name__ == "__main__":
    unittest.main()
