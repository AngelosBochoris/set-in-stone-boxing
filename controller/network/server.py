import socket
import random
class host():
    def __init__(self):
        #info about host
        self.name = "0.0.0.0"
        self.port = 8080
        self.game_over = False

        # sockets using TCP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host binds
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.name, self.port))
        # lets 2 ppl connect
        self.s.listen(2)
        self.moves=random.randint(2,6)

    def start(self):
        #stack with all the clients
        self.clients=[]
        print("Server is listening")

        while len(self.clients)<2:
            clientSocket, addr = self.s.accept()
            clientSocket.send(bytes(str(len(self.clients)), "utf-8"))
            print("Client connected from",len(self.clients))
            self.clients.append((clientSocket,addr))

        print("enough players to start game")

        #tells both the game has started
        for soc, addr in self.clients:
            soc.send(bytes("Game_started", "utf-8"))
            soc.send(bytes(f"Game_started {self.moves}", "utf-8"))
        self.game_over = False
        self.data = ["0","0"]

        #game playing
        while not self.game_over:
            #tries to recive the client data
            for i in range(len(self.clients)):
                soc, addr = self.clients[i]
                message=soc.recv(1024).decode("utf-8")
                if message=='' or message=="End":
                    soc.close()
                    self.clients.remove((soc, addr))
                    self.game_over = True
                    break
                else:
                    self.data[i]=message

            #sends stuff back to the client
            for soc, addr  in self.clients:
                if(self.game_over):
                    break
                soc.send(bytes("£@€".join(self.data), "utf-8"))
        #game is done
        for soc, addr in self.clients:
            soc.send(bytes("Game_ended", "utf-8"))
            soc.close()
            self.clients.remove((soc, addr))
        self.s.close()
        print("Host quit")


