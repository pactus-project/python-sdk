from enum import Enum

from pactus.utils import utils

# Address format: hrp + `1` + type + data + checksum

AddressSize = 21
TreasuryAddressString = "000000000000000000000000000000000000000000"
AddressHRP = "pc"


class AddressType(Enum):
    Treasury = 0
    Validator = 1
    BLSAccount = 2


class Address:
    def __init__(self, address_type: AddressType, data: bytes) -> None:
        if len(data) != AddressSize - 1:
            msg = "Data must be 21 bytes long"
            raise ValueError(msg)

        self.data = bytearray()
        self.data.append(address_type.value)
        self.data.extend(data)

    @classmethod
    def from_string(cls, text: str) -> "Address":
        if text == TreasuryAddressString:
            return bytes([0])

        hrp, typ, data = utils.decode_to_base256_with_type(text)
        if hrp != AddressHRP:
            msg = f"Invalid HRP: {hrp}"
            raise ValueError(msg)

        typ = AddressType(typ)
        if typ in (AddressType.Validator, AddressType.BLSAccount):
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
            return TreasuryAddressString

        return utils.encode_from_base256_with_type(
            AddressHRP,
            self.data[0],
            self.data[1:],
        )

    def address_type(self) -> AddressType:
        return AddressType(self.data[0])

    def is_treasury_address(self) -> bool:
        return self.address_type() == AddressType.Treasury

    def is_account_address(self) -> bool:
        t = self.address_type()
        return t in (AddressType.Treasury, AddressType.BLSAccount)

    def is_validator_address(self) -> bool:
        return self.address_type() == AddressType.Validator
