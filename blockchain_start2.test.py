import unittest
from unittest.mock import patch, MagicMock
import json
import os

from blockchain_start import BlockChain
import server
from Architecture.Transaction import Transaction
from Architecture.Block import Block
from Chain_tools.utils import parse_args

class TestBlockChain(unittest.TestCase):
    def setUp(self):
        # To test the client, create a server first
        self.args = parse_args()
        with patch('blockchain_start.BaseP2PConnection'):
            self.blockchain = server.BlockChain(self.args)

    # Should clone an existing blockchain when 'clone_blockchain' argument is provided
    def test_clone_blockchain(self):
        mock_args = parse_args()
        mock_args.clone_blockchain = "192.168.1.132:1111"
        mock_args.socket_port = 8000
    
        with patch('blockchain_start.BaseP2PConnection'), \
             patch.object(BlockChain, 'clone_blockchain') as mock_clone, \
             patch.object(BlockChain, 'start_socket_server'):
            
            blockchain = BlockChain(mock_args)
            
            mock_clone.assert_called_once_with("192.168.1.132:1111")
    

if __name__ == '__main__':
    unittest.main()
