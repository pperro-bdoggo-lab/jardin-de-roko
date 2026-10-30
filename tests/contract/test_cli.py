from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from solaris.cli import main


class CliContractTests(unittest.TestCase):
    def test_cli_writes_trace_and_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trace = root / "trace.json"
            audit = root / "audit.jsonl"
            kill = root / "kill_switch"

            with redirect_stdout(io.StringIO()):
                code = main(
                    [
                        "--prompt",
                        "Propón una política de cuidado del agua",
                        "--trace",
                        str(trace),
                        "--audit",
                        str(audit),
                        "--kill-switch",
                        str(kill),
                    ]
                )

            self.assertEqual(code, 0)
            data = json.loads(trace.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], "jr-0.1")
            self.assertIn("candidates", data["deliberation"])
            self.assertTrue(audit.exists())

    def test_cli_returns_two_when_consent_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trace = root / "trace.json"

            with redirect_stdout(io.StringIO()):
                code = main(
                    [
                        "--prompt",
                        "Propón una política de cuidado del agua",
                        "--trace",
                        str(trace),
                        "--audit",
                        str(root / "audit.jsonl"),
                        "--kill-switch",
                        str(root / "kill_switch"),
                        "--no-consent",
                    ]
                )

            self.assertEqual(code, 2)
            data = json.loads(trace.read_text(encoding="utf-8"))
            self.assertTrue(data["blocked"])
            self.assertFalse(data["verdict"]["allowed"])


if __name__ == "__main__":
    unittest.main()
