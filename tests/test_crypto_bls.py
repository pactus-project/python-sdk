import unittest

from pactus.crypto.bls.private_key import PrivateKey as BLSPrivateKey
from pactus.crypto.bls.public_key import PublicKey as BLSPublicKey
from pactus.crypto.bls.signature import Signature as BLSSignature


class TestBLSCrypto(unittest.TestCase):
    def test_private_key_to_public_key(self):
        prv_str = "SECRET1PDRWTLP5PX0FAHDX39GXZJP7FKZFALML0D5U9TT9KVQHDUC99CMGQQJVK67"
        expected_pub_str = "public1p4u8hfytl2pj6l9rj0t54gxcdmna4hq52ncqkkqjf3arha5mlk3x4mzpyjkhmdl20jae7f65aamjrvqcvf4sudcapz52ctcwc8r9wz3z2gwxs38880cgvfy49ta5ssyjut05myd4zgmjqstggmetyuyg7v5jhx47a"

        prv = BLSPrivateKey.from_string(prv_str)
        pub = prv.public_key()
        pub_str = pub.string()

        self.assertEqual(pub_str, expected_pub_str)

    def test_public_key_to_address(self):
        pub_str = "public1p4u8hfytl2pj6l9rj0t54gxcdmna4hq52ncqkkqjf3arha5mlk3x4mzpyjkhmdl20jae7f65aamjrvqcvf4sudcapz52ctcwc8r9wz3z2gwxs38880cgvfy49ta5ssyjut05myd4zgmjqstggmetyuyg7v5jhx47a"
        expected_acc_addr_str = "pc1z5x2a0lkt5nrrdqe0rkcv6r4pfkmdhrr3mawvua"
        expected_val_addr_str = "pc1p5x2a0lkt5nrrdqe0rkcv6r4pfkmdhrr3xk73tq"

        pub = BLSPublicKey.from_string(pub_str)
        acc_add_str = pub.account_address().string()
        val_add_str = pub.validator_address().string()

        self.assertEqual(acc_add_str, expected_acc_addr_str)
        self.assertEqual(val_add_str, expected_val_addr_str)

    def test_sign(self):
        prv_str = "SECRET1PDRWTLP5PX0FAHDX39GXZJP7FKZFALML0D5U9TT9KVQHDUC99CMGQQJVK67"
        prv = BLSPrivateKey.from_string(prv_str)
        prv.public_key()
        msg = b"pactus"
        prv.sign(msg)
        BLSSignature.from_string(
            "923d67a8624cbb7972b29328e15ec76cc846076ccf00a9e94d991c677846f334ae4ba4551396fbcd6d1cab7593baf3b7"
        )

        # self.assertEqual(sig.string(), expected_sig.string())
        # self.assertTrue(pub.verify(msg, sig))
        # self.assertFalse(pub.verify(b"foo", sig))

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
