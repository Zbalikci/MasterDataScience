# import datetime
# from joblib import dump, load
from flask import Flask, request, jsonify
import datetime
import joblib 
import numpy as np 
import pandas as pd

app = Flask(__name__)

# Exemple d'une route GET simple :


@app.route("/route1", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

# Exercice 1 - Créer une route "/date" qui montre la date et l'heure du jour
# (utiliser datetime.datetime.now()).

@app.route("/date", methods=['GET'])
def date():
    heure = datetime.datetime.now()
    return f"<p>la date et l'heure du jour : {heure}</p>"


# Exemple d'une route GET avec paramètres
# http://172.20.45.167:5000/print-param?param1=12&param2=34
# pour parama1 = 12 et pour param2 = 34
@app.route("/print-param", methods=['GET'])
def print_param():
    param1 = request.args.get("param1", default=42)
    param2 = request.args["param2"]
    print(type(param1), type(param2))
    return f"<p>{param1}: {param2}<p>"


# Exercice 2 - Créer une route qui affiche le carré d'un flottant passé en argument
# (que faire si l'utilisateur envoie une chaîne de caractères ou rien ?).
@app.route("/<num>", methods=['GET'])
def carre(num):
    try :
        result = float(num)**2
    except : 
        result = "Ce n'est pas un float"
    return f"<p>{result}</p>"

@app.route("/carre", methods=['GET'])
def carre2():
    num = request.args["num"]
    try :
        result = float(num)**2
    except : 
        result = "Ce n'est pas un float"
    return f"<p>{result}</p>"

# Exemple d'une route POST
@app.route("/add-json-value", methods=['POST'])
def add_json_value():
    json_data = request.json

    if json_data is not None:
        json_data['test'] = 'ok'
    else:
        json_data['test'] = 'error'

    return jsonify(json_data)

# Pour tester cette requête, ouvrir un autre terminal et y taper la commande :
# python client.py -r add-json-value


# Exercice 3 - Créer une route 'predict' qui reçoit un JSON, calcule des prévisions
# à partir de ce JSON (et du modèle créé dans creation_modele.ipynb)
# et renvoie un JSON contenant les prévisions.
# Puis compléter le fichier client.py (fonction push_data_for_predict())
# pour envoyer une requête avec les nouvelles données (créées dans le notebook)
# afin de tester cette route.
@app.route("/predict",methods=['POST'])
def predict():
    model = joblib.load('./linear_model.joblib')
    json_data = request.json
    
    if json_data is not None:
        X_new = np.array([[json_data[i]['X0'], json_data[i]['X1'],json_data[i]['X2']] for i in range(len(json_data))])
        #y_new = np.array([json_data[i]['y'] for i in range(len(json_data))])
        predictions = model.predict(X_new)
        print(predictions)
    else :
        pass
    
    return jsonify(pd.Series(predictions).to_json(orient='values'))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
