#! /usr/bin/env python3

import sys
import os
from collections import defaultdict

path = sys.argv[1]
files_repertory = os.listdir(path=path)

user_nbVisites = defaultdict(int)
id_user = None

for file in files_repertory :
    with open(f"{path}/{file}",'r') as f :
        for line in f :
            line_split = line.split(',')
            if line_split[0]=='V' :
                user_nbVisites[id_user] += 1
            elif line_split[0]=='C' :
                id_user = line_split[1]

user_nbVisites = sorted(user_nbVisites.items(), key=lambda kv:kv[1], reverse=True)[:15]
for user,nbVisites in user_nbVisites :
    print(f"{user}\t{nbVisites} visites")
