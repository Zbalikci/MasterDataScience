#!/bin/env python3
import sys , re


def construire(l0=None):
    def _construire():
        nonlocal i  
        l = []          
        while True:
            if l0==None :
                if sys.argv[i]=="[":   
                    i+=1               
                    if i!=2:                  # pour la premiÃ¨re liste, on ne fait rien
                        l.append(_construire()) 
                elif sys.argv[i]=="]":        # c'est la fin de la liste,
                    i+=1
                    return l                  # on renvoie la liste constuite
                else:                         # c'est une liste d'entiers
                    l.append(int(sys.argv[i]))   
                    i+=1
                    
            else :
                if l0[i]=="[":   # c'est une sous-liste de listes
                    i+=1                 
                    if i!=1:             # pour la premiÃ¨re sous-liste, on ne fait rien
                        l.append(_construire())    # sinon on construit cette sous-liste et on la met dans la sous-liste courante
                elif l0[i]=="]": # c'est la fin de la sous-liste courante,
                    i+=1
                    return l             # on renvoie la sous-liste courante
                else:                  # c'est une sous-liste d'entiers
                    l.append(int(l0[i]))   
                    i+=1
    i = 1                              # indice pour parcourir les arguments
    return _construire()
    
def acquisition():
    if len(sys.argv)== 1 : #on n'a pas mis d'argument 
        while True:
            line = input("? ").rstrip("\n").strip()
            if line=="":
                break
            lline = re.split(r' +',line.rstrip("\n"))
            i = 0
            l = construire(lline)                      
            return l
    elif len(sys.argv)== 2 :#on a mis un seul argument (ex = fichier)
        f = open(sys.argv[1], "r")
        for line in f:
            lline = re.split(r' +',line.rstrip("\n"))
            l = construire(lline)
        return l                     
    else : # j'ai mis la liste en argument
        l = construire()                              
        return l