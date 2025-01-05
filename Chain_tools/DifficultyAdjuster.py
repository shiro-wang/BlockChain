class DifficultyAdjuster:
    def __init__(self, target_time_per_block, adjustment_interval):
        self.target_time_per_block = target_time_per_block
        self.adjustment_interval = adjustment_interval

    def adjust_difficulty(self, blockchain):
        """調整區塊鏈的挖礦難度"""
        if len(blockchain) < self.adjustment_interval:
            return blockchain[-1]['difficulty']

        recent_blocks = blockchain[-self.adjustment_interval:]
        total_time = recent_blocks[-1]['timestamp'] - recent_blocks[0]['timestamp']
        average_time = total_time / self.adjustment_interval

        if average_time < self.target_time_per_block:
            return blockchain[-1]['difficulty'] + 1
        elif average_time > self.target_time_per_block:
            return max(1, blockchain[-1]['difficulty'] - 1)
        else:
            return blockchain[-1]['difficulty']