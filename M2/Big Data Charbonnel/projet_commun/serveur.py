#!/bin/env python3

from flask import Flask
from flask.json import jsonify
from flask import Flask, render_template
import json
import os

current_dir = os.getcwd()
dataset = f"{current_dir}/dataset"

with open(f"{dataset}/data_commun.json", "r") as file:
    data = json.load(file)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(f'index.html')

@app.route('/ws')
def index2():
    return jsonify(data)

@app.route('/ws/topics', methods=['GET'])
def show():
    return jsonify(list(data.keys()))

@app.route('/ws/topic/<topic>', methods=['GET'])
def t(topic):
    if str(topic) in data[str(topic)] :
        d = data[str(topic)][str(topic)]
    else : 
        d = data[str(topic)]
    return jsonify(d)

@app.route('/ws/annuaire', methods=['GET'])
def show2():
    with open(f"{dataset}/annuaire.json", "r") as file:
        annuaire = json.load(file)
    return jsonify(annuaire)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

