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

    def encode(self, buf: bytes) -> bytes:
        buf = self.sender.encode(buf)
        buf = self.receiver.encode(buf)
        buf = encoding.append_fixed_bytes(buf, self.public_key)
        return self.stake.encode(buf)

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
