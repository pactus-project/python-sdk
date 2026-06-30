from __future__ import annotations


def append_uint8(buf: bytes, val: int) -> bytes:
    buf += val.to_bytes(1, "little")
    return buf


def append_uint16(buf: bytes, val: int) -> bytes:
    buf += val.to_bytes(2, "little")
    return buf


def append_uint32(buf: bytes, val: int) -> bytes:
    buf += val.to_bytes(4, "little")
    return buf


def append_str(buf: bytes, val: str) -> bytes:
    buf = append_var_int(buf, len(val))
    return append_fixed_bytes(buf, bytes(val, "utf-8"))


def append_var_int(buf: bytes, val: int) -> bytes:
    while val >= 0x80:
        n = (val & 0x7F) | 0x80
        buf += bytes([n])
        val >>= 7

    buf += bytes([val])
    return buf


def append_fixed_bytes(buf: bytes, data: bytes) -> bytes:
    buf += data
    return buf


def read_uint8(buf: bytes) -> tuple[int, bytes]:
    val = int.from_bytes(buf[0:1], "little", signed=False)
    return val, buf[1:]


def read_uint16(buf: bytes) -> tuple[int, bytes]:
    val = int.from_bytes(buf[0:2], "little", signed=False)
    return val, buf[2:]


def read_uint32(buf: bytes) -> tuple[int, bytes]:
    val = int.from_bytes(buf[0:4], "little", signed=False)
    return val, buf[4:]


def read_var_int(buf: bytes) -> tuple[int, bytes]:
    """
    Read a variable-length integer from bytes at given offset.
    Returns (value, new_offset).
    """
    result = 0
    shift = 0
    offset = 0
    while True:
        if offset >= len(buf):
            msg = "unexpected end of data while reading varint"
            raise ValueError(msg)
        byte = buf[offset]
        offset += 1
        result |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            break
        shift += 7
    return result, buf[offset:]


def read_fixed_bytes(buf: bytes, size: int) -> tuple[bytes, bytes]:
    """
    Read a fixed number of bytes from data at given offset.
    Returns (bytes_read, new_offset).
    """
    if size > len(buf):
        msg = "unexpected end of data while reading fixed bytes"
        raise ValueError(msg)
    return buf[0:size], buf[size:]


def read_str(buf: bytes) -> tuple[str, bytes]:
    """
    Read a variable-length string (varint length + utf8 data).
    Returns (string, new_offset).
    """
    length, buf = read_var_int(buf)
    raw, buf = read_fixed_bytes(buf, length)
    return raw.decode("utf-8"), buf
