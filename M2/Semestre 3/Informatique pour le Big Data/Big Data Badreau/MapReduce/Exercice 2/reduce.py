#! /usr/bin/env python3

import sys

""" mot=''
compteur=0

for ligne in sys.stdin:
    cle,valeur = ligne.split('\t')
    if cle==mot:
        compteur+=int(valeur)
    else:
        if mot!='':
            print(f"{mot}\t{compteur}")
        mot=cle
        compteur=int(valeur)
print(f"{mot}\t{compteur}") """

compteur_mot=0
compteur_lettre=0
compteur_ligne=0

for ligne in sys.stdin:
    compteur_ligne+=1
    cle,valeur = ligne.split('\t')
    compteur_mot+=int(cle)
    compteur_lettre+=int(valeur)
    
print(f"lettres\t{compteur_lettre}")
print(f"lignes\t{compteur_ligne}")
print(f"mots\t{compteur_mot}")
