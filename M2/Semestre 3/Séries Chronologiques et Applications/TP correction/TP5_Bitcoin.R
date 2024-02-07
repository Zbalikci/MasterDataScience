
# Indiquer l'adresse où se trouve votre fichier
adr = "L'adresse de votre répertoire de travail"
BTC = read.csv(paste(adr, "//BTC-USD.csv", sep=""), sep=",")

# Remarque : la série BTC évolue en permanence sur le site yahoo/finance
# Selon le moment où vous la récupérez, l'analyse risque d'être légèrement différente de celle donnée ici

# On voit une décroissance linéaire assez nette
plot(BTC$Close, type="l", main="Action BTC", ylab="Valeur à la fermeture", xlab="Jours")

library(TSA)
library(tseries)
library(forecast)

# Passage au log pour atténuer l'échelle
LBTC = log(BTC$Close)
plot(LBTC, type="l", main="Action BTC", ylab="Log-valeur à la fermeture", xlab="Jours")

# Suppression d'une tendance linéaire par la méthode indirecte
n = length(LBTC)
Tps = 1:n
RegLin = lm(LBTC ~ Tps)
summary(RegLin)
a0 = RegLin$coefficients[1]
a1 = RegLin$coefficients[2]
lines(Tps, a0+a1*Tps, col="red", lty=2)
ResLBTC = LBTC-a0-a1*Tps # Résidus : fluctuations autour de la tendance
source(paste(adr, "//TP4_CheckupRes.R", sep=""))
checkupRes(ResLBTC) # Bruit très corrélé avec caractérisation AR(1) très prononcée
adf.test(ResLBTC)
kpss.test(ResLBTC)
# Tests de stationnarité en contradiction
# En vertu des ACF/PACF, on part sur un AR(1) stationnaire

ARMA = TSA::arima(ResLBTC, order=c(1, 0, 0), include.mean=TRUE)
ARMA # Intercept non-significatif, on l'enlève

ARMA = TSA::arima(ResLBTC, order=c(1, 0, 0), include.mean=FALSE)
ARMA

# Par la méthode directe (tendance gérée par Arima de forecast)
ARMA = forecast::Arima(LBTC, order=c(1, 0, 0), include.drift=TRUE)
ARMA
# On trouve un drift très significatif avec a0 = 11.03 et a1=-0.003
# Similaire aux résultats de la régression linéaire précédente

# Superposition des modélisations avec intervalle de confiance à 95%
# Le code qui suit est adapté à l'objet ARMA issu de forecast::Arima ci-dessus
# Pour l'adapter à l'objet ARMA issu de TSA::arima, il faut penser à ajouter l'estimation de la droite de régression
dev.off()
plot(LBTC, type="l", main="Modèle AR(1) sur les résidus", ylab="Log-valeur à la fermeture", xlab="Jours")
lines(fitted(ARMA), col="red")

EstBTC = exp(fitted(ARMA))
plot(BTC$Close, type="l", main="Modèle AR(1) avec drift et IC à 95%", ylab="Valeur à la fermeture", xlab="Jours")
lines(EstBTC, col="red")
EstBTCinf = exp(fitted(ARMA) - sqrt(ARMA$sigma2)*1.96)
EstBTCsup = exp(fitted(ARMA) + sqrt(ARMA$sigma2)*1.96)
polygon(c(1:n, n:1), c(EstBTCinf, rev(EstBTCsup)), col="gray", border="red")
lines(BTC$Close, type="l")

checkupRes(ARMA$residuals)
shapiro.test(ARMA$residuals) 
Box.test(ARMA$residuals, type="Ljung-Box", lag=5)
# Résidus bruit blanc + approximativement gaussiens (visuellement... car test SW rejeté)
