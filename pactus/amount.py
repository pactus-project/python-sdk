import math

NANO_PAC_PER_PAC = 1e9
MAX_NANO_PAC = 42e6 * NANO_PAC_PER_PAC


class Amount:
    """
    NewAmount creates an Amount from a floating-point value representing
    an amount in PAC.  NewAmount returns an error if f is NaN or +-Infinity,
    but it does not check whether the amount is within the total amount of PAC
    producible, as it may not refer to an amount at a single moment in time.

    NewAmount is specifically for converting PAC to NanoPAC.
    For creating a new Amount with an int64 value which denotes a quantity of NanoPAC,
    do a simple type conversion from type int64 to Amount.
    """

    def __init__(self, f: float):
        """
        The amount is only considered invalid if it cannot be represented
            as an integer type. This may happen if f is NaN or +-Infinity.
        """
        if math.isinf(f) or math.isnan(f):
            raise ValueError(f"invalid PAC amount: {f}")

        self.amount = round(f * NANO_PAC_PER_PAC)


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
