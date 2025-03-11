from pactus.crypto.bls.signature import Signature


def main() -> None:
    sig1 = Signature.from_string(
        "a628a8709fe00366d7150244447cc43e8637d76a20674b006b00f7a61109dab53ba5f1f66cd07219fd1e4a6bc7299d2d"
    )
    sig2 = Signature.from_string(
        "b0d544e501408283ac11ca8ae180f0991349252cc76f9db72011ea4917eca87d4640bcf3fab7b0ab95e9b94f05113587"
    )

    sig3 = Signature.aggregate([sig1, sig2])

    print(f"Aggregated signature: {sig3.string()}")


if __name__ == "__main__":
    main()
