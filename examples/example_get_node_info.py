from pactus_grpc.network_pb2_grpc import NetworkStub
from pactus_grpc.network_pb2 import GetNodeInfoRequest
import grpc


def main() -> None:
    # Creating a gRPC channel
    channel = grpc.insecure_channel("bootstrap1.pactus.org:50051")

    # Creating a stub from channel
    stub = NetworkStub(channel)

    # Initialize a request and call get node info method
    req = GetNodeInfoRequest()
    res = stub.GetNodeInfo(req)

    print(f"Node info Response:\n{res.reachability}")


if __name__ == "__main__":
    main()
