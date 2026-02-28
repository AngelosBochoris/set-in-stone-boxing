from controller.network.client import Client
from _thread import *
from controller.network.server import host

import random
import time


class Network:
    def __init__(self,ip,ht=True):
        self.game_over=False
        if ht:
            self.host=host()
            start_new_thread(self.host.start, ())
        else:
            self.host=None

        #set up client object
        self.client=Client(ip)

        #start client
        if not self.client.try_connect():
            raise Exception("Couldn't find server")

        start_new_thread(self.client.wait_for_game_start,())
    def send_move(self,move):
        ack=self.client.send_move(move)
        if ack=="Game_ended" or ack=="":
            self.client.s.close()
            self.game_over=True
            return ack
        else:
            ack=ack.split("£@€")
            return ack[(self.client.number+1)%2]

    def end_game(self):
        if not self.game_over:
            self.send_move("End")

def establish_connection(ip="10.252.95.244"):
    tmp = Network(ip)
    # TODO
    while not tmp.client.ready:
        continue
    return tmp

"""
h=input()=='t'
tmp=Network("10.252.95.244",h)
ct=random.randint(1,90)
#leading screen and what nor
while not tmp.client.ready:
    continue

for i in range(3):
    time.sleep(2)
    print("No. Moves",tmp.client.moves)
    print("Your move:",ct)
    result = tmp.send_move(str(ct))
    if result == "Game_ended" or result == "":
        break
    print("Enemy move:", result)
    ct += 1

time.sleep(1)
print("Game over!")

tmp.end_game()
"""





