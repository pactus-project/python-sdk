from pactus.encoding import encoding


class Round:
    """
    Round represents a consensus round in the Pactus blockchain.

    It encapsulates a raw integer value representing a round number.
    """

    def __init__(self, value: int = 0) -> None:
        self.value = value

    def __eq__(self, other: "Round") -> bool:
        if isinstance(other, Round):
            return self.value == other.value

        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def encode(self, buf: bytes) -> bytes:
        return encoding.append_uint16(buf, self.value)

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        """
        Decode a Round from bytes.
        Returns (Round, remaining_buf).
        """
        val, buf = encoding.read_uint16(buf)
        return cls(val), buf
