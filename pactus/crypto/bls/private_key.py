from __future__ import annotations

import secrets
from math import ceil, log2

from pactus.crypto.hrp import HRP
from pactus.utils import utils

from .bls12_381.bls_sig_g1 import sign
from .bls12_381.consts import q as curve_order
from .bls12_381.curve_ops import g2gen, point_mul
from .hash import hkdf_expand, hkdf_extract, i2osp, os2ip, sha256
from .public_key import PublicKey
from .signature import DST, SIGNATURE_TYPE_BLS, Signature

PRIVATE_KEY_SIZE = 32


class PrivateKey:
    def __init__(self, scalar: int) -> None:
        self.scalar = scalar % curve_order

    @classmethod
    def from_bytes(cls, buffer: bytes) -> PrivateKey:
        return cls(int.from_bytes(buffer, "big"))

    @classmethod
    def key_gen(cls, ikm: bytes = [], key_info: bytes = b"") -> PrivateKey:
        salt = b"BLS-SIG-KEYGEN-SALT-"
        sk = 0
        while sk == 0:
            salt = sha256(salt)
            prk = hkdf_extract(salt, ikm + b"\x00")
            l = ceil((1.5 * ceil(log2(curve_order))) / 8)  # noqa: E741
            okm = hkdf_expand(prk, key_info + i2osp(l, 2), l)
            sk = os2ip(okm) % curve_order

        return cls(sk)

    @classmethod
    def random(cls) -> PrivateKey:
        ikm = secrets.token_bytes(32)

        return cls.key_gen(ikm)

    @classmethod
    def from_string(cls, text: str) -> PrivateKey:
        hrp, typ, data = utils.decode_to_base256_with_type(text)

        if hrp != HRP.PRIVATE_KEY_HRP:
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
        return self.scalar.to_bytes(PRIVATE_KEY_SIZE, "big")

    def string(self) -> str:
        return utils.encode_from_base256_with_type(
            HRP.PRIVATE_KEY_HRP,
            SIGNATURE_TYPE_BLS,
            self.raw_bytes(),
        )

    def public_key(self) -> PublicKey:
        pk_point = point_mul(self.scalar, g2gen)
        return PublicKey(pk_point)

    def sign(self, msg: bytes) -> Signature:
        point_g1 = sign(self.scalar, msg, ciphersuite=DST)
        return Signature(point_g1)

    def split(self, n: int, t: int) -> list[PrivateKey]:
        if n < t:
            msg = f"n must be greater than t: n={n}, t={t}"
            raise ValueError(msg)

        if n < 1:
            msg = f"n must be greater than 1: n={n}"
            raise ValueError(msg)

        # Create the coefficients for the polynomial: c[0] = secret, c[1..t-1] = random private keys
        coeffs = [self.scalar]
        for _ in range(1, t):
            rand_priv = PrivateKey.random()
            coeffs.append(rand_priv.scalar)

        # Generate n shares by evaluating the polynomial at x = 1..n
        shares = []
        for i in range(1, n + 1):
            share_scalar = utils.evaluate_polynomial(coeffs, i, curve_order)
            if share_scalar is None:
                msg = f"Failed to evaluate polynomial at x={i}"
                raise ValueError(msg)

            shares.append(PrivateKey(share_scalar))

        return shares
