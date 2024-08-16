from enum import Enum

from pactus.encoding import encoding
from pactus.crypto.address import Address
from pactus.types.amount import Amount

from abc import ABC, abstractmethod


class PayloadType(Enum):
    Transfer = 1
    Bond = 2
    Sortition = 3
    Unbond = 4
    Withdraw = 5


class Payload(ABC):
    @abstractmethod
    def encode(self, buf: list):
        """
        This method should append the payload data to the buffer.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_type(self) -> PayloadType:
        """
        This method should return the type of the payload.
        Must be implemented by subclasses.
        """
        pass


class TransferPayload:
    def __init__(self, sender: Address, receiver: Address, amount: Amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def encode(self, buf: list):
        encoding.append_fixed_bytes(buf, self.sender.bytes())
        encoding.append_fixed_bytes(buf, self.receiver.bytes())
        encoding.append_var_int(buf, self.amount.value)

    def get_type(self) -> PayloadType:
        return PayloadType.Transfer


class BondPayload:
    def __init__(
        self, sender: Address, receiver: Address, public_key: bytes, stake: Amount
    ):
        self.sender = sender
        self.receiver = receiver
        self.public_key = public_key
        self.stake = stake

    def encode(self, buf: list):
        encoding.append_fixed_bytes(buf, self.sender.bytes())
        encoding.append_fixed_bytes(buf, self.receiver.bytes())
        encoding.append_fixed_bytes(buf, self.public_key)
        encoding.append_var_int(buf, self.stake.value)

    def get_type(self) -> PayloadType:
        return PayloadType.Bond


class UnbondPayload:
    def __init__(self, validator: Address):
        self.validator = validator

    def encode(self, buf: list):
        encoding.append_fixed_bytes(buf, self.validator.bytes())

    def get_type(self) -> PayloadType:
        return PayloadType.Unbond


class WithdrawPayload:
    def __init__(self, from_addr: Address, to_addr: Address, amount: Amount):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount

    def encode(self, buf: list):
        encoding.append_fixed_bytes(buf, self.from_addr.bytes())
        encoding.append_fixed_bytes(buf, self.to_addr.bytes())
        encoding.append_var_int(buf, self.amount)

    def get_type(self) -> PayloadType:
        return PayloadType.Withdraw
