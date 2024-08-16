from pactus.utils import utils

from .bls12_381.bls_sig_g1 import sign
from .bls12_381.curve_ops import g2gen, point_mul
from .public_key import PublicKey
from .signature import DST, SIGNATURE_TYPE_BLS, Signature

PRIVATE_KEY_SIZE = 32
PRIVATE_KEY_HRP = "secret"


class PrivateKey:
    def __init__(self, scalar: any) -> None:
        self.scalar = scalar

    @classmethod
    def from_string(cls, text: str) -> "PrivateKey":
        hrp, typ, data = utils.decode_to_base256_with_type(text)

        if hrp != PRIVATE_KEY_HRP:
            msg = f"Invalid hrp: {hrp}"
            raise ValueError(msg)

        if typ != SIGNATURE_TYPE_BLS:
            msg = f"Invalid Private key type: {typ}"
            raise ValueError(msg)

        if len(data) != PRIVATE_KEY_SIZE:
            msg = "Private key data must be 32 bytes long"
            raise ValueError(msg)

        scalar = int.from_bytes(data, "big")
        return cls(scalar)

    def raw_bytes(self) -> bytes:
        return int.to_bytes(self.scalar)

    def string(self) -> str:
        return utils.encode_from_base256_with_type(
            PRIVATE_KEY_HRP,
            SIGNATURE_TYPE_BLS,
            self.raw_bytes(),
        )

    def public_key(self) -> PublicKey:
        pk_point = point_mul(self.scalar, g2gen)
        return PublicKey(pk_point)

    def sign(self, msg: bytes) -> Signature:
        point_g1 = sign(self.scalar, msg, ciphersuite=DST)
        return Signature(point_g1)
