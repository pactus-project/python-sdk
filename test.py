import unittest
import public_key
import private_key
import signature
from address import Address
from serializer import append_fixed_bytes, append_uint32, append_uint8, append_var_int

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
        pub = prv.public_key()
        msg = b"zarb"
        sig = prv.sign(msg)
        expected_sig = signature.Signature.from_string("ad0f88cec815e9b8af3f0136297cb242ed8b6369af723fbdac077fa927f5780db7df47c77fb53f3a22324673f000c792")

        self.assertEqual(sig.string(), expected_sig.string())
        self.assertTrue(pub.verify(msg, sig))
        self.assertFalse(pub.verify(b"foo", sig))


class TestSerialization(unittest.TestCase):
    def test_var_int(self):
        tests = [
            (0x0, b"\x00"),
            (0xff, b"\xff\x01"),
            (0x7fff, b"\xff\xff\x01"),
            (0x3fffff, b"\xff\xff\xff\x01"),
            (0x1fffffff, b"\xff\xff\xff\xff\x01"),
            (0xfffffffff, b"\xff\xff\xff\xff\xff\x01"),
            (0x7ffffffffff, b"\xff\xff\xff\xff\xff\xff\x01"),
            (0x3ffffffffffff, b"\xff\xff\xff\xff\xff\xff\xff\x01"),
            (0x1ffffffffffffff, b"\xff\xff\xff\xff\xff\xff\xff\xff\x01"),
            (0xffffffffffffffff, b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01"),
            (0x200, b"\x80\x04"),
            (0x027f, b"\xff\x04"),
            (0xff00000000, b"\x80\x80\x80\x80\xf0\x1f"),
            (0xffffffff, b"\xff\xff\xff\xff\x0f"),
            (0x100000000, b"\x80\x80\x80\x80\x10"),
            (0x7ffffffff, b"\xff\xff\xff\xff\x7f"),
            (0x800000000, b"\x80\x80\x80\x80\x80\x01"),
        ]

        for i, (value, expected_bytes) in enumerate(tests):
            buf = b""
            buf = append_var_int(buf, value)
            self.assertEqual(buf, expected_bytes, f"WriteVarInt test {i}")

class TestTransferTx(unittest.TestCase):
    def test_sign_tx(self):
        prv_str = "SECRET1PDRWTLP5PX0FAHDX39GXZJP7FKZFALML0D5U9TT9KVQHDUC99CMGQQJVK67"
        prv = private_key.PrivateKey.from_string(prv_str)
        pub = prv.public_key()
        sender = Address.from_string("pc1z5x2a0lkt5nrrdqe0rkcv6r4pfkmdhrr3mawvua")
        receiver = Address.from_string("pc1zt6qcdymkk48c5ds0fzfsaf6puwu8w8djn3ffpn")
        flags = 0
        version = 1
        amount = 1_000_000_000 # 1 PAC
        fee = 100_000
        lock_time = 0x123456

        buf = []
        append_uint8(buf, flags)
        append_uint8(buf, version)
        append_uint32(buf, lock_time)
        append_var_int(buf, fee)
        append_uint8(buf, 0) # TODO: append_string()
        append_uint8(buf, 1) # Transfer payload
        append_fixed_bytes(buf, sender.bytes())
        append_fixed_bytes(buf, receiver.bytes())
        append_var_int(buf, amount)

        # print(bytes(buf).hex())

        sig = prv.sign(bytes(buf[1:])) # ignore flags

        append_fixed_bytes(buf, sig.bytes())
        append_fixed_bytes(buf, pub.bytes())

        expected_data = (
            "00"        # Flags
            "01"        # Version
            "56341200"  # LockTime
            "a08d06"    # Fee
            "00"        # Memo
            "01" +      # PayloadType
            "02a195d7fecba4c636832f1db0cd0ea14db6db8c71" + # Sender
            "025e81869376b54f8a360f48930ea741e3b8771db2" + # Receiver
            "8094ebdc03" +  # Amount
            "b02ab7af4a42b9f8a1a50c624019a541e58663323d9ee0e1aba3582e76bf69e9f256fd638d98e94bf5fc26a8dfa5eed4"  # Signature
            "af0f74917f5065af94727ae9541b0ddcfb5b828a9e016b02498f477ed37fb44d5d882495afb6fd4f9773e4ea9deee436"  # Public Key
            "030c4d61c6e3a1151585e1d838cae1444a438d089ce77e10c492a55f6908125c5be9b236a246e4082d08de564e111e65") # Public Key

        self.maxDiff = None
        self.assertEqual(expected_data, bytes(buf).hex())


if __name__ == '__main__':
    unittest.main()