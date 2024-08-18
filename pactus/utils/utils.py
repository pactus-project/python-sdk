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
