#!/bin/env python3
############################# Partie 1 sans asyncio #########################################
import time
import asyncio

class Accessoire:
    def __init__(self):  
        self.etat=[]
    def Etat(self):
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] état = {self.etat}")
start_time = time.time()

def chrono():
    current_time=time.time()
    return current_time-start_time

class Pic(Accessoire):
    """ Un pic peut embrocher un post-it par-dessus les post-it déjà présents et libérer le dernier embroché. """
    
    def __init__(self):
        super().__init__()

    def embrocher(self,postit):
        self.etat.append(postit)
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] post-it '{postit}' embroché")

    def liberer(self):
        postit=self.etat[-1]
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] post-it '{postit}' libéré")
        self.etat.remove(postit)
        return postit
     
class Bar(Accessoire):
    """ Un bar peut recevoir des plateaux, et évacuer le dernier reçu """
    def __init__(self):
        super().__init__()

    def recevoir(self,plateau):
        self.etat.append(plateau)
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] '{plateau}' reçu")
    def evacuer(self):
        plateau=self.etat[-1]
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] '{plateau}' évacué")
        self.etat.remove(plateau)
        return plateau

class Serveur:
    def __init__(self,pic,bar,commandes):
        self.pic=pic
        self.bar=bar
        self.commandes=commandes[::-1]
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] prêt pour le service")

    def prendre_commande(self):
        """ Prend une commande et embroche un post-it. """
        for commande in self.commandes:
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] je prends commande de '{commande}'")
            time.sleep(1)
            self.pic.embrocher(commande)
            self.pic.Etat()
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] il n'y a plus de commande à prendre")
        print("plus de commande à prendre")

    def servir(self):
        """ Prend un plateau sur le bar. """
        while len(self.bar.etat)!=0:
            self.bar.Etat()
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] je sers '{self.bar.evacuer()}'")
            time.sleep(1)
        if len(self.bar.etat)==0:
            self.bar.Etat()
            print("Bar est vide")
 
class Barman:
    def __init__(self,pic,bar):
        self.pic=pic 
        self.bar=bar
        print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] prêt pour le service !")

    def preparer(self):
        """ Prend un post-it, prépare la commande et la dépose sur le bar. """
        while len(self.pic.etat)!=0:
            self.pic.Etat()
            boisson=self.pic.liberer()
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] je commence la fabrication de '{boisson}'")
            time.sleep(1)
            print(f"[{chrono():.2f} s]:[{self.__class__.__name__}] je termine la fabrication de '{boisson}'")
            self.bar.recevoir(boisson)
            self.bar.Etat()
        if len(self.pic.etat)==0:
            self.pic.Etat()
            print("Pic est vide")

