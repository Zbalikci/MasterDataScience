# external imports
import numpy as np
import pandera as pa
from marshmallow import Schema  , fields
import pandas as pd
CONTENT_TYPE_LIST = [
    "video", "course", "exercise", "press_article", "web_url", "exam"
]

KEYWORDS_LIST = [
    "maths", "computer_science", "data_science",
    "history", "biology", "physics",
    "arts", "sport", "video_games",
    "economics", "social_sciences", "management"
]

YEAR_LEVEL_LIST = ["L1", "L2", "L3", "M1", "M2"]

# VALIDATE API PARAMETERS


class ParametersSchema(Schema):
    student_id = fields.Int(required=True)
    keyword = fields.Str(required=False,allow_none=True,validate = lambda k : k in KEYWORDS_LIST if k is not None else True)

parameter_schema = ParametersSchema()

# VALIDATE DATAFRAMES

CourseContentData = pa.DataFrameSchema({
    'id': pa.Column(pa.Int, checks=[
        pa.Check(lambda i: i > 0, element_wise=True, error='Doit être un entier positive'),
    ]),
    'title': pa.Column(pa.String, checks=[
        pa.Check(lambda s: s.strip() != '', element_wise=True, error='Ne peut être vide')
    ]),
    'type': pa.Column(pa.String, checks=[
        pa.Check(lambda t: t in CONTENT_TYPE_LIST, element_wise=True, error='Doit être parmi  {}'.format(CONTENT_TYPE_LIST))
    ]),
    'keyword': pa.Column(pa.String, checks=[
        pa.Check(lambda k: k in KEYWORDS_LIST, element_wise=True, error='Doit être parmi  {}'.format(KEYWORDS_LIST))
    ]),
    'duration': pa.Column(pa.Int, checks=[
        pa.Check(lambda d: 0 <= d <= 180, element_wise=True, error='Doit être entre 0 et 180')
    ], nullable=True),
    'creation_date': pa.Column(pa.DateTime, checks=[
        pa.Check(lambda date: date > pd.to_datetime(['1990-01-01']), element_wise=True, error='Doit être après 1990-01-01')
    ], nullable=True)
})

StudentProfileData = pa.DataFrameSchema({
    'student_id': pa.Column(pa.Int, checks=[
        pa.Check(lambda i: i > 0, element_wise=True, error='Doit être un entier positive'),
    ]),
    'year_level': pa.Column(pa.String, checks=[
        pa.Check(lambda level: level in YEAR_LEVEL_LIST, element_wise=True,
                 error='Doit être parmi  {}'.format(YEAR_LEVEL_LIST))
    ], nullable=True),
    'area_of_interest': pa.Column(pa.String, checks=[
        pa.Check(lambda area: area in KEYWORDS_LIST, element_wise=True, error='Doit être parmi {}'.format(KEYWORDS_LIST))
    ], nullable=False)
})
