#!/usr/bin/env python3
"""
Pactus SDK Example: Fetch and Decode a Block
=============================================

This example demonstrates how to:
1. Connect to the Pactus testnet via JSON-RPC
2. Fetch blockchain info and pick a random block height
3. Retrieve a block data and decode the block using pactus-sdk
4. Print the block's details, including header, previous certificate, and transactions.
"""

import asyncio
import random

from pactus.block import Block
from pactus_jsonrpc.client import PactusOpenRPCClient

TESTNET_RPC = "https://testnet1.pactus.org/jsonrpc"

async def fetch_and_decode_block():
    client = PactusOpenRPCClient(
        headers={},
        timeout=30,
        client_url=TESTNET_RPC,
    )

    # print("Connecting to Pactus testnet...")
    # info = await client.pactus.blockchain.get_blockchain_info()
    # latest_height = info["last_block_height"]
    # print(f"  Latest height: {latest_height}")

    height = random.randint(10_000, 1_000_000)
    print(f"\nFetching block at height {height}...")

    res = await client.pactus.blockchain.get_block(height=height, verbosity=0)
    block = Block.decode(bytes.fromhex(res["data"]))

    print(f"  - Hash:       {block.id}")
    print(f"  - Version:    {block.header.version}")
    print(f"  - Prev Hash:  {block.header.prev_block_hash}")
    print(f"  - Time:       {block.header.unix_time}")
    print(f"  - State Root: {block.header.state_root}")
    print(f"  - Proposer:   {block.header.proposer_address.string()}")

    print("  - Previous Certificate:")
    print(f"    - Committers: {block.prev_cert.committers}")
    print(f"    - Absentees:  {block.prev_cert.absentees}")
    print(f"    - Signature:  {block.prev_cert.signature.string()}")


    print("  - Transactions:")
    for i, tx in enumerate(block.transactions):
        print(f"     - {i}: {tx.id()}")

if __name__ == "__main__":
    asyncio.run(fetch_and_decode_block())
