import unittest

from pactus.amount import NANO_PAC_PER_PAC, Amount


class TestAmount(unittest.TestCase):
    def test_from_pac(self):
        test_cases = [
            # Valid cases
            {
                "input": 42.5,
                "expected": Amount(42.5 * NANO_PAC_PER_PAC),
                "raises": None,
            },
            {"input": 0.0, "expected": Amount(0 * NANO_PAC_PER_PAC), "raises": None},
            {
                "input": -10.5,
                "expected": Amount(-10.5 * NANO_PAC_PER_PAC),
                "raises": None,
            },
            # Invalid cases
            {"input": float("nan"), "expected": None, "raises": ValueError},
            {"input": float("inf"), "expected": None, "raises": ValueError},
            {"input": float("-inf"), "expected": None, "raises": ValueError},
        ]

        for case in test_cases:
            if case["raises"]:
                with self.assertRaises(case["raises"]):
                    Amount.from_pac(case["input"])
            else:
                amt = Amount.from_pac(case["input"])
                self.assertEqual(amt, case["expected"])

    def test_from_string(self):
        test_cases = [
            # Valid cases
            {
                "input": "42.5",
                "expected": Amount(42.5 * NANO_PAC_PER_PAC),
                "raises": None,
            },
            {"input": "0.0", "expected": Amount(0 * NANO_PAC_PER_PAC), "raises": None},
            {
                "input": "-10.5",
                "expected": Amount(-10.5 * NANO_PAC_PER_PAC),
                "raises": None,
            },
            # Invalid cases
            {"input": "invalid_string", "expected": None, "raises": ValueError},
            {"input": "nan", "expected": None, "raises": ValueError},
            {"input": "inf", "expected": None, "raises": ValueError},
            {"input": "-inf", "expected": None, "raises": ValueError},
        ]

        for case in test_cases:
            if case["raises"]:
                with self.assertRaises(case["raises"]):
                    Amount.from_string(case["input"])
            else:
                amt = Amount.from_string(case["input"])
                self.assertEqual(amt, case["expected"])


if __name__ == "__main__":
    unittest.main()
