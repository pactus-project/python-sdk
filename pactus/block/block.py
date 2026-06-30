from __future__ import annotations

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
