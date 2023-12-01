#!/bin/env python3
import sys
import re 

pattern_file = re.compile(r'INFO .* =(.*),.* D.*') # pour réupérer le nom de chacun des fichiers
pattern_temps = re.compile(r'Temps d\'execution : ([\d.]+(?:e-\d+)?)') # pour réupérer le temps d'éxecution de chaque fichiers
pattern_worker = re.compile(r'INFO .*Process: ForkPoolWorker-(.*)')
liste_temps = []
dict = {}
if __name__ == "__main__":
    log_file_name = sys.argv[1]
    with open(log_file_name,'r') as file:
        log_text = file.read()
        matches_temps = pattern_temps.findall(log_text)
        matches_worker = pattern_worker.findall(log_text)
        matches_file = pattern_file.findall(log_text)
        for match in matches_temps:
            liste_temps.append(float(match))
        for i, match in enumerate(matches_file):
            dict[(match,matches_worker[i])]=float(matches_temps[i]) # {nom_fichier : temps d'execution du fichier, etc...}
    unite_temps = min(liste_temps) 
    for key,values in dict.items():
        k=int(values/unite_temps)
        print(k,key)
# Pour trier sur le terminal : ./analyse_log.py './app.log' | sort -n -k 2
# -n pour trier numériquement et -k 2 c'est pour dire c'est le 2e élément qu'on trie

