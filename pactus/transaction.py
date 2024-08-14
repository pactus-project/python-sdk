import address
import amount
import serializer as sri
from enum import Enum


class PayloadType(Enum):
    Transfer = 1


class Transfer:
    """
    This class represents a Pactus transaction with transfer payload type.
    Check specs here: https://docs.pactus.org/protocol/transaction/transfer
    """

    def __init__(
        self,
        sender: address.Address,
        receiver: address.Address,
        amount: amount.Amount,
        memo: str,
        lock_time: int,
    ):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.lock_time = lock_time
        self.memo = memo

    def get_unsigned_bytes(self) -> bytes:
        """
        Get bytes method returns unsigned bytes of the transaction.
        It can be passed to sign method using a private key for signing.
        """
        buf = []
        flags = 0
        version = 1

        buf = []

        sri.append_uint8(buf, flags)
        sri.append_uint8(buf, version)

        sri.append_uint32(buf, self.lock_time)
        sri.append_var_int(buf, 0)  # TODO: add fee calculation logic
        sri.append_str(buf, self.memo)
        sri.append_uint8(buf, PayloadType.Transfer)  # Transfer payload
        sri.append_fixed_bytes(buf, self.sender.bytes())
        sri.append_fixed_bytes(buf, self.receiver.bytes())
        sri.append_var_int(buf, self.amount.amount)

        return buf
