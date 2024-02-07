import os
import requests
import argparse

# Exemple de requête POST


def post_dummy_json(route):
    r = requests.post(os.path.join('http://127.0.0.1:5000/', route),
                      json={'userID': 65, 'value': [1, 2, 3]})
    print(r.text)  # les données renvoyées en sortie de la route
    return r


def push_data_for_predict(route):
    pass  # à compléter


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--route', type=str)

args = parser.parse_args()
route = args.route

if 'add-json-value' in route:
    r = post_dummy_json(route)
if 'predict' in route:
    r = push_data_for_predict(route)
r
