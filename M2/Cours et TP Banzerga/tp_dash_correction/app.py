# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from joblib import load
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

linear_model = load("linear_model.joblib")

df = pd.read_csv("new_data.csv")

app.layout = html.Div(children=[
    html.H1(children='Un dashboard simple'),
    html.Br(),
    html.H2("Un graphe"),
    html.Div(
        [html.Label("Variable de l'axe des abscisses"),
         dcc.Dropdown(
            ['X0', 'X1', 'X2'],
            'X0',
            id="X_col_plot")]  # Question 1 : choix de la colonne à tracer
    ),

    dcc.Graph(id='plot_X_vs_y'),  # Question 1 : le scatter plot
    html.Br(),
    html.H2("Calcul d'une prévision"),  # Question 2 : début affichage
    html.H3("Valeurs de X0, X1, X2 :"),
    # ce html.Div regroupe les 3 sliders pour les choix de X0, X1, X2
    html.Div(children=[
        html.Label('X0'),
        html.Div(dcc.Slider(
            min=9,
            max=15,
            marks={i: str(i) for i in range(9, 16)},
            value=9,
            id="X0_input"
        ), style={'width': '30%', 'margin': 5, 'display': 'inline-block'}),  # Question 5

        html.Label('X1'),
        html.Div(dcc.Slider(
            min=24,
            max=31,
            marks={i: str(i) for i in range(24, 31)},
            value=24,
            id="X1_input"
        ), style={'width': '30%', 'margin': 5, 'display': 'inline-block'}),  # Question 5


        html.Label('X2'),
        html.Div(dcc.Slider(
            min=44,
            max=50,
            marks={i: str(i) for i in range(44, 50)},
            value=44,
            id="X2_input"
        ), style={'width': '30%', 'margin': 5, 'display': 'inline-block'}),  # Question 5
    ]),
    html.H3("Valeur de la prévision : "),
    html.Div(id="y_pred"),  # Question 2 : fin affichage

    # Question 3 : affichage histogramme
    html.H2("Histogramme"),
    dcc.Graph(id='plot_X_hist'),
])


# Questions 1 et 4 : scatter plot
@app.callback(
    Output(component_id='plot_X_vs_y', component_property='figure'),
    Input(component_id='X_col_plot', component_property='value'),
    Input(component_id='X0_input', component_property='value'),
    Input(component_id='X1_input', component_property='value'),
    Input(component_id='X2_input', component_property='value'),
)
def update_plot_x_y(col_name, X0_input, X1_input, X2_input):
    # Question 1
    fig = go.Figure(
        go.Scatter(
            x=df[col_name],
            y=df["y"],
            mode="markers",
            name="Training set"
        )
    )
    # Ajouts pour la question 4
    if col_name == "X1":
        x_coord = X1_input
    elif col_name == "X2":
        x_coord = X2_input
    else:
        x_coord = X0_input
    fig.add_trace(
        go.Scatter(
            x=[x_coord],
            y=[compute_forecast(X0_input, X1_input, X2_input)],
            mode="markers",
            marker=dict(size=10),
            name="Forecast"
        )
    )
    return fig


# Question 2 : calcul d'une prévision à partir de sliders
def compute_forecast(X0, X1, X2):
    input_data = np.array([X0, X1, X2]).reshape(1, -1)
    return linear_model.predict(input_data)[0]


@app.callback(
    Output(component_id='y_pred', component_property='children'),
    Input(component_id='X0_input', component_property='value'),
    Input(component_id='X1_input', component_property='value'),
    Input(component_id='X2_input', component_property='value')
)
def update_forecast(X0_input, X1_input, X2_input):
    return f"y = {compute_forecast(X0_input, X1_input, X2_input)}"


# Question 3 : histogramme de la colonne Xi choisie avec "X_col_plot"
@app.callback(
    Output(component_id='plot_X_hist', component_property='figure'),
    Input(component_id='X_col_plot', component_property='value'),
)
def update_hist_x(col_name):
    fig = px.histogram(df, x=col_name)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
