from client import client
from _thread import *
from server import host

import random
import time


class Network:
    def __init__(self):

        self.host=host()

        #if we can host push it to the background
        if(self.host.can_be_host()):
            start_new_thread(self.host.start,())
            print("I have host\n")
        else:
            self.host=None
            print("I'm don't have host\n")

        #set up client object
        self.client=client()

        #start client
        self.client.try_connect()
        start_new_thread(self.client.wait_for_game_start,())
    def send_move(self,move):
        ack=self.client.send_move(move)
        if ack=="Game_ended" or ack=="":
            self.client.s.close()
            return ack
        else:
            ack=ack.split("£@€")
            return ack[(self.client.number+1)%2]

    def end_game(self):
        self.send_move("End")



tmp=Network()
ct=random.randint(1,90)
#leading screen and what nor
while not tmp.client.ready:
    continue

for i in range(3):
    time.sleep(2)
    print("Your move:",ct)
    print("Enemy move:",tmp.send_move(str(ct)))
    ct+=1

time.sleep(1)
tmp.end_game()





