from pactus.crypto.address import Address
from pactus.encoding import encoding

from ._payload import PayloadType


class UnbondPayload:
    def __init__(self, validator: Address) -> None:
        self.validator = validator

    def encode(self, buf: list) -> None:
        encoding.append_fixed_bytes(buf, self.validator.raw_bytes())

    def get_type(self) -> PayloadType:
        return PayloadType.UNBOND

    def signer(self) -> Address:
        return self.validator

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        validator, buf = Address.decode(buf)
        return cls(validator), buf
