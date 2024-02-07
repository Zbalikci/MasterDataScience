import numpy as np
import pandas as pd
from joblib import load
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, dcc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

linear_model = load("linear_model.joblib")

df = pd.read_csv("new_data.csv")

global y_predict
y_predict = None

app.layout = html.Div(children=[
    html.H6("Saisissez le texte de votre choix ci-dessous :"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='toto', type='text')
    ]),
    html.Div(
        "Output: ",id='my-output'
    ), 
    html.Br(),
    
    html.Div([
        html.Label("Choisissez une colonne pour l'axe des x :"),
        dcc.Dropdown(
            id='x-column-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns if col.startswith('X')],
            value=df.columns[1]  # Set the default value to the first column
        )
    ]),
    html.Br(),
    dcc.Graph(id='scatter-plot'),
    dcc.Graph(id='hist-plot'),
    dbc.Row([
        dbc.Col(
        dcc.Slider(
            id='X0-slider',
            min=df['X0'].min(),
            max=df['X0'].max(),
            value=df['X0'].min(),
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            step=None
        ), width = 4),
        dbc.Col(
        dcc.Slider(
            id='X1-slider',
            min=df['X1'].min(),
            max=df['X1'].max(),
            value=df['X1'].min(),
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            step=None
        ), width = 4),
        dbc.Col(
        dcc.Slider(
            id='X2-slider',
            min=df['X2'].min(),
            max=df['X2'].max(),
            value=df['X2'].min(),
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            step=None
        ), width = 4),
    ]),

    html.Div(id='y_predict'),
    ])

# Exemple de callback simple
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'

# Questions

# 0. Exécuter python app.py et tester le dashboard.  http://127.0.0.1:8050/

# Question 1
# 1. Définir un callback permettant de tracer un scatter plot (avec px.scatter(...))
# avec en abscisses une colonne Xi du dataframe df au choix de l'utilisateur
# (définie par un dropdown placé dans le layout ci-dessus)
# et en ordonnées la colonne y du dataframe df

# @app.callback(
#     Output('scatter-plot', 'figure'),
#     [Input('x-column-dropdown', 'value')]
# )
# def update_scatter_plot(selected_column):
#     fig = px.scatter(df, x=selected_column, y='y', title=f'Scatter Plot (y en fonction de {selected_column})')
#     return fig

# Question 2
# 2. Définir un 2e callback permettant, à partir des valeurs de X0, X1, X2
# choisies avec 3 sliders(curseurs) placés dans le layout ci-dessus
# de calculer la prévision de y correspondante (en utilisant linear_model)
# et de l'afficher dans le dashboard
@app.callback(
    Output('y_predict', 'children'),  # Fix: Use 'children' instead of 'predict'
    [Input('X0-slider', 'value'), Input('X1-slider', 'value'), Input('X2-slider', 'value')]
)
def update_predict(X0_value, X1_value, X2_value):
    global y_predict
    y_predict = linear_model.predict(np.array([X0_value, X1_value, X2_value]).reshape(1, -1))
    return f'Predicted y: {y_predict[0]}'

# Questions subsidiaires :

# Question 3
# 3. Tracer un histogramme de Xi (selon le choix du dropdown utilisé en 1.)
@app.callback(
    Output('hist-plot', 'figure'),
    [Input('x-column-dropdown', 'value')]
)
def update_hist_plot(selected_column):
    fig = px.histogram(df[str(selected_column)], x=selected_column, title=f'Histogramme de {selected_column}')
    return fig

# Question 4
# 4. Modifier le graphe du 1er callback pour qu'il affiche le point (Xi, y_pred),
# où y_pred est calculé dans la question 2.
# Question 4
# 4. Modifier le graphe du 1er callback pour qu'il affiche le point (Xi, y_pred),
# où y_pred est calculé dans la question 2.

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('x-column-dropdown', 'value'),
     Input('X0-slider', 'value'),
     Input('X1-slider', 'value'),
     Input('X2-slider', 'value')]
)
def update_scatter_plot(selected_column, X0_value, X1_value, X2_value):
    y_predict = linear_model.predict(np.array([X0_value, X1_value, X2_value]).reshape(1, -1))
    if selected_column == 'X0':
        point_df = pd.DataFrame({selected_column: [X0_value], 'y': [y_predict[0]]})
    elif selected_column == 'X1' :
        point_df = pd.DataFrame({selected_column: [X1_value], 'y': [y_predict[0]]})
    elif selected_column == 'X2':
        point_df = pd.DataFrame({selected_column: [X2_value], 'y': [y_predict[0]]})
    fig = px.scatter(df, x=selected_column, y='y', title=f'Scatter Plot (y en fonction de {selected_column})')
    fig.add_trace(px.scatter(point_df, x=selected_column, y='y',color='y').update_traces(marker=dict(color='red')).data[0])

    return fig


# Question 5
# 5. Aligner les 3 sliders sur la même ligne

if __name__ == '__main__':
    app.run_server(debug=True)













