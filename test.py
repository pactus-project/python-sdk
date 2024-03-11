import unittest
import public_key
import private_key
import signature

class TestCrypto(unittest.TestCase):
    def test_private_key_to_public_key(self):
        prv_str = "SECRET1PDRWTLP5PX0FAHDX39GXZJP7FKZFALML0D5U9TT9KVQHDUC99CMGQQJVK67"
        expected_pub_str = "public1p4u8hfytl2pj6l9rj0t54gxcdmna4hq52ncqkkqjf3arha5mlk3x4mzpyjkhmdl20jae7f65aamjrvqcvf4sudcapz52ctcwc8r9wz3z2gwxs38880cgvfy49ta5ssyjut05myd4zgmjqstggmetyuyg7v5jhx47a"

        prv = private_key.PrivateKey.from_string(prv_str)
        pub = prv.public_key()
        pub_str = pub.string()

        self.assertEqual(pub_str, expected_pub_str)

    def test_public_key_to_address(self):
        pub_str = "public1p4u8hfytl2pj6l9rj0t54gxcdmna4hq52ncqkkqjf3arha5mlk3x4mzpyjkhmdl20jae7f65aamjrvqcvf4sudcapz52ctcwc8r9wz3z2gwxs38880cgvfy49ta5ssyjut05myd4zgmjqstggmetyuyg7v5jhx47a"
        expected_acc_addr_str = "pc1z5x2a0lkt5nrrdqe0rkcv6r4pfkmdhrr3mawvua"
        expected_val_addr_str = "pc1p5x2a0lkt5nrrdqe0rkcv6r4pfkmdhrr3xk73tq"

        pub = public_key.PublicKey.from_string(pub_str)
        acc_add_str = pub.account_address().string()
        val_add_str = pub.validator_address().string()

        self.assertEqual(acc_add_str, expected_acc_addr_str)
        self.assertEqual(val_add_str, expected_val_addr_str)

    def test_sign(self):
        prv_str = "SECRET1PDRWTLP5PX0FAHDX39GXZJP7FKZFALML0D5U9TT9KVQHDUC99CMGQQJVK67"
        prv = private_key.PrivateKey.from_string(prv_str)
        sig = prv.sign(b"zarb")

        expected_sig = "ad0f88cec815e9b8af3f0136297cb242ed8b6369af723fbdac077fa927f5780db7df47c77fb53f3a22324673f000c792"
        print(sig.string())
        self.assertEqual(sig.string(), expected_sig)

if __name__ == '__main__':
    unittest.main()