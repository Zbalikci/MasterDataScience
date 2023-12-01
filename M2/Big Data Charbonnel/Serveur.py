#!/bin/env python3

import time
from socket import *
import re
import threading

class Reac(threading.Thread):
    def __init__(self,liste,c_addr):                                                                              
        threading.Thread.__init__(self)
        self.liste=liste
        self.t0=time.time()
        print("t0=",self.t0-self.t0)
        self.c_addr=c_addr
    def run(self):
        print(f'{self.liste[1]} envoyé par {self.c_addr}')
        while True:
            if time.time()-self.t0>int(self.liste[0]):
                print("t=",time.time()-self.t0)
                print(f'{self.liste[2]} envoyé par {self.c_addr} il y a {self.liste[0]} secondes')
                break

host = '0.0.0.0'
port = 2074
buf = 1024                            # taille du buffer
s_addr = (host,port)

UDPsock = socket(AF_INET,SOCK_DGRAM)  # création du socket
UDPsock.bind(s_addr)                  # activation
m1=re.compile(r'^(\d+) ("\w+") ("\w+")$')
while True:
    data,c_addr = UDPsock.recvfrom(buf)  # écoute
    d1=str(data)[2:-1]
    print(f"\nReçu {d1} de {c_addr}")
    t1=m1.match(d1)
    if t1:
        r=Reac(t1.groups(),c_addr)
        r.start()
    else:
        print(f"requete incompréhensible de {c_addr}")

UDPsock.close()