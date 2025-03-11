import unittest

from pactus.crypto.address import Address
from pactus.crypto.bls.private_key import PrivateKey
from pactus.transaction.transaction import Transaction
from pactus.amount import Amount


class TestTransaction(unittest.TestCase):
    def test_sign_transfer(self):
        prv_str = "SECRET1PDRWTLP5PX0FAHDX39GXZJP7FKZFALML0D5U9TT9KVQHDUC99CMGQQJVK67"
        prv = PrivateKey.from_string(prv_str)
        sender = Address.from_string("pc1z5x2a0lkt5nrrdqe0rkcv6r4pfkmdhrr3mawvua")
        receiver = Address.from_string("pc1zt6qcdymkk48c5ds0fzfsaf6puwu8w8djn3ffpn")
        amount = Amount.from_pac(1.0)  # 1 PAC
        fee = Amount.from_pac(0.001)  # 0.001 PAC
        lock_time = 0x123456
        memo = "test"

        tx = Transaction.create_transfer_tx(
            lock_time, sender, receiver, amount, fee, memo
        )

        signed_data = tx.sign(prv)
        expected_signed_data = (
            "00"  # Flags
            "01"  # Version
            "56341200"  # LockTime
            "c0843d"  # Fee
            "0474657374"  # Memo
            "01"  # PayloadType
            + "02a195d7fecba4c636832f1db0cd0ea14db6db8c71"  # Sender
            + "025e81869376b54f8a360f48930ea741e3b8771db2"  # Receiver
            + "8094ebdc03"  # Amount
            + "a0bac70f3bb937c6ef1ffcc14f7b6e706b9ede00a44541347413db4eb619c2c84d5b38c845dd3f9349c2696409b6c53e"  # Signature
            + "af0f74917f5065af94727ae9541b0ddcfb5b828a9e016b02498f477ed37fb44d5d882495afb6fd4f9773e4ea9deee436"  # Public Key
            + "030c4d61c6e3a1151585e1d838cae1444a438d089ce77e10c492a55f6908125c5be9b236a246e4082d08de564e111e65"
        )
        self.maxDiff = None
        self.assertEqual(expected_signed_data, signed_data.hex())

        sign_bytes = tx.sign_bytes()
        expected_sign_bytes = (
            "01"  # Version
            "56341200"  # LockTime
            "c0843d"  # Fee
            "0474657374"  # Memo
            "01"  # PayloadType
            + "02a195d7fecba4c636832f1db0cd0ea14db6db8c71"  # Sender
            + "025e81869376b54f8a360f48930ea741e3b8771db2"  # Receiver
            + "8094ebdc03"  # Amount
        )
        self.assertEqual(expected_sign_bytes, sign_bytes.hex())


if __name__ == "__main__":
    unittest.main()
