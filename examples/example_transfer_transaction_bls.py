from pactus.crypto import CryptoConfig
from pactus.crypto.address import Address
from pactus.crypto.bls.private_key import PrivateKey
from pactus.transaction.transaction import Transaction
from pactus.amount import Amount


def main() -> None:
    CryptoConfig.use_testnet()

    lock_time = 1_735_096
    memo = "This is a test transaction"
    amount = Amount.from_string("1.5")
    fee = Amount.from_string("0.01")
    receiver = Address.from_string("tpc1zk4eztwv3fs6l9g776cfwkgujham79hrrwn82q5")

    sender = Address.from_string("tpc1z4rlzvq8lv92cnp0k3mk5jfr00kjnz0qvklvn3u")
    sec = PrivateKey.from_string(
        "TSECRET1PZF33H72N9PHXZATY5URH5SS4M33VVDFAWYVESL5JTLT9A00TNWKQYNGM6Z"
    )

    tx = Transaction.create_transfer_tx(lock_time, sender, receiver, amount, fee, memo)
    signed_tx = tx.sign(sec)

    print(f"Signed transaction hex: {signed_tx.hex()}")


if __name__ == "__main__":
    main()
