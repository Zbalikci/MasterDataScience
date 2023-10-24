#!/bin/env python3
import os
import sys 
import glob
import time
import importlib
import logging
#Il faut écrire export PYTHONPATH='./jobs' sur le terminal !!

"""
Question 2 : J'ai changé jobs13-3.py pour qu'il lance une execption

def run():
  try:
    raise NameError('Non !')
  except NameError:
    #print('Un des fichiers ne s'éxécute pas correctement !') # il affiche ce message à l'écran directement
    raise
"""
logging.basicConfig(level=logging.DEBUG, filename="app.log", filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
  path_jobs = sys.argv[1]
  os.chdir(path_jobs)
  jobs_files = glob.glob('*.py') 
  jobs = [module[:-3] for module in jobs_files]
  for job in jobs:
    module = importlib.import_module(job)
    
    try :
      start_time = time.time()
      resultat = module.run()
      finish_time = time.time()
      logging.info(f"File_name = {job}.py,\t Temps d'execution : {finish_time-start_time}")
      logging.info(f"File_name = {job}.py,\t s'est exécuté correctement ! ")

    except Exception as e:
      resultat = e
      logging.warning(f"File_name = {job}.py,\t ne s'est pas exécuté correctement")
    
    with open(f"{job}.result", "w") as fichier:
      fichier.write(str(resultat))