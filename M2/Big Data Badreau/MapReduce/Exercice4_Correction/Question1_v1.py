#! /usr/bin/env python3

import sys
import os
from collections import defaultdict

path = sys.argv[1]
files_repertory = os.listdir(path=path)

id_nbVisites = defaultdict(int)

for file in files_repertory :
    with open(f"{path}/{file}",'r') as f :
        for line in f :
            line_split = line.split(',')
            if line_split[0]=='V' :
                id_nbVisites[line_split[1]] += 1

for id,nbVisites in id_nbVisites.items() :
    if nbVisites >= 1000 :
        print(f"{id}\t{nbVisites} visites")
