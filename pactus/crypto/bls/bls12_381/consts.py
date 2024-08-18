#!/usr/bin/python
#
# constants for BLS signatures over BLS12-381

# z, the BLS parameter
ell_u = -0xD201000000010000
# base field order
p = 0x1A0111EA397FE69A4B1BA7B6434BACD764774B84F38512BF6730D2A0F6B0F6241EABFFFEB153FFFFB9FEFFFFFFFFAAAB
# subgroup order
q = 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001
# exponent for final exp in pairing
k_final = (p**4 - p**2 + 1) // q

# ciphersuite numbers
_gsuite = (
    lambda stype, group, stag: b"BLS_"
    + stype
    + b"_BLS12381G"
    + group
    + b"_XMD:SHA-256_SSWU_RO_"
    + bytes(stag)
    + b"_"
)
g1suite = lambda stag: _gsuite(b"SIG", b"1", stag)
g1pop = _gsuite(b"POP", b"1", b"POP")
g2suite = lambda stag: _gsuite(b"SIG", b"2", stag)
g2pop = _gsuite(b"POP", b"2", b"POP")
