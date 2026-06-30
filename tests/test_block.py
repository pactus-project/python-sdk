import unittest

from pactus.block import Block
from pactus.crypto.address import AddressType
from pactus.transaction.payload import PayloadType


class TestBlockDecode(unittest.TestCase):
    def test_decode_block_from_raw(self):
        raw_hex = (
            "019094b165"
            "84fdb8aac442735c6d4d4457e2236cd6ca86cb0b898ab37a03be1723b8faac55"
            "d24bf4f116090735a366d1818ec48f5d91b4ff1deab091ecef5fc8bbae94cdd5"
            "a50eac535372c874d7150a60cb8a988dde1a60b7ebda1729cc14f6d4d2575ed4"
            "b72089c36ffe9f7ecc60d8be09912feb"
            "010c4cbdcae2ba23a3335f994eaaf104a4f53981a2"
            "770300000000040001020300"
            "8da0b181eaa433b5c9855a89de0f0c7530ec4d2c3aecff290af7ae02b33dd968"
            "43d6f72983bf25ce856946df1360710f"
            "0102017803000000000100"
            "020c8ce957b484397ab248c25ce135e2d0aff0c8e48094ebdc03"
        )

        raw = bytes.fromhex(raw_hex)
        block = Block.decode(raw)

        # --- Header ---
        h = block.header
        self.assertEqual(h.version, 1)
        self.assertEqual(h.unix_time, 1706136720)
        self.assertEqual(
            str(h.prev_block_hash),
            "84fdb8aac442735c6d4d4457e2236cd6ca86cb0b898ab37a03be1723b8faac55",
        )
        self.assertEqual(
            str(h.state_root),
            "d24bf4f116090735a366d1818ec48f5d91b4ff1deab091ecef5fc8bbae94cdd5",
        )
        self.assertEqual(
            h.sortition_seed.hex(),
            "a50eac535372c874d7150a60cb8a988dde1a60b7ebda1729cc14f6d4d2575ed4"
            "b72089c36ffe9f7ecc60d8be09912feb",
        )
        self.assertEqual(h.proposer_address.address_type(), AddressType.VALIDATOR)
        self.assertEqual(
            h.proposer_address.raw_bytes().hex(),
            "010c4cbdcae2ba23a3335f994eaaf104a4f53981a2",
        )
        self.assertEqual(
            h.proposer_address.string(),
            "pc1pp3xtmjhzhg36xv6ln9824ugy5n6nnqdzugzu3j",
        )

        # --- Certificate ---
        cert = block.prev_cert
        self.assertIsNotNone(cert)
        self.assertEqual(cert.height.value, 887)
        self.assertEqual(cert.round.value, 0)
        self.assertEqual(cert.committers, [0, 1, 2, 3])
        self.assertEqual(cert.absentees, [])
        self.assertEqual(
            cert.signature.string(),
            "8da0b181eaa433b5c9855a89de0f0c7530ec4d2c3aecff290af7ae02b33dd968"
            "43d6f72983bf25ce856946df1360710f",
        )

        # --- Transactions ---
        self.assertEqual(len(block.transactions), 1)

        tx = block.transactions[0]
        self.assertEqual(tx.version, 1)
        self.assertEqual(tx.flags, 0x02)  # FLAG_NOT_SIGNED
        self.assertEqual(tx.lock_time.value, 888)
        self.assertEqual(tx.fee.value, 0)
        self.assertEqual(tx.memo, "")
        self.assertEqual(tx.payload.get_type(), PayloadType.TRANSFER)

        # Subsidy transaction: signer is treasury address
        self.assertTrue(tx.payload.signer().is_treasury_address())
        self.assertEqual(tx.signature, None)
        self.assertEqual(tx.public_key, None)

        self.assertEqual(tx.payload.amount.value, 1_000_000_000)
        self.assertEqual(
            tx.payload.receiver.string(),
            "pc1zpjxwj4a5ssuh4vjgcfwwzd0z6zhlpj8ylnhdl8",
        )


if __name__ == "__main__":
    unittest.main()
