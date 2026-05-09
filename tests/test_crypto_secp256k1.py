import unittest

from pactus.crypto.secp256k1 import PrivateKey as Secp256k1PrivateKey
from pactus.crypto.secp256k1 import PublicKey as Secp256k1PublicKey
from pactus.crypto.secp256k1 import Signature as Secp256k1Signature


class TestSecp256k1Crypto(unittest.TestCase):
    def test_private_key_to_public_key(self):
        prv_str = "secret1yqyqszqgpqyqszqgpqyqszqgpqyqszqgpqyqszqgpqyqszqgpqyqsd25y3e"
        expected_pub_str = (
            "public1yqvdcf32k0vfxgsyet5ldt246q4jaw8scx3sysx0lnstlt6w4m5rc7k3ysjp"
        )

        prv = Secp256k1PrivateKey.from_string(prv_str)
        pub = prv.public_key()
        pub_str = pub.string()

        self.assertEqual(pub_str, expected_pub_str)

    def test_public_key_to_address(self):
        pub_str = "public1yqvdcf32k0vfxgsyet5ldt246q4jaw8scx3sysx0lnstlt6w4m5rc7k3ysjp"
        expected_acc_addr_str = "pc1yj7ag28h54jf4e09nnednjhgmg60srnvj7uu39v"

        pub = Secp256k1PublicKey.from_string(pub_str)
        acc_add_str = pub.account_address().string()

        self.assertEqual(acc_add_str, expected_acc_addr_str)

    def test_sign_and_verify(self):
        prv_str = "secret1yqyqszqgpqyqszqgpqyqszqgpqyqszqgpqyqszqgpqyqszqgpqyqsd25y3e"
        prv = Secp256k1PrivateKey.from_string(prv_str)
        pub = prv.public_key()
        msg = b"pactus"
        sig = prv.sign(msg)

        # Verify the signature is correct length (64 bytes)
        self.assertEqual(len(sig.raw_bytes()), 64)

        # Verify the signature verifies correctly
        self.assertTrue(pub.verify(msg, sig))

        # Verify an invalid signature is rejected
        invalid_sig_bytes = b"\x00" * 64
        invalid_sig = Secp256k1Signature.from_string(invalid_sig_bytes.hex())
        self.assertFalse(pub.verify(msg, invalid_sig))

        # Verify a signature for a different message is rejected
        different_msg = b"different"
        sig2 = prv.sign(different_msg)
        self.assertFalse(pub.verify(msg, sig2))

    def test_key_generation(self):
        # Test random key generation
        prv = Secp256k1PrivateKey.random()
        self.assertIsNotNone(prv)

        # Test that we can derive public key from random private key
        pub = prv.public_key()
        self.assertIsNotNone(pub)

        # Test that we can sign and verify with random key
        msg = b"test message"
        sig = prv.sign(msg)
        self.assertTrue(pub.verify(msg, sig))

    def test_key_from_bytes(self):
        # Test creating private key from bytes
        key_bytes = b"\x01" * 32
        prv = Secp256k1PrivateKey.from_bytes(key_bytes)
        self.assertEqual(prv.raw_bytes(), key_bytes)

        # Test that the same bytes produce the same public key
        prv2 = Secp256k1PrivateKey.from_bytes(key_bytes)
        pub1 = prv.public_key()
        pub2 = prv2.public_key()
        self.assertEqual(pub1.string(), pub2.string())

    def test_string_encoding_decoding(self):
        # Test private key string encoding/decoding
        prv = Secp256k1PrivateKey.random()
        prv_str = prv.string()
        prv_decoded = Secp256k1PrivateKey.from_string(prv_str)
        self.assertEqual(prv.raw_bytes(), prv_decoded.raw_bytes())

        # Test public key string encoding/decoding
        pub = prv.public_key()
        pub_str = pub.string()
        pub_decoded = Secp256k1PublicKey.from_string(pub_str)
        self.assertEqual(pub.raw_bytes(), pub_decoded.raw_bytes())

    def test_signature_from_string(self):
        # Test signature creation from hex string
        sig_hex = "a" * 128  # 64 bytes = 128 hex chars
        sig = Secp256k1Signature.from_string(sig_hex)
        self.assertEqual(len(sig.raw_bytes()), 64)
        self.assertEqual(sig.string(), sig_hex)

    def test_signature_invalid_length(self):
        # Test that invalid signature length raises error
        with self.assertRaises(ValueError):
            Secp256k1Signature.from_string("00" * 32)  # Too short

        with self.assertRaises(ValueError):
            Secp256k1Signature.from_string("00" * 100)  # Too long

    def test_private_key_invalid_string(self):
        # Test that invalid private key string raises error
        with self.assertRaises(ValueError):
            # Wrong HRP
            Secp256k1PrivateKey.from_string(
                "invalid1yqyqszqgpqyqszqgpqyqszqgpqyqszqgpqyqszqgpqyqszqgpqyqsd25y3e"
            )

        with self.assertRaises(ValueError):
            # Wrong type
            Secp256k1PrivateKey.from_string(
                "secret1ry2cqw5yfhmr7ve8nctgzg6wgcyc73xqr2uud486jgsq7wu253egsx6msep"
            )

    def test_public_key_invalid_string(self):
        # Test that invalid public key string raises error
        with self.assertRaises(ValueError):
            # Wrong HRP
            Secp256k1PublicKey.from_string(
                "invalid1yqvdcf32k0vfxgsyet5ldt246q4jaw8scx3sysx0lnstlt6w4m5rc7k3ysjp"
            )

        with self.assertRaises(ValueError):
            # Wrong type
            Secp256k1PublicKey.from_string(
                "public1ry2cqw5yfhmr7ve8nctgzg6wgcyc73xqr2uud486jgsq7wu253egsx6msep"
            )

    def test_multiple_signatures(self):
        # Test that multiple signatures for the same message and key are deterministic
        # (secp256k1 library uses deterministic signing with RFC 6979)
        prv = Secp256k1PrivateKey.random()
        pub = prv.public_key()
        msg = b"same message"

        sig1 = prv.sign(msg)
        sig2 = prv.sign(msg)

        # Both signatures should verify
        self.assertTrue(pub.verify(msg, sig1))
        self.assertTrue(pub.verify(msg, sig2))

        # Signatures should be deterministic (same message + same key = same signature)
        self.assertEqual(sig1.string(), sig2.string())


if __name__ == "__main__":
    unittest.main()
