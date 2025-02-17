import sys
import zmq


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 ./example_zmq.py <connect_to> [topic topic ...]")
        sys.exit(0)

    connect_to = sys.argv[1]
    topics = sys.argv[2:]
    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect(connect_to)

    # manage subscriptions
    if not topics:
        print("Receiving messages on ALL topics...")
        s.setsockopt(zmq.SUBSCRIBE, b"")
    else:
        print(f"Receiving messages on topics: {topics} ...")
        for t in topics:
            s.setsockopt(zmq.SUBSCRIBE, bytes.fromhex(t))
    print
    try:
        while True:
            msg = s.recv_multipart()
            hex_string = [b.hex() for b in msg]
            print("msg: {}".format(hex_string))

    except KeyboardInterrupt:
        pass
    print("Done.")


if __name__ == "__main__":
    main()
