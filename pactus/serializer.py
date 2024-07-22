def append_uint8(buf: bytes, val) -> bytes:
    buf += val.to_bytes(1, "little")
    return buf


def append_uint16(buf: bytes, val) -> bytes:
    buf += val.to_bytes(2, "little")
    return buf


def append_uint32(buf: bytes, val) -> bytes:
    buf += val.to_bytes(4, "little")
    return buf


def append_str(buf: bytes, val: str) -> bytes:
    buf += bytes(val, "utf-8")
    return buf


def append_var_int(buf: bytes, val) -> bytes:
    while val >= 0x80:
        n = (val & 0x7F) | 0x80
        buf += bytes([n])
        val >>= 7

    buf += bytes([val])
    return buf


def append_fixed_bytes(buf: bytes, data) -> bytes:
    buf += data
    return buf
