import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Setting up the blockchain values")
    parser.add_argument(
        "--socket_host", 
        type=str,
        default="192.168.1.132",
        help="Set the host IP for the socket server",
    )
    parser.add_argument(
        "--socket_port",
        type=int,
        default=1111,
        help="Must set the host IP for the socket server",
    )
    parser.add_argument(
        "--clone_blockchain",
        type=str,
        default=None,
        help="Path to the target blockchain to clone",
    )
    parser.add_argument(
        "--difficulty",
        type=int,
        default=5,
        help="Set the difficulty of the blockchain",
    )
    parser.add_argument(
        "--adjust_difficulty_blocks",
        type=int,
        default=10,
        help="Set the number of blocks to adjust the difficulty",
    )
    parser.add_argument(
        "--block_time",
        type=int,
        default=30,
        help="Set the avg time bound to adjust the difficulty",
    )
    parser.add_argument(
        "--miner_rewards",
        type=int,
        default=10,
        help="Set the reward for the miner",
    )
    parser.add_argument(
        "--block_limitation",
        type=int,
        default=32,
        help="Set the max number of transactions per block",
    )
    args = parser.parse_args()

    # Sanity checks
    if args.socket_port is None:
        print("Please provide the port number for the socket server")
        sys.exit(1)
    return args