from controller.network.interface import Network

class Connection:
    def __init__(self):
        self.establishing = False
        self.connected = False

    def start_connection(self):
        if self.establishing:
            return
        self.establishing = True
        self.connection = Network("10.252.95.244")  # your networking wrapper
        self.connected

    def is_connected(self) -> bool:
        if not self.establishing:
            return False
        if self.connected:
            return True

        # non-blocking check
        if self.connection and self.connection.client.ready:
            self.connected = True

        return self.connected