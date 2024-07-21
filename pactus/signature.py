import sys

sys.path.insert(0, "./bls")


from bls.serdesZ import serialize
from bls.serdesZ import deserialize

SIGNATURE_SIZE = 48
SIGNATURE_TYPE_BLS = 1
DST = b"BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_"


class Signature:
    def __init__(self, point_g1):
        self.point_g1 = point_g1

    @classmethod
    def from_string(cls, text):
        data = bytes.fromhex(text)

        if len(data) != SIGNATURE_SIZE:
            raise ValueError("Signature data must be 48 bytes long")

        point_g1 = deserialize(bytes(data), is_ell2=False)

        return cls(point_g1)

    def bytes(self):
        return serialize(self.point_g1)

    def string(self):
        return self.bytes().hex()
