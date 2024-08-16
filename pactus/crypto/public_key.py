from .address import Address
from .signature import Signature
from abc import ABC, abstractmethod


class PublicKey(ABC):
    @classmethod
    @abstractmethod
    def from_string(cls, text: str):
        pass

    @abstractmethod
    def bytes(self) -> bytes:
        pass

    @abstractmethod
    def string(self) -> str:
        pass

    def verify(self, msg, sig: Signature) -> bool:
        pass
