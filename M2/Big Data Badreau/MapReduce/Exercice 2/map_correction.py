#! /usr/bin/env python3

import sys
import re

mot = re.compile("\w+")

for ligne in sys.stdin:
    liste_mots = mot.findall(ligne.strip().lower())
    print("lignes\t1")
    print(f"mots\t{len(liste_mots)}")
    print(f"lettres\t{sum([len(mot) for mot in liste_mots])}")