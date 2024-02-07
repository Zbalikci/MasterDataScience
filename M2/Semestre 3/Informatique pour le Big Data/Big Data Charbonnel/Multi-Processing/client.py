#!/bin/env python3

from multiprocessing.managers import BaseManager
import sys 
import glob
import os

if __name__ == "__main__":
    path_jobs = sys.argv[1]

    sys.path.insert(0, path_jobs)
    os.chdir(path_jobs)
    jobs_files = glob.glob('*.py') 
    jobs = [module[:-3] for module in jobs_files]

    manager = BaseManager(address=('172.20.45.168', 5000), authkey=b'pwd')
    manager.connect()

    run_job = manager.RunJob(jobs)
    run_job.process_jobs()


