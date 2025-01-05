import unittest
import os
import json
import threading
import time

from server import BlockChain
from Architecture import Block, BaseP2PConnection
from Chain_tools.utils import parse_args

class TestBlockChain(unittest.TestCase):
    def setUp(self):
        self.args = parse_args()
        self.args.socket_host = "192.168.1.132"
        self.args.socket_port = 1111
        self.blockchain = BlockChain(self.args)

    # Should create a new account if myaccount.json is not found
    def test_create_new_account_when_file_not_found(self):
        # Rename existing myaccount.json if it exists
        if os.path.exists("./server/myaccount.json"):
            os.rename("./server/myaccount.json", "./server/myaccount_temp.json")

        # Create a mock BlockChain instance
        mock_blockchain = BlockChain(self.args)

        # Call the start method
        mock_blockchain.start(force_stop=True)

        # Check if a new myaccount.json file was created
        self.assertTrue(os.path.exists("./server/myaccount.json"))

        # Load the newly created account data
        with open("./server/myaccount.json", 'r') as json_account:
            data = json.load(json_account)

        # Check if the new account data contains address and private key
        self.assertIn("address", data)
        self.assertIn("private", data)

        # Clean up: remove the newly created file and restore the original if it existed
        os.remove("./server/myaccount.json")
        if os.path.exists("./server/myaccount_temp.json"):
            os.rename("./server/myaccount_temp.json", "./server/myaccount.json")

    # Should load existing account data from myaccount.json if present
    def test_load_existing_account(self):
        # Create a temporary account file
        temp_account = {
            "address": "test_address",
            "private": "test_private"
        }
        with open("./server/myaccount.json", "w") as f:
            json.dump(temp_account, f)

        # Create a BlockChain instance
        blockchain = BlockChain(self.args)

        # Call the start method
        blockchain.start(force_stop=True)

        # Assert that the account data was loaded correctly
        self.assertEqual(blockchain.address, "test_address")

        # Clean up the temporary file
        os.remove("./server/myaccount.json")

    # Should generate a valid address and private key pair when creating a new account
    def test_generate_new_account(self):
        # Remove existing account file if present
        if os.path.exists("./server/myaccount.json"):
            os.remove("./server/myaccount.json")

        # Create a new blockchain instance
        blockchain = BlockChain(self.args)

        # Call the start method to trigger account creation
        blockchain.start(force_stop=True)

        # Check if the account file was created
        self.assertTrue(os.path.exists("./server/myaccount.json"))

        # Read the created account file
        with open("./server/myaccount.json", 'r') as json_account:
            data = json.load(json_account)

        # Assert that address and private key are present in the file
        self.assertIn("address", data)
        self.assertIn("private", data)

        # Verify that address and private key are non-empty strings
        self.assertIsInstance(data["address"], str)
        self.assertIsInstance(data["private"], str)
        self.assertTrue(len(data["address"]) > 0)
        self.assertTrue(len(data["private"]) > 0)

        # Clean up: remove the created account file
        os.remove("./server/myaccount.json")

    # # Should create a genesis block when starting the blockchain
    # def test_create_genesis_block(self):
    #     self.blockchain.start(force_stop=True)
    #     self.assertIsNotNone(self.blockchain.chain)
    #     self.assertEqual(len(self.blockchain.chain), 1)
    #     genesis_block = self.blockchain.chain[0]
    #     self.assertEqual(genesis_block.previous_hash, "0")
    #     self.assertEqual(genesis_block.index, 0)

    # # Should continuously mine new blocks and adjust difficulty
    # def test_continuous_mining_and_difficulty_adjustment(self):
    #     # Mock the necessary methods to avoid actual mining and network operations
    #     self.blockchain.mine_block = unittest.mock.MagicMock()
    #     self.blockchain.adjust_difficulty = unittest.mock.MagicMock()
    #     self.blockchain.create_genesis_block = unittest.mock.MagicMock()
        
    #     # Mock the generate_address method to return a fixed address and private key
    #     self.blockchain.generate_address = unittest.mock.MagicMock(return_value=("test_address", "test_private"))
        
    #     # Mock the open function to simulate reading from and writing to myaccount.json
    #     mock_open = unittest.mock.mock_open(read_data='{"address": "test_address", "private": "test_private"}')
        
    #     with unittest.mock.patch('builtins.open', mock_open):
    #         # Call the start method
    #         threading.Thread(target=self.blockchain.start, daemon=True).start(force_stop=True)
            
    #         # Wait for a short time to allow for multiple iterations
    #         time.sleep(0.1)
            
    #         # Stop the infinite loop
    #         self.blockchain.start = unittest.mock.MagicMock()

    #     # Check if mine_block and adjust_difficulty were called multiple times
    #     self.assertGreater(self.blockchain.mine_block.call_count, 1)
    #     self.assertGreater(self.blockchain.adjust_difficulty.call_count, 1)
        
    #     # Verify that mine_block was called with the correct address
    #     self.blockchain.mine_block.assert_called_with("test_address")

    # Should correctly initialize the P2P connection with provided socket host and port
    # def test_blockchain_initialization(self):
    #     self.args.socket_host = "192.168.1.132"
    #     self.args.socket_port = 8000
    #     blockchain = BlockChain(self.args)
        
    #     self.assertIsInstance(blockchain.p2p_connection, BaseP2PConnection)
    #     self.assertEqual(blockchain.p2p_connection.socket_host, self.args.socket_host)
    #     self.assertEqual(blockchain.p2p_connection.socket_port, self.args.socket_port)

    # # Should handle connection errors gracefully when starting the socket server
    # def test_start_socket_server_connection_error(self):
    #     # Mock the BaseP2PConnection to raise a ConnectionError
    #     with unittest.mock.patch('Architecture.BaseP2PConnection.BaseP2PConnection', side_effect=ConnectionError):
    #         # Attempt to create a BlockChain instance, which should trigger the connection error
    #         with self.assertRaises(ConnectionError):
    #             BlockChain(self.socket_host, self.socket_port)

    #     # Verify that the error is logged or handled appropriately
    #     # This part depends on how you want to handle the error in your BlockChain class
    #     # For example, if you're logging the error:
    #     # self.assertIn("Failed to start socket server", caplog.text)

    # # Should properly serialize and deserialize account data to/from JSON format
    # def test_blockchain_integrity_when_mining_multiple_blocks(self):
    #     # Arrange
    #     self.blockchain.start_socket_server = lambda: None  # Mock the start_socket_server method
    #     self.blockchain.generate_address = lambda: ("test_address", "test_private")  # Mock generate_address
    #     self.blockchain.mine_block = lambda address: self.blockchain.chain.append(Block(len(self.blockchain.chain), "", time.time(), "", 0))  # Mock mine_block
    #     self.blockchain.adjust_difficulty = lambda: None  # Mock adjust_difficulty

    #     # Act
    #     self.blockchain.start(force_stop=True)
    #     time.sleep(0.1)  # Allow time for a few blocks to be mined

    #     # Assert
    #     self.assertGreater(len(self.blockchain.chain), 1)  # Check if multiple blocks were mined
    #     for i in range(1, len(self.blockchain.chain)):
    #         self.assertEqual(self.blockchain.chain[i].previous_hash, self.blockchain.chain[i-1].hash())  # Check if each block points to the previous block's hash
    #     self.assertEqual(self.blockchain.chain[0].previous_hash, "")  # Check if the genesis block has an empty previous hash

    # # Should correctly apply difficulty adjustments based on mining speed
    # def test_adjust_difficulty(self):
    #     # Set up initial conditions
    #     self.blockchain.difficulty = 4
    #     self.blockchain.block_time = 10  # seconds
    #     self.blockchain.last_block_time = time.time() - 5  # 5 seconds ago

    #     # Mine a block
    #     self.blockchain.mine_block(self.blockchain.address)

    #     # Check if difficulty was adjusted correctly
    #     if time.time() - self.blockchain.last_block_time < self.blockchain.block_time:
    #         self.assertGreater(self.blockchain.difficulty, 4)
    #     else:
    #         self.assertLess(self.blockchain.difficulty, 4)

    #     # Reset the difficulty
    #     self.blockchain.difficulty = 4

    #     # Test when mining takes longer than block_time
    #     self.blockchain.last_block_time = time.time() - 15  # 15 seconds ago

    #     # Mine another block
    #     self.blockchain.mine_block(self.blockchain.address)

    #     # Check if difficulty was decreased
    #     self.assertLess(self.blockchain.difficulty, 4)

if __name__ == '__main__':
    unittest.main()
