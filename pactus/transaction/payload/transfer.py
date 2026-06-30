from pactus.crypto.address import Address
from pactus.encoding import encoding
from pactus.types.amount import Amount

from ._payload import PayloadType


class TransferPayload:
    def __init__(self, sender: Address, receiver: Address, amount: Amount) -> None:
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def encode(self, buf: list) -> None:
        encoding.append_fixed_bytes(buf, self.sender.raw_bytes())
        encoding.append_fixed_bytes(buf, self.receiver.raw_bytes())
        encoding.append_var_int(buf, self.amount.value)

    def get_type(self) -> PayloadType:
        return PayloadType.TRANSFER

    def signer(self) -> Address:
        return self.sender

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        sender, buf = Address.decode(buf)
        receiver, buf = Address.decode(buf)
        amount, buf = Amount.decode(buf)
        return cls(sender, receiver, amount), buf
