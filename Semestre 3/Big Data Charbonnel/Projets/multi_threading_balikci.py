#!/bin/env python3

import time
import asyncio
from asyncio import LifoQueue
from asyncio import Queue
import threading

tb,tc,tp,ts= 1,1,1,1 # temps que prend un client à boire, temps de prise de commande, temps de préparation du boisson, temps de service
verbose = int(input("Niveau de verbosité pour les messages (0, 1 ou 2): "))
#########################    Variables global    #########################
global commande_termine
commande_termine = False

global preparation_termine
preparation_termine = False

global servie_termine
service_termine = False
###########################################################################

start_time = time.time()

def log(classe_name, message):
    current_time = time.time()
    chrono = current_time - start_time
    print(f"[{chrono:.2f} s]:[{classe_name}] {message}",flush=True)

###########################################################################
class Accessoire():
    """ Classe Mère de Pic et Bar. Initialise Pic et Bar en tant que Queue LIFO."""

    def __init__(self):
        self.etat = asyncio.LifoQueue()

    def Etat(self):
        """ Affiche l'état de Pic ou Bar """
        if verbose >= 2:
            log(self.__class__.__name__ , f"état = {list(self.etat._queue)}")
        else:
            pass

class Pic(Accessoire):
    """ Un pic peut embrocher un post-it par-dessus les post-it déjà présents et libérer le dernier embroché. """

    def __init__(self):
        super().__init__()

    async def embrocher(self, postit):
        await self.etat.put(postit)
        if verbose >= 1:
            log(self.__class__.__name__ , f"post-it '{postit}' embroché")

    async def liberer(self):
        postit = await self.etat.get()
        if verbose >= 1:
            log(self.__class__.__name__ , f"post-it '{postit}' libéré")
        return postit

class Bar(Accessoire):
    """ Un bar peut recevoir des plateaux, et évacuer le dernier reçu """

    def __init__(self):
        super().__init__()

    async def recevoir(self, plateau):
        await self.etat.put(plateau)
        if verbose >= 1:
            log(self.__class__.__name__ ,f"'{plateau}' reçu")

    async def evacuer(self):
        plateau = await self.etat.get()
        if verbose >= 1:
            log(self.__class__.__name__ ,f"'{plateau}' évacué")
        return plateau

class Caisse(Accessoire):
    """ Une caisse qui reçoit la liste des boisssons à encaisser en FIFO """

    def __init__(self):
        self.etat = asyncio.Queue()

    async def recevoir(self, boisson):
        await self.etat.put(boisson)
        if verbose >= 1:
            log(self.__class__.__name__ ,f"'{boisson}' en attente d'encaissement")

    async def evacuer(self):
        await asyncio.sleep(tb)
        boisson = await self.etat.get()
        return boisson

###########################################################################

class Serveur(threading.Thread):

    def __init__(self, caisse, pic, bar, commandes):
        threading.Thread.__init__(self)
        self.pic = pic
        self.bar = bar
        self.caisse = caisse
        self.commandes = commandes[::-1]
        log(self.__class__.__name__ , f"prêt pour le service")

    async def prendre_commande(self):
        """ Prend une commande et embroche un post-it. """

        global commande_termine
        for commande in self.commandes:
            log(self.__class__.__name__ ,f"je prends commande de '{commande}'")
            await asyncio.sleep(tc)
            await asyncio.create_task(self.pic.embrocher(commande))
            self.pic.Etat()
        commande_termine = True
        log(self.__class__.__name__ ,f"il n'y a plus de commande à prendre")
        print("plus de commande à prendre")

    async def servir(self):
        """ Prend un plateau sur le bar. """

        global preparation_termine
        global service_termine
        while True:
            if not self.bar.etat.empty():
                self.bar.Etat()
                boisson = await self.bar.evacuer()
                log(self.__class__.__name__ ,f"je sers '{boisson}'")
                await asyncio.sleep(ts)
                await self.caisse.recevoir(boisson)
                self.caisse.Etat()
            if self.pic.etat.empty() and self.bar.etat.empty() and preparation_termine :
                self.bar.Etat()
                print("Bar est vide",flush=True)
                service_termine = True
                break
            else:
                await asyncio.sleep(0.1)
    def run(self):
        async def main():
            tasks=[self.prendre_commande(),self.servir()]
            await asyncio.gather(*tasks)
        asyncio.run(main())

class Barman(threading.Thread):

    def __init__(self,caisse, pic, bar):
        threading.Thread.__init__(self)
        self.pic = pic
        self.bar = bar
        self.caisse = caisse
        log(self.__class__.__name__ , f"prêt pour le service !")

    async def preparer(self):
        """ Prend un post-it, prépare la commande et la dépose sur le bar. """

        global commande_termine
        global preparation_termine
        while True:
            if not self.pic.etat.empty():
                self.pic.Etat()
                boisson = await self.pic.liberer()
                log(self.__class__.__name__ ,f"je commence la fabrication de '{boisson}'")
                await asyncio.sleep(tp)
                log(self.__class__.__name__ ,f"je termine la fabrication de '{boisson}'")
                await self.bar.recevoir(boisson)
            if self.pic.etat.empty() and self.bar.etat.empty() and commande_termine:
                self.pic.Etat()
                print("Pic est vide",flush=True)
                preparation_termine = True
                break
            else:
                await asyncio.sleep(0.1)

    async def encaisser(self):
        """ Encaisse une addition après le service. """

        global service_termine
        while True:
            if not self.caisse.etat.empty():
                self.caisse.Etat()
                boisson = await self.caisse.evacuer()
                log(self.__class__.__name__ ,f"Encaissement de la commande : '{boisson}'")
                await asyncio.sleep(0.5)
                log(self.__class__.__name__ ,f"Commande '{boisson}' encaisssée! ")
            if self.caisse.etat.empty() and self.pic.etat.empty() and self.bar.etat.empty() and service_termine :
                self.caisse.Etat()
                log(self.__class__.__name__ ,f"Tout les commandes ont été encaissé !")
                break
            else :
                await asyncio.sleep(0.1)
    def run(self):
        async def main():
            tasks=[self.preparer(),self.encaisser()]
            await asyncio.gather(*tasks)
        asyncio.run(main())