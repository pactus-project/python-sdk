from __future__ import annotations

import secp256k1

from pactus.crypto.hrp import HRP
from pactus.utils import utils

from .public_key import PublicKey
from .signature import SIGNATURE_TYPE_SECP256K1, Signature

PRIVATE_KEY_SIZE = 32


class PrivateKey:
    def __init__(self, scalar: secp256k1.PrivateKey) -> None:
        self.scalar = scalar

    @classmethod
    def from_bytes(cls, buffer: bytes) -> PrivateKey:
        sk = secp256k1.PrivateKey()
        sk.set_raw_privkey(buffer)
        return cls(sk)

    @classmethod
    def random(cls) -> PrivateKey:
        sk = secp256k1.PrivateKey()
        return cls(sk)

    @classmethod
    def from_string(cls, text: str) -> PrivateKey:
        hrp, typ, data = utils.decode_to_base256_with_type(text)

        if hrp != HRP.PRIVATE_KEY_HRP:
            msg = f"Invalid hrp: {hrp}"
            raise ValueError(msg)

        if typ != SIGNATURE_TYPE_SECP256K1:
            msg = f"Invalid Private key type: {typ}"
            raise ValueError(msg)

        if len(data) != PRIVATE_KEY_SIZE:
            msg = "Private key data must be 32 bytes long"
            raise ValueError(msg)

        sk = secp256k1.PrivateKey()
        sk.set_raw_privkey(bytes(data))
        return cls(sk)

    def raw_bytes(self) -> bytes:
        # serialize() returns a hex string, convert to bytes
        hex_str = self.scalar.serialize()
        return bytes.fromhex(hex_str)

    def string(self) -> str:
        return utils.encode_from_base256_with_type(
            HRP.PRIVATE_KEY_HRP,
            SIGNATURE_TYPE_SECP256K1,
            self.raw_bytes(),
        )

    def public_key(self) -> PublicKey:
        return PublicKey(self.scalar.pubkey)

    def sign(self, msg: bytes) -> Signature:
        sig = self.scalar.ecdsa_sign(msg)
        sig_compact = self.scalar.ecdsa_serialize_compact(sig)
        return Signature(sig_compact)
