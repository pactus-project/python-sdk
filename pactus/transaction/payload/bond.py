from pactus.crypto.address import Address
from pactus.encoding import encoding
from pactus.types.amount import Amount

from ._payload import PayloadType


class BondPayload:
    def __init__(
        self,
        sender: Address,
        receiver: Address,
        public_key: bytes,
        stake: Amount,
    ) -> None:
        self.sender = sender
        self.receiver = receiver
        self.public_key = public_key
        self.stake = stake

    def encode(self, buf: list) -> None:
        encoding.append_fixed_bytes(buf, self.sender.raw_bytes())
        encoding.append_fixed_bytes(buf, self.receiver.raw_bytes())
        encoding.append_fixed_bytes(buf, self.public_key)
        encoding.append_var_int(buf, self.stake.value)

    def get_type(self) -> PayloadType:
        return PayloadType.BOND

    def signer(self) -> Address:
        return self.sender

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        sender, buf = Address.decode(buf)
        receiver, buf = Address.decode(buf)

        pub_key_size, buf = encoding.read_var_int(buf)
        public_key = None
        if pub_key_size == 96:
            public_key, buf = encoding.read_fixed_bytes(buf, 96)
        elif pub_key_size != 0:
            msg = f"invalid public key size: {pub_key_size}"
            raise ValueError(msg)

        stake, buf = Amount.decode(buf)
        return cls(sender, receiver, public_key, stake), buf
