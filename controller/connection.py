from controller.network.interface import Network


class Connection:
    def __init__(self):
        self.establishing = False
        self.done = False
        self.connection = None

    def start_connection(self):
        if self.establishing:
            return
        self.establishing = True
        self.connection = Network("10.252.95.244")  # your networking wrapper

    def is_connected(self) -> bool:
        if not self.establishing:
            return False
        if self.done:
            return True
        if self.connection and self.connection.client.ready:
            self.done = True
        return self.done
