import sys
sys.path.insert(0, './bls')


from bls.serdesZ import serialize
from bls.serdesZ import deserialize
from bls.curve_ops import g1gen, g2gen, point_mul
from bls.bls_sig_g1 import sign
from bls.util import print_g1_hex, print_g2_hex, print_value

SIGNATURE_SIZE = 48
SIGNATURE_TYPE_BLS = 1
DST = b'BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_'

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


