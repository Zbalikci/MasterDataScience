# external imports
import numpy as np
import pandera as pa
from marshmallow import fields, Schema, validate

CONTENT_TYPES = (
    "video", "course", "exercise", "press_article", "web_url", "exam"
)

KEYWORDS = (
    "maths", "computer_science", "data_science",
    "history", "biology", "physics",
    "arts", "sport", "video_games",
    "economics", "social_sciences", "management"
)

YEAR_LEVELS = ("L1", "L2", "L3", "M1", "M2")

# VALIDATE API PARAMETERS


class ParametersSchema(Schema):
    student_id = fields.Integer(
        required=True
    )
    keyword = fields.String(
        required=False,
        load_default=None,
        validate=validate.OneOf(KEYWORDS)
    )


parameter_schema = ParametersSchema()

# VALIDATE DATAFRAMES

CourseContentData = pa.DataFrameSchema(
    columns={
        "id": pa.Column(
            int,
            nullable=False,
            unique=True,
            checks=pa.Check.ge(0),
        ),
        "title": pa.Column(
            str,
            nullable=False
        ),
        "type": pa.Column(
            str,
            nullable=True,
            checks=pa.Check.isin(CONTENT_TYPES)
        ),
        "keyword": pa.Column(
            str,
            nullable=False,
            checks=pa.Check.isin(KEYWORDS)
        ),
        "duration": pa.Column(
            int,
            nullable=True,
            checks=pa.Check.in_range(
                min_value=0,
                max_value=180
            )
        ),
        "creation_date": pa.Column(
            np.dtype('datetime64[s]'),
            nullable=True,
            coerce=True,
            checks=pa.Check.in_range(
                min_value=np.datetime64('1990-01-01'),
                max_value=np.datetime64('now')
            )
        )
    },
    strict=True,  # pas d'autre colonne que celles indiquées
)

StudentProfileData = pa.DataFrameSchema(
    columns={
        # doit être unique, positif, non vide
        "student_id": pa.Column(
            int,
            nullable=False,
            unique=True,
            checks=pa.Check.ge(0),
        ),
        # isin YEAR_LEVELS peut être vide
        "year_level": pa.Column(
            str,
            nullable=False,
            checks=pa.Check.isin(YEAR_LEVELS)
        ),
        # isin KEYWORDS, doit être non vide (cf. algo)
        "area_of_interest": pa.Column(
            str,
            nullable=False,
            checks=pa.Check.isin(KEYWORDS)
        )
    },
    strict=True,  # pas d'autre colonne que celles indiquées
)
