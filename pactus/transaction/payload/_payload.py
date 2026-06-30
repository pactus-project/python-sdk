from abc import ABC, abstractmethod
from enum import Enum

from pactus.crypto.address import Address


class PayloadType(Enum):
    TRANSFER = 1
    BOND = 2
    SORTITION = 3
    UNBOND = 4
    WITHDRAW = 5


class Payload(ABC):
    @abstractmethod
    def encode(self, buf: bytes) -> bytes:
        """Append the payload data to the buffer."""

    @abstractmethod
    def get_type(self) -> PayloadType:
        """Return the type of the payload."""

    @abstractmethod
    def signer(self) -> Address:
        """Return the signer address of this payload."""
