from __future__ import annotations

import hashlib
from functools import partial

import secp256k1
from ripemd.ripemd160 import ripemd160

from pactus.crypto.address import Address, AddressType
from pactus.crypto.hrp import HRP
from pactus.encoding import encoding
from pactus.utils import utils

from .signature import SIGNATURE_TYPE_SECP256K1, Signature

PUBLIC_KEY_SIZE = 33  # Compressed public key


class PublicKey:
    def __init__(self, pub: secp256k1.PublicKey) -> None:
        self.pub = pub

    @classmethod
    def from_string(cls, text: str) -> PublicKey:
        hrp, typ, data = utils.decode_to_base256_with_type(text)

        if hrp != HRP.PUBLIC_KEY_HRP:
            msg = f"Invalid hrp: {hrp}"
            raise ValueError(msg)

        if typ != SIGNATURE_TYPE_SECP256K1:
            msg = f"Invalid Public key type: {typ}"
            raise ValueError(msg)

        if len(data) != PUBLIC_KEY_SIZE:
            msg = "Public key data must be 33 bytes long"
            raise ValueError(msg)

        pub_key = secp256k1.PublicKey(bytes(data), raw=True)

        return cls(pub_key)

    def raw_bytes(self) -> bytes:
        return self.pub.serialize(compressed=True)

    def string(self) -> str:
        return utils.encode_from_base256_with_type(
            HRP.PUBLIC_KEY_HRP,
            SIGNATURE_TYPE_SECP256K1,
            self.raw_bytes(),
        )

    def encode(self) -> bytes:
        return encoding.append_fixed_bytes(b"", self.raw_bytes())

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        data, buf = encoding.read_fixed_bytes(buf, PUBLIC_KEY_SIZE)
        return cls(secp256k1.PublicKey(data, raw=True)), buf

    def account_address(self) -> Address:
        blake2b = hashlib.blake2b(digest_size=32)
        blake2b.update(self.raw_bytes())
        hash_256 = blake2b.digest()
        hash_160 = ripemd160(hash_256)

        return Address(AddressType.SECP256K1_ACCOUNT, hash_160)

    def verify(self, msg: bytes, sig: Signature) -> bool:
        try:
            digest = partial(hashlib.blake2b, digest_size=32)
            sig_compact = sig.raw_bytes()
            sig_deserialized = self.pub.ecdsa_deserialize_compact(sig_compact)
            return self.pub.ecdsa_verify(msg, sig_deserialized, digest=digest)

        # ruff: noqa: BLE001  #  unable to fix this issue
        except Exception:
            return False
