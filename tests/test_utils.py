import unittest
from pactus.utils import utils


class TestEvaluatePolynomial(unittest.TestCase):
    def test_empty_coefficients(self):
        self.assertIsNone(utils.evaluate_polynomial([], 2, 7))

    def test_single_coefficient(self):
        self.assertEqual(utils.evaluate_polynomial([5], 10, 7), 5)

    def test_x_zero(self):
        # f(0) = c[0] % mod
        self.assertEqual(utils.evaluate_polynomial([3, 2, 1], 0, 5), 3 % 5)

    def test_x_one(self):
        # f(1) = sum(c) % mod
        self.assertEqual(utils.evaluate_polynomial([1, 2, 3], 1, 7), (1 + 2 + 3) % 7)

    def test_multiple_coefficients(self):
        # f(2) = 1 + 2*2 + 3*2^2 = 1 + 4 + 12 = 17 % 5 = 2
        self.assertEqual(utils.evaluate_polynomial([1, 2, 3], 2, 5), 2)

    def test_negative_coefficients(self):
        # f(2) = -1 + 2*2 + (-3)*2^2 = -1 + 4 - 12 = -9 % 7 = 5
        self.assertEqual(utils.evaluate_polynomial([-1, 2, -3], 2, 7), 5)

    def test_negative_x(self):
        # f(-1) = 2 + 3*(-1) + 4*(-1)^2 = 2 - 3 + 4 = 3 % 6 = 3
        self.assertEqual(utils.evaluate_polynomial([2, 3, 4], -1, 6), 3)

    def test_large_modulus(self):
        # f(3) = 2 + 4*3 + 5*9 = 2 + 12 + 45 = 59 % 1000 = 59
        self.assertEqual(utils.evaluate_polynomial([2, 4, 5], 3, 1000), 59)

    def test_modulus_one(self):
        # Any value mod 1 is 0
        self.assertEqual(utils.evaluate_polynomial([1, 2, 3], 5, 1), 0)

    def test_wikipedia_example(self):
        # https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing
        self.assertEqual(utils.evaluate_polynomial([1234, 166, 94], 1, 2 ** 127 - 1), 1494)
        self.assertEqual(utils.evaluate_polynomial([1234, 166, 94], 2, 2 ** 127 - 1), 1942)
        self.assertEqual(utils.evaluate_polynomial([1234, 166, 94], 3, 2 ** 127 - 1), 2578)
        self.assertEqual(utils.evaluate_polynomial([1234, 166, 94], 4, 2 ** 127 - 1), 3402)
        self.assertEqual(utils.evaluate_polynomial([1234, 166, 94], 5, 2 ** 127 - 1), 4414)
        self.assertEqual(utils.evaluate_polynomial([1234, 166, 94], 6, 2 ** 127 - 1), 5614)


if __name__ == "__main__":
    unittest.main()