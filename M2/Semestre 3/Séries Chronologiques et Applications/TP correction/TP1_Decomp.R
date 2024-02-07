# La série est dans le package 'datasets'
Data = AirPassengers
class(Data) # On observe que la série est déjà au format ts ('time series')
frequency(Data) # Période 12 déjà indiquée

# Un coup d'oeil mois par mois par mois
library(forecast)
seasonplot(Data)

plot(Data, ylab="AirPassengers") # Le côté multiplicatif est visible dans l'amplitude des périodes
LData = log(AirPassengers)
plot(LData, ylab="log(AirPassengers)")
seasonplot(LData)

# Modélisation additive sur la série complète
Decomp = decompose(LData, type="additive")
plot(Decomp) # La fonction 'decompose' propose un affichage condensé des composantes

# Voyons ça de plus près...
plot(Decomp$trend, type="l", col="blue", ylab="Tendance")
plot(Decomp$seasonal, type="l", col="red", ylab="Périodicité")
plot(Decomp$figure, type="l", col="magenta", ylab="Motif périodique")
plot(Decomp$random, type="l", col="forestgreen", ylab="Fluctuations")

# R?gression lin?aire sur la tendance
n = length(Decomp$trend)
Tps = 1:n
RegLinTrend = lm(Decomp$trend ~ Tps)
summary(RegLinTrend)
estA0 = RegLinTrend$coefficients[1]
estA1 = RegLinTrend$coefficients[2]
plot(Tps, Decomp$trend, type="l", ylab="Tendance")
lines(Tps, estA0 + estA1*Tps, col="red", lty=2)

# Prédiction de deux nouvelles périodes avec le modèle additif
f = 12
NTps = (n+1):(n+2*f)
PredT = estA0 + estA1*NTps
PredS = Decomp$figure
Pred = PredT + PredS

# On prend la peine de retransformer la concaténation série+prédictions au format ts
plot(ts(c(LData, Pred), frequency=12, start=1949), type="l", ylab="log(AirPassengers)")
lines(ts(Pred, frequency=12, start=1961), col="red", lwd=2)
grid()
# Les prédictions sont surlignées

# Et... n'oublions pas que la série initiale avait été passée au log
plot(ts(c(Data, exp(Pred)), frequency=12, start=1949), type="l", ylab="AirPassengers")
lines(ts(exp(Pred), frequency=12, start=1961), col="red", lwd=2)
grid()

