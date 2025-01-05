class BaseP2PConnection:
    def __init__(self, socket_host, socket_port):
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.node_address = {f"{self.socket_host}:{self.socket_port}"}
        self.connection_nodes = {}
        self.address = ""
        self.__private = ""

    # @property
    # def address(self):
    #     return self.__address
    # @address.setter
    # def address(self, value):
    #     self.__address = value
    @property
    def private(self):
        return self.__private
    @private.setter
    def private(self, value):
        self.__private = value