#!/bin/env python3
import os
import time
import importlib
import logging
from multiprocessing import Pool, current_process
from multiprocessing.managers import BaseManager

logging.basicConfig(level=logging.DEBUG, filename="jobs.log", filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')

class RunJob:
    def __init__(self, jobs):
        self.jobs = jobs

    def run_job(self, job):
        module = importlib.import_module(job)
        start_time = time.time()
        try:
            resultat = module.run()
            finish_time = time.time()
            logging.info(f"File_name = {job}.py,\t Debut : {start_time},\t Fin : {finish_time},\t Temps d'execution : {finish_time-start_time} \t Process: {current_process().name}")
            logging.info(f"File_name = {job}.py,\t s'est exécuté correctement ! ")

        except Exception as e:
            resultat = 'Error : ' + str(e)
            logging.warning(f"File_name = {job}.py,\t ne s'est pas exécuté correctement \t Process: {current_process().name}")

        finish_time = time.time()
        with open(f"{job}.result", "w") as fichier:
            fichier.write(str(resultat))

    def process_jobs(self):
        s = time.time()
        print(f"Running with {os.cpu_count()} processors...")
        with Pool(processes=os.cpu_count()) as pool:
            pool.map(self.run_job, self.jobs)

        total_execution_time = time.time() - s
        print(f"Total execution time with {os.cpu_count()} processors: {total_execution_time} seconds\n")

if __name__ == "__main__":
    BaseManager.register('RunJob', RunJob)
    manager = BaseManager(address=('0.0.0.0', 5000), authkey=b'pwd')
    server = manager.get_server()
    print('server running')
    server.serve_forever()


