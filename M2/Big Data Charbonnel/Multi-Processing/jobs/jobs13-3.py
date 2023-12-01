#!/bin/env python3
import sys
sys.path.insert(0,"./modules")

import binome

def run():
  try:
    raise NameError('Non !')
  except NameError:
    #print('Un des fichiers ne s'éxécute pas correctement !') # il affiche ce message à l'écran directement
    raise
    #return binome.C(13,3)

if __name__=="__main__":
  binome.main()  

