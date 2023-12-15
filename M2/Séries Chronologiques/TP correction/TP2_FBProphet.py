# A faire tourner sur un notebook (pour les graphiques dynamiques) !

import pandas as pd
# Jeu de données contenant le cours horaire du bitcoin BTC/USD sur la période 07/2017-10/2020
Crypto = pd.read_csv("Mettre l'adresse du fichier\\crypto.csv", skiprows=[0])
Crypto.info()
Crypto

from datetime import datetime
# Conversion de la date
Date = Crypto['Unix Timestamp'].apply(lambda x: datetime.fromtimestamp(x))
Crypto["Date"] = Date

# Représentation graphique en candlestick
import plotly.graph_objs as go
fig = go.Figure(data=[go.Candlestick(x=Date, open=Crypto['Open'], high=Crypto['High'],
                                     low=Crypto['Low'], close=Crypto['Close'])])
fig.update_layout(xaxis=dict(title="Cours BTC/USD"), xaxis_rangeslider_visible=False)
fig.show()

# Calcul du prix typique
Crypto['TypPrice'] = (Crypto['Close'] + Crypto['High'] + Crypto['Low'])/3
Crypto

# Evolution des cours bas/typique/haut avec un rangeslider
g1 = go.Scatter(x = Crypto['Date'], y = Crypto['Open'], mode = 'lines', name = 'Open')
g2 = go.Scatter(x = Crypto['Date'], y = Crypto['Close'], mode = 'lines', name = 'Close')
g3 = go.Scatter(x = Crypto['Date'], y = Crypto['TypPrice'], mode = 'lines', name = 'TypPrice')
layout = dict(title='Bitcoin Prices', xaxis=dict(rangeslider=dict(visible = True), type='date'))
 
from plotly.offline import iplot
data = [g1, g2, g3]
fig = dict(data=data, layout=layout)
iplot(fig)

# Formatage pour l'objet Prophet()
CryptoFB = Crypto.reset_index().rename(columns={'Date':'ds', 'TypPrice':'y'})

# Création du modèle Facebook Prophet
from prophet import Prophet
ModFB = Prophet(interval_width=0.95)
ModFB.fit(CryptoFB)

# On propose une périodicité mensuelle
# On veut une prédiction sur un mois
FutureDates = ModFB.make_future_dataframe(periods=3*24*30, freq='H')
Pred = ModFB.predict(df=FutureDates)
Fig = ModFB.plot(Pred)

# Version interactive
from prophet.plot import plot_plotly, plot_components_plotly
plot_plotly(ModFB, Pred)

# Composante par composante
ModFB.plot_components(Pred)

# Un diagnostic par validation croisée
# Attention : on ne fait pas de validation croisée "n'importe comment" lorsqu'il y a une chronologie... !!
from prophet.diagnostics import cross_validation
CryptoCV = cross_validation(ModFB, initial='730 days', horizon = '90 days', period = '183 days')
CryptoCV.head()

from prophet.diagnostics import performance_metrics
CryptoCVPerf = performance_metrics(CryptoCV)
CryptoCVPerf.head()

from prophet.plot import plot_cross_validation_metric
Fig = plot_cross_validation_metric(CryptoCV, metric='rmse')
# Sur un mois les prédictions sont plutôt fiables avant une dégradation rapide