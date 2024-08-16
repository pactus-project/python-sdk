import hashlib

from ripemd.ripemd160 import ripemd160

from pactus.crypto.address import Address, AddressType
from .bls12_381.bls_sig_g1 import verify
from .bls12_381.serdesZ import deserialize, serialize
from .signature import DST, SIGNATURE_TYPE_BLS, Signature

from pactus.utils import utils

PUBLIC_KEY_SIZE = 96
PUBLIC_KEY_HRP = "public"


class PublicKey:
    def __init__(self, point_g2):
        self.point_g2 = point_g2

    @classmethod
    def from_string(cls, text):
        hrp, typ, data = utils.decode_to_base256_with_type(text)

        if hrp != PUBLIC_KEY_HRP:
            raise ValueError(f"Invalid hrp: {hrp}")

        if typ != SIGNATURE_TYPE_BLS:
            raise ValueError(f"Invalid public key type: {typ}")

        if len(data) != PUBLIC_KEY_SIZE:
            raise ValueError("Public key data must be 96 bytes long")

        point_g2 = deserialize(bytes(data), is_ell2=True)

        return cls(point_g2)

    def bytes(self) -> bytes:
        return serialize(self.point_g2)

    def string(self) -> str:
        return utils.encode_from_base256_with_type(
            PUBLIC_KEY_HRP, SIGNATURE_TYPE_BLS, self.bytes()
        )

    def account_address(self) -> Address:
        return self._make_address(AddressType.BLSAccount)

    def validator_address(self) -> Address:
        return self._make_address(AddressType.Validator)

    def _make_address(self, address_type):
        blake2b = hashlib.blake2b(digest_size=32)
        blake2b.update(self.bytes())
        hash_256 = blake2b.digest()
        hash_160 = ripemd160(hash_256)
        addr = Address(address_type, hash_160)
        return addr

    def verify(self, msg, sig: Signature) -> bool:
        return verify(self.point_g2, sig.point_g1, msg, ciphersuite=DST)
