import argparse

from pactus.crypto import CryptoConfig
from pactus.crypto.address import AddressType
from pactus.crypto.bls.private_key import PrivateKey as BLSPrivateKey
from pactus.crypto.ed25519.private_key import PrivateKey as Ed25519PrivateKey
from pactus.crypto.private_key import PrivateKey
from pactus.crypto.public_key import PublicKey
from pactus.crypto.address import Address


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Key Pair")

    parser.add_argument(
        "--address-type",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="Type of address to generate: 1 for Validator, 2 for BLSAccount, 3 for Ed25519Account (default: 3)",
    )

    parser.add_argument(
        "--testnet",
        action="store_true",
        help="Specify if the key should be created for the testnet",
    )
    args = parser.parse_args()

    if args.testnet:
        CryptoConfig.use_testnet()

    match AddressType(args.address_type):
        case AddressType.VALIDATOR:
            # Generate a cryptographically secure IKM (Initial Keying Material).
            sec = BLSPrivateKey.random()
            pub = sec.public_key()
            addr = pub.validator_address()
            show(sec, pub, addr)

        case AddressType.BLS_ACCOUNT:
            sec = BLSPrivateKey.random()
            pub = sec.public_key()
            addr = pub.account_address()
            show(sec, pub, addr)

        case AddressType.ED25519_ACCOUNT:
            sec = Ed25519PrivateKey.random()
            pub = sec.public_key()
            addr = pub.account_address()
            show(sec, pub, addr)

        case _:
            return


def show(sec: PrivateKey, pub: PublicKey, addr: Address):
    print(f"Your PrivateKey: {sec.string()}")
    print(f"Your PublicKey: {pub.string()}")
    print(f"Your Address: {addr.string()}")


if __name__ == "__main__":
    main()
