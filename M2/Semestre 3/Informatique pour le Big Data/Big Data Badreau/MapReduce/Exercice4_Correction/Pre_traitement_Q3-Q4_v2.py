#! /usr/bin/env python3

import sys
import os

path = sys.argv[1]
files_repertory = os.listdir(path=path)

path_bis = f'{path}_bis'
try:
    os.mkdir(path_bis) # création d'un dossier bis
    print(f'Dossier {path_bis} créé')
except:
    print(f'Dossier {path_bis} existe déjà')

for file in files_repertory :
    with open(f"{path}/{file}",'r') as f_read :
        with open(f"{path_bis}/{file}_bis",'w') as f_write : # création d'un fichier bis
            first_line = True
            for line in f_read :            
                if line[0] != 'V' and not first_line :
                    f_write.write('\n')
                f_write.write(line.strip('\n')+',')
                first_line = False
        print(f'Fichier {path_bis}/{file}_bis terminé')