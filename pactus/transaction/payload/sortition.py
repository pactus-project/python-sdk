from pactus.crypto.address import Address
from pactus.encoding import encoding

from ._payload import PayloadType


class SortitionPayload:
    def __init__(self, address: Address, proof: bytes) -> None:
        self.address = address
        self.proof = proof

    def encode(self, buf: list) -> None:
        encoding.append_fixed_bytes(buf, self.address.raw_bytes())
        encoding.append_fixed_bytes(buf, self.proof)

    def get_type(self) -> PayloadType:
        return PayloadType.SORTITION

    def signer(self) -> Address:
        return self.address

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        address, buf = Address.decode(buf)
        proof, buf = encoding.read_fixed_bytes(buf, 48)
        return cls(address, proof), buf
