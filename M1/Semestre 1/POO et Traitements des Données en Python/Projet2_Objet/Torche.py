#!/bin/env python3

import time
import random as rand

class Torche():
    def __init__(self):
        
        self.etat = 0
        self.couleur = 0
        self.temps=0
        self.fin=0
        
    def __str__(self):
        if self.etat == 1 :
            self.fin=time.time()
            self.couleur =int((self.temps-self.fin)+rand.uniform(-self.temps,self.temps))%3
            return ["Vert","Orange","Orange"][self.couleur]
        else:
            return "Off"
    
    def pushA(self):
        self.etat= 1 - self.etat
        if self.etat == 0 :
            return self.couleur

            
    def pushB(self):
        if self.etat == 1:
            self.temps=time.time()
            self.couleur = (self.couleur+1)%3
            self.temps+=1
        return self.couleur


