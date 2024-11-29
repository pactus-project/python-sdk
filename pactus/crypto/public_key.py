from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .signature import Signature


class PublicKey(ABC):
    @classmethod
    @abstractmethod
    def from_string(cls, text: str) -> PublicKey:
        pass

    @abstractmethod
    def raw_bytes(self) -> bytes:
        pass

    @abstractmethod
    def string(self) -> str:
        pass

    @abstractmethod
    def verify(self, msg: str, sig: Signature) -> bool:
        pass
