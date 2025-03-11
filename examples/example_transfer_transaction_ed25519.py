from pactus.crypto import CryptoConfig
from pactus.crypto.address import Address
from pactus.crypto.ed25519.private_key import PrivateKey
from pactus.transaction.transaction import Transaction
from pactus.amount import Amount


def main() -> None:
    CryptoConfig.use_testnet()

    lock_time = 1_735_096
    memo = "This is a test transaction"
    amount = Amount.from_string("1.5")
    fee = Amount.from_string("0.01")
    receiver = Address.from_string("tpc1ryz6m8meyfemyr4dhavz5aq067kkvs9mptpqnxr")

    sender = Address.from_string("tpc1rv75w2y9hj64ht9spxx0e5s7avpclk9ey2eaavf")
    sec = PrivateKey.from_string(
        "TSECRET1RGLSGPYLQRVET27AZUVS9TSP8MPGF9LH4U4RKKARMCATFK9L0KUCS7DCC09"
    )

    tx = Transaction.create_transfer_tx(lock_time, sender, receiver, amount, fee, memo)
    signed_tx = tx.sign(sec)

    print(f"Signed transaction hex: {signed_tx.hex()}")


if __name__ == "__main__":
    main()
