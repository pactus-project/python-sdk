from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .public_key import PublicKey
    from .signature import Signature


class PrivateKey(ABC):
    @classmethod
    @abstractmethod
    def from_string(cls, text: str) -> PrivateKey:
        pass

    @abstractmethod
    def raw_bytes(self) -> bytes:
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
