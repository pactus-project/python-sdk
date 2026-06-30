from pactus.crypto.address import Address
from pactus.encoding import encoding
from pactus.types.amount import Amount

from ._payload import PayloadType


class WithdrawPayload:
    def __init__(self, from_addr: Address, to_addr: Address, amount: Amount) -> None:
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount

    def encode(self, buf: list) -> None:
        encoding.append_fixed_bytes(buf, self.from_addr.raw_bytes())
        encoding.append_fixed_bytes(buf, self.to_addr.raw_bytes())
        encoding.append_var_int(buf, self.amount.value)

    def get_type(self) -> PayloadType:
        return PayloadType.WITHDRAW

    def signer(self) -> Address:
        return self.from_addr

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        from_addr, buf = Address.decode(buf)
        to_addr, buf = Address.decode(buf)
        amount, buf = Amount.decode(buf)
        return cls(from_addr, to_addr, amount), buf
