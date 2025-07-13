from pactus_jsonrpc.client import PactusOpenRPCClient
import asyncio


async def main() -> None:
    client_url = "https://testnet1.pactus.org/jsonrpc"
    client = PactusOpenRPCClient(
        headers={},
        client_url=client_url)

    res = await client.pactus.network.get_node_info()

    print(f"Node info:\n{res}")


if __name__ == "__main__":
    asyncio.run(main())
