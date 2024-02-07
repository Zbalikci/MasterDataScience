import json
import numpy as np
import pandas as pd
import pandera as pa
from flask import Flask, request, jsonify
from data_validation import parameter_schema, CourseContentData, StudentProfileData
from marshmallow.exceptions import ValidationError

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/random-recommendation", methods=['GET'])
def generate_reco():
    """
    Route d'API de recommandation aléatoire de contenu pédagogique pour étudiants.

    La route d'API prend 2 paramètres :
    - student_id : entier identifiant l'étudiant, obligatoire
    - keyword : mot clé désignant le centre d'intérêt pour lequel
    l'étudiant veut une recommandation, facultatif.

    Returns
    -------
    Dataframe converti en JSON correspondant au contenu recommandé.
    """

    try :

        # 1. Récupérer les paramètres de la requête d'API et les valider
        # avec parameter_schema (avec la librairie Marshmallow)
        keyword = request.args.get("keyword", default=None)
        student_id = request.args["student_id"]
        parameter_schema.validate(data = [keyword,student_id])

        # 2. Récupérer les données des étudiants et des cours à partir
        # des CSV & valider ces données (avec la librairie Pandera)
        invalid_courses_data = pd.read_csv("./invalid_courses_data.csv")
        courses_data = pd.read_csv("./courses_data.csv")
        student_data = pd.read_csv("./student_data.csv")
        courses_data["creation_date"] = pd.to_datetime(courses_data["creation_date"])
        StudentProfileData.validate(student_data)
        CourseContentData.validate(courses_data)
        #CourseContentData.validate(invalid_courses_data)

        # 3. Implémenter la logique de recommandation (tirage aléatoire basé sur
        # sur le mot-clé ou le centre d'intérêt)
        if keyword :
            result = courses_data[courses_data['keyword'] == keyword]
        else :
            area_of_interest = student_data[student_data['id'] == int(student_id)]["area_of_interest"].values[0]
            result = courses_data[courses_data["keyword"] == area_of_interest][['title','type']]
        if result.empty :
            return jsonify({'error': 'Aucun cours disponible pour le mot-clé ou le centre d\'intérêt spécifié.'}), 404
        random_course = result.sample(1).iloc(0)

        # 4. Renvoyer (au format JSON) la ligne du dataframe de contenus
        # correspondant au contenu recommandé trouvé ci-dessus.
        return jsonify(random_course)
    
    except ValidationError as ve:
        return jsonify({'error': ve.messages}), 400
    except pa.errors.SchemaError as pe:
        return jsonify({'error': f"Invalide data reçu de la DB: {pe}"}), 400

# Le code ci-dessous permet à Flask de rattraper une exception de type ValidationError
# levée par Marshmallow et de renvoyer en sortie d'API le message d'erreur
# correspondant avec un code HTTP 400.
@app.errorhandler(ValidationError)
def error_handling(error):
    return error.messages, 400


# Même principe pour les 2 ci-dessous avec les erreurs de pandera.
@app.errorhandler(pa.errors.SchemaErrors)
def handle_pandera_validation_error(error):
    message = f"Invalid data received from DB: {error}"
    return message, 400


@app.errorhandler(pa.errors.SchemaErrors)
def handle_multiple_pandera_validation_error(error):
    message = f"Invalid data received from DB: {error}"
    return message, 400


# spécifier le port (par défaut, Flask est sur le 5000) :
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# et faire tourner l'app avec python app.py et non flask run

# autre méthode pour spécifier le port : flask run --host=0.0.0.0 --port=80
