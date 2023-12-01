#!/bin/env python3

from flask import Flask
from flask.json import jsonify
import json
import os
import glob
import requests

current_dir = os.getcwd()
dataset = f"{current_dir}/dataset"

###############################################################################

with open(f"{dataset}/annuaire.json", "r") as file:
    annuaire = json.load(file)

# Récupération des ip à partir des ip que j'ai déjà dans ma base de donée

for ip in annuaire :
    try :
        url = f"{ip}/ws/annuaire"
        reponse = requests.get(url)
        ip_adresses = reponse.json()
        annuaire = annuaire + ip_adresses
    except :
        print(f"NOK : {ip} n'est pas accessible ou bien n'a pas d'annuaire")

annuaire = list(set(annuaire))

with open(f"{dataset}/annuaire.json", "w") as file:
    json.dump(annuaire,file)

###############################################################################

# Récupération des donées des ip que j'ai dans ma base de donnée

for ip in annuaire :
    try :
            url = f"{ip}/ws"
            Dict = {}
            reponse = requests.get(url+'/topics')
            topics = reponse.json()
            for topic in topics :
                reponse = requests.get(url+'/topic/'+topic)
                if str(topic) in reponse.json() :
                    Dict[str(topic)] = reponse.json()[str(topic)]
                    if str(topic) in reponse.json()[str(topic)]:
                        Dict[str(topic)] = reponse.json()[str(topic)][str(topic)]
                    else:
                        Dict[str(topic)] = reponse.json()[str(topic)]
                else:
                    Dict[str(topic)] = reponse.json()
            with open(f"{dataset}/{ip[6:-5]}.json", "w") as f:
                json.dump(Dict,f)
    except :
            print(f'NOK : {ip} Récupération des données a échoué')


###############################################################################

current_dir = os.getcwd()

os.chdir(dataset)
json_files = glob.glob('*[0-9].json') 

os.chdir(current_dir)
current_dir = os.getcwd()

with open(f"{dataset}/data_commun.json", "r") as file:
    data = json.load(file)

########################### mise en commun des données dans un seul fichier json ###########################

# Vérifie si les topics sont dans des dictionnaires et si les items sont dans des dictionnaires
# si les urls sont dans des listes et si les url commencent par http

for json_file in json_files :
        with open(f"{dataset}/{json_file}", "r") as file:
            data_server = json.load(file)
        for key, value in data_server.items():
            new_value = {}
            if isinstance(value,dict): # si les topics sont dans des dictionnaires
                if key not in data :
                    for cle,valeur in value.items():
                        if isinstance(valeur,list):
                            valeur = list(set(valeur))
                            new_valeur = []
                            for url in valeur :
                                if url.startswith('http'):
                                    new_valeur.append(url)
                            new_value[cle] = new_valeur
                        data[key] = new_value
                # Si j'ai le topic, je vérifie si j'ai les items
                else: 
                    for k,v in value.items(): # si les items sont dans des dictionnaires
                        if isinstance(v,list):
                            v=list(set(v))
                            if k not in data[key]:
                                data[key][k]=[]
                                for url in v :
                                    if url.startswith('http'):
                                        data[key][k].append(url)
                                data[key][k] = list(set(data[key][k]))
                            # et si j'ai les items je vérifie si y'a des url que je n'ai pas dans ma base de donnée
                            else : 
                                for url in v :
                                    if (url not in data[key][k]) and (url.startswith('http')):
                                        data[key][k].append(url)
                                    data[key][k] = list(set(data[key][k]))

with open(f"{dataset}/data_commun.json", "w") as file:
    json.dump(data,file)