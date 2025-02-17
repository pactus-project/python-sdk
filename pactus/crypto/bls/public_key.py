from __future__ import annotations

import hashlib

from ripemd.ripemd160 import ripemd160

from pactus.crypto import CryptoConfig
from pactus.crypto.address import Address, AddressType
from pactus.utils import utils

from .bls12_381.bls_sig_g1 import aggregate_pubs, verify
from .bls12_381.serdesZ import deserialize, serialize
from .signature import DST, SIGNATURE_TYPE_BLS, Signature

PUBLIC_KEY_SIZE = 96


class PublicKey:
    def __init__(self, point_g2: any) -> None:
        self.point_g2 = point_g2

    @classmethod
    def from_string(cls, text: str) -> PublicKey:
        hrp, typ, data = utils.decode_to_base256_with_type(text)

        if hrp != CryptoConfig.PUBLIC_KEY_HRP:
            msg = f"Invalid hrp: {hrp}"
            raise ValueError(msg)

        if typ != SIGNATURE_TYPE_BLS:
            msg = f"Invalid public key type: {typ}"
            raise ValueError(msg)

        if len(data) != PUBLIC_KEY_SIZE:
            msg = "Public key data must be 96 bytes long"
            raise ValueError(msg)

        point_g2 = deserialize(bytes(data), is_ell2=True)

        return cls(point_g2)

    @classmethod
    def aggregate(cls, pubs: list[PublicKey]) -> PublicKey:
        point_g2s = []
        point_g2s.extend(pub.point_g2 for pub in pubs)

        return cls(aggregate_pubs(point_g2s))

    def raw_bytes(self) -> bytes:
        return serialize(self.point_g2)

    def string(self) -> str:
        return utils.encode_from_base256_with_type(
            CryptoConfig.PUBLIC_KEY_HRP,
            SIGNATURE_TYPE_BLS,
            self.raw_bytes(),
        )

    def account_address(self) -> Address:
        return self._make_address(AddressType.BLS_ACCOUNT)

    def validator_address(self) -> Address:
        return self._make_address(AddressType.VALIDATOR)

    def _make_address(self, address_type: AddressType) -> Address:
        blake2b = hashlib.blake2b(digest_size=32)
        blake2b.update(self.raw_bytes())
        hash_256 = blake2b.digest()
        hash_160 = ripemd160(hash_256)
        return Address(address_type, hash_160)

    def verify(self, msg: bytes, sig: Signature) -> bool:
        return verify(self.point_g2, sig.point_g1, msg, ciphersuite=DST)
