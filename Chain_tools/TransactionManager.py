class TransactionManager:
    def __init__(self):
        pass

    def validate_transaction(self, transaction, public_key):
        """驗證交易的合法性"""
        # 實作驗證邏輯
        return self.verify_signature(transaction, public_key)

    def sign_transaction(self, transaction, private_key):
        """對交易進行簽名"""
        # 使用私鑰對交易進行簽名
        return private_key.sign(transaction)

    def verify_signature(self, transaction, public_key):
        """驗證簽名的有效性"""
        # 驗證邏輯
        return public_key.verify(transaction['signature'], transaction['data'])