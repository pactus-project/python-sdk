from pactus.rpc.blockchain_pb2_grpc import BlockchainStub
from pactus.rpc.blockchain_pb2 import GetConsensusInfoRequest
import grpc


def main() -> None:
    # Creating a gRPC channel
    channel = grpc.insecure_channel("bootstrap1.pactus.org:50051")

    # Creating a stub from channel
    stub = BlockchainStub(channel)

    # Initialize a request and call get consensus info method
    req = GetConsensusInfoRequest()
    consensus_info = stub.GetConsensusInfo(req)

    print(f"Consensus info:\n{consensus_info}")


if __name__ == "__main__":
    main()
