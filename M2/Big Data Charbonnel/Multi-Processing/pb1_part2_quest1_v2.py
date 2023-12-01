#!/bin/env python3
import os
import sys 
import glob
import time
import importlib
import logging
import matplotlib.pyplot as plt
from multiprocessing import Pool, current_process

logging.basicConfig(level=logging.DEBUG, filename="jobs.log", filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')

def main(job):
    module = importlib.import_module(job)
    start_time = time.time()
    try :
      result = module.run()
      finish_time = time.time()
      logging.info(f"File_name = {job}.py,\t Debut : {start_time},\t Fin : {finish_time},\t Temps d'execution : {finish_time-start_time} \t Process: {current_process().name}")
      logging.info(f"File_name = {job}.py,\t s'est exécuté correctement ! ")
      
    except Exception as e:
      result = 'Error : '+ str(e)
      logging.warning(f"File_name = {job}.py,\t ne s'est pas exécuté correctement \t Process: {current_process().name}")

    finish_time = time.time()
    with open(f"{job}.result", "w") as fichier:
      fichier.write(str(result))

if __name__ == "__main__":

    path_jobs = sys.argv[1]

    sys.path.insert(0, path_jobs)
    os.chdir(path_jobs)
    jobs_files = glob.glob('*.py') 
    jobs = [module[:-3] for module in jobs_files]

    execution_times = []

    for num_processors in range(1,21):
        s = time.time()
        print(f"Running with {num_processors} processors...")
        with Pool(processes=num_processors) as pool:
            pool.map(main, jobs)

        total_execution_time = time.time() - s
        execution_times.append(total_execution_time)
        print(f"Total execution time with {num_processors} processors: {total_execution_time} seconds\n")

    plt.plot(range(1,21), execution_times, marker='o')
    plt.xlabel('Number of Processors')
    plt.ylabel('Total Execution Time (seconds)')
    plt.title('Impact of Number of Processors on Execution Time')
    plt.show()