from __future__ import annotations

import unittest

from core.detector import detect
from core.renderer import redact_text, render_json


class DetectorTests(unittest.TestCase):
    def test_email_redaction(self) -> None:
        text = "Contact alice@example.com now"
        detections = detect(text)
        self.assertEqual(len(detections), 1)
        payload = render_json(text, detections, input_type="text")
        self.assertEqual(payload["detections"][0]["type"], "email")
        self.assertNotIn("match", payload["detections"][0])
        self.assertIn("[[EMAIL:", payload["redacted_text"])

    def test_same_value_reuses_fingerprint_per_run(self) -> None:
        text = "alice@example.com alice@example.com"
        detections = detect(text)
        self.assertEqual(len(detections), 2)
        self.assertEqual(detections[0].fingerprint, detections[1].fingerprint)

    def test_debug_can_include_match(self) -> None:
        text = "Contact alice@example.com now"
        detections = detect(text, debug=True)
        payload = render_json(text, detections, input_type="text", debug=True)
        self.assertEqual(payload["detections"][0]["match"], "alice@example.com")


if __name__ == "__main__":
    unittest.main()
