import unittest

from pactus.crypto.address import Address
from pactus.crypto.bls import PrivateKey
from pactus.transaction import Transaction
from pactus.transaction.payload import PayloadType
from pactus.types.amount import Amount
from pactus.types.height import Height


class TestTransaction(unittest.TestCase):
    def test_sign_transfer(self):
        prv_str = "SECRET1PDRWTLP5PX0FAHDX39GXZJP7FKZFALML0D5U9TT9KVQHDUC99CMGQQJVK67"
        prv = PrivateKey.from_string(prv_str)
        sender = Address.from_string("pc1z5x2a0lkt5nrrdqe0rkcv6r4pfkmdhrr3mawvua")
        receiver = Address.from_string("pc1zt6qcdymkk48c5ds0fzfsaf6puwu8w8djn3ffpn")
        amount = Amount.from_pac(1.0)  # 1 PAC
        fee = Amount.from_pac(0.001)  # 0.001 PAC
        lock_time = Height(0x123456)
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


class TestTransactionDecode(unittest.TestCase):
    def test_decode_transfer_tx(self):
        # https://pactusscan.com/transaction/1b6b7226f7935a15f05371d1a1fefead585a89704ce464b7cc1d453d299d235f
        signed_data_hex = (
            "000124a3230080ade2040b77616c6c65742d636f726501"
            "037098338e0b6808119dfd4457ab806b9c2059b89b"
            "037a14ae24533816e7faaa6ed28fcdde8e55a7df21"
            "8084af5f"
            "4ed8fee3d8992e82660dd05bbe8608fc56ceabffdeeee61e3213b9b49d33a0fc"
            "8dea6d79ee7ec60f66433f189ed9b3c50b2ad6fa004e26790ee736693eda8506"
            "95794161374b22c696dabb98e93f6ca9300b22f3b904921fbf560bb72145f4fa"
        )
        expected_txid = "1b6b7226f7935a15f05371d1a1fefead585a89704ce464b7cc1d453d299d235f"
        expected_sign_bytes = (
            "0124a3230080ade2040b77616c6c65742d636f726501"
            "037098338e0b6808119dfd4457ab806b9c2059b89b"
            "037a14ae24533816e7faaa6ed28fcdde8e55a7df21"
            "8084af5f"
        )

        raw = bytes.fromhex(signed_data_hex)
        tx, _ = Transaction.decode(raw)

        self.assertEqual(tx.version, 1)
        self.assertEqual(tx.lock_time.value, 2335524)
        self.assertEqual(tx.fee.value, 10000000)
        self.assertEqual(tx.memo, "wallet-core")
        self.assertEqual(tx.payload.get_type(), PayloadType.TRANSFER)

        # Transfer payload fields
        pld = tx.payload
        self.assertEqual(
            pld.sender.string(),
            "pc1rwzvr8rstdqypr80ag3t6hqrtnss9nwymcxy3lr",
        )
        self.assertEqual(
            pld.receiver.string(),
            "pc1r0g22ufzn8qtw0742dmfglnw73e260hep0k3yra",
        )
        self.assertEqual(pld.amount.value, 200000000)

        # Signature and public key
        self.assertIsNotNone(tx.signature)
        self.assertIsNotNone(tx.public_key)

        # Transaction ID
        self.assertEqual(str(tx.id()), expected_txid)

        # Sign bytes
        self.assertEqual(tx.sign_bytes().hex(), expected_sign_bytes)

    def test_decode_bond_tx(self):
        # https://pactusscan.com/transaction/f83f583a5c40adf93a90ea536a7e4b467d30ca4f308d5da52624d80c42adec80
        signed_data_hex = (
            "00015ca3230080ade2040b77616c6c65742d636f726502"
            "037098338e0b6808119dfd4457ab806b9c2059b89b"
            "01d2fa2a7d560502199995ea260954f064d90278be"
            "00"
            "8094ebdc03"
            "9e6279fb64067c7d7316ac74630bbb8589df268aa4548f1c7d85c087a8748ff0"
            "715b9149afbd94c5d8ee6b37c787ec63e963cbb38be513ebc436aa58f9a8f00d"
            "95794161374b22c696dabb98e93f6ca9300b22f3b904921fbf560bb72145f4fa"
        )
        expected_txid = "f83f583a5c40adf93a90ea536a7e4b467d30ca4f308d5da52624d80c42adec80"
        expected_sign_bytes = (
            "015ca3230080ade2040b77616c6c65742d636f726502"
            "037098338e0b6808119dfd4457ab806b9c2059b89b"
            "01d2fa2a7d560502199995ea260954f064d90278be"
            "00"
            "8094ebdc03"
        )

        raw = bytes.fromhex(signed_data_hex)
        tx, _ = Transaction.decode(raw)

        self.assertEqual(tx.version, 1)
        self.assertEqual(tx.lock_time.value, 2335580)
        self.assertEqual(tx.fee.value, 10000000)
        self.assertEqual(tx.memo, "wallet-core")
        self.assertEqual(tx.payload.get_type(), PayloadType.BOND)

        # Bond payload fields
        pld = tx.payload
        self.assertEqual(
            pld.sender.string(),
            "pc1rwzvr8rstdqypr80ag3t6hqrtnss9nwymcxy3lr",
        )
        self.assertEqual(
            pld.receiver.string(),
            "pc1p6taz5l2kq5ppnxv4agnqj48svnvsy797xpe6wd",
        )
        self.assertEqual(pld.stake.value, 1000000000)
        self.assertIsNone(pld.public_key)

        # Signature and public key
        self.assertIsNotNone(tx.signature)
        self.assertIsNotNone(tx.public_key)

        # Transaction ID
        self.assertEqual(str(tx.id()), expected_txid)

        # Sign bytes
        self.assertEqual(tx.sign_bytes().hex(), expected_sign_bytes)


if __name__ == "__main__":
    unittest.main()
