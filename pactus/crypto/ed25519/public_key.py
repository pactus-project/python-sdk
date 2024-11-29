from __future__ import annotations

import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519
from ripemd.ripemd160 import ripemd160

from pactus.crypto import CryptoConfig
from pactus.crypto.address import Address, AddressType
from pactus.utils import utils

from .signature import SIGNATURE_TYPE_ED25519, Signature

PUBLIC_KEY_SIZE = 32


class PublicKey:
    def __init__(self, pub: ed25519.Ed25519PublicKey) -> None:
        self.pub = pub

    @classmethod
    def from_string(cls, text: str) -> PublicKey:
        hrp, typ, data = utils.decode_to_base256_with_type(text)

        if hrp != CryptoConfig.PUBLIC_KEY_HRP:
            msg = f"Invalid hrp: {hrp}"
            raise ValueError(msg)

        if typ != SIGNATURE_TYPE_ED25519:
            msg = f"Invalid Private key type: {typ}"
            raise ValueError(msg)

        if len(data) != PUBLIC_KEY_SIZE:
            msg = "Public key data must be 96 bytes long"
            raise ValueError(msg)

        pub_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes(data))

        return cls(pub_key)

    def raw_bytes(self) -> bytes:
        return self.pub.public_bytes_raw()

    def string(self) -> str:
        return utils.encode_from_base256_with_type(
            CryptoConfig.PUBLIC_KEY_HRP,
            SIGNATURE_TYPE_ED25519,
            self.raw_bytes(),
        )

    def account_address(self) -> Address:
        blake2b = hashlib.blake2b(digest_size=32)
        blake2b.update(self.raw_bytes())
        hash_256 = blake2b.digest()
        hash_160 = ripemd160(hash_256)
        return Address(AddressType.ED25519_ACCOUNT, hash_160)

    def verify(self, msg: bytes, sig: Signature) -> bool:
        try:
            self.pub.verify(sig.raw_bytes(), msg)
        except InvalidSignature:
            return False
        else:
            return True
