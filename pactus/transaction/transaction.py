from pactus.crypto.address import Address
from pactus.crypto.private_key import PrivateKey
from pactus.encoding import encoding
from pactus.amount import Amount

from ._payload import (
    BondPayload,
    Payload,
    TransferPayload,
    UnbondPayload,
    WithdrawPayload,
)


class Transaction:
    def __init__(
        self,
        lock_time: int,
        fee: Amount,
        memo: str = "",
        payload: Payload = None,
    ) -> None:
        self.lock_time = lock_time
        self.memo = memo
        self.flags = 0
        self.version = 1
        self.fee = fee
        self.payload = payload

    @classmethod
    def create_transfer_tx(
        cls,
        lock_time: int,
        sender: Address,
        receiver: Address,
        amount: Amount,
        fee: Amount,
        memo: str = "",
    ) -> "Transaction":
        tx = cls(lock_time, fee, memo)
        tx.payload = TransferPayload(sender, receiver, amount)
        return tx

    @classmethod
    def create_bond_tx(
        cls,
        lock_time: int,
        sender: Address,
        receiver: Address,
        public_key: bytes,
        fee: Amount,
        stake: Amount,
        memo: str = "",
    ) -> "Transaction":
        payload = BondPayload(sender, receiver, public_key, stake)
        return cls(lock_time, fee, memo, payload)

    @classmethod
    def create_unbond_tx(
        cls,
        lock_time: int,
        validator: Address,
        memo: str = "",
    ) -> "Transaction":
        payload = UnbondPayload(validator)
        return cls(lock_time, 0, memo, payload)

    @classmethod
    def create_withdraw_tx(
        cls,
        lock_time: int,
        from_addr: Address,
        to_addr: Address,
        amount: Amount,
        fee: Amount,
        memo: str = "",
    ) -> "Transaction":
        payload = WithdrawPayload(from_addr, to_addr, amount)
        return cls(lock_time, fee, memo, payload)

    def _get_unsigned_bytes(self, buf: bytes) -> bytes:
        """Get unsigned bytes of the transaction, including the payload."""
        encoding.append_uint8(buf, self.flags)
        encoding.append_uint8(buf, self.version)
        encoding.append_uint32(buf, self.lock_time)
        encoding.append_var_int(buf, self.fee.value)
        encoding.append_str(buf, self.memo)
        encoding.append_uint8(buf, self.payload.get_type().value)
        self.payload.encode(buf)

        return buf

    def sign(self, private_key: PrivateKey) -> str:
        """Make a raw transaction, sign it and return the signed bytes."""
        buf = bytearray()

        sign_bytes = self._get_unsigned_bytes(buf)
        sig = private_key.sign(
            bytes(sign_bytes[1:]),
        )  # flags is not part of the sign bytes.
        pub = private_key.public_key()

        encoding.append_fixed_bytes(buf, sig.raw_bytes())
        encoding.append_fixed_bytes(buf, pub.raw_bytes())

        return buf.hex()
