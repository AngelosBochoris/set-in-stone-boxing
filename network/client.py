import socket
import time
import random

class client:
    def __init__(self):
        self.name = "10.252.45.248"
        self.port = 8080
        self.number= -1
        self.ready=False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def try_connect(self):
        try:
            self.s.connect((self.name, self.port))
            self.number=int(self.s.recv(1024).decode('utf-8'))
            return True
        except socket.error:
            return False
    def wait_for_game_start(self):
        msg=self.s.recv(1024).decode('utf-8')
        if msg=="Game_started":
            print("Accepted")
            self.ready=True
        else:
            self.s.close()
            raise Exception("Server died or something went wrong")

    def send_move(self,move):
        self.s.send(bytes(move,'utf-8'))
        ack=self.s.recv(1024).decode('utf-8')
        return ack