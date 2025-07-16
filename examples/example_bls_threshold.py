from pactus.crypto.bls.private_key import PrivateKey


# Example of BLS threshold signature aggregation using Shamir's Secret Sharing
# This example demonstrates how to create a threshold signature scheme
# where a subset of signers can create a valid signature.


def main() -> None:
    # msg = "some message".encode()
    N = 3  # Number of signers
    T = 2  # Threshold for aggregation

    msk = PrivateKey.random()  # Master Secret Key
    mpk = msk.public_key()

    print(f"Master Secret Key: {msk.raw_bytes().hex()}")
    print(f"Master Public Key: {mpk.string()}")

    shares = msk.split(N, T)

    for i, sk in enumerate(shares):
        print(f"Private Key Share {i + 1}: {sk.raw_bytes().hex()}")


if __name__ == "__main__":
    main()
