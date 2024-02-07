import os
import json
import requests
import argparse


# Exemple de requête POST
def post_dummy_json(route):
    r = requests.post(os.path.join('http://127.0.0.1:5000/', route),
                      json={'userID': 65, 'value': [1, 2, 3]})
    print(r.text)  # les données renvoyées en sortie de la route


def push_data_for_predict(route):
    with open('new_data.json') as f:
        json_data = json.load(f)
    r = requests.post(os.path.join('http://127.0.0.1:5000/', route),
                      json=json_data)
    print(r.text)


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--route', type=str)

args = parser.parse_args()
route = args.route

if route == 'add-json-value':
    post_dummy_json(route)
if route == 'predict':
    push_data_for_predict(route)
