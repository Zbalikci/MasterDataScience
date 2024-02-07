#! /usr/bin/env python3

import sys
import os
from collections import defaultdict

path = sys.argv[1]
files_repertory = os.listdir(path=path)

id_nbVisites = defaultdict(int)
id_title = {}

for file in files_repertory :
    with open(f"{path}/{file}",'r') as f :
        for line in f :
            line_split = line.split(',')
            if line_split[0]=='V' :
                id_nbVisites[line_split[1]] += 1
            elif line_split[0]=='A' :
                id_title[line_split[1]] = line_split[3]

id_nbVisites = sorted(id_nbVisites.items(), key=lambda kv:kv[1], reverse=True)[:5]
for id,nbVisites in id_nbVisites :
    print(f"{id_title[id]}\t{nbVisites} visites")
