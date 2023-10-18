#! /usr/bin/env python3

import sys
import re
motif=re.compile("\w+")
for ligne in sys.stdin:
    nb_lettres=0
    liste_mots = motif.findall(ligne.strip().lower())
    for mot in liste_mots:
        nb_lettres+=len(mot)
    nb_mot=len(liste_mots)
    print(f"{nb_mot} \t {nb_lettres}")

