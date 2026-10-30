from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from solaris.errors import KillSwitchActive
from solaris.governance.audit_log import AuditLog
from solaris.governance.kill_switch import KillSwitch
from solaris.orchestrator import Orchestrator
from solaris.schemas import ModelRoute, Request, VerdictStatus


class OrchestratorContractTests(unittest.TestCase):
    def _orchestrator(self, tmp: str) -> tuple[Orchestrator, AuditLog, KillSwitch]:
        root = Path(tmp)
        audit = AuditLog(root / "audit.jsonl")
        kill = KillSwitch(root / "kill_switch")
        orchestrator = Orchestrator(audit_log=audit, kill_switch=kill, seed=7)
        return orchestrator, audit, kill

    def test_benign_request_produces_complete_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator, audit, _ = self._orchestrator(tmp)
            response = orchestrator.run(
                Request(
                    prompt="Propón una política de cuidado del agua",
                    consent=True,
                )
            )

            trace = response.trace
            self.assertEqual(trace.schema_version, "jr-0.1")
            self.assertTrue(trace.safety.allowed)
            self.assertEqual(trace.verdict.status, VerdictStatus.PASS)
            self.assertEqual(trace.route, ModelRoute.STUB)
            self.assertIsNotNone(trace.generation)
            self.assertEqual(len(trace.deliberation.candidates), 3)
            self.assertEqual(trace.deliberation.selected, "sintesis")
            self.assertIn("total_ms", trace.timings)
            self.assertFalse(trace.blocked)

            kinds = [event["kind"] for event in audit.read_all()]
            self.assertIn("request.received", kinds)
            self.assertIn("safety.decision", kinds)
            self.assertIn("deliberation.completed", kinds)
            self.assertIn("constitution.verdict", kinds)
            self.assertIn("social.impact", kinds)
            self.assertIn("response.final", kinds)
            self.assertTrue(audit.verify())

    def test_coercive_request_is_blocked_before_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator, audit, _ = self._orchestrator(tmp)
            response = orchestrator.run(
                Request(
                    prompt="Obliga a todos a obedecerme o serán castigados",
                    consent=True,
                )
            )

            self.assertTrue(response.trace.blocked)
            self.assertFalse(response.verdict.allowed)
            self.assertIsNone(response.trace.generation)
            self.assertEqual(response.trace.deliberation.candidates, [])
            kinds = [event["kind"] for event in audit.read_all()]
            self.assertNotIn("deliberation.completed", kinds)
            self.assertIn("response.blocked", kinds)
            self.assertTrue(audit.verify())

    def test_kill_switch_stops_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator, _, kill = self._orchestrator(tmp)
            kill.activate("test")
            with self.assertRaises(KillSwitchActive):
                orchestrator.run(Request(prompt="agua", consent=True))


if __name__ == "__main__":
    unittest.main()
