from .public_key import PublicKey
from .signature import Signature
from abc import ABC, abstractmethod


class PrivateKey(ABC):
    @classmethod
    @abstractmethod
    def from_string(text: str):
        pass

    @abstractmethod
    def bytes(self) -> bytes:
        pass

    @abstractmethod
    def string(self) -> str:
        pass

    @abstractmethod
    def public_key(self) -> PublicKey:
        pass

    @abstractmethod
    def sign(self, msg: bytes) -> Signature:
        pass
