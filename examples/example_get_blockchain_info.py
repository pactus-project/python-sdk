from pactus_grpc.blockchain_pb2_grpc import BlockchainStub
from pactus_grpc.blockchain_pb2 import GetBlockchainInfoRequest
import grpc


def main() -> None:
    # Creating a gRPC channel
    channel = grpc.insecure_channel("testnet1.pactus.org:50052")

    # Creating a stub from channel
    stub = BlockchainStub(channel)

    # Initialize a request and call get blockchain info method
    req = GetBlockchainInfoRequest()
    blockchain_info = stub.GetBlockchainInfo(req)

    print(f"Blockchain info:\n{blockchain_info}")


if __name__ == "__main__":
    main()
