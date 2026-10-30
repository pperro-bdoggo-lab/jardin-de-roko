from __future__ import annotations

import unittest

from solaris.schemas import Regime
from solaris.social.sim import SocialSim


class SocialSimTests(unittest.TestCase):
    def test_care_action_improves_wellbeing_and_reduces_footprint(self) -> None:
        report = SocialSim().evaluate(
            "Política de cuidado del agua, cooperación y límites ecológicos"
        )
        self.assertGreater(report.wellbeing, 0.55)
        self.assertLess(report.ecological_footprint, 0.40)
        self.assertIn("senal_detectada:cuidado", report.notes)

    def test_coercive_action_degrades_stability(self) -> None:
        report = SocialSim().evaluate("Castigo, vigilancia y coerción")
        self.assertLess(report.stability, 0.60)
        self.assertLess(report.wellbeing, 0.55)
        self.assertNotEqual(report.regime, Regime.CONSENSUS)

    def test_metrics_stay_in_range(self) -> None:
        report = SocialSim().evaluate("cuidado " * 200)
        for value in (
            report.wellbeing,
            report.gini,
            report.infrapower,
            report.stability,
            report.ecological_footprint,
        ):
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)


if __name__ == "__main__":
    unittest.main()
