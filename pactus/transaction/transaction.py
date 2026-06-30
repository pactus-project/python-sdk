from pactus.crypto.address import Address, AddressType
from pactus.crypto.bls.public_key import PublicKey as BLSPublicKey
from pactus.crypto.bls.signature import Signature as BLSSignature
from pactus.crypto.ed25519.public_key import PublicKey as Ed25519PublicKey
from pactus.crypto.ed25519.signature import Signature as Ed25519Signature
from pactus.crypto.private_key import PrivateKey
from pactus.crypto.public_key import PublicKey
from pactus.crypto.secp256k1.public_key import PublicKey as Secp256k1PublicKey
from pactus.crypto.secp256k1.signature import Signature as Secp256k1Signature
from pactus.crypto.signature import Signature
from pactus.encoding import encoding
from pactus.types.amount import Amount
from pactus.types.height import Height

from .payload import (
    BondPayload,
    Payload,
    PayloadType,
    SortitionPayload,
    TransferPayload,
    UnbondPayload,
    WithdrawPayload,
)

FLAG_STRIPPED_PUBLIC_KEY = 0x01
FLAG_NOT_SIGNED = 0x02


class Transaction:
    def __init__(
        self,
        lock_time: Height,
        fee: Amount,
        memo: str,
        payload: Payload,
    ) -> None:
        self.lock_time = lock_time
        self.memo = memo
        self.flags = 0
        self.version = 1
        self.fee = fee
        self.payload = payload
        self.public_key: PublicKey = None
        self.signature: Signature = None

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        """
        Decode a Transaction from bytes.
        Returns (Transaction, remaining_buf).
        """
        flags, buf = encoding.read_uint8(buf)
        version, buf = encoding.read_uint8(buf)
        lock_time, buf = Height.decode(buf)
        fee, buf = Amount.decode(buf)
        memo, buf = encoding.read_str(buf)
        payload_type, buf = encoding.read_uint8(buf)

        if payload_type == PayloadType.TRANSFER.value:
            payload, buf = TransferPayload.decode(buf)
        elif payload_type == PayloadType.BOND.value:
            payload, buf = BondPayload.decode(buf)
        elif payload_type == PayloadType.SORTITION.value:
            payload, buf = SortitionPayload.decode(buf)
        elif payload_type == PayloadType.UNBOND.value:
            payload, buf = UnbondPayload.decode(buf)
        elif payload_type == PayloadType.WITHDRAW.value:
            payload, buf = WithdrawPayload.decode(buf)
        else:
            msg = f"unknown payload type: {payload_type}"
            raise ValueError(msg)

        tx = cls.__new__(cls)
        tx.flags = flags
        tx.version = version
        tx.lock_time = lock_time
        tx.fee = fee
        tx.memo = memo
        tx.payload = payload
        tx.public_key = None
        tx.signature = None

        if flags & FLAG_NOT_SIGNED:
            return tx, buf

        signer_type = payload.signer().address_type()
        sig, buf = Transaction._decode_signature(buf, signer_type)
        tx.signature = sig

        if (flags & FLAG_STRIPPED_PUBLIC_KEY) == 0:
            pub, buf = Transaction._decode_public_key(buf, signer_type)
            tx.public_key = pub

        return tx, buf

    @staticmethod
    def _decode_signature(buf: bytes, signer_type: AddressType) -> tuple:
        if signer_type in (AddressType.VALIDATOR, AddressType.BLS_ACCOUNT):
            return BLSSignature.decode(buf)
        if signer_type == AddressType.ED25519_ACCOUNT:
            return Ed25519Signature.decode(buf)
        if signer_type == AddressType.SECP256K1_ACCOUNT:
            return Secp256k1Signature.decode(buf)
        msg = f"cannot decode signature for address type: {signer_type}"
        raise ValueError(msg)

    @staticmethod
    def _decode_public_key(buf: bytes, signer_type: AddressType) -> tuple:
        if signer_type in (AddressType.VALIDATOR, AddressType.BLS_ACCOUNT):
            return BLSPublicKey.decode(buf)
        if signer_type == AddressType.ED25519_ACCOUNT:
            return Ed25519PublicKey.decode(buf)
        if signer_type == AddressType.SECP256K1_ACCOUNT:
            return Secp256k1PublicKey.decode(buf)
        msg = f"cannot decode public key for address type: {signer_type}"
        raise ValueError(msg)

    @classmethod
    def create_transfer_tx(
        cls,
        lock_time: Height,
        sender: Address,
        receiver: Address,
        amount: Amount,
        fee: Amount,
        memo: str = "",
    ) -> "Transaction":
        payload = TransferPayload(sender, receiver, amount)
        return cls(lock_time, fee, memo, payload)

    @classmethod
    def create_bond_tx(
        cls,
        lock_time: Height,
        sender: Address,
        receiver: Address,
        public_key: bytes,
        fee: Amount,
        stake: Amount,
        memo: str = "",
    ) -> "Transaction":
        payload = BondPayload(sender, receiver, public_key, stake)
        return cls(lock_time, fee, memo, payload)

    @classmethod
    def create_unbond_tx(
        cls,
        lock_time: Height,
        validator: Address,
        memo: str = "",
    ) -> "Transaction":
        payload = UnbondPayload(validator)
        return cls(lock_time, 0, memo, payload)

    @classmethod
    def create_withdraw_tx(
        cls,
        lock_time: Height,
        from_addr: Address,
        to_addr: Address,
        amount: Amount,
        fee: Amount,
        memo: str = "",
    ) -> "Transaction":
        payload = WithdrawPayload(from_addr, to_addr, amount)
        return cls(lock_time, fee, memo, payload)

    def _get_unsigned_bytes(self, buf: bytes) -> bytes:
        """
        Generate the unsigned representation of the transaction,
        including flags and payload.

        This method appends various transaction components to the buffer
        in a specific order, ensuring correct serialization.
        """
        encoding.append_uint8(buf, self.flags)
        encoding.append_uint8(buf, self.version)
        encoding.append_uint32(buf, self.lock_time.value)
        encoding.append_var_int(buf, self.fee.value)
        encoding.append_str(buf, self.memo)
        encoding.append_uint8(buf, self.payload.get_type().value)
        self.payload.encode(buf)

        return buf

    def sign_bytes(self) -> bytes:
        """
        Generate the transaction data that needs to be signed.

        The signature should be computed over this data, excluding the
        transaction flags, which are removed before returning.
        """
        buf = bytearray()
        sign_bytes = self._get_unsigned_bytes(buf)

        return sign_bytes[1:]  # flags is not part of the sign bytes.

    def sign(self, private_key: PrivateKey) -> bytes:
        """
        Generate the signed representation of the transaction,
        including the flags, payload, and cryptographic signature.

        This method first generates the data needs to be signed,
        signs it using the provided private key, and then appends
        both the signature and the corresponding public key to ensure
        verifiability.
        """
        buf = bytearray()

        sign_bytes = self._get_unsigned_bytes(buf)
        sig = private_key.sign(
            bytes(sign_bytes[1:]),
        )
        pub = private_key.public_key()

        encoding.append_fixed_bytes(buf, sig.raw_bytes())
        encoding.append_fixed_bytes(buf, pub.raw_bytes())

        self.public_key = pub
        self.signature = sig
        self.flags |= FLAG_NOT_SIGNED

        return buf
