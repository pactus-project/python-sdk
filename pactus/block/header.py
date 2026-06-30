from pactus.crypto.address import Address
from pactus.crypto.hash import Hash
from pactus.encoding import encoding


class Header:
    def __init__(
        self,
        version: int,
        unix_time: int,
        prev_block_hash: Hash,
        state_root: Hash,
        sortition_seed: bytes,
        proposer_address: Address,
    ) -> None:
        self.version = version
        self.unix_time = unix_time
        self.prev_block_hash = prev_block_hash
        self.state_root = state_root
        self.sortition_seed = sortition_seed
        self.proposer_address = proposer_address

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        """
        Decode a Header from bytes.
        Returns (Header, remaining_buf).
        """
        version, buf = encoding.read_uint8(buf)
        unix_time, buf = encoding.read_uint32(buf)
        prev_block_hash, buf = Hash.decode(buf)
        state_root, buf = Hash.decode(buf)
        sortition_seed, buf = encoding.read_fixed_bytes(buf, 48)
        proposer_address, buf = Address.decode(buf)

        header = cls(
            version,
            unix_time,
            prev_block_hash,
            state_root,
            sortition_seed,
            proposer_address,
        )
        return header, buf

    def encode(self, buf: bytes) -> bytes:
        buf = encoding.append_uint8(buf, self.version)
        buf = encoding.append_uint32(buf, self.unix_time)
        buf = self.prev_block_hash.encode(buf)
        buf = self.state_root.encode(buf)
        buf = encoding.append_fixed_bytes(buf, self.sortition_seed)
        return self.proposer_address.encode(buf)
