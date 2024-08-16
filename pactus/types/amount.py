import math

NANO_PAC_PER_PAC = 1e9
MAX_NANO_PAC = 42e6 * NANO_PAC_PER_PAC


class Amount:
    """
    The Amount class represents a quantity in NanoPAC.

    The `from_NanoPAC` method creates an Amount from a floating-point value
    representing an amount in PAC. It raises an error if the value is NaN or
    +-Infinity, but it does not check whether the amount exceeds the total
    amount of PAC producible. This method is specifically for converting PAC
    to NanoPAC. For creating a new Amount with an integer value representing
    NanoPAC, you can initialize the Amount directly with an integer.
    """

    def __init__(self, amt: int = 0):
        self.value = amt

    def __eq__(self, other):
        if isinstance(other, Amount):
            return self.value == other.value
        return False

    def from_NanoPAC(f: float):
        """
        Converts a floating-point value in PAC to NanoPAC and stores it in the Amount instance.

        The conversion is invalid if the floating-point value is NaN or +-Infinity,
        in which case a ValueError is raised.
        """
        if math.isinf(f) or math.isnan(f):
            raise ValueError(f"invalid PAC amount: {f}")

        return Amount(int(round(f * NANO_PAC_PER_PAC)))

    def FromString(s: str):
        """
        Parses a string representing a value in PAC, converts it to NanoPAC,
        and updates the Amount object.

        If the string cannot be parsed as a float, a ValueError is raised.
        """
        try:
            f = float(s)
        except ValueError as e:
            raise ValueError("invalid PAC amount") from e

        return Amount.from_NanoPAC(f)


def round(f: float) -> float:
    """
    round converts a floating point number, which may or may not be representable
    as an integer, to the Amount integer type by rounding to the nearest integer.
    This is performed by adding or subtracting 0.5 depending on the sign, and
    relying on integer truncation to round the value to the nearest Amount.
    """
    if f < 0:
        return f - 0.5

    return f + 0.5
