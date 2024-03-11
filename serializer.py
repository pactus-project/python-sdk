def append_uint8(buf, val):
    buf += val.to_bytes(1, 'little')
    return buf

def append_uint16(buf, val):
    buf += val.to_bytes(2, 'little')
    return buf

def append_uint32(buf, val):
    buf += val.to_bytes(4, 'little')
    return buf

def append_var_int(buf, val):
    while val >= 0x80:
        n = (val & 0x7f) | 0x80
        buf += bytes([n])
        val >>= 7

    buf += bytes([val])
    return buf

def append_fixed_bytes(buf, data):
    buf += data
    return buf