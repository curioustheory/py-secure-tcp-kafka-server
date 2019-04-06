import argparse


def init_program():
    """allows the program parameter to be set via the command line"""

    parser = argparse.ArgumentParser(description="Kafka TCP Stream Forwarder.")

    # KAFKA CONFIG
    # ================================================================================
    parser.add_argument("-k", "--kafka", help="Kafka host:ip to forward to")
    parser.add_argument("-t", "--topic", help="Topic for messages")
    parser.add_argument("-m", "--management", help="Topic for connection events")

    # SOCKET SERVER CONFIG
    # ================================================================================
    parser.add_argument("-c", "--client", help="Add another IP host address or CIDR address to approved clients")
    parser.add_argument("-p", "--port", help="Listen for client connections on this port")

    # SSL CONFIG
    # ================================================================================
    parser.add_argument("-f", "--cert", help="Certificate for server")

    # APPLICATION CONFIG
    # ================================================================================
    parser.add_argument("-w", "--whitelist", nargs="*", help="List of whitelisted IP")
    parser.add_argument("--info", action="store_true", default=False, help="More logging to console")
    parser.add_argument("--debug", action="store_true", default=False, help="Most detailed logging to console")

    args = parser.parse_args()
    return args
