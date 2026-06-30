from pactus.encoding import encoding


class Height:
    """
    Height represents a block height in the Pactus blockchain.

    It encapsulates a raw integer value representing a block height.
    It can be used for transaction lock times.
    """

    def __init__(self, value: int = 0) -> None:
        self.value = value

    def __eq__(self, other: "Height") -> bool:
        if isinstance(other, Height):
            return self.value == other.value

        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def encode(self, buf: bytes) -> bytes:
        return encoding.append_uint32(buf, self.value)

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        """
        Decode a Height from bytes.
        Returns (Height, remaining_buf).
        """
        val, buf = encoding.read_uint32(buf)
        return cls(val), buf
