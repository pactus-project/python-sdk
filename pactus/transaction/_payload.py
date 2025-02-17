from abc import ABC, abstractmethod
from enum import Enum

from pactus.amount import Amount
from pactus.crypto.address import Address
from pactus.encoding import encoding


class PayloadType(Enum):
    TRANSFER = 1
    BOND = 2
    SORTITION = 3
    UNBOND = 4
    WITHDRAW = 5


class Payload(ABC):
    @abstractmethod
    def encode(self, buf: list) -> None:
        """
        Append the payload data to the buffer.
        Must be implemented by subclasses.
        """

    @abstractmethod
    def get_type(self) -> PayloadType:
        """
        Return the type of the payload.
        Must be implemented by subclasses.
        """


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


class BondPayload:
    def __init__(
        self,
        sender: Address,
        receiver: Address,
        public_key: bytes,
        stake: Amount,
    ) -> None:
        self.sender = sender
        self.receiver = receiver
        self.public_key = public_key
        self.stake = stake

    def encode(self, buf: list) -> None:
        encoding.append_fixed_bytes(buf, self.sender.raw_bytes())
        encoding.append_fixed_bytes(buf, self.receiver.raw_bytes())
        encoding.append_fixed_bytes(buf, self.public_key)
        encoding.append_var_int(buf, self.stake.value)

    def get_type(self) -> PayloadType:
        return PayloadType.BOND


class UnbondPayload:
    def __init__(self, validator: Address) -> None:
        self.validator = validator

    def encode(self, buf: list) -> None:
        encoding.append_fixed_bytes(buf, self.validator.raw_bytes())

    def get_type(self) -> PayloadType:
        return PayloadType.UNBOND


class WithdrawPayload:
    def __init__(self, from_addr: Address, to_addr: Address, amount: Amount) -> None:
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount

    def encode(self, buf: list) -> None:
        encoding.append_fixed_bytes(buf, self.from_addr.raw_bytes())
        encoding.append_fixed_bytes(buf, self.to_addr.raw_bytes())
        encoding.append_var_int(buf, self.amount)

    def get_type(self) -> PayloadType:
        return PayloadType.WITHDRAW
