import unittest

from backend.detector import analyze_message


class AnalyzeMessageTests(unittest.TestCase):
    def test_clean_message_has_low_risk(self) -> None:
        result = analyze_message("Hi, are we still meeting for lunch tomorrow?")
        self.assertEqual(result["risk"], "low")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["signals"], [])

    def test_multiple_warning_signs_raise_risk(self) -> None:
        result = analyze_message(
            "URGENT! Your prize expires today. Send your password and pay by gift card."
        )
        self.assertEqual(result["risk"], "high")
        self.assertGreaterEqual(result["score"], 60)
        self.assertGreaterEqual(len(result["signals"]), 3)

    def test_link_is_reported_as_a_warning_sign(self) -> None:
        result = analyze_message("Review this: https://example.test/account")
        self.assertEqual(result["risk"], "low")
        self.assertIn("Contains a web link; verify the destination before opening it", result["signals"])

    def test_score_is_capped_at_one_hundred(self) -> None:
        result = analyze_message(
            "Urgent, act now. Claim your reward. Send your password, bank account, "
            "credit card, and verification code. Pay with bitcoin."
        )
        self.assertEqual(result["score"], 100)


if __name__ == "__main__":
    unittest.main()
