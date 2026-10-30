from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from solaris.governance.audit_log import AuditLog


class AuditLogContractTests(unittest.TestCase):
    def test_appends_and_verifies_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log = AuditLog(Path(tmp) / "audit.jsonl")
            log.append("request.received", {"prompt": "agua"})
            log.append("response.final", {"ok": True})

            events = log.read_all()
            self.assertEqual(len(events), 2)
            self.assertEqual(events[0]["prev_hash"], "GENESIS")
            self.assertEqual(events[1]["prev_hash"], events[0]["hash"])
            self.assertTrue(log.verify())

    def test_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audit.jsonl"
            log = AuditLog(path)
            log.append("one", {"value": 1})
            log.append("two", {"value": 2})

            lines = path.read_text(encoding="utf-8").splitlines()
            first = json.loads(lines[0])
            first["payload"]["value"] = 999
            lines[0] = json.dumps(first, ensure_ascii=False)
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            self.assertFalse(log.verify())


if __name__ == "__main__":
    unittest.main()
