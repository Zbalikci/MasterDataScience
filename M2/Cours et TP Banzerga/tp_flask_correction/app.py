import joblib
import datetime
import pandas as pd

from flask import Flask, request, jsonify

app = Flask(__name__)


# Exemple d'une route GET simple :
@app.route("/route1", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


# Exercice 1 - Créer une route "/date" qui montre la date et l'heure du jour
# (utiliser datetime.datetime.now()).
@app.route("/date", methods=["GET"])
def affiche_date():
    return f"<p>Date et heure : {datetime.datetime.now()}</p>"


# Exemple d'une route GET avec paramètres
@app.route("/print-param", methods=['GET'])
def print_param():
    # .get() : si param1 n'est pas donné par l'utilisateur, il vaut 42 par défaut
    param1 = request.args.get("param1", default=42)

    # [] : si param2 n'est pas donné par l'utilisateur, il y a erreur
    param2 = request.args["param2"]

    # Flask interprète tout en strings par défaut !
    print(type(param1), type(param2))

    return f"<p>param1 = {param1} param2 = {param2} </p>"


# Exercice 2 - Créer une route qui affiche le carré d'un flottant passé en argument
# (que faire si l'utilisateur envoie une chaîne de caractères ou rien ?).
@app.route("/carre", methods=['GET'])
def carre():
    try:
        param = float(request.args["param"])
        return f"{param**2}"
    except Exception:
        return "Erreur : il faut un flottant.", 400


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
# à partir de ce JSON (sauf sa colonne y !!!) et du modèle créé dans creation_modele.ipynb
# et renvoie un JSON contenant les prévisions.
# Puis compléter le fichier client.py (fonction push_data_for_predict())
# pour envoyer une requête avec les nouvelles données (créées dans le notebook)
# afin de tester cette route avec python client.py -r predict.
# NB : Vous aurez besoin de :
# - pandas.DataFrame.from_dict(..., orient='columns') pour transformer le json en pd.DataFrame
# - pour les prévisions, transformer un numpy array ou pd dataframe en json string puis utiliser jsonify.

@app.route("/predict", methods=["POST"])
def predict():
    json_data = request.json
    input_df = pd.DataFrame.from_dict(json_data, orient='columns')
    input_df = input_df.drop(columns=['y'])
    model = joblib.load('linear_model.joblib')
    results = model.predict(input_df)
    return jsonify(results.tolist())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
