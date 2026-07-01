from __future__ import annotations

from pactus.encoding import encoding

HASH_SIZE = 32


class Hash:
    """Hash represents a 32-byte hash in the Pactus blockchain."""

    def __init__(self, data: bytes) -> None:
        if len(data) != HASH_SIZE:
            msg = f"Hash must be {HASH_SIZE} bytes, got {len(data)}"
            raise ValueError(msg)
        self.data = data

    def __eq__(self, other: Hash) -> bool:
        if isinstance(other, Hash):
            return self.data == other.data
        return False

    def __hash__(self) -> int:
        return hash(self.data)

    def __str__(self) -> str:
        return self.data.hex()

    def is_undef(self) -> bool:
        return self.data == bytes(HASH_SIZE)

    def encode(self, buf: bytes) -> bytes:
        return encoding.append_fixed_bytes(buf, self.data)

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        """
        Decode a Hash from bytes.
        Returns (Hash, remaining_buf).
        """
        data, buf = encoding.read_fixed_bytes(buf, HASH_SIZE)
        return cls(data), buf
