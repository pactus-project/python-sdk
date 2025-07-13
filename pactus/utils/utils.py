from __future__ import annotations

from . import bech32m


def decode_to_base256_with_type(text: str) -> tuple[str, int, list[int]]:
    hrp, data, spec = bech32m.bech32_decode(text)
    if spec != bech32m.Encoding.BECH32M:
        msg = "Invalid encoding specification: Expected BECH32M"
        raise ValueError(msg)

    regrouped = bech32m.convertbits(data[1:], 5, 8, pad=False)
    return hrp, data[0], regrouped


def encode_from_base256_with_type(hrp: str, typ: str, data: bytes) -> str:
    converted = bech32m.convertbits(list(data), 8, 5, pad=True)
    converted = [typ, *converted]
    return bech32m.bech32_encode(hrp, converted, bech32m.Encoding.BECH32M)


def evaluate_polynomial(c: list[int], x: int, mod: int) -> int | None:
    """
    Evaluate the polynomial f(x) = c[0] + c[1] * x + c[2] * x^2 + ... + c[n-1] * x^(n-1).

    Args:
        c: List of polynomial coefficients (c[0] is the constant term)
        x: The value at which to evaluate the polynomial
        mod: The modulus to use for the evaluation

    Returns:
        The computed value f(x) if success, None otherwise

    """
    if not c:
        return None

    if len(c) == 1:
        return c[0]

    y = c[-1]
    for i in range(len(c) - 2, -1, -1):
        y = (y * x + c[i]) % mod

    return y
