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
        self.clone_blockchain(args.clone_blockchain)
        print(f"Node list: {self.p2p_connection.node_address}")
        self.broadcast_message_to_nodes("add_node", self.socket_host+":"+str(self.socket_port))
        
        # self.receive_vertified_transaction = False
        self.start_socket_server()

    def fake_mining(self, miner, fake_transaction):
        start = time.process_time()

        last_block = self.chain[-1]
        new_block = Block(last_block.hash, self.difficulty, miner, self.miner_rewards)
        print("check t num before adding:")
        print(len(self.pending_transactions))
        self.add_transaction_to_block(new_block)
        
        new_block.transactions.append(fake_transaction)

        print("put in fake transaction then try to find newblock faster than others")
        print("pre_hash: "+ str(last_block.hash) )
        new_block.previous_hash = last_block.hash
        new_block.difficulty = self.difficulty
        new_block.hash = self.get_hash(new_block, new_block.nonce)
        new_block.nonce = random.getrandbits(32)

        while new_block.hash[0: self.difficulty] != '0' * self.difficulty:
            new_block.nonce += 1
            new_block.hash = self.get_hash(new_block, new_block.nonce)
            if self.receive_verified_block:
                print(f"[**] Verified received block. Mine next!")
                self.receive_verified_block = False
                print("too slow, try again")
                if len(self.pending_transactions) > self.block_limitation:
                    self.pending_transactions = self.pending_transactions[self.block_limitation:]
                else:
                    self.pending_transactions = []
                return False
            # if self.receive_vertified_transaction:
            #     print(f"[**] Verified received transaction. Reset mining!")
            #     self.receive_vertified_transaction = False
            #     block_or_transaction = False
            #     return False
        print("Found newb! broadcast fake block...")
        if len(self.pending_transactions) > self.block_limitation:
            self.pending_transactions = self.pending_transactions[self.block_limitation:]
        else:
            self.pending_transactions = []
        self.pending_transactions = self.pending_transactions[self.block_limitation:]
        self.broadcast_block(new_block)
        
        #self.pending_transactions = self.pending_transactions[state:]

        time_consumed = round(time.process_time() - start, 5)
        print(f"Hash: {new_block.hash} @ diff {self.difficulty}; {time_consumed}s")
        self.chain.append(new_block)
        return False
    

    def start(self):
        try:
            with open(os.path.join("./client/myaccount.json"), 'r') as json_account:
                print("Loading account data...")
                data = json.load(json_account)
                address = data["address"]
                private = data["private"]
        except:
            print("Can't found account data, start create new one!")
            address, private = self.generate_address()
            data = {"address":address, "private": private}
            with open(os.path.join("./client/myaccount.json"), 'w') as json_account:
                account = json.dumps(data)
                json_account.write(account)
        print(f"Miner address: {address}")
        print(f"Miner private: {private}")
        self.address = address
        self.private = private
        print("Please enter number to choose the process you want...")
        print("1: Mining")
        print("2: Add transaction")
        print("3: Show balance")
        print("4: Try add fake transaction")
        while True:
            choise = input()
            if (choise == "1"):
                self.start_mining()
            elif (choise == "2"):
                self.start_create_transaction()
                return False
            elif (choise == "3"):
                self.start_getbalance()
                return False
            elif (choise == "4"):
                self.start_attack()
            else:
                print("Input is not acceptable, please try again")
    
    def start_mining(self):
        while(True):
            self.mine_block(self.address)
            self.adjust_difficulty()

    def start_create_transaction(self):
        print("Start create transaction...")
        receiver = input("Receiver:")
        amounts = int(input("Amount:"))
        fee = int(input("fee:"))
        message = input("Message:")
        self.new_transaction(self.address, receiver, amounts, fee, message, self.private)
        
    def start_getbalance(self):
        print("My balance:")
        print(self.get_balance(self.address))
        print("Finish service...")
        while(True):
            self.adjust_difficulty()

    def start_attack(self):
        print("Start add faked transaction")
        sender = input("Sender:")
        receiver = input("Receiver:")
        amounts = int(input("Amount:"))
        fee = int(input("fee:"))
        message = input("Message:")
        fake_t = self.initialize_transaction(sender, receiver, amounts, fee, message)
        while True:
            self.fake_mining(self.address, fake_t)
            self.adjust_difficulty()

if __name__ == '__main__':
    args = parse_args()
    block = BlockChain(args)
    block.start()