from pactus.crypto.address import Address

from ._payload import PayloadType


class UnbondPayload:
    def __init__(self, validator: Address) -> None:
        self.validator = validator

    def encode(self, buf: bytes) -> bytes:
        return self.validator.encode(buf)

    def get_type(self) -> PayloadType:
        return PayloadType.UNBOND

    def signer(self) -> Address:
        return self.validator

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        validator, buf = Address.decode(buf)
        return cls(validator), buf
