import unittest

from pactus.crypto.secp256k1 import PrivateKey as Secp256k1PrivateKey
from pactus.crypto.secp256k1 import PublicKey as Secp256k1PublicKey
from pactus.crypto.secp256k1 import Signature as Secp256k1Signature
from pactus.crypto import Address


class TestSecp256k1Crypto(unittest.TestCase):
    def test_encoding(self):
        prv_data = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
        pub_data = "036d6caac248af96f6afa7f904f550253a0f3ef3f5aa2fe6838a95b216691468e2"
        addr_data = "042bc1db7e0797c45b918dc401093c9257c6012b4c"

        prv_str = "SECRET1YQQQSYQCYQ5RQWZQFPG9SCRGWPUGPZYSNZS23V9CCRYDPK8QARC0SPVXU8Z"
        pub_str = "public1yqdkke2kzfzheda405lusfa2sy5aq70hn7k4zle5r322my9nfz35wyfamrfs"
        addr_str = "pc1y90qakls8jlz9hyvdcsqsj0yj2lrqz26vqu7l0z"

        prv = Secp256k1PrivateKey.from_string(prv_str)
        pub = Secp256k1PublicKey.from_string(pub_str)
        addr = Address.from_string(addr_str)

        self.assertEqual(prv_data, prv.raw_bytes().hex())
        self.assertEqual(pub_data, pub.raw_bytes().hex())
        self.assertEqual(addr_data, addr.raw_bytes().hex())

        msg = b"pactus"
        sig = Secp256k1Signature.from_string(
            "16e6f8bcdb92964a35773aae200628a5b470b6488d42ceef6538da0b4ffd3b42098dd821eea96f66ba02c9c4473443ab51c411ab78adfbb90d53b07ca1d6862b"
        )

        self.assertTrue(pub.verify(msg, sig))
        self.assertEqual(sig.raw_bytes(), prv.sign(msg).raw_bytes())
        self.assertEqual(pub.raw_bytes(), prv.public_key().raw_bytes())
        self.assertEqual(addr.raw_bytes(), pub.account_address().raw_bytes())

    def test_sign_and_verify(self):
        prv1 = Secp256k1PrivateKey.random()
        prv2 = Secp256k1PrivateKey.random()
        pub1 = prv1.public_key()
        pub2 = prv2.public_key()

        msg = b"pactus"
        sig1 = prv1.sign(msg)
        sig2 = prv2.sign(msg)

        self.assertTrue(pub1.verify(msg, sig1))
        self.assertTrue(pub2.verify(msg, sig2))
        self.assertFalse(pub1.verify(msg, sig2))
        self.assertFalse(pub2.verify(msg, sig1))

        # Verify a signature for a different message is rejected
        different_msg = b"different"
        sig3 = prv1.sign(different_msg)
        self.assertFalse(pub1.verify(msg, sig3))

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
