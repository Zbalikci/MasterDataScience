import os
import requests
import argparse
import pandas as pd
# Exemple de requête POST

def post_dummy_json(route):
    r = requests.post(os.path.join('http://127.0.0.1:5000/', route),
                      json={'userID': 65, 'value': [1, 2, 3]})
    print(r.text)  # les données renvoyées en sortie de la route
    return r

def push_data_for_predict(route):
    r = requests.post(os.path.join('http://127.0.0.1:5000/', route), json = pd.read_csv('new_data.csv').to_dict('records'),)
    print(r.text)
    return r

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--route', type=str)

args = parser.parse_args()
route = args.route

if 'add-json-value' in route:
    r = post_dummy_json(route)
if 'predict' in route:
    r = push_data_for_predict(route)
r
