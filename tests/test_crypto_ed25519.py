import unittest

from pactus.crypto.ed25519.private_key import PrivateKey as Ed25519PrivateKey
from pactus.crypto.ed25519.public_key import PublicKey as Ed25519PublicKey
from pactus.crypto.ed25519.signature import Signature as Ed25519Signature


class TestEd25519Crypto(unittest.TestCase):
    def test_private_key_to_public_key(self):
        prv_str = "SECRET1RJ6STNTA7Y3P2QLQF8A6QCX05F2H5TFNE5RSH066KZME4WVFXKE7QW097LG"
        expected_pub_str = (
            "public1ry2cqw5yfhmr7ve8nctgzg6wgcyc73xqr2uud486jgsq7wu253egsx6msep"
        )

        prv = Ed25519PrivateKey.from_string(prv_str)
        pub = prv.public_key()
        pub_str = pub.string()

        self.assertEqual(pub_str, expected_pub_str)

    def test_public_key_to_address(self):
        pub_str = "public1ry2cqw5yfhmr7ve8nctgzg6wgcyc73xqr2uud486jgsq7wu253egsx6msep"
        expected_acc_addr_str = "pc1reer4damrrdxznmrrl7a9acy7x5cwe6dyt8ftv4"

        pub = Ed25519PublicKey.from_string(pub_str)
        acc_add_str = pub.account_address().string()

        self.assertEqual(acc_add_str, expected_acc_addr_str)

    def test_sign(self):
        prv_str = "secret1r0up878rawjec2evjnd4k42a4g4pcardesjk48jtn64qwjnfv7veqal53e2"
        prv = Ed25519PrivateKey.from_string(prv_str)
        pub = prv.public_key()
        msg = b"pactus"
        sig = prv.sign(msg)

        valid_sig = Ed25519Signature.from_string(
            "55eaa9656158874bff726c8d62abe0a5b66d2434705f46b58c905a42f1b39fb95f640fbacac97e6e6862220fe7b4f249a0f79dc3d37b4460156c58580778b70e"
        )

        invalid_sig = Ed25519Signature.from_string(
            "5a61ecb3c08825010678f12c036cec2e1dd1b8767ed9fd95a97f560dfd6196b600fdc7bba22f13eae19ca578b920eb807eb6cd956d55f1d778fee75155d4ea07"
        )

        self.assertTrue(pub.verify(msg, valid_sig))
        self.assertFalse(pub.verify(msg, invalid_sig))
        self.assertEqual(sig.string(), valid_sig.string())
        self.assertEqual(sig.raw_bytes(), valid_sig.raw_bytes())


if __name__ == "__main__":
    unittest.main()
