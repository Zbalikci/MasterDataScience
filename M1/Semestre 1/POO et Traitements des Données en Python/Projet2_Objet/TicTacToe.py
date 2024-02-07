#!/bin/env python3

import numpy as np

class TicTacToe():
    
    def __init__(self) :
        self.plateau=[[".",".","."],[".",".","."],[".",".","."]]
        self.manche=0
        self.joueurs=[]
        self.etat=True #c'est l'état de la partie c'est-à-dire que personne ne peut plus placer les pions si self.etat=False
        
    def __str__(self) :
        ligne1 = " ".join(self.plateau[0])
        ligne2 = " ".join(self.plateau[1])
        ligne3 = " ".join(self.plateau[2])
        return f"{ligne1}\n{ligne2}\n{ligne3}"
    
    def place(self,ligne,colonne,symbole):
        
        if self.plateau[ligne-1][colonne-1] =="." and self.etat:
            self.plateau[ligne-1][colonne-1]= symbole
            self.manche+=1
            
        self.vainqueur() #pour changé self.etat s'il y a un vainqueur
            
    def vainqueur(self):
        
        sym1=self.joueurs[0][1] # pion du 1er joueur
        sym2=self.joueurs[1][1] # pion du 2nd joueur
        
        for i in range(3):
            #par colonne :
            if self.plateau[0][i]==self.plateau[1][i]==self.plateau[2][i] and self.plateau[0][i]!='.'  :
                self.etat=False  #s'il y a un vainqueur le jeu s'arrête, on ne peut plus placer de pions
                if self.plateau[0][i]==sym1:
                    return f"C'est {self.joueurs[0][0]} qui a gagné la partie en {self.manche} manches"
                else:
                    return f"C'est {self.joueurs[1][0]} qui a gagné la partie en {self.manche} manches"
            
            #par ligne :
            if len(np.unique(self.plateau[i]))==1 and self.plateau[i][0]!='.':
                #np.unique il élimine les doublons donc si il y a la même symbole sur toute la ligne np.unique()=[symbole]
                #donc len() doit être égale à 1
                self.etat=False
                if self.plateau[i][0] == sym1:
                    return f"C'est {self.joueurs[0][0]} qui a gagné la partie en {self.manche} manches"
                else :
                    return f"C'est {self.joueurs[1][0]} qui a gagné la partie en {self.manche} manches"
            
            #les 2 diagonales :

            if (self.plateau[0][0]==self.plateau[1][1]==self.plateau[2][2] or
                self.plateau[0][2]==self.plateau[1][1]==self.plateau[2][0]) and self.plateau[1][1]!='.':
                self.etat=False
                if self.plateau[1][1]==sym1:
                    return f"C'est {self.joueurs[0][0]} qui a gagné la partie en {self.manche} manches"
                else:
                    return f"C'est {self.joueurs[1][0]} qui a gagné la partie en {self.manche} manches"
            
        if self.etat: #il n'y a pas de vainqueur
            return None


class Joueur():
    
    def __init__(self,nom,jeu,pion):
        self.jeu=jeu
        self.nom=nom
        self.pion=pion
        self.jeu.joueurs.append((self.nom,self.pion))
        
    def __str__(self):
        return f"{self.nom} joue avec le symbole {self.pion}"
    def joue(self,l,c):
        self.jeu.place(l,c,self.pion)
        
        
        