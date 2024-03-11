import sys
sys.path.insert(0, "./bls")

import hashlib
from ripemd.ripemd160 import ripemd160
import address
from bls.serdesZ import deserialize, serialize
from bls.bls_sig_g1 import verify
import utils
from signature import Signature, SIGNATURE_TYPE_BLS, DST

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

    def bytes(self):
        return serialize(self.point_g2)

    def string(self):
        return utils.encode_from_base256_with_type(
            PUBLIC_KEY_HRP, SIGNATURE_TYPE_BLS, self.bytes()
        )

    def account_address(self):
        return self._make_address(address.AddressType.BLSAccount)

    def validator_address(self):
        return self._make_address(address.AddressType.Validator)

    def _make_address(self, address_type):
        blake2b = hashlib.blake2b(digest_size=32)
        blake2b.update(self.bytes())
        hash_256 = blake2b.digest()
        hash_160 = ripemd160(hash_256)
        addr = address.Address(address_type, hash_160)
        return addr

    def verify(self, msg, sig: Signature) -> bool:
        return verify(self.point_g2, sig.point_g1, msg, ciphersuite=DST)
