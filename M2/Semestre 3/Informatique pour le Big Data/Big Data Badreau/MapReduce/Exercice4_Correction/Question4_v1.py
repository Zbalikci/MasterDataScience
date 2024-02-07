#! /usr/bin/env python3

import sys
import os
from collections import defaultdict

path = sys.argv[1]
files_repertory = os.listdir(path=path)

user_idPages = defaultdict(list)
id_title = {}
id_user = None

for file in files_repertory :
    with open(f"{path}/{file}",'r') as f :
        for line in f :
            line_split = line.split(',')
            if line_split[0]=='V' :
                user_idPages[id_user] += [line_split[1]]
            elif line_split[0]=='C' :
                id_user = line_split[1]
            elif line_split[0]=='A' :
                id_title[line_split[1]] = line_split[3]

user_idPages = sorted(user_idPages.items(), key=lambda kv:len(kv[1]), reverse=True)[:5]
for user,Visites in user_idPages :
    print(f"{user}\t{len(Visites)} visites : {', '.join([id_title[idPages] for idPages in set(Visites)])} ")
