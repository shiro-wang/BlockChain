import hashlib

class BlockManager:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def create_block(self, transactions, previous_hash):
        """創建新的區塊"""
        block = {
            "transactions": transactions,
            "previous_hash": previous_hash,
            "nonce": 0
        }
        block['hash'] = self.calculate_block_hash(block)
        return block

    def calculate_block_hash(self, block):
        """計算區塊的哈希值"""
        block_string = f"{block['transactions']}{block['previous_hash']}{block['nonce']}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def validate_block(self, block, difficulty):
        """驗證區塊是否滿足難度要求"""
        return block['hash'].startswith('0' * difficulty)