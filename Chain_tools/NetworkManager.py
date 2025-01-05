import socket
import pickle

class NetworkManager:
    def __init__(self, node_address):
        self.node_address = node_address

    def connect_to_node(self, node_address, message):
        """與節點建立連接並發送消息"""
        target_host, target_port = node_address.split(":")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((target_host, int(target_port)))
            client.sendall(pickle.dumps(message))
            client.close()
        except Exception as e:
            print(f"連接節點失敗: {node_address}. 錯誤: {e}")
            self.node_address.remove(node_address)

    def broadcast_message(self, message):
        """向所有節點廣播消息"""
        for node_address in self.node_address.copy():
            self.connect_to_node(node_address, message)