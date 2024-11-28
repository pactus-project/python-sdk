from __future__ import annotations

from enum import Enum

from pactus.crypto import CryptoConfig
from pactus.utils import utils

# Address format: hrp + `1` + type + data + checksum

ADDRESS_SIZE = 21
TREASURY_ADDRESS_STRING = "000000000000000000000000000000000000000000"


class AddressType(Enum):
    TREASURY = 0
    VALIDATOR = 1
    BLS_ACCOUNT = 2
    ED25519_ACCOUNT = 3


class Address:
    def __init__(self, address_type: AddressType, data: bytes) -> None:
        if len(data) != ADDRESS_SIZE - 1:
            msg = "Data must be 21 bytes long"
            raise ValueError(msg)

        self.data = bytearray()
        self.data.append(address_type.value)
        self.data.extend(data)

    @classmethod
    def from_string(cls, text: str) -> Address:
        if text == TREASURY_ADDRESS_STRING:
            return bytes([0])

        hrp, typ, data = utils.decode_to_base256_with_type(text)
        if hrp != CryptoConfig.ADDRESS_HRP:
            msg = f"Invalid HRP: {hrp}"
            raise ValueError(msg)

        typ = AddressType(typ)
        if typ in (AddressType.VALIDATOR, AddressType.BLS_ACCOUNT, AddressType.ED25519_ACCOUNT):
            if len(data) != 20:
                msg = f"Invalid length: {len(data) + 1}"
                raise ValueError(msg)
        else:
            msg = f"Invalid address type: {typ}"
            raise ValueError(msg)

        return cls(typ, data)

    def raw_bytes(self) -> bytes:
        return bytes(self.data)

    def string(self) -> str:
        if self.data == bytes([0]):
            return TREASURY_ADDRESS_STRING

        return utils.encode_from_base256_with_type(
            CryptoConfig.ADDRESS_HRP,
            self.data[0],
            self.data[1:],
        )

    def address_type(self) -> AddressType:
        return AddressType(self.data[0])

    def is_treasury_address(self) -> bool:
        return self.address_type() == AddressType.TREASURY

    def is_account_address(self) -> bool:
        t = self.address_type()
        return t in (AddressType.TREASURY, AddressType.BLS_ACCOUNT, AddressType.ED25519_ACCOUNT)

    def is_validator_address(self) -> bool:
        return self.address_type() == AddressType.VALIDATOR
