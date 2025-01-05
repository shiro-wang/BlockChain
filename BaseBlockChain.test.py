import unittest
import socket
import pickle
from unittest.mock import patch, MagicMock
from Architecture.BaseBlockChain import BaseBlockChain
from Architecture.Transaction import Transaction
from Architecture.Block import Block
from Chain_tools.utils import parse_args

class TestBaseBlockChain(unittest.TestCase):
    def setUp(self):
        self.args = parse_args()
        self.p2p_connection_mock = MagicMock()
        self.blockchain = BaseBlockChain(self.p2p_connection_mock, self.args)

    # Should create a genesis block with correct initial values
    def test_create_genesis_block(self):
        self.blockchain.create_genesis_block()
        
        self.assertEqual(len(self.blockchain.chain), 1)
        genesis_block = self.blockchain.chain[0]
        
        self.assertEqual(genesis_block.previous_hash, 'Hello World!')
        self.assertEqual(genesis_block.difficulty, self.blockchain.difficulty)
        self.assertEqual(genesis_block.miner, 'lkm543')
        self.assertEqual(genesis_block.miner_rewards, self.blockchain.miner_rewards)
        
        expected_hash = self.blockchain.get_hash(genesis_block, 0)
        self.assertEqual(genesis_block.hash, expected_hash)

    # Should correctly adjust difficulty based on average block time
    def test_adjust_difficulty(self):
        # Set up initial conditions
        self.blockchain.adjust_difficulty_blocks = 3
        self.blockchain.difficulty = 3
        self.blockchain.block_time = 30

        # Create mock blocks with specific timestamps
        mock_block1 = MagicMock()
        mock_block1.timestamp = 0
        mock_block2 = MagicMock()
        mock_block2.timestamp = 40
        mock_block3 = MagicMock()
        mock_block3.timestamp = 80
        mock_block4 = MagicMock()
        mock_block4.timestamp = 120

        # Add mock blocks to the chain
        self.blockchain.chain = [mock_block1, mock_block2, mock_block3, mock_block4]

        # Call the adjust_difficulty method
        self.blockchain.adjust_difficulty()

        # Assert that the difficulty has decreased
        self.assertEqual(self.blockchain.difficulty, 2)

        # Change the timestamps to make the average block time shorter
        mock_block2.timestamp = 20
        mock_block3.timestamp = 40
        mock_block4.timestamp = 60

        # Call the adjust_difficulty method again
        self.blockchain.adjust_difficulty()

        # Assert that the difficulty has increased
        self.assertEqual(self.blockchain.difficulty, 3)

    # Should accurately calculate and update account balances after transactions
    # def test_get_balance_after_transactions(self):
    #     # Create a new blockchain instance
    #     blockchain = BaseBlockChain(self.p2p_connection_mock)
    #     blockchain.create_genesis_block()

    #     # Generate test addresses
    #     sender_address, sender_private = blockchain.generate_address()
    #     receiver_address, _ = blockchain.generate_address()

    #     # Add a block with miner rewards to the sender
    #     miner_block = Block(blockchain.chain[-1].hash, blockchain.difficulty, sender_address, blockchain.miner_rewards)
    #     blockchain.chain.append(miner_block)

    #     # Create and add a transaction
    #     transaction = Transaction(sender_address, receiver_address, 5, 1, "Test transaction")
    #     blockchain.pending_transactions.append(transaction)

    #     # Mine a new block to include the transaction
    #     blockchain.mine_block(sender_address)

    #     # Check balances
    #     sender_balance = blockchain.get_balance(sender_address)
    #     receiver_balance = blockchain.get_balance(receiver_address)

    #     # Assert the balances are correct
    #     self.assertEqual(sender_balance, blockchain.miner_rewards * 2 - 6)  # Two miner rewards minus transaction amount and fee
    #     self.assertEqual(receiver_balance, 5)  # Received transaction amount

    # # Should verify the integrity of the entire blockchain
    # def test_verify_blockchain(self):
    #     # Create a blockchain with multiple blocks
    #     self.blockchain.create_genesis_block()
    #     for _ in range(5):
    #         self.blockchain.mine_block("test_miner")

    #     # Verify the integrity of the blockchain
    #     self.assertTrue(self.blockchain.verify_blockchain())

    #     # Tamper with a block in the chain
    #     self.blockchain.chain[2].hash = "tampered_hash"

    #     # Verify the integrity again, should return False
    #     self.assertFalse(self.blockchain.verify_blockchain())

    # Should generate unique public and private key pairs for new addresses
    def test_generate_address(self):
        blockchain = BaseBlockChain(self.p2p_connection_mock, self.args)
        
        # Generate two sets of addresses
        address1, private_key1 = blockchain.generate_address()
        address2, private_key2 = blockchain.generate_address()
        
        # Check that the addresses and private keys are not empty
        self.assertIsNotNone(address1)
        self.assertIsNotNone(private_key1)
        self.assertIsNotNone(address2)
        self.assertIsNotNone(private_key2)
        
        # Check that the addresses and private keys are unique
        self.assertNotEqual(address1, address2)
        self.assertNotEqual(private_key1, private_key2)
        
        # Check that the addresses are in the expected format (no BEGIN/END markers)
        self.assertNotIn("BEGIN RSA PUBLIC KEY", address1)
        self.assertNotIn("END RSA PUBLIC KEY", address1)
        self.assertNotIn("BEGIN RSA PUBLIC KEY", address2)
        self.assertNotIn("END RSA PUBLIC KEY", address2)
        
        # Check that the private keys are in the expected format (no BEGIN/END markers)
        self.assertNotIn("BEGIN RSA PRIVATE KEY", private_key1)
        self.assertNotIn("END RSA PRIVATE KEY", private_key1)
        self.assertNotIn("BEGIN RSA PRIVATE KEY", private_key2)
        self.assertNotIn("END RSA PRIVATE KEY", private_key2)

    # Should reject transactions when sender's balance is insufficient
    def test_reject_transaction_insufficient_balance(self):
        # Arrange
        sender_address, sender_private = self.blockchain.generate_address()
        receiver_address, _ = self.blockchain.generate_address()
        
        # Set up a mock balance for the sender
        with patch.object(self.blockchain, 'get_balance', return_value=50):
            transaction = self.blockchain.initialize_transaction(sender_address, receiver_address, 100, 5, "Test transaction")
            signature = self.blockchain.sign_transaction(transaction, sender_private)

            # Act
            result, message = self.blockchain.add_transaction(transaction, signature)

            # Assert
            self.assertFalse(result)
            self.assertEqual(message, "Balance not enough!")



    # Should validate and add broadcasted blocks to the local chain
    # def test_receive_broadcast_block(self):
    #     # Create a mock block
    #     mock_block = MagicMock()
    #     mock_block.previous_hash = self.blockchain.chain[-1].hash
    #     mock_block.difficulty = self.blockchain.difficulty
    #     mock_block.hash = '0' * self.blockchain.difficulty + 'a' * (64 - self.blockchain.difficulty)

    #     # Mock the get_hash method to return the same hash as the mock block
    #     self.blockchain.get_hash = MagicMock(return_value=mock_block.hash)

    #     # Call the method
    #     result = self.blockchain.receive_broadcast_block(mock_block)

    #     # Assert that the block was added to the chain
    #     self.assertTrue(result)
    #     self.assertEqual(self.blockchain.chain[-1], mock_block)
    #     self.assertTrue(self.blockchain.receive_verified_block)

    #     # Assert that adjust_difficulty was called
    #     self.blockchain.adjust_difficulty.assert_called_once()

if __name__ == '__main__':
    unittest.main()
