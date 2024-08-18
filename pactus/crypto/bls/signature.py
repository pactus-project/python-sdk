from .bls12_381.serdesZ import deserialize, serialize

SIGNATURE_SIZE = 48
SIGNATURE_TYPE_BLS = 1
DST = b"BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_"


class Signature:
    def __init__(self, point_g1: any) -> None:
        self.point_g1 = point_g1

    @classmethod
    def from_string(cls, text: str) -> "Signature":
        data = bytes.fromhex(text)

        if len(data) != SIGNATURE_SIZE:
            msg = "Signature data must be 48 bytes long"
            raise ValueError(msg)

        point_g1 = deserialize(bytes(data), is_ell2=False)

        return cls(point_g1)

    def raw_bytes(self) -> bytes:
        return serialize(self.point_g1)

    def string(self) -> str:
        return self.raw_bytes().hex()
