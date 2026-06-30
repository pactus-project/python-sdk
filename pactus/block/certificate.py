from pactus.crypto.bls.signature import Signature
from pactus.encoding import encoding
from pactus.types.height import Height
from pactus.types.round import Round


class Certificate:
    def __init__(
        self,
        height: Height,
        round_: Round,
        committers: list,
        absentees: list,
        signature: Signature,
    ) -> None:
        self.height = height
        self.round = round_
        self.committers = committers
        self.absentees = absentees
        self.signature = signature

    @classmethod
    def decode(cls, buf: bytes) -> tuple:
        """
        Decode a Certificate from bytes.
        Returns (Certificate, remaining_buf).
        """
        height, buf = Height.decode(buf)
        round_, buf = Round.decode(buf)

        num_committers, buf = encoding.read_var_int(buf)
        committers = []
        for _ in range(num_committers):
            n, buf = encoding.read_var_int(buf)
            committers.append(n)

        num_absentees, buf = encoding.read_var_int(buf)
        absentees = []
        for _ in range(num_absentees):
            n, buf = encoding.read_var_int(buf)
            absentees.append(n)

        signature, buf = Signature.decode(buf)

        cert = cls(height, round_, committers, absentees, signature)
        return cert, buf
