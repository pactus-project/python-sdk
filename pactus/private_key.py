import sys

sys.path.insert(0, "./bls")

import utils
from public_key import PublicKey
from signature import DST, SIGNATURE_TYPE_BLS, Signature
from bls.curve_ops import g2gen, point_mul
from bls.bls_sig_g1 import sign

PRIVATE_KEY_SIZE = 32
PRIVATE_KEY_HRP = "secret"


class PrivateKey:
    def __init__(self, scalar):
        self.scalar = scalar

    @classmethod
    def from_string(cls, text):
        hrp, typ, data = utils.decode_to_base256_with_type(text)

        if hrp != PRIVATE_KEY_HRP:
            raise ValueError(f"Invalid hrp: {hrp}")

        if typ != SIGNATURE_TYPE_BLS:
            raise ValueError(f"Invalid Private key type: {typ}")

        if len(data) != PRIVATE_KEY_SIZE:
            raise ValueError("Private key data must be 32 bytes long")

        scalar = int.from_bytes(data, "big")
        return cls(scalar)

    def bytes(self):
        return int.to_bytes(self.scalar)

    def string(self):
        return utils.encode_from_base256_with_type(
            PRIVATE_KEY_HRP, SIGNATURE_TYPE_BLS, self.bytes()
        )

    def public_key(self) -> PublicKey:
        pk_point = point_mul(self.scalar, g2gen)
        return PublicKey(pk_point)

    def sign(self, msg) -> Signature:
        point_g1 = sign(self.scalar, msg, ciphersuite=DST)
        return Signature(point_g1)
