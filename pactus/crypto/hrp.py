class HRP:
    ADDRESS_HRP = "pc"
    PUBLIC_KEY_HRP = "public"
    PRIVATE_KEY_HRP = "secret"

    @classmethod
    def use_mainnet(cls) -> None:
        cls.ADDRESS_HRP = "pc"
        cls.PUBLIC_KEY_HRP = "public"
        cls.PRIVATE_KEY_HRP = "secret"

    @classmethod
    def use_testnet(cls) -> None:
        cls.ADDRESS_HRP = "tpc"
        cls.PUBLIC_KEY_HRP = "tpublic"
        cls.PRIVATE_KEY_HRP = "tsecret"