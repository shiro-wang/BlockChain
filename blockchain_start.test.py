import sys
import os
import socket
import json
from unittest.mock import patch, MagicMock
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BlockChain.blockchain_start import BlockChain
from Architecture.Block import Block
from Architecture.Transaction import Transaction

class TestBlockChain:
    def setUp(self):
        self.socket_host = "192.168.1.132"
        self.socket_port = 8000
        self.blockchain = BlockChain(self.socket_host, self.socket_port)

    # Should successfully mine a block and add it to the blockchain
    # def test_mine_block_and_add_to_blockchain(self):
    #     initial_chain_length = len(self.blockchain.chain)
    #     miner_address = "test_miner_address"
        
    #     # Mock the get_hash method to always return a valid hash
    #     with patch.object(self.blockchain, 'get_hash', return_value='0' * self.blockchain.difficulty):
    #         self.blockchain.mine_block(miner_address)
        
    #     # Check if a new block was added to the chain
    #     assert len(self.blockchain.chain) == initial_chain_length + 1
        
    #     # Verify the newly added block
    #     new_block = self.blockchain.chain[-1]
    #     assert new_block.miner == miner_address
    #     assert new_block.previous_hash == self.blockchain.chain[-2].hash
    #     assert new_block.hash.startswith('0' * self.blockchain.difficulty)

    # # Should correctly adjust difficulty after mining a block
    # def test_adjust_difficulty_after_mining(self):
    #     initial_difficulty = self.blockchain.difficulty
    #     self.blockchain.mine_block(self.blockchain.address)
    #     self.blockchain.adjust_difficulty()
    #     self.assertNotEqual(initial_difficulty, self.blockchain.difficulty, "Difficulty should be adjusted after mining a block")

    # Should create a new transaction and add it to pending transactions
    def test_start_create_transaction(self):
        with patch('builtins.input', side_effect=['receiver123', '100', '5', 'Test message']):
            with patch.object(self.blockchain, 'new_transaction') as mock_new_transaction:
                self.blockchain.start_create_transaction()

                mock_new_transaction.assert_called_once_with(
                    self.blockchain.address,
                    'receiver123',
                    100,
                    5,
                    'Test message',
                    self.blockchain.private
                )

    # Should broadcast a newly mined block to all nodes in the network
    def test_broadcast_mined_block(self):
        with patch.object(self.blockchain, 'broadcast_block') as mock_broadcast:
            fake_transaction = MagicMock()
            self.blockchain.fake_mining(self.blockchain.address, fake_transaction)
            
            mock_broadcast.assert_called_once()
            broadcasted_block = mock_broadcast.call_args[0][0]
            
            assert isinstance(broadcasted_block, Block)
            assert broadcasted_block.previous_hash == self.blockchain.chain[-2].hash
            assert broadcasted_block.miner == self.blockchain.address
            assert fake_transaction in broadcasted_block.transactions

    # Should correctly calculate and display the balance for a given address
    def test_start_getbalance(self, capsys):
        # Mock the get_balance method to return a specific value
        self.blockchain.get_balance = MagicMock(return_value=100)

        # Call the start_getbalance method
        self.blockchain.start_getbalance()

        # Capture the printed output
        captured = capsys.readouterr()

        # Assert that the correct balance is printed
        assert "My balance:\n100" in captured.out
        assert "Finish service..." in captured.out

        # Assert that the get_balance method was called with the correct address
        self.blockchain.get_balance.assert_called_once_with(self.blockchain.address)

        # Assert that adjust_difficulty is called at least once
        self.blockchain.adjust_difficulty.assert_called()

    # Should generate a new address and private key when account data is not found
    def test_generate_new_address_when_account_data_not_found(self):
        # Mock the file operations
        with patch('builtins.open', side_effect=FileNotFoundError), \
            patch('json.dump'), \
            patch.object(BlockChain, 'generate_address', return_value=('new_address', 'new_private_key')):
            
            # Create a BlockChain instance
            blockchain = BlockChain(self.socket_host, self.socket_port)
            
            # Mock the input function to simulate user input
            with patch('builtins.input', side_effect=['4']):
                # Call the start method
                blockchain.start()
            
            # Assert that the address and private key were set correctly
            self.assertEqual(blockchain.address, 'new_address')
            self.assertEqual(blockchain.private, 'new_private_key')
            
            # Assert that the generate_address method was called
            blockchain.generate_address.assert_called_once()
            
            # Assert that the file write operation was attempted
            open.assert_called_with(os.path.join("./myaccount.json"), 'w')
            json.dump.assert_called_once()

    # Should successfully clone the blockchain from a given source
    @patch('sys.argv', ['script_name', '8000', 'source_blockchain'])
    @patch('blockchain_start.BaseP2PConnection')
    @patch('blockchain_start.BaseBlockChain.clone_blockchain')
    def test_clone_blockchain(self, mock_clone_blockchain, mock_base_p2p_connection):
        # Arrange
        socket_host = "192.168.1.132"
        socket_port = 8000
        mock_p2p_connection = MagicMock()
        mock_base_p2p_connection.return_value = mock_p2p_connection

        # Act
        blockchain = BlockChain(socket_host, socket_port)

        # Assert
        mock_clone_blockchain.assert_called_once_with('source_blockchain')

    # Should reject a fake transaction during the mining process
    def test_reject_fake_transaction_during_mining(self):
        # Mock necessary dependencies
        with patch('time.process_time', return_value=0), \
            patch('random.getrandbits', return_value=0), \
            patch.object(self.blockchain, 'get_hash', return_value='0' * self.blockchain.difficulty):

            # Create a fake transaction
            fake_transaction = MagicMock()

            # Set up the blockchain with a valid block
            self.blockchain.chain = [MagicMock(hash='valid_hash')]
            self.blockchain.difficulty = 1
            self.blockchain.block_limitation = 5
            self.blockchain.pending_transactions = []
            self.blockchain.receive_verified_block = True

            # Call the fake_mining method
            result = self.blockchain.fake_mining('miner_address', fake_transaction)

            # Assert that the method returns False (rejected)
            assert result == False

            # Assert that the fake transaction was not added to the blockchain
            assert len(self.blockchain.chain) == 1
            assert fake_transaction not in self.blockchain.chain[-1].transactions

            # Assert that pending transactions were cleared
            assert len(self.blockchain.pending_transactions) == 0

            # Assert that receive_verified_block was reset
            assert self.blockchain.receive_verified_block == False

    # Should handle network interruptions gracefully during block broadcasting
    def test_broadcast_block_with_network_interruption(self):
        # Mock the broadcast_block method to simulate a network interruption
        with patch.object(self.blockchain, 'broadcast_block', side_effect=socket.error("Network error")):
            miner = "test_miner_address"
            fake_transaction = Transaction("sender", "receiver", 100, 1, "test message")
            
            # Call fake_mining method
            result = self.blockchain.fake_mining(miner, fake_transaction)
            
            # Assert that the method returns False when a network error occurs
            assert result == False
            
            # Check that the block was still added to the chain despite the network error
            assert len(self.blockchain.chain) > 0
            assert self.blockchain.chain[-1].transactions[-1] == fake_transaction
            
            # Verify that an attempt was made to broadcast the block
            self.blockchain.broadcast_block.assert_called_once()

    # Should correctly process and validate incoming transactions from other nodes
    def test_process_incoming_transaction(self):
        # Mock the necessary methods and attributes
        self.blockchain.p2p_connection = MagicMock()
        self.blockchain.pending_transactions = []
        self.blockchain.verify_transaction = MagicMock(return_value=True)
        
        # Create a sample transaction
        sample_transaction = {
            'sender': 'sender_address',
            'receiver': 'receiver_address',
            'amount': 100,
            'fee': 1,
            'message': 'Test transaction'
        }
        
        # Simulate receiving a transaction from another node
        self.blockchain.receive_broadcast_transaction(sample_transaction)
        
        # Assert that the transaction was added to pending_transactions
        self.assertEqual(len(self.blockchain.pending_transactions), 1)
        self.assertEqual(self.blockchain.pending_transactions[0], sample_transaction)
        
        # Assert that verify_transaction was called
        self.blockchain.verify_transaction.assert_called_once_with(sample_transaction)

if __name__ == '__main__':
    unittest.main()
