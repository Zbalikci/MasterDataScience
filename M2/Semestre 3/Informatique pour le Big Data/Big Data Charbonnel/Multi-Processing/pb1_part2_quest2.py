#!/bin/env python3
import os
import sys 
import glob
import time
import importlib
import logging
from multiprocessing import Pool, current_process
from multiprocessing.managers import BaseManager

# Define a custom logger manager
class MyLogManager(BaseManager):
    pass

# Function to create a logger
def create_logger():
    logging.basicConfig(level=logging.DEBUG, filename="jobs.log", filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger()

# Register the logger manager
MyLogManager.register('get_logger', callable=create_logger)

# Function to initialize worker-specific information
def init_worker(logger):
    global worker_logger
    worker_logger = logger

# Function to execute a job
def main(job):
    global worker_logger
    module = importlib.import_module(job)
    start_time = time.time()
    try:
        result = module.run()
        finish_time = time.time()
        worker_logger.info(f"File_name = {job}.py,\t Debut : {start_time},\t Fin : {finish_time},\t Temps d'execution : {finish_time-start_time} \t Worker: {current_process().name}")
        worker_logger.info(f"File_name = {job}.py,\t s'est exécuté correctement ! ")
    except Exception as e:
        result = 'Error : '+ str(e)
        worker_logger.warning(f"File_name = {job}.py,\t ne s'est pas exécuté correctement \t Worker: {current_process().name}")

    finish_time = time.time()
    with open(f"{job}.result", "w") as fichier:
        fichier.write(str(result))

if __name__ == "__main__":
    # Get the IP addresses of workers from command line arguments
    worker_ips = sys.argv[1:]
    num_workers = len(worker_ips)

    # Create a manager server and get the logger
    with MyLogManager() as manager:
        manager.start()
        logger = manager.get_logger()

        # Set up worker-specific information
        pool_initializer = lambda: init_worker(logger)

        s = time.time()
        path_jobs = sys.argv[num_workers + 1]

        sys.path.insert(0, path_jobs)
        os.chdir(path_jobs)
        jobs_files = glob.glob('*.py') 
        jobs = [module[:-3] for module in jobs_files]

        print(f"Running with {num_workers} workers...")
        with Pool(processes=num_workers, initializer=pool_initializer) as pool:
            pool.map(main, jobs)

        total_execution_time = time.time() - s

        print(f"Total execution time with {num_workers} workers: {total_execution_time} seconds\n")
