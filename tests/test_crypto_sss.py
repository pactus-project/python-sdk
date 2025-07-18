import unittest
from pactus.crypto.sss import sss


class TestEvaluatePolynomial(unittest.TestCase):
    def test_wikipedia_example(self):
        # https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing
        self.assertEqual(sss._eval_at([1234, 166, 94], 1, 2**127 - 1), 1494)
        self.assertEqual(sss._eval_at([1234, 166, 94], 2, 2**127 - 1), 1942)
        self.assertEqual(sss._eval_at([1234, 166, 94], 3, 2**127 - 1), 2578)
        self.assertEqual(sss._eval_at([1234, 166, 94], 4, 2**127 - 1), 3402)
        self.assertEqual(sss._eval_at([1234, 166, 94], 5, 2**127 - 1), 4414)
        self.assertEqual(sss._eval_at([1234, 166, 94], 6, 2**127 - 1), 5614)


class TestRecover(unittest.TestCase):
    def test_recover_secret_1(self):
        shares = [(1, 1494), (2, 1942), (3, 2578)]
        prime = 2**127 - 1
        self.assertEqual(sss.recover_secret(shares, prime), 1234)

    def test_recover_secret_2(self):
        shares = [(1, 1494), (3, 2578), (6, 5614)]
        prime = 2**127 - 1
        self.assertEqual(sss.recover_secret(shares, prime), 1234)


if __name__ == "__main__":
    unittest.main()
