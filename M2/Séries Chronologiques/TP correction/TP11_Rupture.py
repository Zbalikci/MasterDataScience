
import pandas as pd
SNCF = pd.read_csv("... l'adresse de votre fichier ... \\SNCF.csv", sep=";")

# Les données représentent le nombre de passagers mensuels de la SNCF sur 18 ans
import matplotlib.pyplot as plt
plt.plot(SNCF["Mois"], SNCF["Voy"])
plt.xlabel("Mois")
plt.ylabel("Voyageurs de la SNCF")
plt.grid()

# Passage au log
import numpy as np
SNCF["LVoy"] = np.log(SNCF["Voy"])
plt.plot(SNCF["Mois"], SNCF["LVoy"])
plt.xlabel("Mois")
plt.ylabel("Voyageurs de la SNCF (log)")
plt.grid()

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# On fait des régressions sur deux tronçons : [0, R-1] et [R, n-1]
# - Constante sur [0, R-1]
# - Linéaire sur [R, n-1]
n = len(SNCF["LVoy"])
MSE = np.zeros(n-1)
for R in range(1, n):
    X1, X2 = np.array(SNCF["LVoy"][:R]).reshape(-1, 1), np.array(SNCF["LVoy"][R:]).reshape(-1, 1)
    Tps1, Tps2 = np.arange(R).reshape(-1, 1), np.arange(R, n).reshape(-1, 1)
    LR1, LR2 = LinearRegression(), LinearRegression()
    LR1.fit(np.ones(len(X1)).reshape(-1, 1), X1)
    LR2.fit(Tps2, X2)
    PredX1, PredX2 = LR1.predict(Tps1), LR2.predict(Tps2)
    MSE[R-1] = (R*mean_squared_error(X1, PredX1) + (n-R)*mean_squared_error(X2, PredX2))/n
    
R = np.argmin(MSE)+1
plt.plot(range(1, n), MSE)
plt.xlabel("Mois de rupture")
plt.ylabel("MSE")
plt.grid()
plt.scatter(R, MSE[R-1], color="red", marker="x")
# La rupture est détectée en R = 57

# Graphiques illustrant la rupture avec les deux régressions linéaires 
X1, X2 = np.array(SNCF["LVoy"][:R]).reshape(-1, 1), np.array(SNCF["LVoy"][R:]).reshape(-1, 1)
Tps1, Tps2 = np.arange(R).reshape(-1, 1), np.arange(R, n).reshape(-1, 1)
LR1, LR2 = LinearRegression(), LinearRegression()
LR1.fit(np.ones(len(X1)).reshape(-1, 1), X1)
LR2.fit(Tps2, X2)
PredX1, PredX2 = LR1.predict(Tps1), LR2.predict(Tps2)
plt.plot(SNCF["Mois"], SNCF["LVoy"])
plt.plot(Tps1, PredX1, color="red")
plt.plot(Tps2, PredX2, color="red")
plt.axvline(R, color="red", linestyle="dotted")
plt.xlabel("Mois")
plt.ylabel("Voyageurs de la SNCF (log)")
plt.grid()

from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima.arima import auto_arima

X = X2
n = len(X)

# Avec (I-B^12)
auto_arima(X, start_p=0, start_q=0, seasonal=True, start_P=0, start_Q=0, m=12, d=0, D=1,
                 with_intercept=True, stepwise=True, trace=True)
# SARIMA(1,0,1)(0,1,2)[12] avec intercept

# Avec (I-B)(I-B^12)
auto_arima(X, start_p=0, start_q=0, seasonal=True, start_P=0, start_Q=0, m=12, d=1, D=1,
                 with_intercept=True, stepwise=True, trace=True)
# SARIMA(0,1,1)(0,1,2)[12] sans intercept

XT = X[:(n-12)]

Mod01 = SARIMAX(XT, order=(1, 0, 1), seasonal_order=(0, 1, 2, 12), trend='c', enforce_stationarity=False, enforce_invertibility=False)
Mod01F = Mod01.fit()
print(Mod01F.summary())
Mod01F.plot_diagnostics()

Mod11 = SARIMAX(XT, order=(0, 1, 1), seasonal_order=(0, 1, 2, 12), enforce_stationarity=False, enforce_invertibility=False)
Mod11F = Mod11.fit()
print(Mod11F.summary())
Mod11F.plot_diagnostics()

# Dans les deux cas : Q=2 est remis en question
# Pour une étude complète, il aurait fallu aussi observer les ACF/PACF, tester les rédidus, etc.

plt.plot(X, color="blue")
plt.ylim([7, 8.5])
plt.plot(Mod01F.fittedvalues, color="orange", linestyle="dotted")
plt.plot(Mod11F.fittedvalues, color="violet", linestyle="dotted")
plt.grid()

Pred01 = Mod01F.get_forecast(steps=24).summary_frame(alpha=0.05)
plt.plot(X, color="blue")
plt.plot(range(n, n+24), Pred01['mean'], linestyle='--', color="orange")
plt.fill_between(range(n, n+24), Pred01['mean_ci_lower'], Pred01['mean_ci_upper'], color='orange', alpha=0.2)
plt.xlabel("Mois")
plt.ylabel("Voyageurs de la SNCF (log)")
plt.grid()

Pred11 = Mod11F.get_forecast(steps=24).summary_frame(alpha=0.05)
plt.plot(X, color="blue")
plt.plot(range(n, n+24), Pred11['mean'], linestyle='--', color="violet")
plt.fill_between(range(n, n+24), Pred11['mean_ci_lower'], Pred11['mean_ci_upper'], color='violet', alpha=0.2)
plt.xlabel("Mois")
plt.ylabel("Voyageurs de la SNCF (log)")
plt.grid()

# Alternative : lissage exponentiel de Holt-Winters (plus rapide... souvent très (trop ?) simpliste)

from statsmodels.tsa.holtwinters import ExponentialSmoothing
ModHW = ExponentialSmoothing(XT, trend="add", seasonal="add", seasonal_periods=12)
ModHWF = ModHW.fit()
plt.plot(X, color="blue")
plt.plot(ModHWF.fittedvalues, color="green", linestyle="dotted")
plt.grid()

PredHW = ModHWF.forecast(steps=24)
plt.plot(X, color="blue")
plt.plot(range(n, n+24), PredHW, linestyle='--', color="green")
plt.xlabel("Mois")
plt.ylabel("Voyageurs de la SNCF (log)")
plt.grid()


# Exemple de prédiction avec Mod01
plt.plot(SNCF["Voy"], color="blue")
n = len(SNCF["Voy"])
plt.plot(range(n, n+24), np.exp(Pred01['mean'] + Mod01F.params[5]/2), linestyle='--', color="violet")
plt.fill_between(range(n, n+24), np.exp(Pred01['mean_ci_lower']), np.exp(Pred01['mean_ci_upper']), color='violet', alpha=0.2)
plt.xlabel("Mois")
plt.ylabel("Voyageurs de la SNCF")
plt.grid()
