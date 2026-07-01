from __future__ import annotations

import hashlib
import struct

from pactus.crypto.hash import Hash
from pactus.encoding import encoding
from pactus.transaction import Transaction

from .certificate import Certificate
from .header import Header


class Block:
    def __init__(
        self,
        header: Header,
        prev_cert: Certificate | None,
        transactions: list,
    ) -> None:
        self.header = header
        self.prev_cert = prev_cert
        self.transactions = transactions

    @classmethod
    def decode(cls, data: bytes) -> Block:
        """Decode a Block from raw bytes."""
        header, data = Header.decode(data)

        # Genesis block has no certificate
        is_genesis = header.prev_block_hash.is_undef()

        prev_cert = None
        if not is_genesis:
            prev_cert, data = Certificate.decode(data)

        num_txs, data = encoding.read_var_int(data)

        transactions = []
        for _ in range(num_txs):
            tx, data = Transaction.decode(data)
            transactions.append(tx)

        return cls(header, prev_cert, transactions)

    @property
    def id(self) -> Hash:
        """Return the block ID (blake2b-256 of header + cert_hash + tx_root + tx_count)."""
        buf = self._header_bytes()
        if self.prev_cert is not None:
            buf += self.prev_cert.hash()
        buf += self._txs_root()
        buf += struct.pack("<i", len(self.transactions))
        return Hash(hashlib.blake2b(buf, digest_size=32).digest())

    def _header_bytes(self) -> bytes:
        return self.header.encode(b"")

    def _txs_root(self) -> bytes:
        return Block._merkle_root([tx.id().data for tx in self.transactions])

    @staticmethod
    def _merkle_root(hashes: list) -> bytes:
        if not hashes:
            return bytes(32)

        # Build simple merkle tree
        n = 1
        while n < len(hashes):
            n <<= 1

        tree = [None] * (n * 2 - 1)
        for i, h in enumerate(hashes):
            tree[i] = h

        offset = n
        for i in range(0, len(tree) - 1, 2):
            left = tree[i]
            right = tree[i + 1]
            if left is None:
                tree[offset] = None
            elif right is None:
                tree[offset] = hashlib.blake2b(left + left, digest_size=32).digest()
            else:
                tree[offset] = hashlib.blake2b(left + right, digest_size=32).digest()
            offset += 1

        return tree[-1] or bytes(32)
