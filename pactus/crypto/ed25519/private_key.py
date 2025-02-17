from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric import ed25519

from pactus.crypto import CryptoConfig
from pactus.utils import utils

from .public_key import PublicKey
from .signature import SIGNATURE_TYPE_ED25519, Signature

PRIVATE_KEY_SIZE = 32


class PrivateKey:
    def __init__(self, scalar: ed25519.Ed25519PrivateKey) -> None:
        self.scalar = scalar

    @classmethod
    def from_bytes(cls, buffer: bytes) -> PrivateKey:
        return cls(ed25519.Ed25519PrivateKey.from_private_bytes(buffer))

    @classmethod
    def random(cls) -> PrivateKey:
        sk = ed25519.Ed25519PrivateKey.generate()

        return cls(sk)

    @classmethod
    def from_string(cls, text: str) -> PrivateKey:
        hrp, typ, data = utils.decode_to_base256_with_type(text)

        if hrp != CryptoConfig.PRIVATE_KEY_HRP:
            msg = f"Invalid hrp: {hrp}"
            raise ValueError(msg)

        if typ != SIGNATURE_TYPE_ED25519:
            msg = f"Invalid Private key type: {typ}"
            raise ValueError(msg)

        if len(data) != PRIVATE_KEY_SIZE:
            msg = "Private key data must be 32 bytes long"
            raise ValueError(msg)

        scalar = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(data))
        return cls(scalar)

    def raw_bytes(self) -> bytes:
        return self.scalar.private_bytes_raw()

    def string(self) -> str:
        return utils.encode_from_base256_with_type(
            CryptoConfig.PRIVATE_KEY_HRP,
            SIGNATURE_TYPE_ED25519,
            self.raw_bytes(),
        )

    def public_key(self) -> PublicKey:
        return PublicKey(self.scalar.public_key())

    def sign(self, msg: bytes) -> Signature:
        sig = self.scalar.sign(msg)
        return Signature(sig)
