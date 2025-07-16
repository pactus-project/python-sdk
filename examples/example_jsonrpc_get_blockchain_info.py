from pactus_jsonrpc.client import PactusOpenRPCClient
import asyncio


async def main() -> None:
    client_url = "https://testnet1.pactus.org/jsonrpc"
    client = PactusOpenRPCClient(headers={}, client_url=client_url)

    res = await client.pactus.blockchain.get_blockchain_info()

    print(f"Blockchain info:\n{res}")


if __name__ == "__main__":
    asyncio.run(main())
