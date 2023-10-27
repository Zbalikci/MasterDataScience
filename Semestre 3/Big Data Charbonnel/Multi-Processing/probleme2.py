#!/bin/env python3
import os
import sys 
import glob
import time
import importlib
import logging
import multiprocessing
from multiprocessing import Pool

nb_coeurs_processeur = os.cpu_count()
print(nb_coeurs_processeur)

logging.basicConfig(level=logging.DEBUG, filename="app.log", filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')

def main(job):
    
    module = importlib.import_module(job)
    try :
      start_time = time.time()
      resultat = module.run()
      finish_time = time.time()
      logging.info(f"File_name = {job}.py,\t Debut : {start_time},\t Fin : {finish_time},\t Temps d'execution : {finish_time-start_time}")
      logging.info(f"File_name = {job}.py,\t s'est exécuté correctement ! ")

    except Exception as e:
      resultat = e
      logging.warning(f"File_name = {job}.py,\t ne s'est pas exécuté correctement")
    
    with open(f"{job}.result", "w") as fichier:
      fichier.write(str(resultat))
    
if __name__ == "__main__":
  n=1
  path_jobs = sys.argv[1]
  os.chdir(path_jobs)
  jobs_files = glob.glob('*.py') 
  jobs = [module[:-3] for module in jobs_files]
  s = time.time()
  with Pool(n) as p:
    p.map(main,jobs)
  print(f'pour {n} process:', time.time() - s)

