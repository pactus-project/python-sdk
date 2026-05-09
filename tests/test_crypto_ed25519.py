import unittest

from pactus.crypto.ed25519 import PrivateKey as Ed25519PrivateKey
from pactus.crypto.ed25519 import PublicKey as Ed25519PublicKey
from pactus.crypto.ed25519 import Signature as Ed25519Signature
from pactus.crypto import Address


class TestEd25519Crypto(unittest.TestCase):
    def test_encoding(self):
        prv_data = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
        pub_data = "03a107bff3ce10be1d70dd18e74bc09967e4d6309ba50d5f1ddc8664125531b8"
        addr_data = "0396a882c41ef85a07c75a6416a57fcce95aad4a3f"

        prv_str = "SECRET1RQQQSYQCYQ5RQWZQFPG9SCRGWPUGPZYSNZS23V9CCRYDPK8QARC0SW5D8X2"
        pub_str = "public1rqwss00lnecgtu8tsm5vwwj7qn9n7f43snwjs6hcamjrxgyj4xxuq5agu5g"
        addr_str = "pc1rj65g93q7lpdq0366vst22l7va9d26j3l2vr0em"

        prv = Ed25519PrivateKey.from_string(prv_str)
        pub = Ed25519PublicKey.from_string(pub_str)
        addr = Address.from_string(addr_str)

        self.assertEqual(prv_data, prv.raw_bytes().hex())
        self.assertEqual(pub_data, pub.raw_bytes().hex())
        self.assertEqual(addr_data, addr.raw_bytes().hex())

        msg = b"pactus"
        sig = Ed25519Signature.from_string(
            "1fc2c800499342d08242db9c3eb654027cb7b821e6af9ede56dfdb67e824f15bddb419d2db3fd5aaf3ef1a9ebb9a9deb749380f0d6a110cbe95319fe9f794305"
        )

        self.assertTrue(pub.verify(msg, sig))
        self.assertEqual(sig.raw_bytes(), prv.sign(msg).raw_bytes())
        self.assertEqual(pub.raw_bytes(), prv.public_key().raw_bytes())
        self.assertEqual(addr.raw_bytes(), pub.account_address().raw_bytes())

    def test_sign_and_verify(self):
        prv1 = Ed25519PrivateKey.random()
        prv2 = Ed25519PrivateKey.random()
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

    def test_multiple_signatures(self):
        # Test that multiple signatures for the same message and key are deterministic
        prv = Ed25519PrivateKey.random()
        pub = prv.public_key()

        msg = b"pactus"
        sig1 = prv.sign(msg)
        sig2 = prv.sign(msg)

        # Both signatures should verify
        self.assertTrue(pub.verify(msg, sig1))
        self.assertTrue(pub.verify(msg, sig2))

        self.assertEqual(sig1.raw_bytes(), sig2.raw_bytes())


if __name__ == "__main__":
    unittest.main()
