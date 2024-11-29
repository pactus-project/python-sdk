from __future__ import annotations

SIGNATURE_SIZE = 64
SIGNATURE_TYPE_ED25519 = 3


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
