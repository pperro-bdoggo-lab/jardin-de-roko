from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from solaris.governance.audit_log import AuditLog
from solaris.governance.kill_switch import KillSwitch
from solaris.orchestrator import Orchestrator
from solaris.schemas import Request


class VerticalSliceIntegrationTests(unittest.TestCase):
    def test_end_to_end_trace_is_written_and_auditable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            audit = AuditLog(root / "audit.jsonl")
            orchestrator = Orchestrator(
                audit_log=audit,
                kill_switch=KillSwitch(root / "kill_switch"),
                seed=123,
            )
            response = orchestrator.run(
                Request(
                    prompt="Propón una política de cuidado del agua",
                    consent=True,
                )
            )

            trace_path = root / "trace.json"
            trace_path.write_text(response.trace.to_json(), encoding="utf-8")
            data = json.loads(trace_path.read_text(encoding="utf-8"))

            for key in (
                "request",
                "safety",
                "affect",
                "ecro",
                "complex_state",
                "memories",
                "deliberation",
                "generation",
                "verdict",
                "impact",
                "route",
                "timings",
            ):
                self.assertIn(key, data)

            self.assertEqual(len(data["deliberation"]["candidates"]), 3)
            self.assertTrue(audit.verify())
            self.assertTrue(
                any(event["kind"] == "response.final" for event in audit.read_all())
            )


if __name__ == "__main__":
    unittest.main()
