import unittest

from pactus.block import Block
from pactus.crypto.address import AddressType
from pactus.transaction.payload import PayloadType


class TestBlockDecode(unittest.TestCase):
    def test_decode_block_88888(self):
        raw_hex = (
            "01d802bf65f805b91ce08e5ee84b4707248fd602db5364da6ba9b273a200228ce9c62be4ac"
            "a846b739df34099e5345088e66ded3f63762cc766c5380c58f788fb134c9467c"
            "b366e61d7dc9f9a63d0b4ce69aa1cfc91cc11436eb43220b4db00ac39b8056e47f6ee34f1846"
            "83626ba43a0f85d7d82b01468a4e63084ff773a7750a52872c665b19b1174c375b"
            "010000003324ee0365e004a605ab079403c305910780089406379203b0077622d6049201bd07e"
            "903fb07bf072cc806c8053fc8014a0f81018901a701870835b301cb05850126b101b00120e2"
            "051d5dae05c506d405a10534b502df0400"
            "8a95d277dd80203ca7b964711f819bdd19b9e028f46d3416c43b1f3f28f746936b9c309960b9"
            "6e01fceb4917e6bd95a3"
            "050201385b01000000010002f9682245d323f7c4b72131cd6d0fac6f1cfc6783a0d689dd0301"
            "01375b010000000301a2aa63337fad6bac1936dc563ada569c7a12e2aa93bf4a3be75443b0c7"
            "8e2e342984bb89c55542cb0d1f09c4ec9ebae998f9c42f4d7385261793325fe1cbdd3141c07d"
            "288252f8c291497f04e572d56bcc7997d19f634880d4c9f238e0791f062e5bc64af160b4c976"
            "6c2c2f3cae588314909fe40101375b01000000030127179f1ae3a28030972f30b0a848053a2c"
            "752bedb4bab53872a3d52e40bc04de319b0a92a70f49983379f113502c2e0e34f7321c9b31b4"
            "eb8ce63c623e468e4ba401e6daadd19f9d254e0894b82f50fef40d1b4ad969b26894e43237c6"
            "8b527571418cee783b5821e5f96234a8dcc53fea17266b0101375b01000000030180e9161eaa"
            "d5285558caa382f1eec2d2642c13eeae3698cdedf32d066e1946b2d92881c0378aaa8155ad3b"
            "52de4eeee2d106b4d0ef0bb69f0d6b2e6e8ce573652553bf0eadd458f64081f3c0bd3cec9566"
            "1188a004a5f2ce81d40007238639a2babe6ba4347616b848098094e1c0c4f396196478010137"
            "5b0100a0c21e000202b9abf7f9a0406e4a9f7262b3d3d23d449d161cad0165d2d2c74fb4cc35"
            "09cdd646f4eeefacb1a9cf720080e497d0128c7d2655bfd876417fb7b18efd83374bd9cacebb"
            "990453ba153defd4c41fb97bcc074552307f6c7194aeeb6e10588358"
        )

        raw = bytes.fromhex(raw_hex)
        block = Block.decode(raw)

        # --- Header ---
        h = block.header
        self.assertEqual(h.version, 1)
        self.assertEqual(h.unix_time, 1707016920)
        self.assertEqual(
            str(h.prev_block_hash),
            "f805b91ce08e5ee84b4707248fd602db5364da6ba9b273a200228ce9c62be4ac",
        )
        self.assertEqual(
            str(h.state_root),
            "a846b739df34099e5345088e66ded3f63762cc766c5380c58f788fb134c9467c",
        )
        self.assertEqual(h.proposer_address.address_type(), AddressType.VALIDATOR)
        self.assertEqual(
            h.proposer_address.string(),
            "pc1pg69yuccgflmh8fm4pffgwtrxtvvmz96vzjuvev",
        )

        # --- Certificate ---
        cert = block.prev_cert
        self.assertIsNotNone(cert)
        self.assertEqual(cert.height.value, 88887)
        self.assertEqual(cert.round.value, 0)
        self.assertEqual(len(cert.committers), 51)
        self.assertEqual(cert.absentees, [])
        self.assertEqual(
            cert.hash().hex(),
            "14aa7049254af312d2f8c5515989271a709a758e552801fe34ac68efa11581ef",
        )

        # --- Block ID ---
        self.assertEqual(
            block.id.hex(),
            "5a12881b1d5fd9bea3a61f24d7555d8900e85d02e9606b5a3176edf3c355a32d",
        )

        # --- Transactions ---
        self.assertEqual(len(block.transactions), 5)

        # Tx 0: Subsidy (transfer from treasury)
        tx = block.transactions[0]
        self.assertEqual(tx.version, 1)
        self.assertEqual(tx.flags, 0x02)
        self.assertEqual(tx.lock_time.value, 88888)
        self.assertEqual(tx.fee.value, 0)
        self.assertEqual(tx.payload.get_type(), PayloadType.TRANSFER)
        self.assertTrue(tx.payload.signer().is_treasury_address())
        self.assertIsNone(tx.signature)
        self.assertIsNone(tx.public_key)
        self.assertEqual(tx.payload.amount.value, 1_000_500_000)
        self.assertEqual(
            tx.payload.receiver.string(),
            "pc1zl95zy3wny0mufdepx8xk6ravduw0ceurudtqqq",
        )

        # Tx 1-3: Sortition
        for i in range(1, 4):
            tx = block.transactions[i]
            self.assertEqual(tx.flags, 0x01)
            self.assertEqual(tx.lock_time.value, 88887)
            self.assertEqual(tx.fee.value, 0)
            self.assertEqual(tx.payload.get_type(), PayloadType.SORTITION)
            self.assertIsNotNone(tx.signature)
            self.assertIsNone(tx.public_key)  # stripped

        # Tx 4: Bond
        tx = block.transactions[4]
        self.assertEqual(tx.flags, 0x01)
        self.assertEqual(tx.lock_time.value, 88887)
        self.assertEqual(tx.fee.value, 500_000)
        self.assertEqual(tx.payload.get_type(), PayloadType.BOND)
        self.assertEqual(tx.payload.stake.value, 5_000_000_000)
        self.assertEqual(
            tx.payload.receiver.string(),
            "pc1pvhfd9360knxr2zwd6er0fmh04jc6nnmjulhkcp",
        )
        self.assertIsNotNone(tx.signature)
        self.assertIsNone(tx.public_key)  # stripped


if __name__ == "__main__":
    unittest.main()
