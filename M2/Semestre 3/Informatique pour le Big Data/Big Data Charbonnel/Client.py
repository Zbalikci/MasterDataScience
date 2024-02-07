#!/bin/env python3

from socket import *
import sys 

host = sys.argv[1]
port = 2074
buf = 1024                              # taille du buffer
s_addr = (host,port)

UDPsock = socket(AF_INET,SOCK_DGRAM)    # création du socket

while True:
    msg = input('>> ')
    if not msg: break

    data = bytes(msg,'utf-8')
    print(f"Envoi de {data}")
    UDPsock.sendto(data,s_addr)         # envoi vers le serveur

UDPsock.close()