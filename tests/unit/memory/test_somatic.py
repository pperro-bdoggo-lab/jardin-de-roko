from __future__ import annotations

import unittest

from solaris.memory.somatic import SomaticMemory
from solaris.schemas import AffectState, MemoryKind


class SomaticMemoryTests(unittest.TestCase):
    def test_retrieves_semantically_related_item(self) -> None:
        memory = SomaticMemory()
        memory.write("cuidado del agua y cooperación", affect=0.5)
        memory.write("vigilancia y castigo", affect=-0.6)

        results = memory.retrieve(
            "agua", AffectState(valence=0.4, intensity=0.4), limit=5
        )
        self.assertTrue(results)
        self.assertIn("agua", results[0].text)
        self.assertEqual(results[0].kind, MemoryKind.SOMATIC)
        self.assertGreater(results[0].score, 0)

    def test_empty_memory_returns_empty(self) -> None:
        self.assertEqual(SomaticMemory().retrieve("agua", AffectState()), [])


if __name__ == "__main__":
    unittest.main()
