import unittest

from pactus.types.amount import NANO_PAC_PER_PAC, Amount


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

    def test_str(self):
        test_cases = [
            {
                "input": Amount(0),
                "expected": "0.0",
            },
            {
                "input": Amount.from_pac(42.5),
                "expected": "42.5",
            },
            {
                "input": Amount.from_pac(1.0),
                "expected": "1.0",
            },
            {
                "input": Amount.from_pac(0.5),
                "expected": "0.5",
            },
            {
                "input": Amount.from_pac(1000000.0),
                "expected": "1000000.0",
            },
            {
                "input": Amount.from_pac(0.000000001),
                "expected": "1e-09",
            },
            {
                "input": Amount.from_pac(-10.5),
                "expected": "-10.5",
            },
            {
                "input": Amount.from_nano_pac(1000000000),
                "expected": "1.0",
            },
            {
                "input": Amount.from_nano_pac(500000000),
                "expected": "0.5",
            },
        ]

        for case in test_cases:
            result = str(case["input"])
            self.assertEqual(result, case["expected"])

    def test_to_pac(self):
        test_cases = [
            {
                "input": Amount(0),
                "expected": 0.0,
            },
            {
                "input": Amount.from_pac(42.5),
                "expected": 42.5,
            },
            {
                "input": Amount.from_pac(1.0),
                "expected": 1.0,
            },
            {
                "input": Amount.from_pac(0.5),
                "expected": 0.5,
            },
            {
                "input": Amount.from_pac(1000000.0),
                "expected": 1000000.0,
            },
            {
                "input": Amount.from_pac(0.000000001),
                "expected": 0.000000001,
            },
            {
                "input": Amount.from_pac(-10.5),
                "expected": -10.5,
            },
            {
                "input": Amount.from_nano_pac(1000000000),
                "expected": 1.0,
            },
            {
                "input": Amount.from_nano_pac(500000000),
                "expected": 0.5,
            },
            {
                "input": Amount.from_nano_pac(1),
                "expected": 0.000000001,
            },
            {
                "input": Amount.from_nano_pac(123456789),
                "expected": 0.123456789,
            },
        ]

        for case in test_cases:
            result = case["input"].to_pac()
            self.assertAlmostEqual(result, case["expected"], places=9)

    def test_to_nano_pac(self):
        test_cases = [
            {
                "input": Amount(0),
                "expected": 0,
            },
            {
                "input": Amount.from_pac(42.5),
                "expected": int(42.5 * NANO_PAC_PER_PAC),
            },
            {
                "input": Amount.from_pac(1.0),
                "expected": int(1.0 * NANO_PAC_PER_PAC),
            },
            {
                "input": Amount.from_pac(0.5),
                "expected": int(0.5 * NANO_PAC_PER_PAC),
            },
            {
                "input": Amount.from_pac(1000000.0),
                "expected": int(1000000.0 * NANO_PAC_PER_PAC),
            },
            {
                "input": Amount.from_pac(-10.5),
                "expected": int(-10.5 * NANO_PAC_PER_PAC),
            },
            {
                "input": Amount.from_nano_pac(1000000000),
                "expected": 1000000000,
            },
            {
                "input": Amount.from_nano_pac(500000000),
                "expected": 500000000,
            },
            {
                "input": Amount.from_nano_pac(1),
                "expected": 1,
            },
            {
                "input": Amount.from_nano_pac(123456789),
                "expected": 123456789,
            },
        ]

        for case in test_cases:
            result = case["input"].to_nano_pac()
            self.assertEqual(result, case["expected"])

    def test_round_trip_conversion(self):
        """Test that converting from PAC to NanoPAC and back preserves the value."""
        test_values = [0.0, 1.0, 42.5, 0.5, 1000000.0, 0.000000001, -10.5]

        for pac_value in test_values:
            amount = Amount.from_pac(pac_value)
            nano_pac = amount.to_nano_pac()
            back_to_pac = amount.to_pac()

            # Create new amount from nano_pac and verify
            amount_from_nano = Amount.from_nano_pac(nano_pac)
            self.assertEqual(amount, amount_from_nano)
            self.assertAlmostEqual(back_to_pac, pac_value, places=9)


if __name__ == "__main__":
    unittest.main()
