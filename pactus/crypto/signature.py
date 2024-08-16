from abc import ABC, abstractmethod


class Signature(ABC):
    @classmethod
    @abstractmethod
    def from_string(cls, text):
        pass

    def bytes(self) -> bytes:
        pass

    def string(self) -> str:
        pass
