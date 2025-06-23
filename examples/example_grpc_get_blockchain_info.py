from pactus_grpc.blockchain_pb2_grpc import BlockchainStub
from pactus_grpc.blockchain_pb2 import GetBlockchainInfoRequest
import grpc


def main() -> None:
    # Creating a gRPC channel
    channel = grpc.insecure_channel("bootstrap1.pactus.org:50051")

    # Creating a stub from channel
    stub = BlockchainStub(channel)

    # Initialize a request and call get blockchain info method
    req = GetBlockchainInfoRequest()
    res = stub.GetBlockchainInfo(req)

    print(f"Blockchain info:\n{res}")


if __name__ == "__main__":
    main()
