#!/bin/env python3
import time
import asyncio
from asyncio import LifoQueue
from asyncio import Queue

tc = int(input("Temps de prise de commande en seconde (nombre positif) : "))           # temps de prise de commande
tp = int(input("Temps de préparation du boisson en seconde (nombre positif) : "))      # temps de préparation du boisson
ts = int(input("Temps de service en seconde (nombre positif) : "))                     # temps de service
tb = int(input("Temps que prend le client pour boire en seconde (nombre positif) : ")) # temps de boisson

verbose = int(input("Niveau de verbosité pour les messages (0, 1 ou 2): "))

#########################    Variables global    #########################
global commande_termine
commande_termine = False

global preparation_termine
preparation_termine = False

global service_termine
service_termine=False 
###########################################################################

start_time = time.time()

def chrono():
    current_time = time.time()
    return current_time - start_time

###########################################################################
class Accessoire():
    """ Classe Mère de Pic et Bar. Initialise Pic et Bar en tant que Queue LIFO."""

    def __init__(self):
        self.etat = asyncio.LifoQueue()

    def Etat(self):
        """ Affiche l'état de Pic ou Bar """
        if verbose >= 2:
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] état = {list(self.etat._queue)}",flush=True)
        else:
            pass

class Pic(Accessoire):
    """ Un pic peut embrocher un post-it par-dessus les post-it déjà présents et libérer le dernier embroché. """

    def __init__(self):
        super().__init__()

    async def embrocher(self, postit):
        await asyncio.sleep(0)
        await self.etat.put(postit)
        if verbose >= 1:
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] post-it '{postit}' embroché",flush=True)

    async def liberer(self):
        await asyncio.sleep(0)
        postit = await self.etat.get()
        if verbose >= 1:
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] post-it '{postit}' libéré",flush=True)
        return postit


class Bar(Accessoire):
    """ Un bar peut recevoir des plateaux, et évacuer le dernier reçu """

    def __init__(self):
        super().__init__()

    async def recevoir(self, plateau):
        await asyncio.sleep(0)
        await self.etat.put(plateau)
        if verbose >= 1:
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] '{plateau}' reçu",flush=True)

    async def evacuer(self):
        await asyncio.sleep(0)
        plateau = await self.etat.get()
        if verbose >= 1:
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] '{plateau}' évacué",flush=True)
        return plateau

class Caisse(Accessoire):

    def __init__(self):
        self.etat = asyncio.Queue()
    
    async def attente(self, boisson):
        await asyncio.sleep(0)
        await self.etat.put(boisson)
        if verbose >= 1:
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] En attente d'encaisser : '{boisson}'",flush=True)

    async def encaisser(self):
        await asyncio.sleep(0)
        boisson = await self.etat.get()
        if verbose >= 1:
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] Boisson '{boisson}' encaissé",flush=True)
        return boisson

class Serveur():
    def __init__(self, pic, bar, commandes):
        self.pic = pic
        self.bar = bar
        self.commandes = commandes[::-1]
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] prêt pour le service",flush=True)

    async def prendre_commande(self):
        """ Prend une commande et embroche un post-it. """
        global commande_termine
        for commande in self.commandes:
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] je prends commande de '{commande}'",flush=True)
            await asyncio.sleep(tc)
            await asyncio.create_task(self.pic.embrocher(commande))
            self.pic.Etat()

        commande_termine = True
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] il n'y a plus de commande à prendre",flush=True)
        print("plus de commande à prendre")

    async def servir(self):
        """ Prend un plateau sur le bar. """
        global preparation_termine
        while True:
            if not self.bar.etat.empty():
                self.bar.Etat()
                print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] je sers '{await self.bar.evacuer()}'",flush=True)
                await asyncio.sleep(ts)
            if self.pic.etat.empty() and self.bar.etat.empty() and preparation_termine :
                self.bar.Etat()
                print("Bar est vide",flush=True)
                break
            else:
                await asyncio.sleep(0.1)

class Barman():
    def __init__(self, pic, bar):
        self.pic = pic
        self.bar = bar
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] prêt pour le service !")

    async def preparer(self):
        """ Prend un post-it, prépare la commande et la dépose sur le bar. """
        global commande_termine
        global preparation_termine
        while True:
            if not self.pic.etat.empty():
                self.pic.Etat()
                boisson = await self.pic.liberer()
                print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] je commence la fabrication de '{boisson}'",flush=True)
                await asyncio.sleep(tp)
                print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] je termine la fabrication de '{boisson}'",flush=True)
                await self.bar.recevoir(boisson)
                #self.bar.Etat()
            if self.pic.etat.empty() and self.bar.etat.empty() and commande_termine:
                self.pic.Etat()
                print("Pic est vide",flush=True)
                preparation_termine = True
                break
            else:
                await asyncio.sleep(0.1)
    async def encaisser(self):
        """ Encaisse les commandes """
        global service_termine
        while True:
            await asyncio.sleep(tb)
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] je commence la fabrication de ",flush=True)
            if service_termine :
                break
        