class Height:
    """
    Height represents a block height in the Pactus blockchain.

    It encapsulates a raw integer value representing a block height.
    It can be used for transaction lock times.
    """

    def __init__(self, height: int = 0) -> None:
        self.value = height

    def __eq__(self, other: "Height") -> bool:
        if isinstance(other, Height):
            return self.value == other.value

        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return str(self.value)
