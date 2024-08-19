from pactus.crypto import CryptoConfig
from pactus.crypto.address import Address
from pactus.crypto.bls.private_key import PrivateKey
from pactus.transaction.transaction import Transaction
from pactus.types.amount import Amount


def main() -> None:
    CryptoConfig.use_testnet()

    lock_time = 1_735_096
    memo = "This is a test transaction"
    amount = Amount.from_string("1.5")
    fee = Amount.from_string("0.01")
    receiver = Address.from_string("tpc1zk4eztwv3fs6l9g776cfwkgujham79hrrwn82q5")

    sender = Address.from_string("tpc1z4rlzvq8lv92cnp0k3mk5jfr00kjnz0qvklvn3u")
    sec = PrivateKey.from_string(
        "tsecret1pzf33h72n9phxzaty5urh5ss4m33vvdfawyvesl5jtlt9a00tnwkqyngm6z"
    )

    tx = Transaction.create_transfer_tx(lock_time, sender, receiver, amount, fee, memo)
    tx.sign(sec)
    # 0001b8791a0080ade2041a5468697320697320612074657374207472616e7
    # 3616374696f6e0102a8fe2600ff61558985f68eed49246f7da5313c0c02b5
    # 7225b9914c35f2a3ded612eb2392bf77e2dc6380dea0cb05b8f2408955432
    # 25d79b919396bab6b5cbe195e844ace823f6f798292840a6182a04c501ffa
    # 67a2a9062ba248b4b81771ab5390b7c5771f1c7c8bc2040374423ad46c23e
    # 2ad54754a43fbc9661a51b29a2b4e844b31de5e81ecd3f124562526e90367
    # 935ee2e663449603b53745766863856ffd9477b18013ce06950d2c56e00fb
    # 00b78eeb6c737ea0960060a1c63eb67


if __name__ == "__main__":
    main()
