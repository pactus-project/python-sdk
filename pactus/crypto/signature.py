from __future__ import annotations

from abc import ABC, abstractmethod


class Signature(ABC):
    @classmethod
    @abstractmethod
    def from_string(cls, text: str) -> Signature:
        pass

    @abstractmethod
    def raw_bytes(self) -> bytes:
        pass

    @abstractmethod
    def string(self) -> str:
        pass
