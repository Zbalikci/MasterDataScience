#!/bin/env python3

from module_projet1 import acquisition

"""
    Soit L le type liste dont les elements sont soit tous de type int, soit tous de type L.
    Par exemple, l = [ [1,2], [ [2,3,4], [5,4,3,2], [[3,1],[2]]], [0,9] ] est de type L.  
    Ce programme est appele avec une liste de type L sur la ligne de commande,
    et sort le min des max de ses sous-listes.  
    Avec la liste l ci-dessus, la liste des max est [2, 4, 5, 3, 2, 9] donc le programme sort 2.
    La liste doit etre fournie sous la forme : [ [ 1 2 ] [ [ 2 3 4 ] [ 5 4 3 2 ] [ [ 3 1 ] [ 2 ] ] ] [ 0 9 ] ]
"""

def minmax(l):
    """
    Cette fonction recursive retourne le minmax de la liste passee en argument.
    """
    if type(l[0])==int:
        maxi.append(max(l))
    else:
        for i in l:
            minmax(i)

if __name__=="__main__":
    l=acquisition()
    maxi=[]
    minmax(l)
    print(min(maxi))