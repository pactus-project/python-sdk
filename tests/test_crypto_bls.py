import unittest

from pactus.crypto.bls import PrivateKey as BLSPrivateKey
from pactus.crypto.bls import PublicKey as BLSPublicKey
from pactus.crypto.bls import Signature as BLSSignature
from pactus.crypto import Address


class TestBLSCrypto(unittest.TestCase):
    def test_encoding(self):
        prv_data = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
        pub_data = "a7290fc800d2d14f2dc5e5cb416bebf3267dfed1c6c3a79c6edc4ebd1e657d956daa06a2fcaafd42c94b65b32d4d43ea1368f861006829c475b7d54763a502dfd717e9d51c5cc7deae2981e56090a821c9c5bcafc129b8599203ab99031f4ce7"
        val_addr_data = "01c40b914373d4fc9c1e4611ad0acd5f23abf58a0d"
        acc_addr_data = "02c40b914373d4fc9c1e4611ad0acd5f23abf58a0d"

        prv_str = "SECRET1PQQQSYQCYQ5RQWZQFPG9SCRGWPUGPZYSNZS23V9CCRYDPK8QARC0SEZYD4L"
        pub_str = "public1p5u5sljqq6tg57tw9uh95z6lt7vn8mlk3cmp608rwm38t68n90k2km2sx5t724l2ze99ktvedf4p75ymglpssq6pfc36m0428vwjs9h7hzl5a28zucl02u2vpu4sfp2ppe8zmet7p9xu9nysr4wvsx86vuujrva2z"
        val_addr_str = "pc1pcs9ezsmn6n7fc8jxzxks4n2lyw4ltzsdc9v8qn"
        acc_addr_str = "pc1zcs9ezsmn6n7fc8jxzxks4n2lyw4ltzsd9wu6hw"

        prv = BLSPrivateKey.from_string(prv_str)
        pub = BLSPublicKey.from_string(pub_str)
        val_addr = Address.from_string(val_addr_str)
        acc_addr = Address.from_string(acc_addr_str)

        self.assertEqual(prv_data, prv.raw_bytes().hex())
        self.assertEqual(pub_data, pub.raw_bytes().hex())
        self.assertEqual(val_addr_data, val_addr.raw_bytes().hex())
        self.assertEqual(acc_addr_data, acc_addr.raw_bytes().hex())

        msg = b"pactus"
        sig = BLSSignature.from_string(
            "8bdda74336efdf43b428a3811d3d6867a19e20889c91261b02a6b950b130f5bb22621394667c27660bfed2a8719d9c52"
        )

        self.assertTrue(pub.verify(msg, sig))
        self.assertEqual(sig.raw_bytes(), prv.sign(msg).raw_bytes())
        self.assertEqual(pub.raw_bytes(), prv.public_key().raw_bytes())
        self.assertEqual(val_addr.raw_bytes(), pub.validator_address().raw_bytes())
        self.assertEqual(acc_addr.raw_bytes(), pub.account_address().raw_bytes())

    def test_sign_and_verify(self):
        prv1 = BLSPrivateKey.random()
        prv2 = BLSPrivateKey.random()
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
        prv = BLSPrivateKey.random()
        pub = prv.public_key()

        msg = b"pactus"
        sig1 = prv.sign(msg)
        sig2 = prv.sign(msg)

        # Both signatures should verify
        self.assertTrue(pub.verify(msg, sig1))
        self.assertTrue(pub.verify(msg, sig2))

        self.assertEqual(sig1.raw_bytes(), sig2.raw_bytes())

    def test_key_gen(self):
        tests = [
            {"ikm": "", "sk": "Err"},
            {
                "ikm": "00000000000000000000000000000000000000000000000000000000000000",
                "sk": "Err",
            },
            {
                "ikm": "0000000000000000000000000000000000000000000000000000000000000000",
                "sk": "4d129a19df86a0f5345bad4cc6f249ec2a819ccc3386895beb4f7d98b3db6235",
            },
            {
                "ikm": "2b1eb88002e83a622792d0b96d4f0695e328f49fdd32480ec0cf39c2c76463af",
                "sk": "0000f678e80740072a4a7fe8c7344db88a00ccc7db36aa51fa51f9c68e561584",
            },
            # Test vectors from EIP-2333
            {
                "ikm": "c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e5349553"
                "1f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04",
                "sk": "0d7359d57963ab8fbbde1852dcf553fedbc31f464d80ee7d40ae683122b45070",
            },
            {
                "ikm": "3141592653589793238462643383279502884197169399375105820974944592",
                "sk": "41c9e07822b092a93fd6797396338c3ada4170cc81829fdfce6b5d34bd5e7ec7",
            },
            {
                "ikm": "0099FF991111002299DD7744EE3355BBDD8844115566CC55663355668888CC00",
                "sk": "3cfa341ab3910a7d00d933d8f7c4fe87c91798a0397421d6b19fd5b815132e80",
            },
            {
                "ikm": "d4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3",
                "sk": "2a0e28ffa5fbbe2f8e7aad4ed94f745d6bf755c51182e119bb1694fe61d3afca",
            },
        ]

        for i, test in enumerate(tests):
            ikm = bytes.fromhex(test["ikm"])
            try:
                sk = BLSPrivateKey.key_gen(ikm)
                if test["sk"] == "Err":
                    self.fail(f"Test '{i}' failed. Expected an error, but got none.")
                else:
                    expected_sk = bytes.fromhex(test["sk"])
                    self.assertEqual(
                        sk.raw_bytes(),
                        expected_sk,
                        f"Test '{i}' failed. Expected '{expected_sk}', but got '{sk.raw_bytes()}'.",
                    )
            except Exception as e:
                if test["sk"] != "Err":
                    self.fail(f"Test '{i}' failed. Unexpected error: {e}")

    def test_aggregate_sig(self):
        sig1 = BLSSignature.from_string(
            "923d67a8624cbb7972b29328e15ec76cc846076ccf00a9e94d991c677846f334ae4ba4551396fbcd6d1cab7593baf3b7"
        )
        sig2 = BLSSignature.from_string(
            "ab025936daaed80ca2f85a418c8a47c3d9f4137d7b7651ca52646260d2018e55628bba118d4993a3aa75de268d55e72b"
        )

        agg = BLSSignature.aggregate([sig1, sig2])
        self.assertEqual(
            agg.string(),
            "ad747172697127cb08dda29a386e106eb24ab0edfbc044014c3bd7a5f583cc38b3a223ff2c1df9c0b4df110630e6946b",
        )

    def test_aggregate_pub(self):
        pub1 = BLSPublicKey.from_string(
            "public1p4u8hfytl2pj6l9rj0t54gxcdmna4hq52ncqkkqjf3arha5mlk3x4mzpyjkhmdl20jae7f65aamjrvqcvf4sudcapz52ctcwc8r9wz3z2gwxs38880cgvfy49ta5ssyjut05myd4zgmjqstggmetyuyg7v5jhx47a"
        )
        pub2 = BLSPublicKey.from_string(
            "public1pkms34vh00p0jwpdrv6hpqzsx3u26v547948h38wzpp0vc7j408sdy5cql5w5s4rpz60jnzm8rqw4crcw00lgrjeqydpagwstfgdfd79p9yr6rlrr2edtjaqp0shreqxmx0sk4gwlz336hyvnzh7lquxgwcw5nynk"
        )

        agg = BLSPublicKey.aggregate([pub1, pub2])
        self.assertEqual(
            agg.string(),
            "public1pk5pfgdfe9l6q8mc03wfksx2l4r0h3hrx309sjcyuaredzh5krsfh8a86fuk0kcv2nslcduwz3w0zyqlvv2d42ne04c87hha5dw7dc9r2au5l7vhrruud7wf9u5k4fzg5rma6n940uqgfpjph8d9yg20dzswk7wxj",
        )


if __name__ == "__main__":
    unittest.main()
