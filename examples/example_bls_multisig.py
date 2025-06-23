from pactus.crypto.bls.private_key import PrivateKey
from pactus.crypto.bls.public_key import PublicKey
from pactus.crypto.bls.signature import Signature


def main() -> None:
    msg = "some message".encode()
    prv1 = PrivateKey.random()
    prv2 = PrivateKey.random()

    pub1 = prv1.public_key()
    pub2 = prv2.public_key()

    sig1 = prv1.sign(msg)
    sig2 = prv2.sign(msg)

    agg_pub = PublicKey.aggregate([pub1, pub2])
    agg_sig = Signature.aggregate([sig1, sig2])

    if not agg_pub.verify(msg, agg_sig):
        print("Signature verification failed")
        exit(1)

    print(f"Aggregated signature: {agg_sig.string()}")


if __name__ == "__main__":
    main()
