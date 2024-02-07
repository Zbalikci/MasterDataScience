# On importe quelques outils pour les SARIMA, ACF/PACF, tests usuels, ...
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import kpss, adfuller

# On va travailler sur le jeu de données "CO2"
Data = sm.datasets.co2.load_pandas().data

# On garde l'année 2000 en réserve (pour la comparaison finale)
Ann2000 = Data[ (Data.index >= '2000') & (Data.index < '2001') ]

# On tronque sur la période 1990-2000
Data = Data[ (Data.index >= '1990') & (Data.index < '2000') ] # L'index de la série est reconnu comme l'indice temporel
Data.plot()
# On va retenir une période de 52 (une mesure par semaine sur cycle annuel)

DataDiffS = Data.diff(52)
DataDiffS = DataDiffS.dropna()
DataDiffS.plot()
# Plus de périodicité visible après une différenciation d'ordre 52

# Avant toute chose, faisons un simple "decompose"
Decomp = sm.tsa.seasonal_decompose(Data, model='additive', period=52)
Decomp.plot()
# Tendance linéaire assez évidente, motif périodique parfaitement retrouvé
# Accès aux éléments de la décomposition par Decomp.* avec * = trend, seasonal ou resid

# Testons la stationnarité après désaisonnalisation
TestA = adfuller(DataDiffS) # Test ADF
print("ADF p-val : ", TestA[1])
TestK = kpss(DataDiffS) # Test KPSS
print("KPSS p-val : ", TestK[1])
# Pas stationnaire après la différenciation saisonnière (D=1)

# On redifférencie (on passe à d=1)
DataDiffS2 = DataDiffS.diff()
DataDiffS2 = DataDiffS2.dropna()
DataDiffS2.plot()
TestA = adfuller(DataDiffS2) # Test ADF
print("ADF p-val : ", TestA[1])
TestK = kpss(DataDiffS2) # Test KPSS
print("KPSS p-val : ", TestK[1])
# Cette fois OK : on retient d=1 et D=1

plot_acf(DataDiffS2, lags=100, alpha=0.05)
plot_pacf(DataDiffS2, lags=100, alpha=0.05)
# Difficile à évaluer visuellement...
# Localement : comportement ARMA
# Périodiquement : commençons par Q=1 et P=1

# SARIMA(2, 1, 2)x(1, 1, 1)_52 avec tendance linéaire
# Trend = 'ct' signifie constante + tendance linéaire (d'autres options sont possibles)
Mod = sm.tsa.statespace.SARIMAX(Data, order=(2, 1, 2), seasonal_order=(1, 1, 1, 52), trend='ct', enforce_stationarity=False, enforce_invertibility=False)
ModF = Mod.fit()
print(ModF.summary()) # Non-singificativité dans les parties AR et MA et dans le trend

# On réduit les ordres AR et MA mais on garde le trend (visuellement présent...)
# SARIMA(1, 1, 1)x(1, 1, 1)_52 avec tendance linéaire
Mod = sm.tsa.statespace.SARIMAX(Data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 52), trend='ct', enforce_stationarity=False, enforce_invertibility=False)
ModF = Mod.fit()
print(ModF.summary()) # Tout est très significatif, on garde ce modèle

# Superposition des données et des fitted values à partir de 1995
Fig = Data[Data.index >= '1995'].plot()
ModF.fittedvalues[ModF.fittedvalues.index >= '1995'].plot(ax = Fig)
Fig.figure

# Coup d'oeil sur les résidus
ModF.plot_diagnostics()
TestLB = sm.stats.acorr_ljungbox(ModF.resid, lags=[52]) # Test de Ljung-Box au lag 52
print("LB p-val : ", TestLB["lb_pvalue"])
TestN = sm.stats.diagnostic.lilliefors(ModF.resid) # Test de Lilliefors de normalité
print("Norm p-val : ", TestN[1])
# Bruit blanc mais normalité douteuse

# Prédiction d'une année supplémentaire (avec intervalle à 99% de sécurité)
Pred = ModF.get_forecast(steps=52).summary_frame(alpha=0.05)
Fig = Data.plot()
Pred['mean'].plot(ax=Fig, style='--')
Fig.fill_between(Pred.index, Pred['mean_ci_lower'], Pred['mean_ci_upper'], color='orange', alpha=0.2)
Fig.figure

# Erreur entre la prédiction et l'année 2000
Fig = Ann2000.plot()
Pred['mean'].plot(ax=Fig, style='--')
Fig.fill_between(Pred.index, Pred['mean_ci_lower'], Pred['mean_ci_upper'], color='orange', alpha=0.2)
Fig.figure
# Prédiction ponctuelle qui sous-estime légèrement mais intervalle de sécurité englobant les vraies valeurs
