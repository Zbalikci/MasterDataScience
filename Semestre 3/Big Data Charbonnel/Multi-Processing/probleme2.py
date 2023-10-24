#!/bin/env python3
import sys
import os

nb_coeurs_processeur = os.cpu_count()

import multiprocessing


class MyProcess(multiprocessing.Process):
  def __init__(self,...):
    multiprocessing.Process.__init__(self)


  def run(self):


if __name__ == '__main__':
  myprocess = MyProcess(...)
  myprocess.start()
  myprocess.join()
