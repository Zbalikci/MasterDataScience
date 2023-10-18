#!/bin/env python3

from multi_threading_balikci import Caisse, Bar, Pic, Barman, Serveur
import sys
import threading

if __name__ == "__main__":
    commandes = sys.argv[1:]
    pic = Pic()
    bar = Bar()
    caisse = Caisse()
    barman = Barman(caisse, pic, bar)
    serveur = Serveur(caisse, pic, bar, commandes)

    serveur.start()
    barman.start()

    serveur.join()
    barman.join()