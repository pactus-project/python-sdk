from pactus.crypto.address import Address
from pactus.types.amount import Amount

from ._payload import PayloadType


class TransferPayload:
    def __init__(self, sender: Address, receiver: Address, amount: Amount) -> None:
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def encode(self, buf: bytes) -> bytes:
        buf = self.sender.encode(buf)
        buf = self.receiver.encode(buf)
        return self.amount.encode(buf)

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
