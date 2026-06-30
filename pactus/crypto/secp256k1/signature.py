from __future__ import annotations

from pactus.encoding import encoding

SIGNATURE_SIZE = 64
SIGNATURE_TYPE_SECP256K1 = 4


class Signature:
    def __init__(self, sig: bytes) -> None:
        self.sig = sig

    @classmethod
    def from_string(cls, text: str) -> Signature:
        data = bytes.fromhex(text)

        if len(data) != SIGNATURE_SIZE:
            msg = "Signature data must be 64 bytes long"
            raise ValueError(msg)

        return cls(data)

    def raw_bytes(self) -> bytes:
        return self.sig

    def string(self) -> str:
        return self.sig.hex()

    def encode(self, buf: bytes) -> bytes:
        return encoding.append_fixed_bytes(buf, self.sig)

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        data, buf = encoding.read_fixed_bytes(buf, SIGNATURE_SIZE)
        return cls(data), buf
