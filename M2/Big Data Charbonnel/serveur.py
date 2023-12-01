#!/bin/env python3
import asyncio
import os, sys, time

addr = "0.0.0.0"
port = 1234
from pathlib import Path
async def handle(reader, writer):
    data = await reader.read(100) 
    print(f"réception de : {data.decode()}") 
    if data.decode()=="où?":
        response="là"
    elif data.decode()=="qui?":
        response="Zeynep"
    elif data.decode()=="quand?":
        #file=f"{os.getcwd()}/{os.path.basename(__file__)}"
        file=sys.argv[0]
        response=f"{time.ctime(os.lstat(file).st_ctime)}"
    elif data.decode()=="comment?":
        response="le code source"
    else:
        response = "pas compris!"
    writer.write(response.encode()) 
    await writer.drain() 
    print(f"envoi de : {response}")

    writer.close()

async def main(addr,port):
    server = await asyncio.start_server(handle,addr,port) 

    async with server:
        await server.serve_forever() 

asyncio.run(main(addr,port))