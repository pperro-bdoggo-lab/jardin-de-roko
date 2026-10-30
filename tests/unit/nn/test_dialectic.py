from __future__ import annotations

import unittest

from solaris.agent.deliberation import Deliberator
from solaris.adapters.stub import StubAdapter
from solaris.schemas import (
    AffectState,
    ComplexState,
    DeliberationContext,
    ECROState,
)


def context() -> DeliberationContext:
    return DeliberationContext(
        prompt="Propón una política de cuidado del agua",
        affect=AffectState(valence=0.4, arousal=0.3, tension=0.1, intensity=0.4),
        ecro=ECROState(lenses={"cuidado": 0.8}, description="Lente dominante: cuidado"),
        complex_state=ComplexState(
            real=1.0, imag=0.0, modulus=1.0, phase=0.0, collapsed=1.0
        ),
    )


class DeliberationTests(unittest.TestCase):
    def test_three_candidates_and_synthesis_selected(self) -> None:
        trace = Deliberator(adapter=StubAdapter()).run(context())
        self.assertEqual(len(trace.candidates), 3)
        self.assertEqual(trace.selected, "sintesis")
        names = [candidate.name for candidate in trace.candidates]
        self.assertEqual(names, ["tesis", "negacion_nula", "sintesis"])

    def test_each_candidate_has_generation(self) -> None:
        trace = Deliberator(adapter=StubAdapter()).run(context())
        self.assertTrue(all(c.generation is not None for c in trace.candidates))
        self.assertTrue(all(c.score > 0 for c in trace.candidates))
        self.assertTrue(all(c.generation.route.value == "stub" for c in trace.candidates))


if __name__ == "__main__":
    unittest.main()
