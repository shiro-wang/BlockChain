import hashlib
import pickle
import socket
import sys
import threading
import time
import random
import json
import os
import argparse

import rsa
from threading import Timer

from Architecture.Transaction import Transaction
from Architecture.Block import Block
from Architecture.BaseBlockChain import BaseBlockChain
from Architecture.BaseP2PConnection import BaseP2PConnection
from Chain_tools.utils import parse_args

class BlockChain(BaseBlockChain):
    def __init__(self, args):
        self.p2p_connection = BaseP2PConnection(args.socket_host, args.socket_port)
        super().__init__(self.p2p_connection, args)
        
        # self.receive_vertified_transaction = False
        self.start_socket_server()

    def start(self, force_stop=False):
        print("Start server...")
        try:
            with open(os.path.join("./server/myaccount.json"), 'r') as json_account:
                print("Loading account data...")
                data = json.load(json_account)
                address = data["address"]
                private = data["private"]
        except:
            print("Can't found account data, start create new one!")
            address, private = self.generate_address()
            data = {"address":address, "private": private}
            with open(os.path.join("./server/myaccount.json"), 'w') as json_account:
                account = json.dumps(data)
                json_account.write(account)
        print(f"Miner address: {address}")
        print(f"Miner private: {private}")
        self.address = address
        self.create_genesis_block()

        while(True):
            self.mine_block(address)
            self.adjust_difficulty()
            if force_stop:
                break

   

if __name__ == '__main__':
    args = parse_args()
    block = BlockChain(args)
    block.start()