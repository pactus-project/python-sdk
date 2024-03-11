import sys
sys.path.insert(0, './bls')


from bls.serdesZ import serialize
from bls.serdesZ import deserialize
from bls.curve_ops import g1gen, g2gen, point_mul
from bls.bls_sig_g1 import sign
from bls.util import print_g1_hex, print_g2_hex, print_value

SignatureSize = 48

class Signature:
    def __init__(self, point_g1):
        self.point_g1 = point_g1

    @classmethod
    def from_string(cls, text):
        data = bytes.fromhex(text)

        if len(data) != SignatureSize:
            raise ValueError("Signature data must be 48 bytes long")

        point_g1 = deserialize(bytes(data), is_ell2=False)

        return cls(point_g1)

    def string(self):
        data = serialize(self.point_g1)
        return data.hex()


