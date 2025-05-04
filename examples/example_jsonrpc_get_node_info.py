from pactus_jsonrpc.client import PactusOpenRPCClient
import pactus_jsonrpc.client
import asyncio


async def main() -> None:
    pactus_jsonrpc.client.CLIENT_URL = "https://testnet1.pactus.org/jsonrpc"
    client = PactusOpenRPCClient([])

    res = await client.pactus.network.get_node_info()

    print(f"Node info:\n{res}")


if __name__ == "__main__":
    asyncio.run(main())
