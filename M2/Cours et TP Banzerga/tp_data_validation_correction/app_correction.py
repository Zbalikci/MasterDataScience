import json

import numpy as np
import pandas as pd
import pandera as pa

from flask import request, Flask, jsonify
from data_validation_correction import parameter_schema, CourseContentData, StudentProfileData
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
    params = parameter_schema.load(request.args)

    # data loading & validation from csv files
    raw_student_data = pd.read_csv("student_data.csv")
    student_data = StudentProfileData.validate(raw_student_data)

    raw_course_data = pd.read_csv("invalid_courses_data.csv")
    course_data = CourseContentData.validate(raw_course_data)

    if params["keyword"] is None:
        keyword = student_data.loc[
            student_data.student_id == params["student_id"],
            "area_of_interest"
        ].values[0]
    else:
        keyword = params["keyword"]

    possible_content_ids = course_data.loc[course_data.keyword == keyword, "id"]

    recommended_id = np.random.choice(possible_content_ids, 1)[0]

    return jsonify(
        json.loads(
            course_data.loc[course_data.id ==
                            recommended_id, :].to_json(orient="records")
        )
    )


@app.errorhandler(ValidationError)
def error_handling(error):
    return error.messages, 400


@app.errorhandler(pa.errors.SchemaError)
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
