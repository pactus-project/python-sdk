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
